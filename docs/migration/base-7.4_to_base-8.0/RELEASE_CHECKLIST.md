# RELEASE_CHECKLIST — base-7.4 → base-8.0

**Train:** constitution morph · **Jira:** none · **Breaking wire:** No · **Date:** 2026-11-21

Parent: `base-8.0` ← `base-7.4`. The bytes were first cut as `base-8-prototype-1`. This hop gives that cut its numbered name.

## Pack

- [x] New folder `v2/base/base-8.0/` via `new_base.py --from v2/base/base-8-prototype-1 --base 8.0` (base-7.4 not edited)
- [x] All 10 modes · `_lineage.base_id` `base-8.0` · `parent_base_id` `base-7.4`
- [x] System text and verb schemas match `base-8-prototype-1`
- [x] Contract hash copied from base-7.4 · not invented
- [x] `verify_base_pack.py --base 8.0` OK
- [x] `diff_modes.py --base 8.0 --fail-if-clone` OK
- [x] `assemble_mode_prompts.py` not run
- [x] `scan_catalogs.py` count 200, size page, and constitution exam recorded. The exam sorts a word suffix before the numbered id, so latest is base-8.0. Open 0 is the gate, not accuracy.

## Docs

- [x] Hop README + GUIDE + lessons
- [x] ROADMAP content train points at `v2/base/base-8.0/` as the released catalog (2026-11-21). `CURRENT.json` stays base-1. Suite not run.
- [x] COMPAT candidate row (Zeus served pin stays base-7.1)
- [x] RELEASE_NOTES section `base-8.0 — 2026-11-21` (not an unreleased highlight)
- [x] Playbook jump row
- [x] Pack OVERVIEW / README

## Jira

- [x] No new ticket. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays To Do.

## Residual

- [ ] 21-question suite on base-8.0
- [ ] Zeus `WALK_PATHS` brief still says find and hybrid results must not go in `src_keys`
- [ ] Zeus embed. Local 5.5TH tree still embeds **base-6.1** and **base-7.1** (served pin **base-7.1**)
- [ ] Beelink image may still list `base-8-prototype-1` until it is rebuilt from `base-8.0`
- [ ] CURRENT pin (still base-1)
- [ ] Stamped `rail` run (inherited; Zeus does not execute `rail` yet)
