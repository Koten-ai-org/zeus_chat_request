# GUIDE — base-7.2 → base-7.3

Additive sentence diet. The wire does not change. Parent is `base-7.2`. No new ticket. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays open.

Placement is CORE plus the `find` and `traverse` tool descriptions. The failure is the wrong verb on any scope, so the rule stays in the always-on contract. The new words are a clause on sentences that already exist. There is no new paragraph.

## Stayed

- All 14 catalog verbs, including `rail` (`name` plus `binds`, no SQL). Zeus still does not execute `rail`.
- Required Layer A four: `summary`, `query_decomposition`, `decomposition`, `confidence`.
- `response_output_*`, `report_sink_*`, and `settings_ai_process_result.example.json`, copied from base-7.2. `new_base.py` copies the response-output pair. The report companions were copied with `cp -n`.
- Envelope `_format: "zeus.chat_request.v2"`.
- The base-7.2 slot rule. Node-id slots take `@step.node_ids`. `walk_path` `src_keys` takes `@step.doc_keys`. `project`, `order`, and `enrich` accept either. FTS search leaves `node_ids` empty.
- `@step.ids` as the node-id alias.
- The analytics ranked-list example (`find` → `order` → `project`) stays `@cands.node_ids` and `@ord.node_ids`.
- Copied `contract.hash` / `contract.id` (`md5:5aacbf1d7a4d9d5de9436cdffbce050f`). This cut does not invent a hash.
- `CURRENT.json` on **base-1**.
- The Zeus 5.5TH embed on **base-6.1** and **base-7.1**. This pack is not that pin.

## Moved

Nothing was renamed or removed. base-7.2 stays the measured slot-rule pack. The next edit scaffolds another folder. It does not edit base-7.3 in place.

## Added

One clause, in the lines that already talk about `find` and the walk close:

- A known stored value stays `find`, unless that value is the other end of a WALK_PATHS chain.
- The walk close still runs when the seed row already shows that field.

System text grows **+156** characters on every mode (analytics 12562 → 12718). Every mode file grows **+247** characters. The token delta is **+61** or **+62** because UTF-8 bytes ÷ 4 rounds on a boundary. Analytics is **+61** tk (11723 → 11784). `search`, `pipeline`, `return`, and `rail` character counts are unchanged. The `find` and `traverse` description growth is the JSON-wrap remainder, **+91** characters. A structural diff against base-7.2, with lineage and text-pack ids scrubbed, is only those clauses.

## Process choices

- Scaffold with `new_base.py --from v2/base/base-7.2 --base 7.3`, then diet the new tree. `apply_base_id` set `parent_base_id` to `base-7.2`.
- Re-export text with `--no-set-base-id`. That kept the hand-written README.
- Then `--refresh-manifest`. The refresh rewrote MANIFEST status toward scaffold. Status and note were set back to `walk_close` and the walk-close sentence after the refresh. `parent_source` stayed the refresh wording `(refresh) v2/base/base-7.3`.
- Do not run `assemble_mode_prompts.py` on this pack. That script can pull the base-6.2 skinny back in.
- `python3 scripts/chat_request_size.py` rewrote `v2/base/chat_request_size.csv` and then `v2/base/chat_request_size.html` from that CSV. The page was not hand-edited.
- Inspector Diff is `catalog-index.json` from `scan_catalogs.py` (160 catalogs, 10 of them base-7.3). `index.html` loads that file. It has no hardcoded base id.
