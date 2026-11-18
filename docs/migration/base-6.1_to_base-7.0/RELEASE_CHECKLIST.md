# RELEASE_CHECKLIST — base-6.1 → base-7.0

**Train:** Plan, then call + boolean / `one_of` teaching · **Jira:** CR-35, CR-37 · **Breaking wire:** No

Parent chain: `base-7.0` ← `base-7.x` ← `base-6.1`. base-6.2 is not the parent.

## Pack

- [x] `v2/base/base-7.x/` working train from base-6.1
- [x] `v2/base/base-7.0/` numbered snapshot via `new_base.py`
- [x] All 10 modes
- [x] Plan, then call on every mode
- [x] `rail` on every mode · parameters `name` and `binds` only
- [x] Boolean and `one_of` sentences on MINI-SCHEMA, `find`, and `where` (CR-37)
- [x] `where` stays `additionalProperties: true`
- [x] report_sink + settings companions copied (unchanged from base-6.1)
- [x] `verify_base_pack.py --base 7.0` OK
- [x] `diff_modes.py --base 7.0 --fail-if-clone` OK
- [x] text export + MANIFEST refresh
- [x] `scan_catalogs.py` (catalog-index count 130)
- [x] Prompt growth vs base-6.1 measured about +3043 characters (~12%)

## Docs

- [x] Hop README + lessons
- [x] ROADMAP § base-7.x points at `v2/base/base-7.0/`
- [x] COMPAT candidate row
- [x] RELEASE_NOTES unreleased highlight
- [x] Pack OVERVIEW / README

## Residual (not blocking this catalog candidate)

- [ ] Stamped run: a hard fact with a named rail is a last `rail` call (Zeus does not execute `rail` yet)
- [ ] A/B or gold books (CR-36)
- [ ] Zeus vendor pin
- [ ] CURRENT pin (still base-1)
