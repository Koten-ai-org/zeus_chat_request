#!/usr/bin/env python3
"""Compare two chat_request packs on one Zeus and one model.

The model sees the pack's system text plus the live SCOPE BRIEF. Each
question runs through zeus_client ZeusRuntime.agent.run_turn, which opens
a durable /v2/session and stamps the trace headers Hub Debug needs.
Passwords and API keys stay in baseline/.env, which is gitignored.

  ZEUS_URL, ZEUS_USER_BEER, ZEUS_PASS_BEER, ZEUS_USER_TRAVEL,
  ZEUS_PASS_TRAVEL, LLM_API_KEY, LLM_MODEL, LLM_PROVIDER, LLM_BASE_URL

Optional script ceilings, used as written (not reduced a second time):
  LLM_TPM, LLM_RPM, LLM_RPS, LLM_REQUEST_TOKENS

Beer-sample and travel-sample each get a runtime and run at the same time.
They share one provider budget. Questions inside one scope stay in order.
The two packs still run one after the other.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Mapping
from datetime import date
from pathlib import Path

import client_turn
import provider_budget
import report_bundle

# OpenAI chat-completions bases. The client posts {base}/chat/completions.
# Docs and the compatibility note live in baseline/README.md.
PROVIDERS = {
    "xai": "https://api.x.ai/v1",
    "openai": "https://api.openai.com/v1",
    "groq": "https://api.groq.com/openai/v1",
    "together": "https://api.together.xyz/v1",
    "fireworks": "https://api.fireworks.ai/inference/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "deepseek": "https://api.deepseek.com",
    "mistral": "https://api.mistral.ai/v1",
    "cerebras": "https://api.cerebras.ai/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai",
    "perplexity": "https://api.perplexity.ai/v2",
}


def parse_env_text(text: str) -> dict[str, str]:
    """Read KEY=VALUE lines. Blank lines and comments are skipped."""
    values: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        if key:
            values[key] = value
    return values


def load_env_file(path: Path) -> None:
    """Fill missing process env vars from a file. Existing vars win."""
    if not path.is_file():
        return
    for key, value in parse_env_text(path.read_text()).items():
        if key not in os.environ:
            os.environ[key] = value


def load_local_env() -> None:
    """Load repo-root .env, then baseline/.env.

    A name already set in the process stays. When both files set the same
    name, baseline/.env wins. Values are never printed.
    """
    here = Path(__file__).resolve().parent
    root = here.parent
    original = set(os.environ)
    load_env_file(root / ".env")
    baseline = here / ".env"
    if not baseline.is_file():
        return
    for key, value in parse_env_text(baseline.read_text()).items():
        if key not in original:
            os.environ[key] = value


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def response_req_id(headers, body: dict | str) -> str:
    """Zeus echoes the debugger id on X-Zeus-Req-Id. Some bodies also carry req_id."""
    if headers is not None:
        header = headers.get("X-Zeus-Req-Id") or headers.get("X-Request-Id") or ""
        if header:
            return str(header)
    if isinstance(body, dict):
        value = body.get("req_id")
        if isinstance(value, str) and value:
            return value
    return ""


def request_json(method: str, url: str, payload: dict | None, headers: dict, timeout: int) -> tuple[int, dict | str, int, str]:
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    started = time.perf_counter()
    last_error = "transport"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode()
                ms = int((time.perf_counter() - started) * 1000)
                try:
                    body = json.loads(raw) if raw else {}
                except json.JSONDecodeError:
                    body = raw[:2000]
                return resp.status, body, ms, response_req_id(resp.headers, body)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode(errors="replace")
            ms = int((time.perf_counter() - started) * 1000)
            try:
                body = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                body = raw[:2000]
            return exc.code, body, ms, response_req_id(exc.headers, body)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = type(exc).__name__
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
    ms = int((time.perf_counter() - started) * 1000)
    return 0, {"error": "transport", "message": last_error}, ms, ""


def resolve_llm(
    provider: str | None,
    base_url: str | None,
    env: Mapping[str, str],
) -> tuple[str, str] | None:
    """Provider name plus base URL. CLI wins, then the env, then the table.

    An unknown name is accepted when a base URL is set. That URL must
    serve OpenAI chat completions at ``{base}/chat/completions``.
    """
    name = (provider or env.get("LLM_PROVIDER") or "xai").strip().lower()
    base = (base_url or env.get("LLM_BASE_URL") or "").strip().rstrip("/")
    if not base:
        base = PROVIDERS.get(name, "")
    if not name or not base:
        return None
    return name, base


def scope_groups(questions: list[dict]) -> list[tuple[str, list[dict]]]:
    """Bucket questions by scope, preserving file order inside each bucket."""
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for question in questions:
        scope = str(question.get("scope") or "")
        bucket = scope.split("/", 1)[0] or scope or "scope"
        if bucket not in groups:
            groups[bucket] = []
            order.append(bucket)
        groups[bucket].append(question)
    return [(bucket, groups[bucket]) for bucket in order]


def credentials_for(bucket: str) -> tuple[str, str]:
    """Beer and travel each have their own login. Do not reuse one for the other."""
    if bucket == "beer-sample":
        user = os.environ.get("ZEUS_USER_BEER", "") or os.environ.get("ZEUS_USER", "")
        password = os.environ.get("ZEUS_PASS_BEER", "") or os.environ.get("ZEUS_PASS", "")
        return user, password
    if bucket == "travel-sample":
        return os.environ.get("ZEUS_USER_TRAVEL", ""), os.environ.get("ZEUS_PASS_TRAVEL", "")
    return os.environ.get("ZEUS_USER", ""), os.environ.get("ZEUS_PASS", "")


def zeus_version(base: str) -> str:
    status, body, _, _req = request_json("GET", base.rstrip("/") + "/version", None, {}, 15)
    if status != 200:
        return f"http_{status}"
    if isinstance(body, dict):
        return str(body.get("version") or body)
    text = str(body).strip().strip('"')
    return text


def flatten_calls(calls: list[dict]) -> list[dict]:
    """Top-level tool calls plus steps inside a pipeline."""
    out: list[dict] = []
    for call in calls:
        out.append(call)
        if call.get("verb") != "pipeline":
            continue
        steps = (call.get("args") or {}).get("steps") or []
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            params = step.get("params") if isinstance(step.get("params"), dict) else {}
            merged = {
                key: value
                for key, value in step.items()
                if key not in {"as", "verb", "params", "on_error", "abort_if_empty", "step_timeout_ms"}
            }
            merged.update(params)
            out.append({"verb": step.get("verb"), "args": merged, "via": "pipeline"})
    return out


def spec_matches(spec: dict, call: dict) -> bool:
    args = call.get("args") or {}
    if not isinstance(args, dict):
        args = {}
    for key, expected in spec.items():
        if key == "verb":
            if call.get("verb") != expected:
                return False
            continue
        if args.get(key) != expected:
            return False
    return True


def score_question(question: dict, calls: list[dict], http_status: int | None, evidence: bool) -> dict:
    flat = flatten_calls(calls)
    expect = question.get("expect") or {}
    all_of = expect.get("all_of") or []
    any_of = expect.get("any_of") or []
    missing = [spec for spec in all_of if not any(spec_matches(spec, call) for call in flat)]
    any_hit = True if not any_of else any(spec_matches(spec, call) for spec in any_of for call in flat)
    verb_hit = not missing and any_hit
    return {
        "verb_hit": verb_hit,
        "missing": missing,
        "evidence_nonempty": evidence,
        "evidence_required": bool(question.get("evidence_required")),
        "http_status": http_status,
        "verbs": [call.get("verb") for call in flat],
    }


def evidence_nonempty(body: dict | str) -> bool:
    if not isinstance(body, dict):
        return False
    blobs = [body]
    result = body.get("result")
    if isinstance(result, dict):
        blobs.append(result)
    data = body.get("data")
    if isinstance(data, dict):
        blobs.append(data)
        cards = data.get("cards")
        if isinstance(cards, dict):
            blobs.append(cards)
    so_far = body.get("results_so_far")
    if isinstance(so_far, dict):
        blobs.extend(value for value in so_far.values() if isinstance(value, dict))
    for blob in blobs:
        for key in ("items", "node_ids", "rows", "ids", "src_keys"):
            value = blob.get(key)
            if isinstance(value, list) and value:
                return True
        cards = blob.get("cards")
        if isinstance(cards, dict):
            rows = cards.get("rows")
            if isinstance(rows, list) and rows:
                return True
    return False


def evidence_sample(body: dict | str) -> dict:
    """Short proof of what Zeus returned. No session, key, or password fields."""
    if not isinstance(body, dict):
        text = str(body)[:240]
        return {"text": text} if text else {}
    hidden = {"api_key", "authorization", "password", "session_id", "token", "secret"}
    sample: dict = {}
    for key in ("status", "error", "message", "reason"):
        value = body.get(key)
        if key in hidden or value in (None, "", {}, []):
            continue
        sample[key] = value if isinstance(value, (str, int, float, bool)) else str(value)[:200]
    blobs = [body]
    for key in ("result", "data"):
        value = body.get(key)
        if isinstance(value, dict):
            blobs.append(value)
    so_far = body.get("results_so_far")
    if isinstance(so_far, dict):
        blobs.extend(value for value in so_far.values() if isinstance(value, dict))
    best: list = []
    for blob in blobs:
        for key in ("items", "node_ids", "rows", "ids", "src_keys"):
            value = blob.get(key)
            if isinstance(value, list) and len(value) > len(best):
                best = value
        cards = blob.get("cards")
        if isinstance(cards, dict) and isinstance(cards.get("rows"), list) and len(cards["rows"]) > len(best):
            best = cards["rows"]
    if best:
        sample["row_count"] = len(best)
        sample["preview"] = [_preview_item(item) for item in best[:3]]
    return sample


def _preview_item(item) -> object:
    if not isinstance(item, dict):
        return str(item)[:80]
    node = item.get("node") if isinstance(item.get("node"), dict) else item
    meta = node.get("metadata") if isinstance(node.get("metadata"), dict) else {}
    picked = {}
    for key in ("doc_key", "id", "name", "entity_type"):
        value = node.get(key)
        if value in (None, "") and key in meta:
            value = meta.get(key)
        if value not in (None, ""):
            picked[key] = value
    if not picked:
        picked["keys"] = sorted(str(key) for key in node.keys())[:8]
    return picked


def slim_args(args: dict) -> dict:
    """Keep the fields that show which API was called. Drop bulk id lists."""
    if not isinstance(args, dict):
        return {}
    slim = {}
    for key in ("entity_type", "strategy", "shape", "query_text", "limit", "name", "format"):
        if key in args:
            slim[key] = args[key]
    where = args.get("where")
    if isinstance(where, dict):
        slim["where"] = {key: where[key] for key in list(where)[:6]}
    walk = args.get("walk_path")
    if isinstance(walk, dict):
        kept = {}
        for key in ("from", "path", "where", "limit", "return", "aggregate"):
            if key in walk:
                kept[key] = walk[key]
        slim["walk_path"] = kept
    steps = args.get("steps")
    if isinstance(steps, list):
        slim["steps"] = []
        for step in steps[:8]:
            if not isinstance(step, dict):
                continue
            merged = dict(step)
            params = step.get("params")
            if isinstance(params, dict):
                merged.update(params)
            one = slim_args(merged)
            if step.get("verb"):
                one["verb"] = step["verb"]
            if step.get("as"):
                one["as"] = step["as"]
            slim["steps"].append(one)
    return slim


def print_table(report: dict) -> None:
    print(
        f"zeus {report['zeus_version']}  provider {report['provider']}  model {report['model']}"
    )
    packs = report.get("packs") or []
    if len(packs) < 2:
        print("incomplete suite")
        return
    print(f"{'question':<24} {'A verb':<8} {'A rows':<8} {'B verb':<8} {'B rows':<8}")
    by_a = {row["id"]: row for row in packs[0]["questions"]}
    by_b = {row["id"]: row for row in packs[1]["questions"]}
    for key in by_a:
        a = by_a[key]
        b = by_b.get(key) or {}
        print(
            f"{key:<24} {str(a.get('verb_hit')):<8} {str(a.get('evidence_nonempty')):<8} "
            f"{str(b.get('verb_hit')):<8} {str(b.get('evidence_nonempty')):<8}"
        )


def _suite_rows(doc: dict) -> list[dict]:
    """The fields that define the test. Notes can change. These cannot."""
    rows = []
    for question in doc.get("questions") or []:
        rows.append(
            {
                "id": question.get("id"),
                "scope": question.get("scope"),
                "collection": question.get("collection"),
                "text": question.get("text"),
                "expect": question.get("expect"),
                "evidence_required": bool(question.get("evidence_required")),
            }
        )
    return rows


def check_question_lock() -> int:
    """Fail when the locked suite drifts from baseline/suite.lock.json."""
    root = Path(__file__).resolve().parent
    suite = json.loads((root / "questions.json").read_text())
    locked = json.loads((root / "suite.lock.json").read_text())
    current = _suite_rows(suite)
    frozen = _suite_rows(locked)
    if current != frozen:
        print("question suite does not match baseline/suite.lock.json")
        return 1
    scopes = [str(row.get("scope") or "").split("/", 1)[0] for row in current]
    if len(current) != 21 or scopes.count("beer-sample") != 11 or scopes.count("travel-sample") != 10:
        print("question suite shape failed", len(current), scopes.count("beer-sample"), scopes.count("travel-sample"))
        return 1
    return 0


def self_check() -> int:
    if check_question_lock() != 0:
        return 1
    question = {
        "id": "demo",
        "evidence_required": True,
        "expect": {"all_of": [{"verb": "pipeline"}, {"verb": "search", "strategy": "hybrid", "entity_type": "Beer"}]},
    }
    calls = [
        {
            "verb": "pipeline",
            "args": {
                "steps": [
                    {"as": "recall", "verb": "search", "params": {"strategy": "hybrid", "entity_type": "Beer", "query_text": "hoppy citrus"}}
                ]
            },
        }
    ]
    scored = score_question(question, calls, 200, True)
    if not scored["verb_hit"] or scored["missing"]:
        print("self-check failed", scored)
        return 1
    slimmed = [{"verb": "pipeline", "args": slim_args(calls[0]["args"])}]
    if not score_question(question, slimmed, 200, True)["verb_hit"]:
        print("self-check slim score failed", slimmed)
        return 1
    sample = evidence_sample({"result": {"items": [{"node": {"doc_key": "x", "name": "IPA"}}]}})
    if sample.get("row_count") != 1 or sample["preview"][0].get("name") != "IPA":
        print("self-check sample failed", sample)
        return 1
    empty = score_question(question, [{"verb": "find", "args": {"entity_type": "Beer"}}], 200, False)
    if empty["verb_hit"]:
        print("self-check expected a miss", empty)
        return 1
    body = {"result": {"items": [{"node": {"doc_key": "x"}}], "node_ids": []}}
    if not evidence_nonempty(body):
        print("self-check evidence failed")
        return 1
    cards = {"result": {"cards": {"rows": [{"doc_key": "hotel_26497", "name": "Loews Santa Monica Beach Hotel"}]}}}
    if not evidence_nonempty(cards):
        print("self-check card evidence failed")
        return 1
    parsed = parse_env_text(
        "\n# comment\nexport LLM_MODEL=grok-4.7\nZEUS_USER='kept'\nSKIP\n"
    )
    if parsed != {"LLM_MODEL": "grok-4.7", "ZEUS_USER": "kept"}:
        print("self-check env parse failed")
        return 1
    if response_req_id({"X-Zeus-Req-Id": "req-1"}, {}) != "req-1":
        print("self-check req_id failed")
        return 1
    if response_req_id(None, {"req_id": "req-2"}) != "req-2":
        print("self-check body req_id failed")
        return 1
    if report_bundle.check_verdicts() != 0:
        return 1
    traced = client_turn.tool_rows_from_trace(
        [
            {
                "type": "tool",
                "name": "find",
                "round": 1,
                "args": {"entity_type": "Beer", "where": {"style": "ipa"}},
                "status": 200,
                "req_id": "11111111-1111-4111-8111-111111111111",
            }
        ],
        [
            {
                "req_id": "11111111-1111-4111-8111-111111111111",
                "result_json": {"result": {"items": [{"node": {"name": "IPA"}}]}},
            }
        ],
    )
    if len(traced) != 1 or traced[0]["verb"] != "find" or traced[0]["http"] != 200:
        print("self-check trace map failed", traced)
        return 1
    if not evidence_nonempty(traced[0]["body"]):
        print("self-check trace evidence failed", traced)
        return 1
    posted_return = client_turn.tool_rows_from_trace(
        [{"type": "return", "round": 2, "args": {"summary": "done"}, "status": 200, "req_id": "r1"}],
        [],
    )
    if posted_return[0]["http"] != 200 or posted_return[0]["body"].get("posted") is not True:
        print("self-check posted return failed", posted_return)
        return 1
    local_return = client_turn.tool_rows_from_trace(
        [{"type": "return", "round": 2, "args": {}}],
        [],
    )
    if local_return[0]["http"] != 0 or local_return[0]["body"].get("skipped") is not True:
        print("self-check local return failed", local_return)
        return 1
    if client_turn.chat_id_for("2026-10-21", "base-6.1", "beer-find-style") != "ab-2026-10-21-base-6-1-beer-find-style":
        print("self-check chat id failed")
        return 1
    groq = resolve_llm(None, None, {"LLM_PROVIDER": "groq"})
    if groq != ("groq", PROVIDERS["groq"]):
        print("self-check provider failed", groq)
        return 1
    override = resolve_llm("xai", None, {"LLM_BASE_URL": "https://example.test/v1/"})
    if override != ("xai", "https://example.test/v1"):
        print("self-check provider override failed", override)
        return 1
    if resolve_llm("custom", None, {}) is not None:
        print("self-check unknown provider should fail")
        return 1
    groups = scope_groups(
        [
            {"id": "b", "scope": "beer-sample/_default"},
            {"id": "t", "scope": "travel-sample/inventory"},
            {"id": "b2", "scope": "beer-sample/_default"},
        ]
    )
    if [name for name, _rows in groups] != ["beer-sample", "travel-sample"]:
        print("self-check scope groups failed", groups)
        return 1
    if [row["id"] for row in groups[0][1]] != ["b", "b2"]:
        print("self-check scope order failed", groups)
        return 1
    if provider_budget.self_check() != 0:
        return 1
    print("self-check ok")
    return 0


def row_from_result(question: dict, result) -> tuple[dict, dict]:
    """Score one client turn. The Hub session id is kept; the auth token is not."""
    debug = result.debug
    public = debug.public_trace if isinstance(debug.public_trace, Mapping) else {}
    steps = list(public.get("steps") or [])
    hops = [dict(hop) for hop in (debug.hops or ()) if isinstance(hop, Mapping)]
    raw_calls = client_turn.tool_rows_from_trace(steps, hops)
    error_info = result.error
    if error_info is not None and str(error_info.code) == "060006":
        verb = ""
        details = error_info.details if isinstance(error_info.details, dict) else {}
        verb = str(details.get("verb") or "")
        if verb and not any(call.get("verb") == verb for call in raw_calls):
            raw_calls.append(
                {
                    "round": debug.rounds or 1,
                    "verb": verb,
                    "args": {},
                    "http": 0,
                    "req_id": "",
                    "body": {"skipped": True, "reason": "verb is not posted by zeus_client"},
                }
            )
    calls = []
    last_http = None
    saw_evidence = False
    for call in raw_calls:
        body = call.get("body") if isinstance(call.get("body"), dict) else {}
        http = call.get("http")
        if http:
            last_http = http
        if evidence_nonempty(body):
            saw_evidence = True
        slim = slim_args(call.get("args") if isinstance(call.get("args"), dict) else {})
        calls.append(
            {
                "round": call.get("round") or 0,
                "verb": call.get("verb"),
                "args": slim,
                "http": http if http is not None else 0,
                "req_id": call.get("req_id") or "",
                "evidence": evidence_nonempty(body),
                "sample": evidence_sample(body),
            }
        )
    scored = score_question(question, calls, last_http, saw_evidence)
    session = result.session
    session_id = str(debug.session_id or "")
    if not session_id and session is not None:
        session_id = str(session.session_id or "")
    chat_id = str(debug.chat_id or "")
    if not chat_id and session is not None:
        chat_id = str(session.chat_id or "")
    error = None
    if not calls and error_info is not None:
        error = {"where": "client", "body": str(error_info.message or "")[:300]}
    session_error = ""
    if session is not None and session.error:
        session_error = str(session.error)[:300]
    if not session_id and session_error and error is None:
        error = {"where": "session", "body": session_error}
    notes = []
    for note in debug.notes or ():
        text = str(note)
        if text.startswith(("session", "turn_error", "llm_error", "scope_brief")):
            notes.append(text[:240])
    zeus_ms = 0
    for hop in hops:
        try:
            zeus_ms += int(hop.get("ms") or 0)
        except (TypeError, ValueError):
            continue
    req_ids = [str(item) for item in (debug.req_ids or ()) if item]
    for call in calls:
        if call["req_id"] and call["req_id"] not in req_ids:
            req_ids.append(call["req_id"])
    row = {
        "id": question["id"],
        "text": question["text"],
        "scope": question["scope"],
        "rounds_used": debug.rounds or max((call["round"] for call in calls), default=0),
        "llm_ms": 0,
        "zeus_ms": zeus_ms,
        "error": error,
        "chat_id": chat_id,
        "turn_id": str(debug.turn_id or ""),
        "session_id": session_id,
        "contract_status": debug.contract_status or "",
        "client_version": str(debug.client_version or ""),
        "hub_notes": notes,
        "req_ids": req_ids,
        "calls": [
            {
                "round": call["round"],
                "verb": call["verb"],
                "strategy": (call["args"] or {}).get("strategy"),
                "entity_type": (call["args"] or {}).get("entity_type"),
                "shape": (call["args"] or {}).get("shape"),
                "http": call["http"],
                "req_id": call.get("req_id") or "",
                "evidence": call["evidence"],
                "args": call["args"],
                "sample": call["sample"],
            }
            for call in calls
        ],
        **scored,
    }
    return row, client_turn.brief_flags(result)


def _print_turn(label: str, row: dict) -> None:
    err = (row.get("error") or {}).get("where") or "-"
    reqs = ",".join(row.get("req_ids") or []) or "-"
    print(
        f"{label} {row['id']} hit={row['verb_hit']} rows={row['evidence_nonempty']} "
        f"http={row['http_status']} err={err} "
        f"session={row.get('session_id') or 'MISSING'} "
        f"chat={row.get('chat_id') or '-'} turn={row.get('turn_id') or '-'} "
        f"reqs={reqs}",
        flush=True,
    )


def _empty_session_detail(row: dict) -> str:
    if row.get("hub_notes"):
        return "; ".join(row["hub_notes"])
    if row.get("error"):
        return str((row.get("error") or {}).get("body") or "")
    return ""


async def _run_scope(
    runtime,
    pack: dict,
    questions: list[dict],
    label: str,
    args,
    report_date: str,
    stop: asyncio.Event,
    budget_reasons: list[str],
) -> tuple[list[dict], tuple[str, dict] | None]:
    """Questions for one scope, in file order. stop ends the scope after the current turn."""
    rows: list[dict] = []
    stored: tuple[str, dict] | None = None
    for question in questions:
        if stop.is_set():
            break
        try:
            result = await client_turn.ask(
                runtime,
                pack=pack,
                question=question,
                label=label,
                model=args.model,
                max_rounds=args.max_rounds,
                report_date=report_date,
                mode=args.mode,
            )
        except provider_budget.BudgetExceeded as exc:
            # The sibling finishes the turn already in flight, then both stop.
            # Do not shrink the prompt and do not write a partial comparison.
            print(
                f"provider budget exceeded for {label} {question.get('id')}: {exc}",
                file=sys.stderr,
                flush=True,
            )
            if not budget_reasons:
                budget_reasons.append(str(exc))
            stop.set()
            break
        row, brief = row_from_result(question, result)
        rows.append(row)
        if stored is None and brief.get("has_scope_brief"):
            stored = (question["scope"], brief)
        _print_turn(label, row)
        if not row.get("session_id"):
            stop.set()
            detail = _empty_session_detail(row)
            print(
                f"Hub session_id is empty for {label} {row['id']}. {detail}".rstrip(),
                file=sys.stderr,
                flush=True,
            )
            break
    return rows, stored


async def run_suite(
    questions: list[dict],
    args,
    report_date: str,
    version: str,
    budget: provider_budget.ProviderBudget,
) -> tuple[dict, bool, str]:
    """One event loop. Each scope has its own runtime so beer and travel overlap.

    An empty session_id, or a request that cannot fit the shared provider
    budget, stops both scopes after the turn that is already in flight.
    """
    groups = scope_groups(questions)
    runtimes = {
        bucket: client_turn.open_runtime(
            zeus_url=args.zeus_url,
            provider=args.provider,
            base_url=args.base_url,
            model=args.model,
            mode=args.mode,
            max_rounds=args.max_rounds,
            budget=budget,
        )
        for bucket, _scope_questions in groups
    }
    briefs: dict[str, dict] = {}
    packs = []
    hub_ok = True
    budget_stop = ""
    try:
        for label, path in ((args.label_a, args.pack_a), (args.label_b, args.pack_b)):
            pack = load_json(path)
            names = ", ".join(bucket for bucket, _rows in groups)
            print(f"{label} running together: {names}", flush=True)
            stop = asyncio.Event()
            budget_reasons: list[str] = []
            async with asyncio.TaskGroup() as group:
                tasks = [
                    group.create_task(
                        _run_scope(
                            runtimes[bucket],
                            pack,
                            scope_questions,
                            label,
                            args,
                            report_date,
                            stop,
                            budget_reasons,
                        )
                    )
                    for bucket, scope_questions in groups
                ]
            parts = [task.result() for task in tasks]
            by_id: dict[str, dict] = {}
            for rows, stored in parts:
                for row in rows:
                    by_id[row["id"]] = row
                if stored is not None:
                    scope_key, brief = stored
                    if scope_key not in briefs:
                        briefs[scope_key] = brief
            ordered = [by_id[question["id"]] for question in questions if question["id"] in by_id]
            if len(ordered) != len(questions) or stop.is_set():
                hub_ok = False
                if budget_reasons and not budget_stop:
                    budget_stop = budget_reasons[0]
            lineage = pack.get("_lineage") or {}
            hits = sum(1 for row in ordered if row.get("verb_hit"))
            packs.append(
                {
                    "label": label,
                    "path": str(path),
                    "base_id": lineage.get("base_id"),
                    "verb_hits": hits,
                    "questions_run": len(ordered),
                    "questions": ordered,
                }
            )
            if not hub_ok:
                break
    finally:
        for runtime in runtimes.values():
            await runtime.aclose()
    report = {
        "suite": args.suite_name,
        "zeus_url": args.zeus_url,
        "zeus_version": version,
        "provider": args.provider,
        "provider_base": args.base_url,
        "model": args.model,
        "max_rounds": args.max_rounds,
        "client": "zeus_client.run_turn",
        "client_version": next(
            (
                row.get("client_version")
                for pack in packs
                for row in pack["questions"]
                if row.get("client_version")
            ),
            "",
        ),
        "packs": packs,
        "scope_briefs": list(briefs.values()),
    }
    return report, hub_ok, budget_stop


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--pack-a", type=Path)
    parser.add_argument("--pack-b", type=Path)
    parser.add_argument("--label-a", default="A")
    parser.add_argument("--label-b", default="B")
    parser.add_argument("--questions", type=Path, default=Path("baseline/questions.json"))
    parser.add_argument("--mode", default="analytics", help="Mode passed when fetching the live scope brief")
    parser.add_argument(
        "--provider",
        default=None,
        help="LLM provider name. Overrides LLM_PROVIDER. Default xai. See baseline/README.md.",
    )
    parser.add_argument("--base-url", default=None, help="Overrides LLM_BASE_URL and the provider table")
    parser.add_argument("--model", default=None, help="Overrides LLM_MODEL")
    parser.add_argument("--zeus-url", default=os.environ.get("ZEUS_URL", ""))
    parser.add_argument("--max-rounds", type=int, default=4)
    parser.add_argument("--id", action="append", dest="ids", help="Run only these question ids. Repeatable.")
    parser.add_argument("--out", type=Path, default=Path("/tmp/chat_request_ab.json"))
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("baseline/reports"),
        help="Directory for the dated HTML table and JSON evidence file",
    )
    parser.add_argument("--report-date", default="", help="Date prefix for the report files, YYYY-MM-DD")
    parser.add_argument(
        "--preview-report",
        action="store_true",
        help="Write the report shell from the question file. Does not call the model or Zeus.",
    )
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    load_local_env()
    if not args.zeus_url:
        args.zeus_url = os.environ.get("ZEUS_URL", "")
    if not args.model:
        args.model = os.environ.get("LLM_MODEL", "")
    resolved = resolve_llm(args.provider, args.base_url, os.environ)
    if resolved is None:
        known = ", ".join(sorted(PROVIDERS))
        print(
            "Set LLM_PROVIDER to a known name or set LLM_BASE_URL. "
            f"Known names: {known}.",
            file=sys.stderr,
        )
        return 2
    args.provider, args.base_url = resolved
    report_date = args.report_date or date.today().isoformat()
    if args.preview_report:
        suite = load_json(args.questions)
        label_a = args.label_a if args.label_a != "A" else "base-6.1"
        label_b = args.label_b if args.label_b != "B" else "base-7.x"
        view = report_bundle.build_pending(suite, label_a, label_b, report_date)
        written = report_bundle.write_bundle(view, args.reports_dir)
        for path in written:
            print(f"wrote {path}")
        return 0
    if not args.pack_a or not args.pack_b or not args.model:
        parser.error("--pack-a, --pack-b, and --model (or LLM_MODEL in baseline/.env) are required")
    args.api_key = os.environ.get("LLM_API_KEY", "")
    beer_user, beer_pass = credentials_for("beer-sample")
    travel_user, travel_pass = credentials_for("travel-sample")
    if not args.zeus_url or not args.api_key or not beer_user or not beer_pass or not travel_user or not travel_pass:
        print(
            "Set ZEUS_URL, ZEUS_USER_BEER, ZEUS_PASS_BEER, ZEUS_USER_TRAVEL, "
            "ZEUS_PASS_TRAVEL, and LLM_API_KEY in baseline/.env.",
            file=sys.stderr,
        )
        return 2
    suite = load_json(args.questions)
    questions = suite.get("questions") or []
    if args.ids:
        wanted = set(args.ids)
        questions = [question for question in questions if question["id"] in wanted]
        if not questions:
            print("no questions matched --id", file=sys.stderr)
            return 2
    try:
        budget = provider_budget.budget_for(args.provider, args.model, os.environ)
    except provider_budget.BudgetConfigError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(budget.pace_line(), flush=True)
    version = zeus_version(args.zeus_url)
    args.suite_name = suite.get("suite")
    report, hub_ok, budget_stop = asyncio.run(run_suite(questions, args, report_date, version, budget))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print_table(report)
    print(f"wrote {args.out}")
    if not hub_ok:
        messages = []
        if budget_stop:
            messages.append(f"Stopped because the provider budget would be exceeded. {budget_stop}")
        missing_session = any(
            not row.get("session_id")
            for pack in report["packs"]
            for row in pack["questions"]
        )
        if missing_session or not budget_stop:
            messages.append("Stopped because a turn had no Hub session_id.")
        messages.append("The comparison HTML and JSON were not written.")
        print(" ".join(messages), file=sys.stderr)
        return 3
    view = report_bundle.build_view(report, questions, report_date)
    written = report_bundle.write_bundle(view, args.reports_dir)
    for path in written:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
