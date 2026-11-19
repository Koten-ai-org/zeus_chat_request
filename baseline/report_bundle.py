#!/usr/bin/env python3
"""Write the dated A/B report as HTML plus a JSON evidence file.

Verdicts compare the new pack with the previous pack:

- better: the new pack met the target API and the previous pack did not
- worse: the previous pack met the target and the new pack did not
- same: both met it, or neither did
- not run: a model call is missing, so the row cannot justify a pack change

Meeting the target means verb_hit. When the question sets evidence_required,
rows must also come back. A travel 403 does not fail a pack whose evidence
is optional and whose verb matched.
"""

from __future__ import annotations

import html
import json
import re
import tempfile
from pathlib import Path


# Locked CDN pins. Do not float these to "latest".
# Pico 2.0.6 is the page CSS. ECharts 5.6.0 is the last 5.x release.
PICO_CSS = "https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css"
ECHARTS_JS = "https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"

# Hidden comment emitted on every report. The visible page stays render_html.
# There is no template_report.html. baseline/AGENT.md is the run contract.
REPORT_CONTRACT = """<!--
report-contract: baseline/AGENT.md
render_html is the only writer. Do not hand-edit this file. Do not add a template HTML file.
Frozen suite: baseline/questions.json checked against baseline/suite.lock.json. Do not pass --id.
Section order: Summary, What changed in the text, What in that text shows up in the score, Size, Hub pointer, Hits rounds and rows, Better worse and the score, then beer-sample, then travel-sample.
Columns: Question, Target API, each pack, Versus the previous pack, Why, Notes.
Versus words: better, worse, both hit, both missed, Orange, not run. both hit and both missed still score as same. Orange is a turn that ended on HTTP 400 or higher and stays out of better and worse.
A pack cell leads with hit, rounds, and rows. pipeline is a yellow mark. fts is an orange mark only when the target was hybrid and this side did not call hybrid.
The CR-35 story is written only when the labels are base-6.1 and base-7.x. A later pair gets measured size and the rows that moved the score.
Size cells show characters, then tk. tk is UTF-8 bytes divided by 4, rounded up. When the evidence JSON has injection counts, Size adds the live suffix per dataset and the system message after that suffix is appended.
-->"""

VERDICT_RULE = (
    "better means the new pack called the target API and the previous pack did not. "
    "worse means the previous pack called the target API and the new pack did not. "
    "Rows from a different verb do not count. "
    "On Find hoppy citrus beers the target is search hybrid. "
    "That row is worse when the previous pack calls search hybrid and the new pack calls "
    "search fts, find, or set, even when both sides are HTTP 200 and both returned beers. "
    "same means both called the target, or neither did. "
    "not run means a model call is missing. "
    "When the question says rows are required, an empty Zeus result is not met."
)


def format_spec(spec: dict) -> str:
    parts = [str(spec.get("verb") or "")]
    for key in ("shape", "strategy", "entity_type"):
        if spec.get(key):
            parts.append(str(spec[key]))
    return " ".join(part for part in parts if part)


def target_api(question: dict) -> str:
    expect = question.get("expect") or {}
    parts = [format_spec(spec) for spec in (expect.get("all_of") or [])]
    any_of = expect.get("any_of") or []
    if any_of:
        parts.append("or " + " or ".join(format_spec(spec) for spec in any_of))
    text = " + ".join(part for part in parts if part)
    if question.get("evidence_required"):
        text = f"{text} (rows required)" if text else "rows required"
    return text


def called_api(row: dict | None) -> str:
    if not row or row.get("status") == "not_run":
        return ""
    seen: list[str] = []
    calls = row.get("calls") or []
    if calls:
        for call in calls:
            label = format_spec(
                {
                    "verb": call.get("verb"),
                    "shape": call.get("shape"),
                    "strategy": call.get("strategy"),
                    "entity_type": call.get("entity_type"),
                }
            )
            if label and label not in seen:
                seen.append(label)
            for step in ((call.get("args") or {}).get("steps") or []):
                if not isinstance(step, dict):
                    continue
                step_label = format_spec(step)
                if step_label and step_label not in seen:
                    seen.append(step_label)
        return ", ".join(seen)
    return ", ".join(str(verb) for verb in (row.get("verbs") or []) if verb)


def side_met(row: dict | None, evidence_required: bool) -> bool | None:
    """True when this pack met the target. None when it did not run."""
    if not row or row.get("status") == "not_run" or row.get("verb_hit") is None:
        return None
    if row.get("error") and not row.get("calls"):
        return None
    if not row.get("verb_hit"):
        return False
    if evidence_required and not row.get("evidence_nonempty"):
        return False
    return True


def verdict_pair(previous_met: bool | None, new_met: bool | None) -> tuple[str, str]:
    if previous_met is None or new_met is None:
        return "not run", "No model call is recorded for this pair."
    if previous_met and new_met:
        return "same", "Both packs hit the target API."
    if new_met and not previous_met:
        return "better", "The new pack hit the target API. The previous pack did not."
    if previous_met and not new_met:
        return "worse", "The previous pack hit the target API. The new pack did not."
    return "same", "Neither pack hit the target API."


_HTTP_CODES = (200, 400, 401, 429, 500)


def _fault_text(call: dict) -> str:
    sample = call.get("sample") if isinstance(call.get("sample"), dict) else {}
    parts = []
    for key in ("error", "message", "status", "reason"):
        value = sample.get(key)
        if value not in (None, "", {}, []):
            parts.append(str(value))
    return " ".join(parts).lower()


def api_error_source(http: int, text: str) -> str:
    """Who has to be re-tested. koten_converter is reserved for a later hop."""
    lowered = (text or "").lower()
    if "koten_converter" in lowered or "koten converter" in lowered:
        return "koten_converter (FUTURE)"
    if any(
        mark in lowered
        for mark in (
            "050010",
            "050015",
            "050016",
            "050005",
            "050011",
            "pipeline_unknown_binding",
            "unknown_binding",
            "ids must be node_ids",
            "must be doc_keys",
            "bad_request",
        )
    ):
        return "LLM"
    if http in {401, 429, 500, 502, 503, 504} or any(
        mark in lowered
        for mark in ("session_force_closed", "session_expired", "session exceeded")
    ):
        return "Zeus"
    if http == 400:
        return "LLM"
    return "Zeus"


def side_turn_fault(side: dict | None) -> tuple[int, str] | None:
    """The status printed on the pack cell, when that status is an API error."""
    if not isinstance(side, dict):
        return None
    http = _as_int(side.get("http"))
    if http is None or http < 400:
        return None
    text = ""
    for call in reversed(side.get("calls") or []):
        if not isinstance(call, dict):
            continue
        if _as_int(call.get("http")) == http:
            text = _fault_text(call)
            break
    return http, api_error_source(http, text)


def _retest_why(label_a: str, label_b: str, faults: list[tuple[str, int, str]]) -> str:
    pieces = [
        f"{label} ended on HTTP {code} ({source})"
        for label, code, source in faults
    ]
    return (
        "Re-test. API error: "
        + "; ".join(pieces)
        + ". This row stays out of better and worse."
    )


def apply_http_retest(view: dict) -> dict:
    """Hold a row out of the net when a pack cell ends on HTTP 400 or higher."""
    label_a = view.get("label_a") or "previous"
    label_b = view.get("label_b") or "new"
    rows = []
    for scope in view.get("scopes") or []:
        for row in scope.get("rows") or []:
            rows.append(row)
            if row.get("verdict") == "not run":
                continue
            faults = []
            for key, label in (("a", label_a), ("b", label_b)):
                side = row.get(key)
                if not isinstance(side, dict):
                    continue
                found = side_turn_fault(side)
                if found is None:
                    side.pop("api_source", None)
                    continue
                code, source = found
                side["api_source"] = source
                faults.append((label, code, source))
            if faults:
                row["verdict"] = "retest"
                row["why"] = _retest_why(label_a, label_b, faults)
                continue
            # A saved Orange row goes back to the target-API verdict when the
            # turn HTTP is no longer an error. The stored met flags are the source.
            if row.get("verdict") != "retest":
                continue
            met_a = (row.get("a") or {}).get("met")
            met_b = (row.get("b") or {}).get("met")
            if isinstance(met_a, bool) and isinstance(met_b, bool):
                row["verdict"], row["why"] = verdict_pair(met_a, met_b)
        scope["tallies"] = _tally(scope.get("rows") or [])
        scope["score"] = score_block(scope.get("rows") or [], label_a, label_b)
    if not rows:
        return view
    tallies = _tally(rows)
    view["tallies"] = tallies
    view["score"] = score_block(rows, label_a, label_b)
    view["justification"] = justification(tallies, label_a, label_b)
    return view


def _http_counts(rows: list[dict], side: str) -> dict[int, int]:
    counts: dict[int, int] = {}
    for row in rows:
        for call in (row.get(side) or {}).get("calls") or []:
            if not isinstance(call, dict):
                continue
            http = _as_int(call.get("http"))
            if http is None:
                continue
            counts[http] = counts.get(http, 0) + 1
    return counts


def _http_axis(views_counts: list[dict[int, int]]) -> list[int]:
    seen = set()
    for counts in views_counts:
        seen.update(counts)
    head = [code for code in _HTTP_CODES if code in seen or code in (200, 400, 500)]
    extras = sorted(code for code in seen if code not in head and code != 0)
    axis = head + extras
    if 0 in seen:
        axis.append(0)
    return axis


def slug_label(label: str) -> str:
    cleaned = []
    for char in label.strip():
        if char.isalnum() or char in {"-", "_"}:
            cleaned.append(char)
        elif char in {".", " "}:
            cleaned.append("_")
    return "".join(cleaned) or "pack"


def _yn(value) -> str:
    if value is None:
        return "—"
    return "yes" if value else "no"


def _as_int(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _max_row_count(calls: list) -> int:
    """Largest Zeus row list on this turn. A second hop does not add to the first."""
    best = 0
    for call in calls:
        if not isinstance(call, dict):
            continue
        sample = call.get("sample") if isinstance(call.get("sample"), dict) else {}
        count = _as_int(sample.get("row_count"))
        if count is not None and count > best:
            best = count
    return best


def _call_view(call: dict) -> dict:
    return {
        "round": call.get("round"),
        "verb": call.get("verb"),
        "strategy": call.get("strategy"),
        "entity_type": call.get("entity_type"),
        "shape": call.get("shape"),
        "http": call.get("http"),
        "req_id": call.get("req_id") or "",
        "rows": bool(call.get("evidence")),
        "args": call.get("args") if isinstance(call.get("args"), dict) else {},
        "sample": call.get("sample") if isinstance(call.get("sample"), dict) else {},
    }


def _side_view(row: dict | None) -> dict:
    if not row or row.get("status") == "not_run" or row.get("verb_hit") is None:
        return {
            "called": "",
            "hit": None,
            "rows": None,
            "row_count": None,
            "http": None,
            "rounds": None,
            "calls": [],
            "req_ids": [],
            "chat_id": "",
            "turn_id": "",
            "session_id": "",
        }
    calls = [_call_view(call) for call in (row.get("calls") or []) if isinstance(call, dict)]
    req_ids = [call["req_id"] for call in calls if call.get("req_id")]
    for req_id in row.get("req_ids") or []:
        if req_id and req_id not in req_ids:
            req_ids.append(req_id)
    return {
        "called": called_api(row),
        "hit": bool(row.get("verb_hit")),
        "rows": bool(row.get("evidence_nonempty")),
        "row_count": _max_row_count(calls),
        "http": row.get("http_status"),
        "rounds": _as_int(row.get("rounds_used")),
        "calls": calls,
        "req_ids": req_ids,
        "chat_id": row.get("chat_id") or "",
        "turn_id": row.get("turn_id") or "",
        "session_id": row.get("session_id") or "",
    }


def _tally(rows: list[dict]) -> dict:
    counts = {"better": 0, "worse": 0, "same": 0, "retest": 0, "not run": 0, "total": len(rows)}
    for row in rows:
        counts[row["verdict"]] += 1
    return counts


def score_block(rows: list[dict], label_a: str, label_b: str) -> dict:
    """Met counts plus better:worse. Net is better minus worse."""
    total = len(rows)
    met_a = sum(1 for row in rows if row.get("a", {}).get("met") is True)
    met_b = sum(1 for row in rows if row.get("b", {}).get("met") is True)
    tallies = _tally(rows)
    better = tallies["better"]
    worse = tallies["worse"]
    return {
        "total": total,
        "met_a": met_a,
        "met_b": met_b,
        "ratio_a": f"{met_a}/{total}",
        "ratio_b": f"{met_b}/{total}",
        "better": better,
        "worse": worse,
        "same": tallies["same"],
        "retest": tallies.get("retest", 0),
        "net": better - worse,
        "better_to_worse": f"{better}:{worse}",
        "label_a": label_a,
        "label_b": label_b,
    }


def score_line(score: dict) -> str:
    return (
        f"{score['label_a']} met {score['ratio_a']}. "
        f"{score['label_b']} met {score['ratio_b']}. "
        f"better:worse {score['better_to_worse']}. "
        f"Net {score['net']} (better minus worse)."
        + (
            f" Orange {score['retest']} held out for an API error."
            if score.get("retest")
            else ""
        )
    )


def justification(tallies: dict, label_a: str, label_b: str) -> str:
    better = tallies["better"]
    worse = tallies["worse"]
    same = tallies["same"]
    retest = tallies.get("retest", 0)
    held = (
        f" {retest} question(s) ended on an API error and stay out of the net until a re-test."
        if retest
        else ""
    )
    if tallies["not run"] == tallies["total"]:
        return (
            f"This file does not justify switching to {label_b}. "
            "Every row is not run. The target API column is filled from the question file. "
            "Same, better, and worse are written only after both packs are sent to the model."
        )
    if better == 0 and worse == 0:
        same_line = (
            f"Every scored question is the same ({same})."
            if not retest
            else f"{same} question(s) are the same."
        )
        return (
            f"{same_line} "
            f"This suite does not show a reason to switch to {label_b}.{held}"
        )
    if better > 0 and worse == 0 and retest:
        return (
            f"{label_b} met the target API on {better} question(s) where {label_a} did not, "
            f"and matched {label_a} on {same}.{held}"
        )
    if better > 0 and worse == 0:
        return (
            f"{label_b} met the target API on {better} question(s) where {label_a} did not, "
            f"and matched {label_a} on {same}. No question got worse. "
            f"That supports using {label_b} on this suite."
        )
    if worse > better:
        return (
            f"{label_b} is worse on {worse} question(s) and better on {better}. "
            f"{same} question(s) are the same. This run does not justify switching to {label_b}.{held}"
        )
    if better > worse:
        return (
            f"{label_b} is better on {better} question(s) and worse on {worse}. "
            f"{same} question(s) are the same. Read the worse rows before treating this run as a promotion.{held}"
        )
    return (
        f"{label_b} is better on {better} and worse on {worse}. "
        f"The wins and losses tie. Read the rows before switching.{held}"
    )


def build_view(report: dict, questions: list[dict], date: str) -> dict:
    packs = report.get("packs") or [{}, {}]
    pack_a = packs[0] if packs else {}
    pack_b = packs[1] if len(packs) > 1 else {}
    label_a = pack_a.get("label") or "previous"
    label_b = pack_b.get("label") or "new"
    by_a = {row.get("id"): row for row in pack_a.get("questions") or []}
    by_b = {row.get("id"): row for row in pack_b.get("questions") or []}
    families: dict[str, dict] = {}
    order: list[str] = []
    for question in questions:
        scope = question.get("scope") or ""
        family = scope.split("/", 1)[0] or scope or "scope"
        if family not in families:
            families[family] = {"name": family, "scopes": [], "rows": []}
            order.append(family)
        bucket = families[family]
        if scope and scope not in bucket["scopes"]:
            bucket["scopes"].append(scope)
        previous = by_a.get(question["id"])
        new = by_b.get(question["id"])
        required = bool(question.get("evidence_required"))
        previous_met = side_met(previous, required)
        new_met = side_met(new, required)
        verdict, why = verdict_pair(previous_met, new_met)
        previous_blocked = bool(previous and previous.get("error") and not previous.get("calls"))
        new_blocked = bool(new and new.get("error") and not new.get("calls"))
        if previous_blocked or new_blocked:
            verdict = "not run"
            previous_met = None
            new_met = None
            if previous_blocked and new_blocked:
                why = "Neither pack reached the model."
            elif previous_blocked:
                why = "The previous pack did not reach the model."
            else:
                why = "The new pack did not reach the model."
        side_a = _side_view(previous)
        side_b = _side_view(new)
        side_a["met"] = previous_met
        side_b["met"] = new_met
        bucket["rows"].append(
            {
                "id": question["id"],
                "text": question.get("text") or "",
                "scope": scope,
                "target_api": target_api(question),
                "notes": question.get("notes") or "",
                "a": side_a,
                "b": side_b,
                "verdict": verdict,
                "why": why,
            }
        )
    scopes = []
    all_rows = []
    for name in order:
        bucket = families[name]
        bucket["tallies"] = _tally(bucket["rows"])
        bucket["score"] = score_block(bucket["rows"], label_a, label_b)
        scopes.append(bucket)
        all_rows.extend(bucket["rows"])
    tallies = _tally(all_rows)
    status = "not_run" if tallies["not run"] == tallies["total"] else "ran"
    view = {
        "title": f"{label_a} vs {label_b}",
        "date": date,
        "status": status,
        "label_a": label_a,
        "label_b": label_b,
        "base_id_a": pack_a.get("base_id"),
        "base_id_b": pack_b.get("base_id"),
        "zeus_version": report.get("zeus_version"),
        "provider": report.get("provider"),
        "provider_base": report.get("provider_base"),
        "model": report.get("model"),
        "client": report.get("client"),
        "client_version": report.get("client_version"),
        "verdict_rule": VERDICT_RULE,
        "tallies": tallies,
        "scopes": scopes,
    }
    view["justification"] = justification(tallies, label_a, label_b)
    view["score"] = score_block(all_rows, label_a, label_b)
    view["stem"] = f"{date}_{slug_label(label_a)}_vs_{slug_label(label_b)}"
    view["scope_briefs"] = list(report.get("scope_briefs") or [])
    return apply_http_retest(view)


def build_pending(suite: dict, label_a: str, label_b: str, date: str) -> dict:
    questions = suite.get("questions") or []
    blanks = [
        {
            "id": question["id"],
            "status": "not_run",
            "text": question.get("text") or "",
            "scope": question.get("scope") or "",
        }
        for question in questions
    ]
    report = {
        "zeus_version": suite.get("zeus_version_probed"),
        "provider": None,
        "provider_base": None,
        "model": None,
        "packs": [
            {"label": label_a, "base_id": label_a, "questions": blanks},
            {"label": label_b, "base_id": label_b, "questions": [dict(row) for row in blanks]},
        ],
    }
    return build_view(report, questions, date)


def _side_lines(side: dict) -> str:
    if side.get("hit") is None and not side.get("called"):
        return "—"
    lines = [
        side.get("called") or "—",
        f"hit: {_yn(side.get('hit'))}",
        f"rounds: {side['rounds'] if side.get('rounds') is not None else '—'}",
        f"rows: {side['row_count'] if side.get('row_count') is not None else '—'}",
    ]
    if side.get("http"):
        lines.append(f"HTTP {side['http']}")
    if side.get("session_id"):
        lines.append(f"session: {side['session_id']}")
    if side.get("chat_id"):
        lines.append(f"chat: {side['chat_id']}")
    return "\n".join(lines)


def _tally_line(tallies: dict) -> str:
    return (
        f"better {tallies['better']}, worse {tallies['worse']}, "
        f"same {tallies['same']}, not run {tallies['not run']}"
    )


def _chart_flag(value) -> int | None:
    if value is None:
        return None
    return 1 if value else 0


def _chart_model(view: dict) -> dict:
    """Numbers the charts plot. None means that side did not run."""
    scopes = []
    suite_counts = []
    for scope in view.get("scopes") or []:
        rows = scope.get("rows") or []
        counts_a = _http_counts(rows, "a")
        counts_b = _http_counts(rows, "b")
        suite_counts.extend((counts_a, counts_b))
        axis = _http_axis([counts_a, counts_b])
        scopes.append(
            {
                "name": scope.get("name") or "",
                "ids": [row.get("id") or "" for row in rows],
                "hits_a": [_chart_flag(row["a"].get("hit")) for row in rows],
                "hits_b": [_chart_flag(row["b"].get("hit")) for row in rows],
                "rounds_a": [row["a"].get("rounds") for row in rows],
                "rounds_b": [row["b"].get("rounds") for row in rows],
                "rows_a": [row["a"].get("row_count") for row in rows],
                "rows_b": [row["b"].get("row_count") for row in rows],
                "http_codes": [str(code) for code in axis],
                "http_a": [counts_a.get(code, 0) for code in axis],
                "http_b": [counts_b.get(code, 0) for code in axis],
            }
        )
    suite_axis = _http_axis(suite_counts)
    return {
        "label_a": view.get("label_a") or "previous",
        "label_b": view.get("label_b") or "new",
        "http_codes": [str(code) for code in suite_axis],
        "http_a": [
            sum(counts.get(code, 0) for counts in suite_counts[0::2]) for code in suite_axis
        ],
        "http_b": [
            sum(counts.get(code, 0) for counts in suite_counts[1::2]) for code in suite_axis
        ],
        "scopes": scopes,
    }


def _mark_pipeline(text: str) -> str:
    """Highlight the verb pipeline in a pack column. Other words stay plain."""
    escaped = html.escape(text)
    return re.sub(
        r"\bpipeline\b",
        '<mark class="pipeline">pipeline</mark>',
        escaped,
    )


def _mark_called(text: str, target: str) -> str:
    """Mark pipeline, and mark fts when the target was hybrid and this side missed it."""
    marked = _mark_pipeline(text)
    target_l = target.lower()
    called_l = text.lower()
    missed_hybrid = (
        "hybrid" in target_l
        and "hybrid" not in called_l
        and re.search(r"\bfts\b", called_l) is not None
    )
    if not missed_hybrid:
        return marked
    return re.sub(
        r"\bfts\b",
        '<mark class="missed-strategy">fts</mark>',
        marked,
    )


def _display_verdict(row: dict) -> str:
    """Column label. both hit and both missed still score as same."""
    verdict = str(row.get("verdict") or "")
    if verdict == "retest":
        return "Orange"
    if verdict != "same":
        return verdict
    met_a = (row.get("a") or {}).get("met")
    met_b = (row.get("b") or {}).get("met")
    if met_a is True and met_b is True:
        return "both hit"
    if met_a is False and met_b is False:
        return "both missed"
    return "same"


def _display_tally(rows: list[dict]) -> str:
    counts = {"better": 0, "worse": 0, "both hit": 0, "both missed": 0, "Orange": 0, "not run": 0}
    for row in rows:
        label = _display_verdict(row)
        if label in counts:
            counts[label] += 1
    return (
        f"better {counts['better']}, worse {counts['worse']}, "
        f"both hit {counts['both hit']}, both missed {counts['both missed']}, "
        f"Orange {counts['Orange']}, not run {counts['not run']}"
    )


def _empty_hit_note(scope: dict) -> str:
    """Shown under a scope's charts when a hit of 1 stored no rows."""
    for row in scope.get("rows") or []:
        for key in ("a", "b"):
            side = row.get(key) or {}
            if side.get("hit") and side.get("met") is False and (side.get("row_count") or 0) == 0:
                return (
                    '<p class="chart-hint">A hit of 1 with 0 rows means that pack called the target verb '
                    "and the stored result list was empty. When the question requires rows, "
                    "the score counts that as not met.</p>"
                )
    return ""


def _html_side(side: dict, target: str = "") -> str:
    if side.get("hit") is None and not side.get("called"):
        return "—"
    hit = _chart_flag(side.get("hit"))
    rounds = "—" if side.get("rounds") is None else str(side.get("rounds"))
    rows = "—" if side.get("row_count") is None else str(side.get("row_count"))
    bits = [
        '<div class="metrics">',
        f'<span><span class="metric">{hit if hit is not None else "—"}</span> hit</span>',
        f'<span><span class="metric">{html.escape(rounds)}</span> rounds</span>',
        f'<span><span class="metric">{html.escape(rows)}</span> rows</span>',
        "</div>",
        f'<div class="called">{_mark_called(str(side.get("called") or "—"), target)}</div>',
    ]
    if side.get("http"):
        source = side.get("api_source")
        status = f'HTTP {html.escape(str(side["http"]))}'
        if source:
            status += f' · {html.escape(str(source))}'
        bits.append(f'<div class="sub">{status}</div>')
    if side.get("session_id"):
        bits.append(f'<div class="sub">session {html.escape(str(side["session_id"]))}</div>')
    if side.get("chat_id"):
        bits.append(f'<div class="sub">chat {html.escape(str(side["chat_id"]))}</div>')
    return "".join(bits)


def _chart_boxes(prefix: str) -> str:
    return (
        '<div class="charts">'
        f'<div id="{prefix}-hits" class="chart"></div>'
        f'<div id="{prefix}-rounds" class="chart"></div>'
        f'<div id="{prefix}-rows" class="chart"></div>'
        f'<div id="{prefix}-http" class="chart chart-http"></div>'
        "</div>"
    )


def _scope_dom_id(name: str) -> str:
    cleaned = []
    for char in name.lower():
        cleaned.append(char if char.isalnum() else "-")
    return "".join(cleaned).strip("-") or "scope"


def _sum_metric(view: dict, side: str, key: str) -> int | None:
    total = 0
    seen = False
    for scope in view.get("scopes") or []:
        for row in scope.get("rows") or []:
            value = (row.get(side) or {}).get(key)
            if value is None:
                continue
            seen = True
            if isinstance(value, bool):
                total += 1 if value else 0
            else:
                number = _as_int(value)
                if number is None:
                    continue
                total += number
    return total if seen else None


def _why_class(row: dict) -> str:
    """Yellow when only one side met the target. Orange when both missed or an API error holds the row."""
    if row.get("verdict") == "retest":
        return "why-retest"
    met_a = (row.get("a") or {}).get("met")
    met_b = (row.get("b") or {}).get("met")
    if met_a is True and met_b is False:
        return "why-one"
    if met_a is False and met_b is True:
        return "why-one"
    if met_a is False and met_b is False:
        return "why-neither"
    return ""


def _moved_rows(view: dict) -> list[dict]:
    rows = []
    for scope in view.get("scopes") or []:
        for row in scope.get("rows") or []:
            if row.get("verdict") in {"better", "worse"}:
                rows.append(row)
    return rows


def _tool_catalog(doc: dict) -> dict:
    catalog = {}
    for item in doc.get("verbs") or []:
        function = item.get("function") or {}
        name = function.get("name")
        if name:
            catalog[name] = function
    return catalog


def _tokens_from_bytes(nbytes: int) -> int:
    """Pack-viewer budget: UTF-8 bytes ÷ 4, rounded up. Not the model tokenizer."""
    if nbytes <= 0:
        return 0
    return max(1, (nbytes + 3) // 4)


def _tokens(text: str) -> int:
    return _tokens_from_bytes(len(text.encode("utf-8")))


def _tool_text(tool: dict | None) -> str:
    if not tool:
        return ""
    return json.dumps(tool, ensure_ascii=False)


def _pack_mode_path(root: Path, label: str, mode: str) -> Path | None:
    """Analytics file for one pack label. The label is a directory name, not a path."""
    if not label or "/" in label or "\\" in label or ".." in label or label.startswith("."):
        return None
    return root / "v2" / "base" / label / "min" / f"chat_request_{mode}_{label}.json"


def _prompt_facts(label_a: str, label_b: str) -> dict | None:
    """Size of the analytics packs this suite sends. None when either file is absent."""
    root = Path(__file__).resolve().parents[1]
    path_a = _pack_mode_path(root, label_a, "analytics")
    path_b = _pack_mode_path(root, label_b, "analytics")
    if path_a is None or path_b is None or not path_a.is_file() or not path_b.is_file():
        return None
    raw_a = path_a.read_bytes()
    raw_b = path_b.read_bytes()
    doc_a = json.loads(raw_a.decode())
    doc_b = json.loads(raw_b.decode())
    system_a = (doc_a.get("messages") or [{}])[0].get("content") or ""
    system_b = (doc_b.get("messages") or [{}])[0].get("content") or ""
    tools_a = _tool_catalog(doc_a)
    tools_b = _tool_catalog(doc_b)
    pieces = []
    for name in ("search", "pipeline", "return"):
        if name not in tools_a or name not in tools_b:
            continue
        text_a = _tool_text(tools_a[name])
        text_b = _tool_text(tools_b[name])
        tk_a = _tokens(text_a)
        tk_b = _tokens(text_b)
        pieces.append(
            {
                "name": name,
                "a": len(text_a),
                "b": len(text_b),
                "delta": len(text_b) - len(text_a),
                "tk_a": tk_a,
                "tk_b": tk_b,
                "tk_delta": tk_b - tk_a,
            }
        )
    rail_text_a = _tool_text(tools_a.get("rail"))
    rail_text_b = _tool_text(tools_b.get("rail"))
    rail_chars_a = len(rail_text_a)
    rail_chars = len(rail_text_b)
    rail_tk_a = _tokens(rail_text_a)
    rail_tk_b = _tokens(rail_text_b)
    system_tk_a = _tokens(system_a)
    system_tk_b = _tokens(system_b)
    system_delta = len(system_b) - len(system_a)
    content_delta = system_delta + sum(piece["delta"] for piece in pieces) + (rail_chars - rail_chars_a)
    content_tk = (system_tk_b - system_tk_a) + sum(piece["tk_delta"] for piece in pieces) + (rail_tk_b - rail_tk_a)
    file_chars_a = len(raw_a.decode())
    file_chars_b = len(raw_b.decode())
    file_tk_a = _tokens_from_bytes(len(raw_a))
    file_tk_b = _tokens_from_bytes(len(raw_b))
    mode_deltas = []
    mode_tk_deltas = []
    for mode in (
        "analytics",
        "auto",
        "code",
        "custom",
        "fraud",
        "open",
        "private",
        "regulated",
        "research",
        "tenant",
    ):
        mode_a = _pack_mode_path(root, label_a, mode)
        mode_b = _pack_mode_path(root, label_b, mode)
        if mode_a is not None and mode_b is not None and mode_a.is_file() and mode_b.is_file():
            mode_text_a = mode_a.read_text()
            mode_text_b = mode_b.read_text()
            mode_deltas.append(len(mode_text_b) - len(mode_text_a))
            mode_tk_deltas.append(_tokens(mode_text_b) - _tokens(mode_text_a))
    plan_at = system_b.find("**Plan, then call**")
    access_at = system_b.find("2) **Access path")
    plan_chars = access_at - plan_at if plan_at >= 0 and access_at > plan_at else 0
    return {
        "bytes_a": len(raw_a),
        "bytes_b": len(raw_b),
        "chars_a": file_chars_a,
        "chars_b": file_chars_b,
        "tk_a": file_tk_a,
        "tk_b": file_tk_b,
        "system_a": len(system_a),
        "system_b": len(system_b),
        "system_tk_a": system_tk_a,
        "system_tk_b": system_tk_b,
        "system_delta": system_delta,
        "system_tk_delta": system_tk_b - system_tk_a,
        "plan_chars": plan_chars,
        "pieces": pieces,
        "rail_chars_a": rail_chars_a,
        "rail_chars": rail_chars,
        "rail_tk_a": rail_tk_a,
        "rail_tk_b": rail_tk_b,
        "added_verbs": sorted(set(tools_b) - set(tools_a)),
        "removed_verbs": sorted(set(tools_a) - set(tools_b)),
        "content_delta": content_delta,
        "content_tk": content_tk,
        "json_wrap": (file_chars_b - file_chars_a) - content_delta,
        "json_wrap_tk": (file_tk_b - file_tk_a) - content_tk,
        "verbs_a": len(tools_a),
        "verbs_b": len(tools_b),
        "unchanged_verbs": sum(
            1
            for name, tool in tools_a.items()
            if json.dumps(tool, sort_keys=True, ensure_ascii=False)
            == json.dumps(tools_b.get(name) or {}, sort_keys=True, ensure_ascii=False)
        ),
        "has_plan": plan_at >= 0,
        "mode_deltas": mode_deltas,
        "mode_tk_deltas": mode_tk_deltas,
    }


def _fmt_delta(value: int) -> str:
    return f"{value:+,}"


def _tk_under(chars: int, tokens: int) -> str:
    """Character count, then the token budget on the next line."""
    return f"{chars:,}<br><span class=\"tk\">({tokens:,} tk)</span>"


def _tk_delta(chars: int, tokens: int) -> str:
    return f"{_fmt_delta(chars)}<br><span class=\"tk\">({_fmt_delta(tokens)} tk)</span>"


def _stored_int(item: dict, key: str) -> int | None:
    if key not in item or item.get(key) is None:
        return None
    try:
        return int(item[key])
    except (TypeError, ValueError):
        return None


def _append_suffix(system: str, full_chars: int, full_bytes: int) -> tuple[int, int]:
    """System message after merge_scope_brief: rstrip, blank line, stripped suffix."""
    base = system.rstrip(" \t\n\r")
    chars = len(base) + 2 + full_chars
    nbytes = len(base.encode("utf-8")) + 2 + full_bytes
    return chars, _tokens_from_bytes(nbytes)


def _pct(part: int, whole: int) -> str:
    if whole <= 0:
        return "0%"
    return f"{100.0 * part / whole:.1f}%"


def _injection_html(view: dict, facts: dict | None) -> str:
    """Per-dataset live suffix. Omitted when the evidence file has no split."""
    briefs = [
        item
        for item in (view.get("scope_briefs") or [])
        if isinstance(item, dict) and _stored_int(item, "full_chars") is not None
    ]
    if not briefs:
        return ""
    label_a = html.escape(view.get("label_a") or "previous")
    label_b = html.escape(view.get("label_b") or "new")
    headers = "".join(
        f"<th>{html.escape(str(item.get('scope') or ''))}</th>" for item in briefs
    )
    rows = (
        ("scope_brief", "Scope brief"),
        ("mini_schema", "Mini-schema"),
        ("walk_paths", "Walk paths"),
        ("full", "Full injection"),
    )
    body = []
    for key, label in rows:
        cells = []
        for item in briefs:
            chars = _stored_int(item, f"{key}_chars")
            tokens = _stored_int(item, f"{key}_tk")
            if chars is None or tokens is None:
                cells.append("<td>—</td>")
            else:
                cells.append(f"<td>{_tk_under(chars, tokens)}</td>")
        body.append(f"<tr><td>{label}</td>{''.join(cells)}</tr>")
    shares = []
    gaps = []
    for item in briefs:
        scope = html.escape(str(item.get("scope") or ""))
        full = _stored_int(item, "full_chars") or 0
        mini = _stored_int(item, "mini_schema_chars")
        walk = _stored_int(item, "walk_paths_chars")
        brief_chars = _stored_int(item, "scope_brief_chars")
        if mini is not None:
            shares.append(
                f"mini-schema is {_tk_under(mini, _stored_int(item, 'mini_schema_tk') or 0).replace('<br>', ' ')} "
                f"({_pct(mini, full)} of {scope})"
            )
        if walk is not None:
            shares.append(
                f"walk paths are {_tk_under(walk, _stored_int(item, 'walk_paths_tk') or 0).replace('<br>', ' ')} "
                f"({_pct(walk, full)} of {scope})"
            )
        if brief_chars is not None and mini is not None and walk is not None:
            gap = full - (brief_chars + mini + walk)
            if gap > 0:
                gaps.append((gap, scope))
    share_line = ""
    if shares:
        share_line = "<p>" + ". ".join(part[0].upper() + part[1:] for part in shares) + ".</p>"
    gap_line = ""
    if gaps:
        detail = " and ".join(f"{gap:,} characters on {scope}" for gap, scope in gaps)
        if all(gap <= 8 for gap, _scope in gaps):
            gap_line = f"<p>Blank lines between the headings account for {detail}.</p>"
        else:
            gap_line = f"<p>Text outside those three headings accounts for {detail}.</p>"
    recorded = []
    matched = True
    for item in briefs:
        chars = _stored_int(item, "chars")
        brief_bytes = _stored_int(item, "scope_brief_bytes")
        mini_bytes = _stored_int(item, "mini_schema_bytes")
        if chars is None:
            matched = False
            continue
        recorded.append(
            f"{chars:,} UTF-8 bytes for {html.escape(str(item.get('scope') or ''))}"
        )
        if brief_bytes is None or mini_bytes is None or brief_bytes + mini_bytes != chars:
            matched = False
    recorded_line = ""
    if recorded:
        recorded_line = (
            "The evidence file recorded "
            + " and ".join(recorded)
            + ". That figure is the scope-brief slice plus the mini-schema slice. "
        )
        if matched:
            recorded_line += "Those two byte lengths match this measurement. "
    sources = {str(item.get("injection_source") or "") for item in briefs}
    if sources == {"catalog-fetch"}:
        origin = (
            "<p>These counts come from a catalog fetch after the run. "
            "The scope-brief sha12 matches the hash stored on this run. "
            + recorded_line
            + "Walk paths are the next heading.</p>"
        )
    else:
        origin = (
            "<p>These counts come from the system message on the turn that first "
            "merged the brief. "
            + recorded_line
            + "Walk paths are the next heading.</p>"
        )
    appended = ""
    if facts:
        systems = _pack_systems(str(view.get("label_a") or ""), str(view.get("label_b") or ""))
        if systems is not None:
            system_a, system_b = systems
            append_rows = []
            for item in briefs:
                full_chars = _stored_int(item, "full_chars")
                full_bytes = _stored_int(item, "full_bytes")
                if full_chars is None or full_bytes is None:
                    continue
                chars_a, tk_a = _append_suffix(system_a, full_chars, full_bytes)
                chars_b, tk_b = _append_suffix(system_b, full_chars, full_bytes)
                append_rows.append(
                    "<tr><td>"
                    + html.escape(str(item.get("scope") or ""))
                    + f"</td><td>{_tk_under(chars_a, tk_a)}</td>"
                    + f"<td>{_tk_under(chars_b, tk_b)}</td></tr>"
                )
            if append_rows:
                appended = (
                    "<p>System message after that suffix is appended. "
                    "The gap between the packs stays the system-message delta above.</p>"
                    "<table><thead><tr><th>Dataset</th>"
                    f"<th>{label_a}</th><th>{label_b}</th></tr></thead><tbody>"
                    + "".join(append_rows)
                    + "</tbody></table>"
                )
    return (
        "<p>The live suffix Zeus appends to the system message, one column per dataset. "
        "Both packs receive the same suffix. The table above is the pack file before that append.</p>"
        "<table><thead><tr><th>Piece</th>"
        + headers
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
        + share_line
        + gap_line
        + origin
        + appended
    )


def _pack_systems(label_a: str, label_b: str) -> tuple[str, str] | None:
    root = Path(__file__).resolve().parents[1]
    path_a = _pack_mode_path(root, label_a, "analytics")
    path_b = _pack_mode_path(root, label_b, "analytics")
    if path_a is None or path_b is None or not path_a.is_file() or not path_b.is_file():
        return None
    doc_a = json.loads(path_a.read_text())
    doc_b = json.loads(path_b.read_text())
    system_a = (doc_a.get("messages") or [{}])[0].get("content") or ""
    system_b = (doc_b.get("messages") or [{}])[0].get("content") or ""
    if not isinstance(system_a, str) or not isinstance(system_b, str):
        return None
    return system_a, system_b


def _summary_html(view: dict) -> str:
    """Opening summary: score, text that was added, and file size."""
    label_a = html.escape(view.get("label_a") or "previous")
    label_b = html.escape(view.get("label_b") or "new")
    score = view.get("score") or {}
    hits_a = _sum_metric(view, "a", "hit")
    hits_b = _sum_metric(view, "b", "hit")
    rounds_a = _sum_metric(view, "a", "rounds")
    rounds_b = _sum_metric(view, "b", "rounds")
    moved = _moved_rows(view)
    parts = [
        "<h2>Summary</h2>",
        f"<p>{html.escape(view.get('justification') or '')} "
        f"{html.escape(score_line(score) if score else '')}</p>",
    ]
    if hits_a is not None and hits_b is not None:
        if moved:
            names = ", ".join(html.escape(str(row.get("id") or "")) for row in moved)
            moved_line = f" The score moved on {names}."
        else:
            moved_line = " No question moved the score."
        parts.append(
            "<p>Across the questions that ran: "
            f"hits {hits_a} versus {hits_b}, "
            f"rounds {rounds_a} versus {rounds_b}."
            f"{moved_line} "
            "Hits count a target-API call. Rounds are a sum. "
            "Row totals are left off this line because one large find swamps the rest. "
            "Read rows on the question charts and in each pack cell. "
            "A hit with an empty required result still counts as a hit here and as not met in the score.</p>"
        )
    parts.append("<h3>What changed in the text</h3>")
    raw_a = str(view.get("label_a") or "")
    raw_b = str(view.get("label_b") or "")
    cr35 = raw_a == "base-6.1" and raw_b == "base-7.x"
    facts = _prompt_facts(raw_a, raw_b)
    if cr35 and facts and facts.get("has_plan"):
        parts.append(
            "<p>base-7.x starts from a copy of base-6.1 and adds the CR-35 method. "
            f"The analytics system message grew by {facts['system_delta']:,} characters. "
            f"{facts['plan_chars']:,} of those are the new <strong>Plan, then call</strong> block: "
            "World, Entry, Path, Goal, and a budget of at most 8 calls. "
            "The access-path line changed from “prefer cheapest that answers” and “8 steps” "
            "to “the cheapest move that still follows the plan” and “one pipeline is one call”.</p>"
            "<ul>"
            "<li><code>search</code>: one soft phrase, the user's words unchanged, entry limit up to 200, "
            "and a second soft phrase goes to <code>pipeline</code>.</li>"
            "<li><code>pipeline</code>: one drill-down is one call; later steps use <code>narrow_to</code>; "
            "page at 10 or 20, then <code>project</code>.</li>"
            "<li><code>return</code>: a browse with no hard fact ends on 10 or 20 cards.</li>"
            f"<li><code>rail</code> is new ({facts['rail_chars']:,} characters in the tool JSON). "
            "Copy <code>name</code> from the scope brief and pass <code>binds</code> only. No SQL.</li>"
            f"<li>{facts['verbs_a']} verbs became {facts['verbs_b']}. "
            f"{facts['unchanged_verbs']} of the original tools are unchanged.</li>"
            "</ul>"
        )
    elif facts:
        parts.append(
            "<p>The analytics system message changed by "
            f"{_fmt_delta(facts['system_delta'])} characters. "
            f"{facts['verbs_a']} verbs became {facts['verbs_b']}. "
            f"{facts['unchanged_verbs']} of the previous tools are unchanged.</p>"
        )
        verb_items = []
        added = ", ".join(
            f"<code>{html.escape(name)}</code>" for name in facts.get("added_verbs") or []
        )
        removed = ", ".join(
            f"<code>{html.escape(name)}</code>" for name in facts.get("removed_verbs") or []
        )
        if added:
            verb_items.append(f"<li>New tools: {added}.</li>")
        if removed:
            verb_items.append(f"<li>Removed tools: {removed}.</li>")
        if verb_items:
            parts.append("<ul>" + "".join(verb_items) + "</ul>")
    else:
        parts.append("<p>Pack text was not measured for this pair.</p>")
    parts.append("<h3>What in that text shows up in the score</h3>")
    if not moved:
        parts.append("<p>No question is better or worse, so the added text did not move the score.</p>")
    else:
        items = []
        for row in moved:
            side_a = row.get("a") or {}
            side_b = row.get("b") or {}
            items.append(
                "<li><strong>"
                + html.escape(str(row.get("id") or ""))
                + "</strong> is "
                + html.escape(str(row.get("verdict") or ""))
                + ". "
                + html.escape(label_a)
                + " called "
                + html.escape(str(side_a.get("called") or "—"))
                + f" ({side_a.get('rounds')} rounds, {side_a.get('row_count')} rows). "
                + html.escape(label_b)
                + " called "
                + html.escape(str(side_b.get("called") or "—"))
                + f" ({side_b.get('rounds')} rounds, {side_b.get('row_count')} rows).</li>"
            )
        parts.append("<ul>" + "".join(items) + "</ul>")
        if cr35 and facts and facts.get("has_plan"):
            parts.append(
                "<p>Those wins are the questions where base-7.x called <code>traverse walk_path</code> "
                "and base-6.1 did not. The new lines that talk about that job are the plan: "
                "the world already includes <code>WALK_PATHS</code>, and the path goes from a large set "
                "to a smaller set. <code>rail</code> was not called. "
                "The search and pipeline rewrites did not change <code>beer-pipeline-cards</code>: "
                "both packs still called <code>search fts</code> inside the pipeline. "
                "Travel stayed even.</p>"
            )
    parts.append("<h3>Size</h3>")
    if not facts:
        parts.append("<p>The two pack files were not both on disk, so this page has no size delta.</p>")
    else:
        char_delta = facts["chars_b"] - facts["chars_a"]
        byte_delta = facts["bytes_b"] - facts["bytes_a"]
        tk_delta = facts["tk_b"] - facts["tk_a"]
        pct = (100.0 * char_delta / facts["chars_a"]) if facts["chars_a"] else 0
        mode_deltas = facts.get("mode_deltas") or []
        mode_tk_deltas = facts.get("mode_tk_deltas") or []
        same_modes = len(mode_deltas) > 1 and len(set(mode_deltas)) == 1
        same_mode_tk = len(mode_tk_deltas) > 1 and len(set(mode_tk_deltas)) == 1
        parts.append(
            "<p>This run sent the analytics file. "
            f"{label_a} is {facts['chars_a']:,} characters "
            f"({facts['tk_a']:,} tk, {facts['bytes_a']:,} bytes). "
            f"{label_b} is {facts['chars_b']:,} characters "
            f"({facts['tk_b']:,} tk, {facts['bytes_b']:,} bytes). "
            f"That is {_fmt_delta(char_delta)} characters ({_fmt_delta(tk_delta)} tk) "
            f"and {_fmt_delta(byte_delta)} bytes ({pct:.1f}%).</p>"
            "<table><thead><tr><th>Piece</th>"
            f"<th>{label_a}</th><th>{label_b}</th><th>Delta</th></tr></thead><tbody>"
            f"<tr><td>Analytics file</td><td>{_tk_under(facts['chars_a'], facts['tk_a'])}</td>"
            f"<td>{_tk_under(facts['chars_b'], facts['tk_b'])}</td>"
            f"<td>{_tk_delta(char_delta, tk_delta)}</td></tr>"
            f"<tr><td>System message</td>"
            f"<td>{_tk_under(facts['system_a'], facts['system_tk_a'])}</td>"
            f"<td>{_tk_under(facts['system_b'], facts['system_tk_b'])}</td>"
            f"<td>{_tk_delta(facts['system_delta'], facts['system_tk_delta'])}</td></tr>"
        )
        for piece in facts["pieces"]:
            parts.append(
                f"<tr><td><code>{html.escape(piece['name'])}</code> tool JSON</td>"
                f"<td>{_tk_under(piece['a'], piece['tk_a'])}</td>"
                f"<td>{_tk_under(piece['b'], piece['tk_b'])}</td>"
                f"<td>{_tk_delta(piece['delta'], piece['tk_delta'])}</td></tr>"
            )
        rail_a = facts.get("rail_chars_a") or 0
        rail_b = facts.get("rail_chars") or 0
        rail_tk_a = facts.get("rail_tk_a") or 0
        rail_tk_b = facts.get("rail_tk_b") or 0
        if rail_a or rail_b:
            cell_a = "—" if not rail_a else _tk_under(rail_a, rail_tk_a)
            cell_b = "—" if not rail_b else _tk_under(rail_b, rail_tk_b)
            parts.append(
                f"<tr><td><code>rail</code> tool JSON</td><td>{cell_a}</td><td>{cell_b}</td>"
                f"<td>{_tk_delta(rail_b - rail_a, rail_tk_b - rail_tk_a)}</td></tr>"
            )
        parts.append(
            f"<tr><td>Changed prose and tool JSON</td><td></td><td></td>"
            f"<td>{_tk_delta(facts['content_delta'], facts['content_tk'])}</td></tr>"
            f"<tr><td>JSON wrapping around those edits</td><td></td><td></td>"
            f"<td>{_tk_delta(facts['json_wrap'], facts['json_wrap_tk'])}</td></tr>"
            "</tbody></table>"
        )
        if same_modes:
            if same_mode_tk:
                parts.append(
                    f"<p>The same {_fmt_delta(mode_deltas[0])} character delta "
                    f"({_fmt_delta(mode_tk_deltas[0])} tk) is on all "
                    f"{len(mode_deltas)} mode files. This run used analytics only.</p>"
                )
            else:
                low = min(mode_tk_deltas)
                high = max(mode_tk_deltas)
                parts.append(
                    f"<p>The same {_fmt_delta(mode_deltas[0])} character delta is on all "
                    f"{len(mode_deltas)} mode files. The token budget on those files is "
                    f"{_fmt_delta(low)} tk or {_fmt_delta(high)} tk. This run used analytics only.</p>"
                )
        parts.append(_injection_html(view, facts))
        parts.append(
            "<p class=\"tk-note\">The first line of a cell is characters. "
            "tk is the token budget from the pack viewer: UTF-8 bytes ÷ 4, rounded up. "
            "It is not the model's own tokenizer.</p>"
        )
    return "".join(parts)


def render_html(view: dict) -> str:
    apply_http_retest(view)
    label_a = html.escape(view["label_a"])
    label_b = html.escape(view["label_b"])
    sections = []
    for scope in view["scopes"]:
        body_rows = []
        for row in scope["rows"]:
            label = _display_verdict(row)
            css = {
                "better": "better",
                "worse": "worse",
                "both hit": "both-hit",
                "both missed": "both-missed",
                "same": "same",
                "not run": "not-run",
                "Orange": "retest",
            }.get(label, "")
            why_class = _why_class(row)
            why_attr = f' class="{why_class}"' if why_class else ""
            target = str(row.get("target_api") or "")
            body_rows.append(
                "<tr>"
                f"<td><strong>{html.escape(row['id'])}</strong><br>{html.escape(row['text'])}</td>"
                f"<td>{html.escape(target)}</td>"
                f"<td>{_html_side(row['a'], target)}</td>"
                f"<td>{_html_side(row['b'], target)}</td>"
                f"<td class=\"{css}\">{html.escape(label)}</td>"
                f"<td{why_attr}>{html.escape(row['why'])}</td>"
                f"<td>{html.escape(row['notes'])}</td>"
                "</tr>"
            )
        scope_names = html.escape(", ".join(scope["scopes"]))
        scope_score = scope.get("score") or {}
        chart_id = _scope_dom_id(str(scope.get("name") or "scope"))
        sections.append(
            f"<h2>{html.escape(scope['name'])}</h2>"
            f"<p>Scope: {scope_names}. {html.escape(_display_tally(scope['rows']))}. "
            f"{html.escape(score_line(scope_score) if scope_score else '')}</p>"
            f"{_chart_boxes('chart-' + chart_id)}"
            f"{_empty_hit_note(scope)}"
            "<table>"
            "<thead><tr>"
            "<th>Question</th><th>Target API</th>"
            f"<th>{label_a}</th><th>{label_b}</th>"
            f"<th>Versus {label_a}</th><th>Why</th><th>Notes</th>"
            "</tr></thead><tbody>"
            + "".join(body_rows)
            + "</tbody></table>"
        )
    provider = html.escape(str(view.get("provider") or "—"))
    base = html.escape(str(view.get("provider_base") or ""))
    chart_json = json.dumps(_chart_model(view), ensure_ascii=False).replace("<", "\\u003c")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(view["title"])}</title>
<link rel="stylesheet" href="{PICO_CSS}">
<style>
main.container {{ max-width: 1280px; padding-bottom: 3rem; }}
.charts {{ display: grid; grid-template-columns: 1fr; gap: 0.75rem; margin: 0.75rem 0 1.25rem; }}
@media (min-width: 1100px) {{
  .charts {{ grid-template-columns: 1fr 1fr 1fr; }}
}}
.chart {{ height: 360px; border: 1px solid #d8dde6; border-radius: 8px; }}
.chart-http {{ grid-column: 1 / -1; height: 280px; }}
.metrics {{ display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 0 0 0.35rem; }}
.metric {{ font-size: 1.35rem; font-weight: 700; line-height: 1; }}
.called {{ font-weight: 600; margin-bottom: 0.2rem; }}
mark.pipeline {{ background-color: #ffe14a; color: #3a2e04; font-weight: 700; padding: 0 0.2rem; border-radius: 3px; }}
mark.missed-strategy {{ background-color: #ff8a1e; color: #3a1500; font-weight: 700; padding: 0 0.2rem; border-radius: 3px; }}
.sub {{ color: #52606d; font-size: 0.72rem; line-height: 1.25; }}
span.tk {{ color: #52606d; font-size: 0.78rem; font-weight: 500; }}
p.tk-note {{ color: #52606d; font-size: 0.82rem; margin-top: 0.35rem; }}
.chart-hint {{ margin-top: 0; }}
table td.better {{ background-color: #21d15a; color: #04210e; font-weight: 700; }}
table td.worse {{ background-color: #ff2d2d; color: #3a0000; font-weight: 700; }}
table td.same, table td.both-hit, table td.both-missed {{ background-color: #8e99a4; color: #14181c; font-weight: 700; }}
table td.not-run {{ background-color: #ffe08a; color: #3a2e04; font-weight: 700; }}
table td.retest {{ background-color: #ff8a1e; color: #3a1500; font-weight: 700; }}
table td.why-one {{ background-color: #ffe14a; color: #3a2e04; }}
table td.why-neither {{ background-color: #ff8a1e; color: #3a1500; }}
table td.why-retest {{ background-color: #ffe0c2; color: #3a1500; }}
table {{ font-size: 0.86rem; }}
#chart-note:empty {{ display: none; }}
</style>
</head>
<body>
{REPORT_CONTRACT}
<main class="container">
<h1>{html.escape(view["title"])}</h1>
<p>Date: {html.escape(view["date"])}<br>
Zeus: {html.escape(str(view.get("zeus_version") or "—"))}<br>
Provider: {provider} {base}<br>
Model: {html.escape(str(view.get("model") or "—"))}<br>
Client: {html.escape(str(view.get("client") or "—"))} {html.escape(str(view.get("client_version") or ""))}</p>
{_summary_html(view)}
<p>Hub Debug, Session lists <code>session</code>. Inspector and Analysis open a <code>req_id</code> from that session. <code>chat</code> is the harness label for the turn. The evidence JSON stores <code>chat_id</code>, <code>turn_id</code>, <code>session_id</code>, and each hop <code>req_id</code>.</p>
<h2>Hits, rounds, and rows</h2>
<p>The first three charts are the comparison. A <strong>hit</strong> of 1 means that pack called the target API. <strong>Rows</strong> are the largest Zeus result on that turn. <strong>Rounds</strong> are how many model turns it used. The pattern to look for is a hit, with rows, in fewer rounds. A missing bar means that side did not run. The HTTP chart counts every Zeus call, including 200, 400, and 500. The verdict column below is still the target-API rule. It does not award a point for extra rows. A turn that ends on HTTP 400 or higher is Orange and stays out of that rule.</p>
<p id="chart-note"></p>
{_chart_boxes("chart-suite")}
<h2>Better, worse, and the score</h2>
<p>The verdict column compares {label_b} with {label_a} on the Target API column. It does not score which prose answer was nicer. A different verb that still returns rows is not a hit.</p>
<ul>
<li><strong>better</strong>: {label_b} called the target API and {label_a} did not.</li>
<li><strong>worse</strong>: {label_a} called the target API and {label_b} did not. On “Find hoppy citrus beers” the target is search hybrid. That row is worse when {label_a} calls search hybrid and {label_b} calls search fts, find, or set, even when both sides are HTTP 200 and both returned beers.</li>
<li><strong>both hit</strong>: both packs met the target.</li>
<li><strong>both missed</strong>: neither pack met the target.</li>
<li><strong>not run</strong>: a model call is missing, so the row is left out of the score.</li>
<li><strong>Orange</strong>: a pack cell ends on HTTP 400 or higher, so the row is re-tested later. The source is <strong>LLM</strong> when the model sent a request Zeus rejected, <strong>Zeus</strong> when the service closed or failed the call, and <strong>koten_converter (FUTURE)</strong> when that hop reports the error. koten_converter is not wired into this suite yet. Orange stays out of better and worse. An earlier HTTP 400 on a turn that ends at 200 stays in the HTTP chart and does not turn the row Orange.</li>
</ul>
<p>Both hit and both missed stay out of the better and worse counts. The score still counts them as same. When the question says rows are required, an empty Zeus result is not met. In a pack cell, <mark class="pipeline">pipeline</mark> means a pipeline ran. <mark class="missed-strategy">fts</mark> means the target was hybrid and this side called fts instead.</p>
<p><strong>Score.</strong> {html.escape(score_line(view.get("score") or {"label_a": view["label_a"], "label_b": view["label_b"], "ratio_a": "0/0", "ratio_b": "0/0", "better_to_worse": "0:0", "net": 0}))} A positive net means {label_b} covered more targets that {label_a} missed than it lost.</p>
<p>{html.escape(view["justification"])}</p>
<p>Suite tally: {html.escape(_display_tally([row for scope in view["scopes"] for row in scope["rows"]]))}.</p>
{"".join(_brief_paragraphs(view))}
{"".join(sections)}
</main>
<script src="{ECHARTS_JS}"></script>
<script>
const AB = {chart_json};
(function () {{
  const note = document.getElementById("chart-note");
  if (!window.echarts) {{
    if (note) note.textContent = "Charts did not load. The tables still list hit, rounds, and rows.";
    return;
  }}
  const colorA = "#3d5a80";
  const colorB = "#2a9d8f";
  function sum(values) {{
    let total = 0;
    let any = false;
    (values || []).forEach(function (value) {{
      if (value == null) return;
      any = true;
      total += Number(value) || 0;
    }});
    return any ? total : null;
  }}
  function paint(id, title, categories, seriesA, seriesB, yName) {{
    const el = document.getElementById(id);
    if (!el) return;
    const chart = echarts.init(el);
    chart.setOption({{
      title: {{ text: title, left: 8, top: 8, textStyle: {{ fontSize: 14, fontWeight: 600 }} }},
      tooltip: {{ trigger: "axis" }},
      legend: {{ data: [AB.label_a, AB.label_b], top: 8, right: 8 }},
      grid: {{ left: 52, right: 16, top: 52, bottom: 88 }},
      xAxis: {{
        type: "category",
        data: categories,
        axisLabel: {{ rotate: 40, fontSize: 10, interval: 0 }}
      }},
      yAxis: {{ type: "value", name: yName, minInterval: 1 }},
      series: [
        {{ name: AB.label_a, type: "bar", data: seriesA, itemStyle: {{ color: colorA }} }},
        {{ name: AB.label_b, type: "bar", data: seriesB, itemStyle: {{ color: colorB }} }}
      ]
    }});
    window.addEventListener("resize", function () {{ chart.resize(); }});
  }}
  const scopeNames = AB.scopes.map(function (scope) {{ return scope.name; }});
  paint(
    "chart-suite-hits",
    "Hits by scope",
    scopeNames,
    AB.scopes.map(function (scope) {{ return sum(scope.hits_a); }}),
    AB.scopes.map(function (scope) {{ return sum(scope.hits_b); }}),
    "hits"
  );
  paint(
    "chart-suite-rounds",
    "Rounds by scope",
    scopeNames,
    AB.scopes.map(function (scope) {{ return sum(scope.rounds_a); }}),
    AB.scopes.map(function (scope) {{ return sum(scope.rounds_b); }}),
    "rounds"
  );
  paint(
    "chart-suite-rows",
    "Rows by scope",
    scopeNames,
    AB.scopes.map(function (scope) {{ return sum(scope.rows_a); }}),
    AB.scopes.map(function (scope) {{ return sum(scope.rows_b); }}),
    "rows"
  );
  paint(
    "chart-suite-http",
    "HTTP calls",
    AB.http_codes || [],
    AB.http_a || [],
    AB.http_b || [],
    "calls"
  );
  AB.scopes.forEach(function (scope) {{
    const prefix = "chart-" + String(scope.name || "scope").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    paint(prefix + "-hits", scope.name + " hits", scope.ids, scope.hits_a, scope.hits_b, "hit");
    paint(prefix + "-rounds", scope.name + " rounds", scope.ids, scope.rounds_a, scope.rounds_b, "rounds");
    paint(prefix + "-rows", scope.name + " rows", scope.ids, scope.rows_a, scope.rows_b, "rows");
    paint(prefix + "-http", scope.name + " HTTP", scope.http_codes || [], scope.http_a || [], scope.http_b || [], "calls");
  }});
}})();
</script>
</body>
</html>
"""


def _brief_paragraphs(view: dict) -> list[str]:
    briefs = view.get("scope_briefs") or []
    if not briefs:
        return []
    measured = any(
        isinstance(item, dict) and item.get("full_chars") is not None for item in briefs
    )
    items = []
    for item in briefs:
        scope = html.escape(str(item.get("scope") or ""))
        version = html.escape(str(item.get("client_version") or ""))
        sha = html.escape(str(item.get("brief_sha12") or ""))
        if measured:
            items.append(
                f"<li>{scope}: brief sha12 {sha}, zeus_client {version}</li>"
            )
            continue
        mini = "yes" if item.get("has_mini_schema") else "no"
        chars = html.escape(str(item.get("chars") or 0))
        items.append(
            f"<li>{scope}: mini-schema {mini}. {chars} UTF-8 bytes cover the "
            "scope-brief slice plus the mini-schema slice. Walk paths are the next heading. "
            f"zeus_client {version}</li>"
        )
    intro = (
        "<p>Live scope brief, mini-schema, and walk paths are sized in the Size section. "
        "Brief text stays out of the evidence file.</p>"
        if measured
        else (
            "<p>Live scope brief merged into both packs through zeus_client "
            "(GET /v1/ai/chat_request.json, suffix from ## SCOPE BRIEF, "
            "which includes ## MINI-SCHEMA and ## WALK_PATHS).</p>"
        )
    )
    return [intro, "<ul>" + "".join(items) + "</ul>"]


def write_bundle(view: dict, directory: Path) -> list[Path]:
    """Write the HTML table and the JSON evidence file with the same stem."""
    directory.mkdir(parents=True, exist_ok=True)
    html_path = directory / f"{view['stem']}.html"
    json_path = directory / f"{view['stem']}.json"
    html_path.write_text(render_html(view))
    json_path.write_text(json.dumps(view, indent=2, ensure_ascii=False) + "\n")
    return [html_path, json_path]


def check_verdicts() -> int:
    same, why = verdict_pair(True, True)
    if same != "same" or "Both" not in why:
        print("verdict same failed", same, why)
        return 1
    better, _ = verdict_pair(False, True)
    if better != "better":
        print("verdict better failed", better)
        return 1
    worse, _ = verdict_pair(True, False)
    if worse != "worse":
        print("verdict worse failed", worse)
        return 1
    missed, why = verdict_pair(False, False)
    if missed != "same" or "Neither" not in why:
        print("verdict neither failed", missed, why)
        return 1
    pending, _ = verdict_pair(None, None)
    if pending != "not run":
        print("verdict pending failed", pending)
        return 1
    both = {"verdict": "same", "a": {"met": True}, "b": {"met": True}}
    neither = {"verdict": "same", "a": {"met": False}, "b": {"met": False}}
    if _display_verdict(both) != "both hit" or _display_verdict(neither) != "both missed":
        print("display verdict failed", _display_verdict(both), _display_verdict(neither))
        return 1
    marked = _mark_called("pipeline, search fts Beer, project", "search hybrid Beer (rows required)")
    if '<mark class="pipeline">' not in marked or '<mark class="missed-strategy">' not in marked:
        print("strategy mark failed", marked)
        return 1
    if "missed-strategy" in _mark_called("search hybrid Beer", "search hybrid Beer (rows required)"):
        print("hybrid call was marked as a miss")
        return 1
    plain = _mark_called("pipeline, search fts Brewery, traverse walk_path", "traverse walk_path Beer")
    if "missed-strategy" in plain or '<mark class="pipeline">' not in plain:
        print("fts marked outside a hybrid target", plain)
        return 1
    mixed = _mark_called("search fts Hotel, search hybrid Hotel", "search hybrid Hotel (rows required)")
    if "missed-strategy" in mixed:
        print("fts marked even though hybrid was called", mixed)
        return 1
    tally = _display_tally([
        {"verdict": "same", "a": {"met": True}, "b": {"met": True}},
        {"verdict": "same", "a": {"met": False}, "b": {"met": False}},
        {"verdict": "better", "a": {"met": False}, "b": {"met": True}},
    ])
    if tally != "better 1, worse 0, both hit 1, both missed 1, Orange 0, not run 0":
        print("display tally failed", tally)
        return 1
    empty = _empty_hit_note({"rows": [{"a": {"hit": True, "met": False, "row_count": 0}, "b": {}}]})
    if "0 rows" not in empty:
        print("empty hit note missing", empty)
        return 1
    if _empty_hit_note({"rows": [{"a": {"hit": True, "met": True, "row_count": 10}, "b": {}}]}):
        print("empty hit note shown for a met row")
        return 1
    if api_error_source(400, "PIPELINE_UNKNOWN_BINDING") != "LLM":
        print("llm source failed")
        return 1
    if api_error_source(429, "session_force_closed") != "Zeus":
        print("zeus source failed")
        return 1
    if api_error_source(500, "koten_converter failed the row") != "koten_converter (FUTURE)":
        print("converter source failed")
        return 1
    if side_turn_fault({"http": 200, "calls": [{"http": 400, "sample": {"error": "ids must be node_ids"}}]}) is not None:
        print("a recovered HTTP 400 was treated as the turn status")
        return 1
    beach = {
        "id": "travel-beach-itinerary",
        "text": "Plan a beach trip for me.",
        "notes": "",
        "target_api": "traverse walk_path",
        "verdict": "worse",
        "why": "The previous pack hit the target API. The new pack did not.",
        "a": {
            "met": True,
            "http": 200,
            "hit": True,
            "rounds": 4,
            "row_count": 15,
            "calls": [{"http": 200, "verb": "traverse", "sample": {}}],
        },
        "b": {
            "met": False,
            "http": 400,
            "hit": False,
            "rounds": 4,
            "row_count": 0,
            "calls": [{
                "http": 400,
                "verb": "pipeline",
                "sample": {"status": "rejected", "error": "PIPELINE_UNKNOWN_BINDING"},
            }],
        },
    }
    orange_view = {
        "title": "base-6.1 vs base-7.0",
        "date": "2026-11-18",
        "label_a": "base-6.1",
        "label_b": "base-7.0",
        "justification": "held",
        "score": {},
        "status": "ran",
        "scopes": [{
            "name": "travel-sample",
            "scopes": ["travel-sample/inventory"],
            "rows": [beach],
        }],
    }
    orange_page = render_html(orange_view)
    if beach["verdict"] != "retest" or "API error" not in beach["why"] or "LLM" not in beach["why"]:
        print("retest failed", beach.get("verdict"), beach.get("why"))
        return 1
    if ">Orange<" not in orange_page or "chart-suite-http" not in orange_page or "td.retest" not in orange_page:
        print("orange page missing the retest mark or the HTTP chart")
        return 1
    if orange_view["tallies"]["worse"] != 0 or orange_view["tallies"]["retest"] != 1:
        print("retest tally failed", orange_view["tallies"])
        return 1
    if "supports using" in orange_view.get("justification", ""):
        print("held-out row was treated as a switch", orange_view["justification"])
        return 1
    render_html(orange_view)
    if beach["verdict"] != "retest":
        print("retest was not stable", beach.get("verdict"))
        return 1
    if side_met({"verb_hit": True, "evidence_nonempty": False}, True) is not False:
        print("required evidence was treated as a hit")
        return 1
    if side_met({"verb_hit": True, "evidence_nonempty": False}, False) is not True:
        print("optional evidence was treated as a miss")
        return 1
    if side_met({"status": "not_run"}, False) is not None:
        print("not_run was scored")
        return 1
    view = build_pending(
        {
            "zeus_version_probed": "0.9.19",
            "questions": [
                {
                    "id": "beer-demo",
                    "scope": "beer-sample/_default",
                    "text": "Find hoppy citrus beers.",
                    "expect": {"all_of": [{"verb": "search", "strategy": "hybrid", "entity_type": "Beer"}]},
                    "evidence_required": True,
                    "notes": "probe note",
                },
                {
                    "id": "travel-demo",
                    "scope": "travel-sample/inventory",
                    "text": "Find beach hotels.",
                    "expect": {"all_of": [{"verb": "search", "strategy": "hybrid", "entity_type": "Hotel"}]},
                    "evidence_required": False,
                },
            ],
        },
        "base-6.1",
        "base-7.x",
        "2026-10-21",
    )
    if view["stem"] != "2026-10-21_base-6_1_vs_base-7_x":
        print("stem failed", view["stem"])
        return 1
    if [scope["name"] for scope in view["scopes"]] != ["beer-sample", "travel-sample"]:
        print("scope split failed", view["scopes"])
        return 1
    if view["tallies"] != {"better": 0, "worse": 0, "same": 0, "retest": 0, "not run": 2, "total": 2}:
        print("tally failed", view["tallies"])
        return 1
    if "does not justify" not in view["justification"]:
        print("justification failed", view["justification"])
        return 1
    score = view.get("score") or {}
    if score.get("ratio_a") != "0/2" or score.get("ratio_b") != "0/2" or score.get("net") != 0:
        print("score failed", score)
        return 1
    if score.get("better_to_worse") != "0:0":
        print("ratio failed", score.get("better_to_worse"))
        return 1
    if "search hybrid Beer" not in view["scopes"][0]["rows"][0]["target_api"]:
        print("target failed", view["scopes"][0]["rows"][0]["target_api"])
        return 1
    if view["scopes"][0]["rows"][0]["a"].get("calls") != []:
        print("pending calls failed", view["scopes"][0]["rows"][0]["a"])
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        written = write_bundle(view, Path(tmp))
        suffixes = sorted(path.suffix for path in written)
        if suffixes != [".html", ".json"]:
            print("bundle files failed", suffixes)
            return 1
        loaded = json.loads((Path(tmp) / f"{view['stem']}.json").read_text())
        if loaded.get("stem") != view["stem"] or loaded.get("tallies") != view["tallies"]:
            print("evidence json failed", loaded.get("stem"), loaded.get("tallies"))
            return 1
        page = (Path(tmp) / f"{view['stem']}.html").read_text()
        if PICO_CSS not in page or ECHARTS_JS not in page:
            print("cdn pin missing")
            return 1
        if "echarts@latest" in page or "@picocss/pico@2/" in page:
            print("cdn pin floated")
            return 1
        for pin in ("chart-suite-hits", "chart-suite-rounds", "chart-suite-rows", "chart-suite-http", "chart-beer-sample-rows"):
            if pin not in page:
                print("chart missing", pin)
                return 1
        if "<h2>Summary</h2>" not in page:
            print("summary missing")
            return 1
        if "report-contract: baseline/AGENT.md" not in page or "CR-35 method" not in page:
            print("report contract or CR-35 story missing")
            return 1
        if "Pack text was not measured" in page:
            print("known pair was not measured")
            return 1
        later = _summary_html(
            {
                "label_a": "base-6.1",
                "label_b": "base-does-not-exist",
                "justification": "later",
                "score": {},
                "scopes": [],
            }
        )
        if "Pack text was not measured" not in later or "CR-35 method" in later:
            print("later pair borrowed the CR-35 story", later[:400])
            return 1
        facts = _prompt_facts("base-6.1", "base-7.x")
        if not facts or not facts.get("has_plan") or not facts.get("rail_chars"):
            print("prompt facts failed")
            return 1
        if _tokens("") != 0 or _tokens("abcd") != 1 or _tokens("abcde") != 2:
            print("token budget failed", _tokens(""), _tokens("abcd"), _tokens("abcde"))
            return 1
        if facts["tk_b"] - facts["tk_a"] != facts["content_tk"] + facts["json_wrap_tk"]:
            print("token budget does not add up", facts["tk_a"], facts["tk_b"], facts["content_tk"], facts["json_wrap_tk"])
            return 1
        if " tk)" not in page or "tk-note" not in page:
            print("token line missing")
            return 1
        if "Full injection" in page:
            print("pending page invented an injection table")
            return 1
        import hashlib

        import scope_brief

        sample_brief = "## SCOPE BRIEF\nalpha"
        sample_mini = "## MINI-SCHEMA\n### Beer\nname"
        sample_walk = "## WALK_PATHS\ncity"
        sample_full = f"{sample_brief}\n\n{sample_mini}\n\n{sample_walk}"
        counted = scope_brief.injection_counts("You are a pack.\n\n" + sample_full)
        if counted["scope_brief"]["chars"] != len(sample_brief):
            print("scope brief slice failed", counted["scope_brief"])
            return 1
        if counted["mini_schema"]["chars"] != len(sample_mini):
            print("mini slice failed", counted["mini_schema"])
            return 1
        if counted["walk_paths"]["chars"] != len(sample_walk):
            print("walk slice failed", counted["walk_paths"])
            return 1
        if counted["full"]["chars"] != len(sample_full):
            print("full suffix failed", counted["full"])
            return 1
        expect_sha = hashlib.sha256(sample_brief.encode("utf-8")).hexdigest()[:12]
        if counted["scope_brief"]["sha12"] != expect_sha:
            print("brief sha failed", counted["scope_brief"]["sha12"], expect_sha)
            return 1
        if counted["scope_brief"]["bytes"] + counted["mini_schema"]["bytes"] == counted["full"]["bytes"]:
            print("walk paths were folded into the old byte sum")
            return 1
        joined_chars, joined_tk = _append_suffix("pack text\n", 5, 5)
        if joined_chars != len("pack text") + 2 + 5 or joined_tk != _tokens_from_bytes(len("pack text") + 2 + 5):
            print("suffix append failed", joined_chars, joined_tk)
            return 1
        injected = _summary_html(
            {
                "label_a": "base-6.1",
                "label_b": "base-7.x",
                "justification": "later",
                "score": {},
                "scopes": [],
                "scope_briefs": [
                    {
                        "scope": "beer-sample/_default",
                        "chars": 30,
                        "brief_sha12": "090e8427ceb0",
                        "scope_brief_chars": 10,
                        "scope_brief_bytes": 10,
                        "scope_brief_tk": 3,
                        "mini_schema_chars": 12,
                        "mini_schema_bytes": 12,
                        "mini_schema_tk": 3,
                        "walk_paths_chars": 4,
                        "walk_paths_bytes": 4,
                        "walk_paths_tk": 1,
                        "full_chars": 30,
                        "full_bytes": 30,
                        "full_tk": 8,
                        "injection_source": "turn",
                    }
                ],
            }
        )
        if "Mini-schema" not in injected or "Full injection" not in injected or "40.0%" not in injected:
            print("injection table failed")
            return 1
        if "catalog fetch after the run" in injected:
            print("turn source was labeled as a later fetch")
            return 1
        if "System message after that suffix" not in injected:
            print("appended system message missing")
            return 1
        if _prompt_facts("base-6.1", "base-does-not-exist") is not None:
            print("missing pack was measured")
            return 1
        if _prompt_facts("../base-6.1", "base-7.x") is not None:
            print("pack path escaped the label")
            return 1
        for color in ("#21d15a", "#ff2d2d", "#8e99a4", "#ffe14a", "#ff8a1e", "mark.pipeline", "both-hit", "both-missed", "missed-strategy"):
            if color not in page:
                print("verdict color missing", color)
                return 1
    print("report verdict check ok")
    return 0
