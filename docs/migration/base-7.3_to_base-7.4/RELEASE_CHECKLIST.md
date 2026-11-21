# RELEASE_CHECKLIST — base-7.3 → base-7.4

**Train:** call align · **Jira:** none (parent bind bug [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays To Do) · **Breaking wire:** No · **Date:** 2026-11-20

Parent: `base-7.4` ← `base-7.3`. Short gate, same shape as the [base-7.3 checklist](../base-7.2_to_base-7.3/RELEASE_CHECKLIST.md).

## Pack (Phases B–D)

- [x] New folder `v2/base/base-7.4/` via `new_base.py --from v2/base/base-7.3 --base 7.4` (base-7.3 not edited)
- [x] All 10 modes · `_lineage.base_id` `base-7.4` · `parent_base_id` `base-7.3`
- [x] Diet aligns the plan, tool text, and mode examples with the verb schemas
- [x] Walk close and slot rule left in place
- [x] Ranked example caps `order`. `project` has no `limit`
- [x] `@step.ids` stays node ids only. The text says not to bind it
- [x] `set.id_kind` is required (`node_ids` or `doc_keys`)
- [x] Search examples unchanged
- [x] `report_sink_*` + settings companion copied from base-7.3
- [x] Layer A `response_output_*` unchanged
- [x] Text re-export `--no-set-base-id` + MANIFEST refresh (status hand-set back to `call_align` after refresh)
- [x] `verify_base_pack.py --base 7.4` OK
- [x] `diff_modes.py --base 7.4 --fail-if-clone` OK
- [x] `assemble_mode_prompts.py` not run
- [x] Contract hash copied from base-7.3 · not invented
- [x] `scan_catalogs.py` (catalog-index count **170**, 10 of them base-7.4)
- [x] `python3 scripts/chat_request_size.py` rewrote the CSV, then the HTML from that CSV
- [x] Analytics system **+69** characters (12718 → 12787). File **+677** characters. Token delta is not shared across modes (`modes_share_file_delta` **no**)

## Docs (Phase E)

- [x] Hop README + GUIDE + lessons
- [x] ROADMAP content train points at `v2/base/base-7.4/` as the catalog candidate (Zeus served pin stays base-7.1)
- [x] COMPAT candidate row (5.5TH served-pin cell stays base-7.1)
- [x] RELEASE_NOTES unreleased highlight
- [x] Playbook jump row
- [x] Pack OVERVIEW / README
- [x] Inspector Diff is the scanned index (`index.html` loads `catalog-index.json`; no hardcoded base id)

## Jira (Phase J)

- [x] No new ticket. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays To Do. No new Client parser story.

## Residual (not blocking this catalog candidate)

- [ ] 21-question suite on base-7.4
- [ ] Zeus `WALK_PATHS` brief still says find and hybrid results must not go in `src_keys`
- [ ] Zeus embed. Local 5.5TH tree still embeds **base-6.1** and **base-7.1** (served pin **base-7.1**). The lab image still serves base-7.0.
- [ ] CURRENT pin (still base-1)
- [ ] Stamped `rail` run (inherited; Zeus does not execute `rail` yet)
