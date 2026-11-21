# RELEASE_CHECKLIST — base-7.1 → base-7.2

**Train:** copy the list the next slot requires · **Jira:** none (parent bind bug [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays To Do) · **Breaking wire:** No · **Date:** 2026-11-20

Parent: `base-7.2` ← `base-7.1`. Short gate, same shape as the [base-7.1 checklist](../base-7.0_to_base-7.1/RELEASE_CHECKLIST.md). The full template phases are the headings below.

## Pack (Phases B–D)

- [x] New folder `v2/base/base-7.2/` via `new_base.py --from v2/base/base-7.1 --base 7.2` (base-7.1 not edited)
- [x] All 10 modes · `_lineage.base_id` `base-7.2` · `parent_base_id` `base-7.1`
- [x] Diet is the slot rule (`@step.node_ids` for a node-id slot, `@step.doc_keys` for `walk_path` `src_keys`, either list for `project` / `order` / `enrich`)
- [x] Ranked example left as `@cands.node_ids` / `@ord.node_ids`
- [x] `@step.ids` stays node ids only (warnings kept; no engine fall-through)
- [x] `report_sink_*` + settings companion copied from base-7.1 (`new_base.py` does not copy them)
- [x] Layer A `response_output_*` unchanged
- [x] Text re-export `--no-set-base-id` + MANIFEST refresh (status hand-set back to `slot_rule` after refresh)
- [x] `verify_base_pack.py --base 7.2` OK
- [x] `diff_modes.py --base 7.2 --fail-if-clone` OK
- [x] `assemble_mode_prompts.py` not run (can pull the base-6.2 skinny back)
- [x] Contract hash copied from base-7.1 · not invented
- [x] `scan_catalogs.py` (catalog-index count **150**, 10 of them base-7.2)
- [x] System growth vs base-7.1: **+156** characters on every mode (analytics 12406 → 12562)

## Docs (Phase E)

- [x] Hop README + GUIDE + lessons
- [x] ROADMAP content train points at `v2/base/base-7.2/` as the catalog candidate (Zeus served pin stays base-7.1)
- [x] COMPAT candidate row (5.5TH served-pin cell stays base-7.1)
- [x] RELEASE_NOTES unreleased highlight
- [x] Playbook jump row
- [x] Pack OVERVIEW / README
- [x] Inspector Diff is the scanned index (`index.html` loads `catalog-index.json`; no hardcoded base id)

## Jira (Phase J)

- [x] No new ticket. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays To Do. Wire unchanged, so no new Client parser story.

## Residual (not blocking this catalog candidate)

- [ ] 21-question suite on base-7.2
- [ ] Zeus embed. Local 5.5TH tree still embeds **base-6.1** and **base-7.1** (served pin **base-7.1**). The lab image still serves base-7.0.
- [ ] CURRENT pin (still base-1)
- [ ] Stamped `rail` run (inherited; Zeus does not execute `rail` yet)
