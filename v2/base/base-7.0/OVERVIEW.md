# base-7.0 overview

Short pack changelog. Full method: [ROADMAP § base-7.x](../../../docs/ROADMAP.md) · [CR-35](https://kotenai.atlassian.net/browse/CR-35) · [CR-37](https://kotenai.atlassian.net/browse/CR-37).

| | |
| --- | --- |
| **BASE id** | `base-7.0` |
| **Scaffolded from** | `v2/base/base-7.x` (that folder's parent is `base-6.1`) |
| **Breaking wire?** | **No** — same Layer A; one added verb |
| **Jira** | [CR-35](https://kotenai.atlassian.net/browse/CR-35) · [CR-37](https://kotenai.atlassian.net/browse/CR-37) |
| **JSON** | `min/chat_request_<mode>_base-7.0.json` |
| **Status** | Numbered ship of the base-7.x train. Not the production pin. |

`base-7.x` is the working train id. This folder is the numbered snapshot of that train. base-6.2 cut the base-6.1 prefix and that size cut was a performance regression, so neither folder parents on base-6.2.

## What changed

- System lead **Plan, then call** (world, entry, path, goal, 8-call budget) in front of the access-path list.
- Access-path lead is **the cheapest move that still follows the plan**.
- `search`: one clause, user's words unchanged, entry limit up to 200, do not shrink an FTS limit.
- `pipeline`: one drill-down is one call; later steps `narrow_to`; shrink later hybrid or vector limits only; page at 10 or 20 then `project` (`project` ignores limit).
- New **`rail`** verb on every mode: `name` copied from the SCOPE BRIEF, `binds` already in hand, no SQL. Last call only, and only when the brief names a rail.
- **14 verbs** (the base-6.1 thirteen plus `rail`). Required Layer A four unchanged.
- MINI-SCHEMA teaching ([CR-37](https://kotenai.atlassian.net/browse/CR-37)): a boolean row accepts `true`, `false`, or one listed spelling, and the server matches the stored strings `"true"` and `"false"`. A `one_of` row is the whole set: copy one listed string. The same law is on `find` and on `where`. No tenant value lists are in this pack. Those lists stay on the entity map and are injected at runtime.

## Measured

System text plus tool JSON is **+3043 characters** versus the matching base-6.1 mode on all 10 modes (about **+12%**). The prototype `_hash` is still the copied parent value. It is not a Hub stamp.

## Left out of the shared pin

- Hotel nouns, tag lists, and strength numbers.
- `find` `offset`. The V2 mapper does not forward it yet.
- A call to `embed(scope, text)`. [ZE-406](https://kotenai.atlassian.net/browse/ZE-406) and [ZE-407](https://kotenai.atlassian.net/browse/ZE-407) own that. This pack only tells the model to pass `query_text` through.

`rail` is catalog teaching. Zeus does not execute that verb until an engine change lands. `CURRENT.json` stays **base-1**.

## Checks

`verify_base_pack.py --base 7.0` and `diff_modes.py --base 7.0 --fail-if-clone` passed on this snapshot.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.0/min --base 7.0 --out v2/base/base-7.0 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.0
python3 scripts/verify_base_pack.py --base 7.0
python3 scripts/diff_modes.py --base 7.0 --fail-if-clone
```

Do not run `assemble_mode_prompts.py` on this pack. That script pulls the CORE overlay and can reintroduce the base-6.2 skinny. Do not edit this folder in place for the next train. Scaffold a new `base-<id>/`.
