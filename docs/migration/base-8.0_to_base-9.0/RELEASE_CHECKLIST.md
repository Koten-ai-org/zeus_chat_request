# RELEASE_CHECKLIST — base-8.0 → base-9.0

**Train:** constitution v2 · **Jira:** none · **Breaking wire:** No · **Date:** 2026-11-22

Parent: `base-9.0` ← `base-8.0`. The bytes were first cut as `base-9-prototype-7`. This hop gives that cut its numbered name.

## Pack

- [x] New folder `v2/base/base-9.0/` via `new_base.py --from v2/base/base-9-prototype-7 --base 9.0` (base-8.0 not edited)
- [x] All 10 modes · `_lineage.base_id` `base-9.0` · `parent_base_id` `base-8.0`
- [x] System text and verb schemas match `base-9-prototype-7`
- [x] Contract hash copied · not invented · analytics `md5:5aacbf1d7a4d9d5de9436cdffbce050f`
- [x] `verify_base_pack.py --base 9.0` OK
- [x] `diff_modes.py --base 9.0 --fail-if-clone` OK
- [x] `assemble_mode_prompts.py` not run
- [x] `scan_catalogs.py` count 280. Size page rewritten. v1 exam latest is base-9.0, open 0. That count is the gate, not accuracy, and it is not the v2 spec.

## Docs

- [x] Hop README + GUIDE + lessons
- [x] ROADMAP content train points at `v2/base/base-9.0/` as the released catalog (2026-11-22). `CURRENT.json` stays base-1.
- [x] COMPAT candidate row (Zeus served pin stays base-7.1)
- [x] RELEASE_NOTES section `base-9.0 — 2026-11-22` (not an unreleased highlight)
- [x] Playbook jump row
- [x] Pack OVERVIEW / README

## Jira

- [x] No new ticket. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays To Do. Client and Zeus residual stay open. The pin epic is not this pack.

## Residual

- [ ] Current question lock on base-9.0 (the 2026-11-22 full suite used the lock from before the Paris split)
- [ ] Zeus embed. Local 5.5TH tree still embeds **base-6.1** and **base-7.1** (served pin **base-7.1**)
- [ ] Beelink image is still the base-9-prototype-6 build until it is rebuilt from `base-9.0`
- [ ] CURRENT pin (still base-1)
- [ ] Stamped `rail` run (inherited; Zeus does not execute `rail` yet)
