# GUIDE — base-7.1 → base-7.2

Additive sentence diet. The wire does not change. Parent is `base-7.1`. No new ticket. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays open.

## Stayed

- All 14 catalog verbs, including `rail` (`name` plus `binds`, no SQL). Zeus still does not execute `rail`. The public engine set is the 13 verbs in `PublicV2Verbs`. `explain` is in that set and has no id chain.
- Required Layer A four: `summary`, `query_decomposition`, `decomposition`, `confidence`.
- `response_output_*`, `report_sink_*`, and `settings_ai_process_result.example.json`, copied from base-7.1 with `cp -n` (`new_base.py` does not copy them).
- Envelope `_format: "zeus.chat_request.v2"`.
- `@step.ids` as the node-id alias. The pack still says it is node ids only.
- The analytics ranked-list example (`find` → `order` → `project`) stays `@cands.node_ids` and `@ord.node_ids`. That chain is legal.
- Copied `contract.hash` / `contract.id`. This cut does not invent a hash.
- `CURRENT.json` on **base-1**.
- The Zeus 5.5TH embed on **base-6.1** and **base-7.1**. This pack is not that pin.

## Moved

Nothing was renamed or removed. base-7.1 stays the measured binding fix. The next edit scaffolds another folder. It does not edit base-7.2 in place.

## Added

The model copies the list the next slot requires:

- `@step.node_ids` feeds get, hop, bfs, path, subgraph, `narrow_to`, and analyze.
- `@step.doc_keys` feeds `walk_path` `src_keys`.
- `project`, `order`, and `enrich` accept either list.
- FTS search leaves `node_ids` empty, so a node-id slot cannot follow that step, and `narrow_to` of an FTS step is not taught.

System text grows **+156** characters on every mode (analytics 12406 → 12562). A structural diff against base-7.1, with lineage and text-pack ids scrubbed, is only those sentences.

## Process choices

- Scaffold with `new_base.py --from v2/base/base-7.1 --base 7.2`, then diet the new tree. `apply_base_id` set `parent_base_id` to `base-7.1`.
- Re-export text with `--no-set-base-id`. That kept the hand-written README.
- Then `--refresh-manifest`. The refresh rewrote MANIFEST status toward scaffold. Status and note were set back to `slot_rule` and the slot-rule sentence after the refresh. `parent_source` stayed the refresh wording `(refresh) v2/base/base-7.2`.
- Do not run `assemble_mode_prompts.py` on this pack. That script can pull the base-6.2 skinny back in.
- Inspector Diff is `catalog-index.json` from `scan_catalogs.py` (150 catalogs, 10 of them base-7.2). `index.html` loads that file. It has no hardcoded base id.
