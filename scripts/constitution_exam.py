#!/usr/bin/env python3
"""Score each chat_request base against the constitution and write a static page.

The page is the progression: what each base still breaks, what the next base
fixed, which misses keep coming back, and where shrinking the pack moved the
issue count. It does not run the 21-question suite.

  python3 scripts/constitution_exam.py

Writes v2/base/constitution_exam.html. The rows are embedded. Do not hand-edit
the page. Open the file. It does not need a web server.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

PICO = "https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css"
ECHARTS = "https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"

# Measured suites only. Do not invent a score for a base that was not run.
SUITE = {
    "base-7.1": "Full pass versus base-7.0: 17/21 versus 17/21, net 0.",
    "base-7.2": "Full pass versus base-7.1: 16/21 versus 20/21, net -4. Issue count is not accuracy.",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def version_key(base_id: str) -> tuple:
    """Sort base ids. `x` sorts before 0. A word suffix sorts before the numbered id of the same major, so base-8-prototype-1 comes before base-8.0."""
    body = base_id.removeprefix("base-")
    key = []
    for part in re.split(r"[.\-]", body):
        if part.isdigit():
            key.append((0, int(part)))
        elif part == "x":
            key.append((0, -1))
        else:
            key.append((0, -2))
            key.append((1, part))
    return tuple(key)


def analytics_json(pack_dir: Path) -> Path | None:
    files = sorted((pack_dir / "min").glob("chat_request_analytics_*.json"))
    return files[0] if files else None


def load_pack(path: Path) -> tuple[str, list[dict]]:
    doc = json.loads(path.read_text())
    messages = doc.get("messages") or []
    system = ""
    if messages and isinstance(messages[0], dict):
        system = str(messages[0].get("content") or "")
    verbs = []
    for verb in doc.get("verbs") or []:
        fn = verb.get("function") if isinstance(verb, dict) else None
        if isinstance(fn, dict) and fn.get("name"):
            verbs.append(fn)
    return system, verbs


def fn_blob(fn: dict) -> str:
    return json.dumps(fn, ensure_ascii=False)


def search_example_count(fn: dict | None) -> int:
    if not fn:
        return 0
    examples = fn.get("examples")
    if isinstance(examples, list):
        return len(examples)
    params = fn.get("parameters") or {}
    examples = params.get("examples") if isinstance(params, dict) else None
    return len(examples) if isinstance(examples, list) else 0


def required_of(fn: dict | None) -> list[str]:
    if not fn:
        return []
    params = fn.get("parameters") or {}
    required = params.get("required") if isinstance(params, dict) else None
    return list(required) if isinstance(required, list) else []


def properties_of(fn: dict | None) -> dict:
    if not fn:
        return {}
    params = fn.get("parameters") or {}
    props = params.get("properties") if isinstance(params, dict) else None
    return props if isinstance(props, dict) else {}


def strip_ids_warnings(text: str) -> str:
    text = re.sub(r"not (?:bare )?@[A-Za-z0-9_.]*\.ids", "", text, flags=re.I)
    text = re.sub(r"Do not bind `?@step\.ids`?[^.]*", "", text, flags=re.I)
    text = re.sub(r"`?@step\.ids`? is node ids only[^.]*", "", text, flags=re.I)
    text = re.sub(r"that name is node ids only[^.]*", "", text, flags=re.I)
    return text


def issue(issue_id: str, title: str, detail: str) -> dict:
    return {"id": issue_id, "title": title, "detail": detail}


def examine(system: str, verbs: list[dict], mode_blobs: dict[str, str]) -> list[dict]:
    by_name = {fn["name"]: fn for fn in verbs}
    names = set(by_name)
    blob = system + "\n" + "\n".join(fn_blob(fn) for fn in verbs)
    found = []

    if "rail" not in names:
        found.append(issue(
            "rail_missing",
            "rail is not a verb",
            "The catalog the model sees has no rail tool. A hard fact has no legal last call, so the model invents a statement.",
        ))

    if "set" in names and "id_kind" not in required_of(by_name["set"]):
        found.append(issue(
            "set_id_kind",
            "set does not require id_kind",
            "The engine rejects a set call that omits id_kind. The schema teaches a call the server will not run.",
        ))

    project = by_name.get("project")
    project_props = properties_of(project)
    teaches_project_limit = bool(re.search(
        r"project`?\s*/\s*`?get`?.{0,30}limit",
        system,
        re.I,
    ))
    if teaches_project_limit or "limit" in project_props:
        found.append(issue(
            "project_limit",
            "project is taught a limit",
            "project has no limit field. order applies limit. A sentence that puts limit on project is a second schema.",
        ))

    stray_by_mode = {}
    for mode, text in mode_blobs.items():
        stray = sorted(set(re.findall(r"@[A-Za-z0-9_]+\.ids\b", strip_ids_warnings(text))))
        if stray:
            stray_by_mode[mode] = stray
    if stray_by_mode:
        shown = "; ".join(
            f"{mode}: {', '.join(names_)}"
            for mode, names_ in sorted(stray_by_mode.items())
        )
        found.append(issue(
            "ids_bind",
            "a bind still uses @alias.ids",
            "@step.ids is node ids only. Warning sentences are ignored. Remaining binds: " + shown + ".",
        ))

    if re.search(r"pre-write summary", system, re.I) and re.search(r"before seeing data", system, re.I):
        found.append(issue(
            "prewrite_summary",
            "summary is pre-written before the rows",
            "The fast path may carry the shape with the pipeline. Writing the summary before any rows is an unconditional guess.",
        ))

    examples = search_example_count(by_name.get("search"))
    if "search" in names and examples != 3:
        found.append(issue(
            "search_examples",
            f"search has {examples} examples",
            "Search keeps three examples (full-text, hybrid plus where, spatial) because that verb is the one the model invents inputs for.",
        ))

    edge_modes = []
    edge_near_traverse = re.compile(
        r'"verb"\s*:\s*"traverse".{0,400}"edge_types"|"edge_types".{0,250}"verb"\s*:\s*"traverse"',
        re.S,
    )
    for mode, text in mode_blobs.items():
        if edge_near_traverse.search(text):
            edge_modes.append(mode)
    if edge_modes:
        found.append(issue(
            "edge_types_example",
            "a traverse example uses edge_types",
            "traverse takes via, one string. Modes: " + ", ".join(edge_modes) + ". describe may still list edge_types.",
        ))

    if "walk_path" in blob and "from.src_keys" not in blob and "src_keys" not in system:
        found.append(issue(
            "walk_seed_missing",
            "walk_path has no src_keys seed",
            "A listed related type is walk_path and from.src_keys is @step.doc_keys. The pack names the shape and not the list it reads.",
        ))

    doc_key_mentions = len(re.findall(r"@step\.doc_keys", system))
    if doc_key_mentions >= 4:
        found.append(issue(
            "bind_copies",
            f"the doc_keys bind is said {doc_key_mentions} times",
            "The access rule is one statement. Repeating @step.doc_keys on later tools is the copy the constitution refuses.",
        ))

    if not re.search(r"query_decomposition", system):
        found.append(issue(
            "no_decomposition",
            "query_decomposition is absent from the system text",
            "The intent is a required terminate field. A pack that never names it cannot record the fast-path or probe suggestion.",
        ))

    if not re.search(r"\b8\b.{0,40}(call|round)", system, re.I) and not re.search(
        r"(at most|max(?:imum)?|budget of)\s+8", system, re.I
    ):
        found.append(issue(
            "no_ceiling",
            "the 8-round ceiling is not stated",
            "The session ceiling is 8 rounds. A pack that does not say so has no stop.",
        ))

    cities = re.findall(r"\b(?:Paris|New York|fruit beers?)\b", system)
    if cities:
        found.append(issue(
            "dataset_story",
            "a dataset story is in the universal text",
            "A city or a hot path named in the catalog is inherited by every tenant. Shown: " + ", ".join(sorted(set(cities))) + ".",
        ))

    return found


def size_rows(csv_path: Path) -> dict[str, dict]:
    if not csv_path.is_file():
        return {}
    out = {}
    with csv_path.open() as handle:
        for row in csv.DictReader(handle):
            if row.get("kind") == "pack" and row.get("mode") == "analytics":
                out[row["base_id"]] = row
    return out


def suggestions(bases: list[dict]) -> list[str]:
    notes = []
    latest = bases[-1]
    open_ids = {item["id"] for item in latest["issues"]}
    if "project_limit" in open_ids:
        notes.append(
            "base-8.0 should delete the project-limit sentence. The constitution already says project has no limit. Leaving it is a fight, not a new law."
        )
    if "bind_copies" in open_ids:
        notes.append(
            "base-8.0 should keep one doc_keys statement and remove the copies. The constitution's no-copy rule is doing its job. The pack has not been morphed yet."
        )
    if "prewrite_summary" in open_ids:
        notes.append(
            "The pre-write sentence is still unconditional. The constitution allows that shape only on a fast path, after decomposition has already filled the plan. base-8.0 should say that, not add a second evidence paragraph."
        )
    if "ids_bind" in open_ids:
        notes.append(
            "An @alias.ids bind is still outside the warning. base-8.0 removes the bind. It does not add another 'do not bind' sentence."
        )
    # Suite versus issue count.
    for base in bases:
        if base["id"] != "base-7.2":
            continue
        prev = next((item for item in bases if item["id"] == "base-7.1"), None)
        if prev and base["issue_count"] <= prev["issue_count"]:
            notes.append(
                "base-7.2 did not increase the issue count and the 21-question pass still fell by 4. Suggested constitution line, already the ground-truth rule: a falling issue count is not accuracy. A SQL++ count near 200 against a Zeus zero is the miss, and it is the LLM, the pipeline, or the Zeus API."
            )
    for issue_id in sorted({item["id"] for base in bases for item in base["issues"]}):
        flags = [any(x["id"] == issue_id for x in base["issues"]) for base in bases]
        title = next(x["title"] for base in bases for x in base["issues"] if x["id"] == issue_id)
        seen = False
        went_quiet = False
        came_back = None
        for base, on in zip(bases, flags):
            if on and went_quiet:
                came_back = base["id"]
                break
            if on:
                seen = True
            elif seen:
                went_quiet = True
        if came_back:
            notes.append(
                f"{title} was fixed and then came back at {came_back}. That is a recurring error. base-8.0 closes it once and does not paste the warning onto another tool."
            )
        streak = [base["id"] for base, on in zip(bases, flags) if on]
        if len(streak) < 8 or came_back:
            continue
        if streak[-1] != bases[-1]["id"]:
            notes.append(
                f"{title} was open on {len(streak)} bases, {streak[0]} to {streak[-1]}, and a later base closed it. No new constitution statement."
            )
        else:
            notes.append(
                f"{title} is open on {len(streak)} bases, {streak[0]} to {streak[-1]}, including the latest. Pack debt for base-8.0. No new constitution statement."
            )
    notes.append(
        "This exam cannot see a ground-truth zero. It does not replace the suite. It is the gate before a base-8.0 versus base-8.1 run."
    )
    return notes


def build(root: Path) -> dict:
    packs = []
    skipped = []
    base_root = root / "v2" / "base"
    for pack_dir in sorted(p for p in base_root.iterdir() if p.is_dir() and p.name.startswith("base-")):
        path = analytics_json(pack_dir)
        if path is None:
            skipped.append(pack_dir.name + " has no analytics min JSON")
            continue
        system, verbs = load_pack(path)
        mode_blobs = {}
        for mode_path in sorted((pack_dir / "min").glob("chat_request_*.json")):
            mode_system, mode_verbs = load_pack(mode_path)
            mode = re.search(r"chat_request_([a-z0-9]+)_", mode_path.name)
            mode_name = mode.group(1) if mode else mode_path.stem
            mode_blobs[mode_name] = mode_system + "\n" + "\n".join(fn_blob(fn) for fn in mode_verbs)
        manifest = {}
        manifest_path = pack_dir / "MANIFEST.json"
        if manifest_path.is_file():
            try:
                manifest = json.loads(manifest_path.read_text())
            except json.JSONDecodeError:
                manifest = {}
        issues = examine(system, verbs, mode_blobs)
        packs.append({
            "id": pack_dir.name,
            "status": str(manifest.get("status") or ""),
            "file": str(path.relative_to(root)),
            "system_chars": len(system),
            "file_chars": path.stat().st_size,
            "verb_count": len(verbs),
            "issues": issues,
            "issue_count": len(issues),
        })
    packs.sort(key=lambda item: version_key(item["id"]))
    sizes = size_rows(base_root / "chat_request_size.csv")
    previous = None
    for pack in packs:
        size = sizes.get(pack["id"]) or {}
        pack["file_chars"] = int(size["file_chars"]) if size.get("file_chars") else pack["file_chars"]
        pack["system_chars"] = int(size["system_chars"]) if size.get("system_chars") else pack["system_chars"]
        pack["file_tk"] = int(size["file_tk"]) if size.get("file_tk") else None
        current_ids = {item["id"] for item in pack["issues"]}
        if previous is None:
            pack["fixed"] = []
            pack["introduced"] = pack["issues"]
            pack["carried"] = []
            pack["chars_delta"] = None
        else:
            prev_ids = {item["id"] for item in previous["issues"]}
            pack["fixed"] = [item for item in previous["issues"] if item["id"] not in current_ids]
            pack["introduced"] = [item for item in pack["issues"] if item["id"] not in prev_ids]
            pack["carried"] = [item for item in pack["issues"] if item["id"] in prev_ids]
            pack["chars_delta"] = pack["file_chars"] - previous["file_chars"]
        pack["suite"] = SUITE.get(pack["id"])
        previous = pack

    # Shrink hops: file got smaller and the issue picture changed.
    shrinks = []
    for pack in packs:
        delta = pack["chars_delta"]
        if delta is None or delta >= 0:
            continue
        shrinks.append({
            "id": pack["id"],
            "chars_delta": delta,
            "issue_count": pack["issue_count"],
            "fixed": [item["title"] for item in pack["fixed"]],
            "introduced": [item["title"] for item in pack["introduced"]],
            "suite": pack["suite"],
        })

    # Common: open on at least half the packs, or on 4+ packs.
    counts: dict[str, dict] = {}
    for pack in packs:
        for item in pack["issues"]:
            slot = counts.setdefault(item["id"], {"id": item["id"], "title": item["title"], "bases": []})
            slot["bases"].append(pack["id"])
    common = [
        slot for slot in counts.values()
        if len(slot["bases"]) >= max(4, len(packs) // 2)
    ]
    common.sort(key=lambda slot: (-len(slot["bases"]), slot["id"]))

    return {
        "measured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "packs": len(packs),
        "bases": packs,
        "shrinks": shrinks,
        "common": common,
        "suggestions": suggestions(packs),
        "skipped": skipped,
    }


def html_page(report: dict) -> str:
    payload = json.dumps(report, ensure_ascii=False).replace("<", "\\u003c")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>chat_request constitution exam</title>
<link rel="stylesheet" href="{PICO}">
<script src="{ECHARTS}"></script>
<style>
  body {{ max-width: 1100px; margin: 0 auto; padding: 1.25rem 1.25rem 3rem; }}
  h1 {{ margin-bottom: 0.25rem; }}
  .note {{ color: #57606a; }}
  .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.75rem; margin: 1rem 0; }}
  .kpi {{ border: 1px solid #d0d7de; border-radius: 8px; padding: 0.7rem 0.9rem; background: #fff; }}
  .kpi .label {{ display: block; font-size: 0.78rem; color: #57606a; }}
  .kpi .value {{ display: block; font-size: 1.35rem; font-weight: 650; }}
  .chart {{ height: 420px; width: 100%; }}
  article.base {{ border-top: 1px solid #d0d7de; padding-top: 0.6rem; }}
  .fixed {{ color: #1b7f4e; }}
  .new {{ color: #9a3412; }}
  ul {{ margin-top: 0.2rem; }}
</style>
</head>
<body>
<!-- constitution-exam: scripts/constitution_exam.py writes this file. Do not hand-edit. -->
<h1>Constitution exam</h1>
<p class="note" id="lead"></p>
<div class="kpis" id="kpis"></div>
<h2>Issue count and pack size</h2>
<p class="note">Left axis is open constitution issues on the analytics pack. Right axis is the analytics file size in characters. A smaller file with more issues is a diet that lost a law. A smaller file with fewer issues is a diet that removed a fight or a copy.</p>
<div id="chart-progression" class="chart"></div>
<h2>Common errors</h2>
<p class="note">Open on at least half the bases, or on four or more. These are the sentences that keep surviving a new base.</p>
<div id="common"></div>
<h2>When the pack shrank</h2>
<p class="note">A negative character delta is the minification. The suite line is present only for a pass that was actually run.</p>
<div id="shrinks"></div>
<h2>Suggested constitution changes</h2>
<ul id="suggestions"></ul>
<h2>Base by base</h2>
<div id="bases"></div>
<script>
const EXAM = {payload};
const lead = document.getElementById("lead");
lead.textContent = "Scored " + EXAM.packs + " bases at " + EXAM.measured_at + ". System and schema checks use the analytics pack. Example checks look at every mode. Today's laws are applied backward. base-7.x sorts before base-7.0 because the id x sorts first. A word suffix sorts before the numbered id of the same major, so base-8-prototype-1 sorts before base-8.0. This is the gate before a suite, not the suite."
  + (EXAM.skipped.length ? " Not scored: " + EXAM.skipped.join("; ") + "." : "");
const latest = EXAM.bases[EXAM.bases.length - 1];
const kpis = document.getElementById("kpis");
function kpi(label, value, sub) {{
  const el = document.createElement("div");
  el.className = "kpi";
  el.innerHTML = "<span class=\\"label\\"></span><span class=\\"value\\"></span><span class=\\"sub\\"></span>";
  el.querySelector(".label").textContent = label;
  el.querySelector(".value").textContent = value;
  el.querySelector(".sub").textContent = sub || "";
  kpis.appendChild(el);
}}
kpi("Bases", String(EXAM.packs), "analytics pack each");
kpi("Open on latest", String(latest.issue_count), latest.id);
kpi("Common errors", String(EXAM.common.length), "long-lived checks");
kpi("Shrink hops", String(EXAM.shrinks.length), "file got smaller");

const chart = echarts.init(document.getElementById("chart-progression"));
chart.setOption({{
  color: ["#3d5a80", "#2a9d8f"],
  tooltip: {{ trigger: "axis" }},
  legend: {{ data: ["Open issues", "File characters"] }},
  grid: {{ left: 48, right: 64, bottom: 80 }},
  xAxis: {{
    type: "category",
    data: EXAM.bases.map(function (b) {{ return b.id.replace("base-", ""); }}),
    axisLabel: {{ rotate: 55 }}
  }},
  yAxis: [
    {{ type: "value", name: "Issues", minInterval: 1 }},
    {{ type: "value", name: "Chars", splitLine: {{ show: false }} }}
  ],
  series: [
    {{ name: "Open issues", type: "line", data: EXAM.bases.map(function (b) {{ return b.issue_count; }}), symbol: "circle" }},
    {{ name: "File characters", type: "line", yAxisIndex: 1, data: EXAM.bases.map(function (b) {{ return b.file_chars; }}), lineStyle: {{ type: "dotted" }} }}
  ]
}});
window.addEventListener("resize", function () {{ chart.resize(); }});

const common = document.getElementById("common");
if (!EXAM.common.length) {{
  common.innerHTML = "<p class=\\"note\\">No check stayed open long enough to call common.</p>";
}} else {{
  common.innerHTML = "<table><thead><tr><th>Error</th><th class=\\"num\\">Bases</th><th>Where</th></tr></thead><tbody>"
    + EXAM.common.map(function (row) {{
      return "<tr><td></td><td class=\\"num\\"></td><td class=\\"note\\"></td></tr>";
    }}).join("") + "</tbody></table>";
  const rows = common.querySelectorAll("tbody tr");
  EXAM.common.forEach(function (row, i) {{
    const cells = rows[i].children;
    cells[0].textContent = row.title;
    cells[1].textContent = String(row.bases.length);
    cells[2].textContent = row.bases.join(", ");
  }});
}}

const shrinks = document.getElementById("shrinks");
if (!EXAM.shrinks.length) {{
  shrinks.innerHTML = "<p class=\\"note\\">No later base is smaller than the one before it.</p>";
}} else {{
  shrinks.innerHTML = EXAM.shrinks.map(function () {{
    return "<article><h3></h3><p></p><p class=\\"fixed\\"></p><p class=\\"new\\"></p><p class=\\"note\\"></p></article>";
  }}).join("");
  const articles = shrinks.querySelectorAll("article");
  EXAM.shrinks.forEach(function (row, i) {{
    const el = articles[i];
    el.querySelector("h3").textContent = row.id + "  " + row.chars_delta + " characters";
    el.querySelector("p").textContent = "Open issues after the shrink: " + row.issue_count + ".";
    el.querySelector(".fixed").textContent = row.fixed.length ? "Fixed: " + row.fixed.join("; ") : "Fixed: nothing.";
    el.querySelector(".new").textContent = row.introduced.length ? "Introduced: " + row.introduced.join("; ") : "Introduced: nothing.";
    el.querySelector(".note").textContent = row.suite || "";
  }});
}}

const suggestions = document.getElementById("suggestions");
EXAM.suggestions.forEach(function (text) {{
  const li = document.createElement("li");
  li.textContent = text;
  suggestions.appendChild(li);
}});

const bases = document.getElementById("bases");
EXAM.bases.forEach(function (base) {{
  const art = document.createElement("article");
  art.className = "base";
  const h = document.createElement("h3");
  h.textContent = base.id + (base.status ? "  ·  " + base.status : "") + "  ·  " + base.issue_count + " open";
  art.appendChild(h);
  const meta = document.createElement("p");
  meta.className = "note";
  const delta = base.chars_delta == null ? "first pack" : (base.chars_delta > 0 ? "+" : "") + base.chars_delta + " characters versus the previous base";
  meta.textContent = base.file_chars + " file characters, " + base.system_chars + " system characters, " + base.verb_count + " verbs. " + delta + ".";
  art.appendChild(meta);
  function block(className, label, items) {{
    const p = document.createElement("p");
    p.className = className;
    p.textContent = label;
    art.appendChild(p);
    const ul = document.createElement("ul");
    if (!items.length) {{
      const li = document.createElement("li");
      li.className = "note";
      li.textContent = "None.";
      ul.appendChild(li);
    }}
    items.forEach(function (item) {{
      const li = document.createElement("li");
      li.textContent = item.title + " — " + item.detail;
      ul.appendChild(li);
    }});
    art.appendChild(ul);
  }}
  block("fixed", "Fixed since the previous base", base.fixed);
  block("new", "Introduced", base.introduced);
  block("", "Still open", base.carried);
  if (base.suite) {{
    const s = document.createElement("p");
    s.className = "note";
    s.textContent = base.suite;
    art.appendChild(s);
  }}
  bases.appendChild(art);
}});
</script>
</body>
</html>
"""


def main() -> None:
    root = repo_root()
    report = build(root)
    out = root / "v2" / "base" / "constitution_exam.html"
    out.write_text(html_page(report))
    print(f"wrote {out.relative_to(root)} packs={report['packs']} latest={report['bases'][-1]['id']} open={report['bases'][-1]['issue_count']}")


if __name__ == "__main__":
    main()
