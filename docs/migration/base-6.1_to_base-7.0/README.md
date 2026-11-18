# Migration hop: base-6.1 → base-7.0

| | |
| --- | --- |
| **From** | `base-6.1` |
| **Through** | [`base-7.x`](../base-6.1_to_base-7.x/) (working train id) |
| **To** | `base-7.0` |
| **Breaking wire?** | **No** — additive method on the base-6.1 catalog. One new verb: `rail`. |
| **Pack** | [`v2/base/base-7.0/`](../../../v2/base/base-7.0/) |
| **Jira** | [CR-35](https://kotenai.atlassian.net/browse/CR-35) · [CR-37](https://kotenai.atlassian.net/browse/CR-37) |
| **ROADMAP** | [§ base-7.x](../../ROADMAP.md) |

## Theme

base-6.2 reduced the base-6.1 prefix. That size cut was a performance regression, so this train does not parent on base-6.2 and does not diet.

1. Copy base-6.1 into `base-7.x`.
2. Add **Plan, then call** (world, entry, path, goal, at most 8 calls).
3. Add `rail` (`name` from the SCOPE BRIEF, `binds` only, no SQL).
4. Teach boolean rows and `one_of` rows in MINI-SCHEMA, `find`, and `where`. No tenant lists.
5. Cut the numbered folder `base-7.0` from `base-7.x`. Do not edit `base-7.0` in place for the next train.

Prompt growth versus base-6.1 is about **+3043 characters** (~12%) on every mode. That growth is the method plus `rail`.

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-7.x --base 7.0
python3 scripts/export_base_text.py --from v2/base/base-7.0/min --base 7.0 --out v2/base/base-7.0 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.0
python3 scripts/verify_base_pack.py --base 7.0
python3 scripts/diff_modes.py --base 7.0 --fail-if-clone
```

Do not run `assemble_mode_prompts.py` on this pack.

## Docs

| Doc | Role |
| --- | --- |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate |
| [lessons-learned.md](lessons-learned.md) | What this cut kept open |
| [OVERVIEW.md](../../../v2/base/base-7.0/OVERVIEW.md) | Pack delta |

## Pin / engine

- `CURRENT.json` stays **base-1**.
- Zeus does not execute `rail` until an engine change lands. The verb is in the catalog so the model can plan the last call.
- No Client API change is required for the system-text edit.
