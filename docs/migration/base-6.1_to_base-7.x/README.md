# Migration hop: base-6.1 → base-7.x

| | |
| --- | --- |
| **From** | `base-6.1` |
| **To** | `base-7.x` |
| **Breaking wire?** | **No** — additive method on the base-6.1 catalog. One new verb: `rail`. |
| **Pack** | [`v2/base/base-7.x/`](../../../v2/base/base-7.x/) |
| **Numbered ship** | [`base-7.0`](../../../v2/base/base-7.0/) · [checklist](../base-6.1_to_base-7.0/RELEASE_CHECKLIST.md) |
| **Jira** | [CR-35](https://kotenai.atlassian.net/browse/CR-35) |
| **ROADMAP** | [§ base-7.x](../../ROADMAP.md) |

## Theme

base-6.2 reduced the base-6.1 prefix. That size cut was a performance regression, so this train does not parent on base-6.2 and does not diet.

1. Copy base-6.1.
2. Add **Plan, then call** (world, entry, path, goal, at most 8 calls).
3. Add `rail` (`name` from the SCOPE BRIEF, `binds` only, no SQL).
4. Teach `search` and `pipeline` the narrow rules. Do not mention `offset`.

Prompt growth versus base-6.1 is about **+3043 characters** (~12%) on every mode. That growth is the method plus `rail`.

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-6.1 --base 7.x
# edit the copied min JSON in place. Do not run assemble_mode_prompts.py.
python3 scripts/export_base_text.py --from v2/base/base-7.x/min --base 7.x --out v2/base/base-7.x --no-set-base-id
python3 scripts/verify_base_pack.py --base 7.x
python3 scripts/diff_modes.py --base 7.x --fail-if-clone
```

## Pin / engine

- `CURRENT.json` may remain **base-1**.
- Zeus does not execute `rail` until an engine change lands. The verb is in the catalog so the model can plan the last call.
- No Client API change is required for the system-text edit. Adding `rail` starts a new plan set once a pack is stamped. This folder does not invent that stamp.
