# GUIDE — base-7.0 → base-7.1

Additive sentence diet. The wire does not change. Parent is `base-7.0`. Ticket is [CR-40](https://kotenai.atlassian.net/browse/CR-40).

## Stayed

- All 14 verbs, including `rail` (`name` plus `binds`, no SQL). Zeus still does not execute `rail`.
- Required Layer A four: `summary`, `query_decomposition`, `decomposition`, `confidence`.
- `response_output_*`, `report_sink_*`, and `settings_ai_process_result.example.json`, copied from base-7.0.
- Envelope `_format: "zeus.chat_request.v2"`.
- `@step.ids` as the node-id alias. The pack still says it is node ids only.
- Copied `contract.hash` / `contract.id`. This cut does not invent a hash.
- `CURRENT.json` on **base-1**.

## Moved

Nothing was renamed or removed. base-7.0 stays the previous numbered ship. The next edit scaffolds another folder. It does not edit base-7.1 in place.

## Added

The model is told which id list to copy:

- After an FTS `search`, bind `@step.doc_keys`.
- After `find`, hybrid, or node-vector, bind `@step.node_ids`.
- The analytics ranked-list example (`find` → `order` → `project`) uses `@cands.node_ids` and `@ord.node_ids`.

System text grows **+384** characters on nine modes and **+394** on analytics. The extra ten characters are that ranked example. A structural diff of all ten modes against base-7.0, with lineage and text-pack ids scrubbed, is only those sentences.

## Process choices

- Scaffold with `new_base.py --from v2/base/base-7.0 --base 7.1`, then diet the new tree.
- `new_base.py` does not copy `report_sink_*` or `settings_ai_process_result.example.json`. Those three files were copied from base-7.0.
- Re-export text with `--no-set-base-id`, then `--refresh-manifest`. The refresh rewrote MANIFEST status toward scaffold. Status and note were set back to `binding_fix` and the CR-40 sentence.
- Do not run `assemble_mode_prompts.py` on this pack. That script can pull the base-6.2 skinny back in.
- Inspector Diff is `catalog-index.json` from `scan_catalogs.py` (140 catalogs, 10 of them base-7.1). `index.html` loads that file. It has no hardcoded base id.
