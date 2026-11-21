# RELEASE_CHECKLIST — base-7.0 → base-7.1

**Train:** FTS `@step.doc_keys` · find / hybrid / node-vector `@step.node_ids` · **Jira:** [CR-40](https://kotenai.atlassian.net/browse/CR-40) · **Breaking wire:** No · **Date:** 2026-11-20

Parent: `base-7.1` ← `base-7.0`. Short gate, same shape as the [base-7.0 checklist](../base-6.1_to_base-7.0/RELEASE_CHECKLIST.md). The full template phases are the headings below.

## Pack (Phases B–D)

- [x] New folder `v2/base/base-7.1/` via `new_base.py --from v2/base/base-7.0 --base 7.1` (base-7.0 not edited)
- [x] All 10 modes · `_lineage.base_id` `base-7.1` · `parent_base_id` `base-7.0`
- [x] Diet is the bind sentences only (FTS `@step.doc_keys`; find / hybrid / node-vector `@step.node_ids`; analytics example `@cands.node_ids` / `@ord.node_ids`)
- [x] `@step.ids` stays node ids only (warnings kept; no engine fall-through)
- [x] `report_sink_*` + settings companion copied from base-7.0 (`new_base.py` does not copy them)
- [x] Layer A `response_output_*` unchanged
- [x] Text re-export `--no-set-base-id` + MANIFEST refresh (status hand-set back to `binding_fix` after refresh)
- [x] `verify_base_pack.py --base 7.1` OK
- [x] `diff_modes.py --base 7.1 --fail-if-clone` OK
- [x] `assemble_mode_prompts.py` not run (can pull the base-6.2 skinny back)
- [x] Contract hash copied from base-7.0 · not invented
- [x] `scan_catalogs.py` (catalog-index count **140**, 10 of them base-7.1)
- [x] System growth vs base-7.0: **+384** characters on nine modes, **+394** on analytics

## Docs (Phase E)

- [x] Hop README + GUIDE + lessons
- [x] ROADMAP content train points at `v2/base/base-7.1/` (base-7.0 stays the previous numbered ship)
- [x] COMPAT candidate row
- [x] RELEASE_NOTES unreleased highlight
- [x] Playbook jump row
- [x] Pack OVERVIEW / README
- [x] Inspector Diff is the scanned index (`index.html` loads `catalog-index.json`; no hardcoded base id)

## Jira (Phase J)

- [x] [CR-40](https://kotenai.atlassian.net/browse/CR-40) filed (To Do). Wire unchanged, so no new Client parser story.
- [ ] Do not close CR-40 from this checklist. Suite, lab image, and pin are still open.

## Residual (not blocking this catalog candidate)

- [ ] 21-question suite on base-7.1
- [ ] Lab image. Local Zeus 5.5TH tree embeds **base-6.1** and **base-7.1** (served pin **base-7.1**). That tree is uncommitted. The lab image still serves base-7.0.
- [ ] CURRENT pin (still base-1)
- [ ] Stamped `rail` run (inherited from base-7.0; Zeus does not execute `rail` yet)
