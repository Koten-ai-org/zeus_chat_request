# GUIDE — base-7.3 → base-7.4

Sentence align. The HTTP wire does not change. Parent is `base-7.3`. No new ticket. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays open.

Placement is CORE, the tool descriptions, and the mode examples that taught a different call. There is no new section.

## Stayed

- All 14 catalog verbs, including `rail` (`name` plus `binds`, no SQL). Zeus still does not execute `rail`.
- Required Layer A four: `summary`, `query_decomposition`, `decomposition`, `confidence`.
- `response_output_*`, `report_sink_*`, and `settings_ai_process_result.example.json`, copied from base-7.3.
- Envelope `_format: "zeus.chat_request.v2"`.
- The walk close and the slot rule.
- The three search examples.
- Copied `contract.hash` / `contract.id` (`md5:5aacbf1d7a4d9d5de9436cdffbce050f`).
- `CURRENT.json` on **base-1**.
- The Zeus 5.5TH embed on **base-6.1** and **base-7.1**.

## Moved

Nothing was renamed on the wire. `set` gained `id_kind` in the tool schema because the engine already returns an error when that field is missing. base-7.3 stays the walk-close pack. The next edit scaffolds another folder. It does not edit base-7.4 in place.

## Aligned

- Pipeline: page with search limit 10 or 20, then `project` `@step.doc_keys`. `narrow_to` only follows node ids. Typical chain is `search` → `project` `@step.doc_keys`.
- `traverse`: hop, bfs, path, and subgraph take node ids. `walk_path` seeds `from.src_keys` from `@step.doc_keys`. WHEN NOT is first-step orientation, or traverse in place of search.
- `get`: after a step published node ids. FTS leaves `node_ids` empty.
- `order.ids`: `@step.node_ids` or `@step.doc_keys`. The walk seed is not on this field.
- Ranked example: `limit` is on `order`. `project` has no `limit`.
- `rail` and `return`: a browse ends on 10 or 20 cards unless the question asks for a related type.
- Execution lines and the terminate footer: do not bind `@step.ids`; that name is node ids only.
- Code, fraud, research, and regulated examples use `shape`, `via`, `max_nodes`, and `@step.node_ids`. They no longer teach `edge_types` or a limit on `project`.

## Size

Modes do not share one file delta. The shared tool lines are the same length. The mode examples were different lengths, so the file delta is not.

On every mode: `search` character delta 0, `pipeline` **+42**, `return` **+67**, `rail` **+67**.

Analytics versus base-7.3: system 12718 → **12787** (**+69** characters, **+18** tk). File 47003 → **47680** characters (**+677**, **+169** tk, **+1.4%** bytes). Other modes: system **+45** to **+102**, file **+653** to **+718**. `modes_share_file_delta` is **no**.

`verify_base_pack.py --base 7.4` and `diff_modes.py --fail-if-clone` passed. `scan_catalogs.py` count is **170** (10 of them base-7.4).

## Process choices

- Scaffold with `new_base.py --from v2/base/base-7.3 --base 7.4`, then diet the new tree.
- Re-export text with `--no-set-base-id`.
- `--refresh-manifest` rewrote status toward scaffold. Status was set back to `call_align`.
- `assemble_mode_prompts.py` was not run.
- `python3 scripts/chat_request_size.py` rewrote the CSV and then the HTML. The page was not hand-edited.
