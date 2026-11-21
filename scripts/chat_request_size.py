#!/usr/bin/env python3
"""Write the chat_request size table as CSV.

Counts the pack files on disk and, when a baseline evidence file recorded
them, the live suffix Zeus appends. tk is the pack-viewer budget: UTF-8
bytes ÷ 4, rounded up. It is not the model's tokenizer. The same rules are
in baseline/report_bundle.py.

One row per catalog JSON (kind=pack), with deltas against
_lineage.parent_base_id of the same mode. One row per recorded scope brief
(kind=injection). One row per analytics pack times each scope on the newest
evidence file (kind=appended): system message after that suffix.

Usage:
  python3 scripts/chat_request_size.py
  python3 scripts/chat_request_size.py --out v2/base/chat_request_size.csv

The CSV is written first. The HTML page beside it embeds those rows as a
static object. Open the file. It does not fetch the CSV.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

MODES = (
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
)
TOOL_NAMES = ("search", "pipeline", "return", "rail")
INJECTION_PARTS = ("scope_brief", "mini_schema", "walk_paths", "full")

COLUMNS = [
    "kind",
    "measured_at",
    "report_date",
    "base_id",
    "parent_base_id",
    "mode",
    "manifest_status",
    "manifest_updated_at",
    "scope",
    "source_file",
    "file_chars",
    "file_bytes",
    "file_tk",
    "system_chars",
    "system_bytes",
    "system_tk",
    "search_chars",
    "search_bytes",
    "search_tk",
    "pipeline_chars",
    "pipeline_bytes",
    "pipeline_tk",
    "return_chars",
    "return_bytes",
    "return_tk",
    "rail_chars",
    "rail_bytes",
    "rail_tk",
    "prose_and_tools_chars",
    "prose_and_tools_tk",
    "text_chars",
    "text_bytes",
    "text_tk",
    "verb_count",
    "file_chars_delta",
    "file_bytes_delta",
    "file_tk_delta",
    "file_bytes_delta_pct",
    "system_chars_delta",
    "system_tk_delta",
    "search_chars_delta",
    "pipeline_chars_delta",
    "return_chars_delta",
    "rail_chars_delta",
    "prose_and_tools_chars_delta",
    "prose_and_tools_tk_delta",
    "json_wrap_chars_delta",
    "json_wrap_tk_delta",
    "modes_share_file_delta",
    "scope_brief_chars",
    "scope_brief_bytes",
    "scope_brief_tk",
    "mini_schema_chars",
    "mini_schema_bytes",
    "mini_schema_tk",
    "walk_paths_chars",
    "walk_paths_bytes",
    "walk_paths_tk",
    "full_chars",
    "full_bytes",
    "full_tk",
    "outside_headings_chars",
    "recorded_bytes",
    "system_plus_chars",
    "system_plus_tk",
    "injection_report_date",
    "injection_source",
]


def tokens_from_bytes(nbytes: int) -> int:
    if nbytes <= 0:
        return 0
    return max(1, (nbytes + 3) // 4)


def tokens(text: str) -> int:
    return tokens_from_bytes(len(text.encode("utf-8")))


def piece(text: str) -> tuple[int, int, int]:
    raw = text.encode("utf-8")
    return len(text), len(raw), tokens_from_bytes(len(raw))


def tool_catalog(doc: dict) -> dict:
    catalog = {}
    for item in doc.get("verbs") or []:
        function = item.get("function") or {}
        name = function.get("name")
        if name:
            catalog[name] = function
    return catalog


def blank() -> dict:
    return {column: "" for column in COLUMNS}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def mode_of(path: Path) -> str:
    match = re.match(r"chat_request_([a-z0-9]+)_.+\.json$", path.name)
    if not match:
        return ""
    return match.group(1)


def load_manifest(pack_dir: Path) -> dict:
    path = pack_dir / "MANIFEST.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def text_sibling(json_path: Path) -> Path | None:
    candidate = json_path.parent.parent / "text" / f"{json_path.stem}.txt"
    if candidate.is_file():
        return candidate
    return None


def measure_pack(json_path: Path, measured_at: str) -> dict | None:
    try:
        raw = json_path.read_bytes()
        doc = json.loads(raw.decode())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(doc, dict):
        return None
    mode = mode_of(json_path)
    if mode not in MODES:
        return None
    pack_dir = json_path.parent.parent
    lineage = doc.get("_lineage") or {}
    base_id = str(lineage.get("base_id") or pack_dir.name)
    parent = lineage.get("parent_base_id") or ""
    manifest = load_manifest(pack_dir)
    messages = doc.get("messages") or [{}]
    system = ""
    if messages and isinstance(messages[0], dict):
        system = messages[0].get("content") or ""
    if not isinstance(system, str):
        system = ""
    tools = tool_catalog(doc)
    row = blank()
    row["kind"] = "pack"
    row["measured_at"] = measured_at
    row["base_id"] = base_id
    row["parent_base_id"] = str(parent) if parent else ""
    row["mode"] = mode
    row["manifest_status"] = str(manifest.get("status") or "")
    row["manifest_updated_at"] = str(manifest.get("updated_at") or "")
    row["source_file"] = json_path.relative_to(repo_root()).as_posix()
    file_chars = len(raw.decode())
    row["file_chars"] = file_chars
    row["file_bytes"] = len(raw)
    row["file_tk"] = tokens_from_bytes(len(raw))
    system_chars, system_bytes, system_tk = piece(system)
    row["system_chars"] = system_chars
    row["system_bytes"] = system_bytes
    row["system_tk"] = system_tk
    prose = system_chars
    prose_tk = system_tk
    for name in TOOL_NAMES:
        text = ""
        if name in tools:
            text = json.dumps(tools[name], ensure_ascii=False)
        chars, nbytes, tk = piece(text) if text else (0, 0, 0)
        row[f"{name}_chars"] = chars
        row[f"{name}_bytes"] = nbytes
        row[f"{name}_tk"] = tk
        prose += chars
        prose_tk += tk
    row["prose_and_tools_chars"] = prose
    row["prose_and_tools_tk"] = prose_tk
    row["verb_count"] = len(tools)
    sibling = text_sibling(json_path)
    if sibling is not None:
        text_raw = sibling.read_bytes()
        row["text_chars"] = len(text_raw.decode())
        row["text_bytes"] = len(text_raw)
        row["text_tk"] = tokens_from_bytes(len(text_raw))
    row["_system"] = system
    return row


def add_deltas(row: dict, parent: dict | None) -> None:
    if parent is None:
        return
    for field in (
        "file_chars",
        "file_bytes",
        "file_tk",
        "system_chars",
        "system_tk",
        "search_chars",
        "pipeline_chars",
        "return_chars",
        "rail_chars",
        "prose_and_tools_chars",
        "prose_and_tools_tk",
    ):
        row[f"{field}_delta"] = int(row[field]) - int(parent[field])
    previous = int(parent["file_bytes"])
    if previous:
        pct = 100.0 * int(row["file_bytes_delta"]) / previous
        row["file_bytes_delta_pct"] = f"{pct:.1f}"
    row["json_wrap_chars_delta"] = int(row["file_chars_delta"]) - int(
        row["prose_and_tools_chars_delta"]
    )
    row["json_wrap_tk_delta"] = int(row["file_tk_delta"]) - int(
        row["prose_and_tools_tk_delta"]
    )


def mark_shared_deltas(rows: list[dict]) -> None:
    by_base: dict[str, list[dict]] = {}
    for row in rows:
        if row["kind"] != "pack" or row["file_chars_delta"] == "":
            continue
        by_base.setdefault(row["base_id"], []).append(row)
    for group in by_base.values():
        deltas = {row["file_chars_delta"] for row in group}
        tk = {row["file_tk_delta"] for row in group}
        shared = "yes" if len(deltas) == 1 and len(tk) == 1 else "no"
        for row in group:
            row["modes_share_file_delta"] = shared


def report_date_of(path: Path, view: dict) -> str:
    stem = str(view.get("stem") or path.stem)
    match = re.match(r"(\d{4}-\d{2}-\d{2})", stem)
    if match:
        return match.group(1)
    return ""


def stored_int(item: dict, key: str) -> int | None:
    if key not in item or item.get(key) is None:
        return None
    try:
        return int(item[key])
    except (TypeError, ValueError):
        return None


def injection_rows(reports_dir: Path, measured_at: str) -> list[dict]:
    rows = []
    if not reports_dir.is_dir():
        return rows
    for path in sorted(reports_dir.rglob("*.json")):
        try:
            view = json.loads(path.read_text())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(view, dict):
            continue
        briefs = view.get("scope_briefs")
        if not isinstance(briefs, list):
            continue
        date = report_date_of(path, view)
        rel = path.relative_to(repo_root()).as_posix()
        for item in briefs:
            if not isinstance(item, dict):
                continue
            if stored_int(item, "full_chars") is None and stored_int(item, "chars") is None:
                continue
            row = blank()
            row["kind"] = "injection"
            row["measured_at"] = measured_at
            row["report_date"] = date
            row["scope"] = str(item.get("scope") or "")
            row["source_file"] = rel
            row["injection_report_date"] = date
            row["injection_source"] = rel
            for part in INJECTION_PARTS:
                for unit in ("chars", "bytes", "tk"):
                    value = stored_int(item, f"{part}_{unit}")
                    if value is not None:
                        row[f"{part}_{unit}"] = value
            recorded = stored_int(item, "chars")
            if recorded is not None:
                row["recorded_bytes"] = recorded
            full = stored_int(item, "full_chars")
            brief = stored_int(item, "scope_brief_chars")
            mini = stored_int(item, "mini_schema_chars")
            walk = stored_int(item, "walk_paths_chars")
            if None not in (full, brief, mini, walk):
                row["outside_headings_chars"] = full - (brief + mini + walk)
            row["_full_chars"] = stored_int(item, "full_chars")
            row["_full_bytes"] = stored_int(item, "full_bytes")
            row["_mtime"] = path.stat().st_mtime
            rows.append(row)
    return rows


def newest_injection(rows: list[dict]) -> list[dict]:
    """One scope from the newest evidence file that split the suffix."""
    dated = [row for row in rows if row.get("_full_chars") is not None]
    if not dated:
        return []
    best_date = max(row["report_date"] or "" for row in dated)
    pool = [row for row in dated if (row["report_date"] or "") == best_date]
    best_mtime = max(row["_mtime"] for row in pool)
    source = next(row["injection_source"] for row in pool if row["_mtime"] == best_mtime)
    return [row for row in pool if row["injection_source"] == source]


def append_suffix(system: str, full_chars: int, full_bytes: int) -> tuple[int, int]:
    """Match report_bundle: rstrip, blank line, then the suffix."""
    base = system.rstrip(" \t\n\r")
    chars = len(base) + 2 + full_chars
    nbytes = len(base.encode("utf-8")) + 2 + full_bytes
    return chars, tokens_from_bytes(nbytes)


def appended_rows(packs: list[dict], injections: list[dict]) -> list[dict]:
    latest = newest_injection(injections)
    if not latest:
        return []
    out = []
    for pack in packs:
        if pack["mode"] != "analytics":
            continue
        system = pack.get("_system") or ""
        for item in latest:
            full_chars = item.get("_full_chars")
            full_bytes = item.get("_full_bytes")
            if full_chars is None or full_bytes is None:
                continue
            chars, tk = append_suffix(system, full_chars, full_bytes)
            row = blank()
            row["kind"] = "appended"
            row["measured_at"] = pack["measured_at"]
            row["base_id"] = pack["base_id"]
            row["parent_base_id"] = pack["parent_base_id"]
            row["mode"] = "analytics"
            row["scope"] = item["scope"]
            row["source_file"] = pack["source_file"]
            row["system_chars"] = pack["system_chars"]
            row["system_tk"] = pack["system_tk"]
            row["full_chars"] = full_chars
            row["full_bytes"] = full_bytes
            row["full_tk"] = item.get("full_tk", "")
            row["system_plus_chars"] = chars
            row["system_plus_tk"] = tk
            row["injection_report_date"] = item["report_date"]
            row["injection_source"] = item["injection_source"]
            out.append(row)
    return out


def version_key(base_id: str) -> tuple:
    """Working train `x` sits before the numbered ship of that major."""
    body = base_id.removeprefix("base-")
    key = []
    for part in re.split(r"[.\-]", body):
        if part.isdigit():
            key.append((0, int(part)))
        elif part == "x":
            key.append((0, -1))
        else:
            key.append((1, part))
    return tuple(key)


def sort_key(row: dict) -> tuple:
    kind_order = {"pack": 0, "injection": 1, "appended": 2}
    return (
        kind_order.get(row["kind"], 9),
        version_key(row["base_id"]),
        MODES.index(row["mode"]) if row["mode"] in MODES else 99,
        row["report_date"],
        row["scope"],
    )


def rows_from_csv(path: Path) -> list[dict]:
    """Read the CSV back so the page is that file, not a second measurement."""
    number_suffixes = ("_chars", "_bytes", "_tk", "_delta", "_count")
    out = []
    with path.open(newline="") as handle:
        for raw in csv.DictReader(handle):
            row = {}
            for key, value in raw.items():
                if value == "":
                    row[key] = None
                    continue
                if key.endswith("_pct") and re.fullmatch(r"-?\d+(?:\.\d+)?", value):
                    row[key] = float(value)
                elif (key == "verb_count" or key.endswith(number_suffixes)) and re.fullmatch(
                    r"-?\d+", value
                ):
                    row[key] = int(value)
                else:
                    row[key] = value
            out.append(row)
    return out


def write_html(csv_path: Path, html_path: Path) -> None:
    payload = json.dumps(
        {"source": csv_path.name, "rows": rows_from_csv(csv_path)},
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("<", "\\u003c")
    html_path.write_text(PAGE_HTML.replace("__SIZE_JSON__", payload))


PAGE_HTML = r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>chat_request size</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css">
<script src="https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"></script>
<style>
  body { max-width: 1100px; margin: 0 auto; padding: 1.25rem 1.25rem 3rem; }
  h1 { margin-bottom: 0.25rem; }
  .note { color: #57606a; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.75rem; margin: 1rem 0 0.5rem; }
  .kpi { border: 1px solid #d0d7de; border-radius: 8px; padding: 0.7rem 0.9rem; background: #fff; }
  .kpi .label { display: block; font-size: 0.78rem; color: #57606a; }
  .kpi .value { display: block; font-size: 1.35rem; font-weight: 650; line-height: 1.2; }
  .kpi .sub { display: block; font-size: 0.82rem; color: #57606a; }
  .chart { height: 380px; width: 100%; }
  .toolbar { max-width: 220px; margin-top: 1rem; }
  table { font-size: 0.9rem; }
  td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
</style>
</head>
<body>
<!-- size-contract: scripts/chat_request_size.py writes this file from chat_request_size.csv. Do not hand-edit. -->
<h1>chat_request size</h1>
<p class="note" id="lead"></p>
<div class="toolbar">
  <label for="mode">Mode
    <select id="mode"></select>
  </label>
</div>
<div class="kpis" id="kpis"></div>
<h2>File and system message</h2>
<p class="note">Characters in the catalog JSON. The token budget is in the tooltip. tk is UTF-8 bytes ÷ 4, rounded up. The dotted line is the percent change from the previous point, on the right axis (0 to 100).</p>
<div id="chart-file" class="chart"></div>
<h2>Tool JSON</h2>
<p class="note">search, pipeline, return, and rail. The system message is on the chart above so these smaller pieces stay visible.</p>
<div id="chart-tools" class="chart"></div>
<h2>Added since the parent base</h2>
<p class="note">Each bar is this base minus <code>_lineage.parent_base_id</code> for the same mode. A new base adds a row. Older bases stay as measured.</p>
<div id="chart-delta" class="chart"></div>
<h2>Every mode</h2>
<p class="note">File characters. A shared hop delta shows up as parallel steps. Each dotted line is that mode’s percent change from the previous point, on the right axis.</p>
<div id="chart-modes" class="chart"></div>
<h2>Live suffix</h2>
<p class="note">Recorded on a comparison run. The pack file does not contain this text. Zeus appends the same suffix to every pack.</p>
<div id="chart-injection" class="chart"></div>
<h2>System message after the suffix</h2>
<p class="note">Analytics system message plus the newest recorded suffix. One line per dataset. The dotted line is the percent change from the previous point, on the right axis.</p>
<div id="chart-appended" class="chart"></div>
<h2>Analytics hops</h2>
<table id="hops">
  <thead>
    <tr>
      <th>Base</th><th>Parent</th><th>Measured</th>
      <th class="num">File</th><th class="num">Delta</th><th class="num">tk</th>
      <th class="num">System</th><th class="num">System delta</th>
    </tr>
  </thead>
  <tbody></tbody>
</table>
<script>
const SIZE = __SIZE_JSON__;
const COLORS = ["#3d5a80", "#2a9d8f", "#e9c46a", "#e76f51", "#6d597a", "#457b9d", "#bc6c25", "#588157", "#9b2226", "#264653"];

function versionKey(baseId) {
  const body = String(baseId || "").replace(/^base-/, "");
  return body.split(/[.\-]/).filter(Boolean).map(function (part) {
    if (/^\d+$/.test(part)) return [0, Number(part)];
    if (part === "x") return [0, -1];
    return [1, part];
  });
}

function cmpVersion(a, b) {
  const ka = versionKey(a);
  const kb = versionKey(b);
  const n = Math.max(ka.length, kb.length);
  for (let i = 0; i < n; i++) {
    const pa = ka[i] || [0, 0];
    const pb = kb[i] || [0, 0];
    if (pa[0] !== pb[0]) return pa[0] - pb[0];
    if (typeof pa[1] === "number" && typeof pb[1] === "number") {
      if (pa[1] !== pb[1]) return pa[1] - pb[1];
    } else if (String(pa[1]) !== String(pb[1])) {
      return String(pa[1]) < String(pb[1]) ? -1 : 1;
    }
  }
  return 0;
}

function rows(kind) {
  return SIZE.rows.filter(function (row) { return row.kind === kind; });
}

function packs(mode) {
  return rows("pack").filter(function (row) { return row.mode === mode; })
    .sort(function (a, b) { return cmpVersion(a.base_id, b.base_id); });
}

function fmt(value) {
  if (value === null || value === undefined || value === "") return "—";
  return Number(value).toLocaleString("en-US");
}

function signed(value) {
  if (value === null || value === undefined || value === "") return "—";
  const n = Number(value);
  return (n > 0 ? "+" : "") + n.toLocaleString("en-US");
}

function tip(chars, tk) {
  if (chars === null || chars === undefined) return "—";
  const token = tk === null || tk === undefined ? "" : " (" + fmt(tk) + " tk)";
  return fmt(chars) + token;
}

const charts = {};
function chart(id) {
  if (!charts[id]) {
    const el = document.getElementById(id);
    charts[id] = echarts.init(el);
  }
  return charts[id];
}

function baseAxis(list) {
  return {
    type: "category",
    data: list.map(function (row) { return row.base_id; }),
    axisLabel: { rotate: 40 }
  };
}

function pctBetween(values) {
  return values.map(function (value, i) {
    const prev = i === 0 ? null : values[i - 1];
    if (value === null || value === undefined || prev === null || prev === undefined || prev === 0) {
      return null;
    }
    return Math.round((1000 * (value - prev) / Math.abs(prev))) / 10;
  });
}

function axes() {
  return [
    { type: "value", name: "characters" },
    {
      type: "value",
      name: "% from previous",
      position: "right",
      min: function (extent) { return extent.min >= 0 ? 0 : Math.floor(extent.min / 5) * 5; },
      max: function (extent) { return Math.max(100, Math.ceil(extent.max / 10) * 10); },
      axisLabel: { formatter: "{value}%" },
      splitLine: { show: false }
    }
  ];
}

function levelLine(name, data, color) {
  return {
    name: name,
    type: "line",
    yAxisIndex: 0,
    data: data,
    itemStyle: { color: color },
    lineStyle: { color: color }
  };
}

function pctLine(name, data, color) {
  return {
    name: name + " Δ%",
    type: "line",
    yAxisIndex: 1,
    data: pctBetween(data),
    itemStyle: { color: color },
    lineStyle: { color: color, type: "dotted", width: 2 },
    symbol: "emptyCircle",
    symbolSize: 6
  };
}

function drawFile(list) {
  const file = list.map(function (row) { return row.file_chars; });
  const system = list.map(function (row) { return row.system_chars; });
  const text = list.map(function (row) { return row.text_chars; });
  const filePct = pctBetween(file);
  const systemPct = pctBetween(system);
  const textPct = pctBetween(text);
  chart("chart-file").setOption({
    color: COLORS,
    tooltip: {
      trigger: "axis",
      formatter: function (items) {
        const i = items[0].dataIndex;
        const row = list[i];
        return row.base_id
          + "<br>File " + tip(row.file_chars, row.file_tk)
          + (filePct[i] === null ? "" : " · " + signed(filePct[i]) + "%")
          + "<br>System " + tip(row.system_chars, row.system_tk)
          + (systemPct[i] === null ? "" : " · " + signed(systemPct[i]) + "%")
          + (row.text_chars === null ? "" : "<br>Text export " + tip(row.text_chars, row.text_tk)
            + (textPct[i] === null ? "" : " · " + signed(textPct[i]) + "%"));
      }
    },
    legend: { top: 0 },
    grid: { left: 64, right: 64, top: 36, bottom: 72 },
    xAxis: baseAxis(list),
    yAxis: axes(),
    series: [
      levelLine("File", file, COLORS[0]),
      pctLine("File", file, COLORS[0]),
      levelLine("System message", system, COLORS[1]),
      pctLine("System message", system, COLORS[1]),
      levelLine("Text export", text, COLORS[2]),
      pctLine("Text export", text, COLORS[2])
    ]
  }, true);
}

function drawTools(list) {
  const names = ["search", "pipeline", "return", "rail"];
  chart("chart-tools").setOption({
    color: COLORS.slice(1),
    tooltip: { trigger: "axis" },
    legend: { top: 0 },
    grid: { left: 64, right: 24, top: 36, bottom: 72 },
    xAxis: baseAxis(list),
    yAxis: { type: "value", name: "characters" },
    series: names.map(function (name) {
      return {
        name: name,
        type: "bar",
        stack: "tools",
        data: list.map(function (row) { return row[name + "_chars"] || 0; })
      };
    })
  }, true);
}

function drawDelta(list) {
  const hops = list.filter(function (row) { return row.file_chars_delta !== null; });
  chart("chart-delta").setOption({
    tooltip: {
      trigger: "axis",
      formatter: function (items) {
        const row = hops[items[0].dataIndex];
        return row.parent_base_id + " → " + row.base_id
          + "<br>File " + signed(row.file_chars_delta) + " (" + signed(row.file_tk_delta) + " tk)"
          + (row.file_bytes_delta_pct === null ? "" : ", " + row.file_bytes_delta_pct + "%")
          + "<br>System " + signed(row.system_chars_delta) + " (" + signed(row.system_tk_delta) + " tk)"
          + "<br>Prose and tools " + signed(row.prose_and_tools_chars_delta)
          + "<br>JSON wrapping " + signed(row.json_wrap_chars_delta);
      }
    },
    grid: { left: 64, right: 24, top: 24, bottom: 80 },
    xAxis: {
      type: "category",
      data: hops.map(function (row) { return row.base_id; }),
      axisLabel: { rotate: 40 }
    },
    yAxis: { type: "value", name: "characters" },
    series: [{
      name: "File delta",
      type: "bar",
      data: hops.map(function (row) {
        return {
          value: row.file_chars_delta,
          itemStyle: { color: row.file_chars_delta < 0 ? "#9b2226" : "#2a9d8f" }
        };
      })
    }]
  }, true);
}

function drawModes() {
  const all = rows("pack");
  const modes = [];
  all.forEach(function (row) {
    if (modes.indexOf(row.mode) === -1) modes.push(row.mode);
  });
  const ids = [];
  all.forEach(function (row) {
    if (ids.indexOf(row.base_id) === -1) ids.push(row.base_id);
  });
  ids.sort(cmpVersion);
  const series = [];
  modes.forEach(function (mode, index) {
    const byId = {};
    packs(mode).forEach(function (row) { byId[row.base_id] = row.file_chars; });
    const data = ids.map(function (id) { return byId[id] === undefined ? null : byId[id]; });
    const color = COLORS[index % COLORS.length];
    series.push(levelLine(mode, data, color));
    const dotted = pctLine(mode, data, color);
    dotted.showSymbol = false;
    series.push(dotted);
  });
  chart("chart-modes").setOption({
    color: COLORS,
    tooltip: { trigger: "axis" },
    legend: { type: "scroll", top: 0 },
    grid: { left: 64, right: 64, top: 36, bottom: 72 },
    xAxis: { type: "category", data: ids, axisLabel: { rotate: 40 } },
    yAxis: axes(),
    series: series
  }, true);
}

function injectionLabel(row, seen) {
  const base = (row.report_date || "undated") + " " + (row.scope || "");
  if (seen[base]) return base + " " + String(row.source_file || "").split("/").slice(-2, -1)[0];
  seen[base] = true;
  return base;
}

function drawInjection() {
  const list = rows("injection").filter(function (row) {
    return row.full_chars !== null || row.recorded_bytes !== null;
  });
  const seen = {};
  const labels = list.map(function (row) { return injectionLabel(row, seen); });
  const stacked = list.some(function (row) { return row.scope_brief_chars !== null; });
  const series = stacked ? [
    ["Scope brief", "scope_brief_chars"],
    ["Mini-schema", "mini_schema_chars"],
    ["Walk paths", "walk_paths_chars"],
    ["Outside the headings", "outside_headings_chars"]
  ].map(function (pair) {
    return {
      name: pair[0],
      type: "bar",
      stack: "suffix",
      data: list.map(function (row) { return row[pair[1]] || 0; })
    };
  }) : [{
    name: "Recorded bytes",
    type: "bar",
    data: list.map(function (row) { return row.recorded_bytes; })
  }];
  chart("chart-injection").setOption({
    color: ["#3d5a80", "#e9c46a", "#2a9d8f", "#adb5bd"],
    tooltip: { trigger: "axis" },
    legend: { top: 0 },
    grid: { left: 64, right: 24, top: 36, bottom: 120 },
    xAxis: { type: "category", data: labels, axisLabel: { rotate: 50 } },
    yAxis: { type: "value", name: stacked ? "characters" : "bytes" },
    series: series
  }, true);
  document.getElementById("chart-injection").style.display = list.length ? "block" : "none";
}

function drawAppended() {
  const list = rows("appended");
  const ids = [];
  const scopes = [];
  list.forEach(function (row) {
    if (ids.indexOf(row.base_id) === -1) ids.push(row.base_id);
    if (scopes.indexOf(row.scope) === -1) scopes.push(row.scope);
  });
  ids.sort(cmpVersion);
  const series = [];
  scopes.forEach(function (scope, index) {
    const byId = {};
    list.forEach(function (row) {
      if (row.scope === scope) byId[row.base_id] = row;
    });
    const data = ids.map(function (id) { return byId[id] ? byId[id].system_plus_chars : null; });
    const color = COLORS[index % COLORS.length];
    series.push(levelLine(scope, data, color));
    series.push(pctLine(scope, data, color));
  });
  chart("chart-appended").setOption({
    color: COLORS,
    tooltip: {
      trigger: "axis",
      formatter: function (items) {
        return items.map(function (item) {
          if (item.seriesName.slice(-3) === " Δ%") {
            return item.seriesName + " " + (item.value === null || item.value === undefined ? "—" : signed(item.value) + "%");
          }
          const scope = item.seriesName;
          const row = list.filter(function (candidate) {
            return candidate.base_id === ids[item.dataIndex] && candidate.scope === scope;
          })[0];
          return item.seriesName + " " + tip(item.value, row ? row.system_plus_tk : null);
        }).join("<br>");
      }
    },
    legend: { top: 0 },
    grid: { left: 64, right: 64, top: 36, bottom: 72 },
    xAxis: { type: "category", data: ids, axisLabel: { rotate: 40 } },
    yAxis: axes(),
    series: series
  }, true);
  document.getElementById("chart-appended").style.display = list.length ? "block" : "none";
}

function drawKpis(list) {
  const latest = list.length ? list[list.length - 1] : null;
  const box = document.getElementById("kpis");
  if (!latest) {
    box.innerHTML = "";
    return;
  }
  const cards = [
    ["Latest base", latest.base_id, latest.parent_base_id ? "parent " + latest.parent_base_id : "no parent"],
    ["File", fmt(latest.file_chars), fmt(latest.file_tk) + " tk · " + fmt(latest.file_bytes) + " bytes"],
    ["System message", fmt(latest.system_chars), fmt(latest.system_tk) + " tk"],
    ["Since parent", signed(latest.file_chars_delta), signed(latest.file_tk_delta) + " tk"
      + (latest.file_bytes_delta_pct === null ? "" : " · " + latest.file_bytes_delta_pct + "%")],
    ["System since parent", signed(latest.system_chars_delta), signed(latest.system_tk_delta) + " tk"],
    ["Modes share the file delta", latest.modes_share_file_delta || "—", latest.manifest_status || ""]
  ];
  box.innerHTML = cards.map(function (card) {
    return "<div class=\"kpi\"><span class=\"label\">" + card[0]
      + "</span><span class=\"value\">" + card[1]
      + "</span><span class=\"sub\">" + card[2] + "</span></div>";
  }).join("");
}

function drawHops() {
  const body = document.querySelector("#hops tbody");
  body.innerHTML = packs("analytics").map(function (row) {
    return "<tr><td>" + row.base_id + "</td><td>" + (row.parent_base_id || "—")
      + "</td><td>" + (row.manifest_updated_at || row.measured_at || "—")
      + "</td><td class=\"num\">" + fmt(row.file_chars)
      + "</td><td class=\"num\">" + signed(row.file_chars_delta)
      + "</td><td class=\"num\">" + fmt(row.file_tk)
      + "</td><td class=\"num\">" + fmt(row.system_chars)
      + "</td><td class=\"num\">" + signed(row.system_chars_delta) + "</td></tr>";
  }).join("");
}

function draw(mode) {
  const list = packs(mode);
  drawKpis(list);
  drawFile(list);
  drawTools(list);
  drawDelta(list);
}

const modeSelect = document.getElementById("mode");
const modes = [];
rows("pack").forEach(function (row) {
  if (modes.indexOf(row.mode) === -1) modes.push(row.mode);
});
modeSelect.innerHTML = modes.map(function (mode) {
  return "<option>" + mode + "</option>";
}).join("");
if (modes.indexOf("analytics") !== -1) modeSelect.value = "analytics";
modeSelect.addEventListener("change", function () { draw(modeSelect.value); });

const measured = (SIZE.rows[0] && SIZE.rows[0].measured_at) || "";
document.getElementById("lead").textContent =
  "Snapshot " + measured + " from " + SIZE.source
  + ". Open this file directly. The rows are baked in. A new base is appended by regenerating the CSV, then this page.";

drawHops();
if (!window.echarts) {
  document.getElementById("lead").textContent += " ECharts did not load. The hop table below still lists the numbers.";
} else {
  draw(modeSelect.value);
  drawModes();
  drawInjection();
  drawAppended();
  window.addEventListener("resize", function () {
    Object.keys(charts).forEach(function (id) { charts[id].resize(); });
  });
}
</script>
</body>
</html>
"""


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in COLUMNS})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=repo_root() / "v2" / "base" / "chat_request_size.csv",
    )
    parser.add_argument(
        "--reports",
        type=Path,
        default=repo_root() / "baseline" / "reports",
        help="Evidence JSON. Live suffix rows are omitted when this directory has none.",
    )
    args = parser.parse_args()
    measured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    root = repo_root()
    packs = []
    for path in sorted((root / "v2" / "base").glob("*/min/chat_request_*.json")):
        row = measure_pack(path, measured_at)
        if row is not None:
            packs.append(row)
    by_key = {(row["base_id"], row["mode"]): row for row in packs}
    for row in packs:
        parent_id = row["parent_base_id"]
        parent = by_key.get((parent_id, row["mode"])) if parent_id else None
        add_deltas(row, parent)
    mark_shared_deltas(packs)
    injections = injection_rows(args.reports, measured_at)
    appended = appended_rows(packs, injections)
    rows = sorted(packs + injections + appended, key=sort_key)
    write_csv(args.out, rows)
    html_path = args.out.with_suffix(".html")
    write_html(args.out, html_path)
    analytics = [
        row
        for row in packs
        if row["mode"] == "analytics" and row["file_chars_delta"] != ""
    ]
    print(
        f"wrote {args.out} rows={len(rows)} packs={len(packs)} injection={len(injections)}"
    )
    print(f"wrote {html_path}")
    for row in analytics:
        if row["base_id"] in {"base-7.1", "base-7.2"}:
            print(
                f"{row['base_id']} file={row['file_chars']} chars "
                f"({row['file_tk']} tk, {row['file_bytes']} bytes) "
                f"system={row['system_chars']} "
                f"delta={row['file_chars_delta']} chars "
                f"({row['file_tk_delta']} tk) "
                f"prose={row['prose_and_tools_chars_delta']} "
                f"wrap={row['json_wrap_chars_delta']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
