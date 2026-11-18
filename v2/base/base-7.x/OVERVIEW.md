# base-7.x overview

Short pack changelog. Full method: [ROADMAP § base-7.x](../../../docs/ROADMAP.md) · [CR-35](https://kotenai.atlassian.net/browse/CR-35).

| | |
| --- | --- |
| **BASE id** | `base-7.x` |
| **Scaffolded from** | `v2/base/base-6.1` |
| **Breaking wire?** | **No** — same Layer A; one added verb |
| **Jira** | [CR-35](https://kotenai.atlassian.net/browse/CR-35) · [CR-37](https://kotenai.atlassian.net/browse/CR-37) |
| **JSON** | `min/chat_request_<mode>_base-7.x.json` |
| **Status** | Working train. Numbered ship is [`base-7.0`](../base-7.0/). Not a production stamp. |

base-6.2 cut the base-6.1 prefix and that size cut was a performance regression. This pack copies base-6.1 and adds the method. It does not continue the diet.

## What changed

- System lead **Plan, then call** (world, entry, path, goal, 8-call budget) in front of the access-path list.
- Access-path lead is **the cheapest move that still follows the plan**.
- `search`: one clause, user's words unchanged, entry limit up to 200, do not shrink an FTS limit.
- `pipeline`: one drill-down is one call; later steps `narrow_to`; shrink later hybrid or vector limits only; page at 10 or 20 then `project` (`project` ignores limit).
- New **`rail`** verb on every mode: `name` copied from the SCOPE BRIEF, `binds` already in hand, no SQL. Last call only, and only when the brief names a rail.
- **14 verbs** (the base-6.1 thirteen plus `rail`). Required Layer A four unchanged.

## Measured

System text plus tool JSON is **+3043 characters** versus the matching base-6.1 mode on all 10 modes (about **+12%**). The prototype `_hash` is still the copied parent value. It is not a Hub stamp.

## Left out of the shared pin

- Hotel nouns, tag lists, and strength numbers.
- `find` `offset`. The V2 mapper does not forward it yet.
- A call to `embed(scope, text)`. [ZE-406](https://kotenai.atlassian.net/browse/ZE-406) and [ZE-407](https://kotenai.atlassian.net/browse/ZE-407) own that. This pack only tells the model to pass `query_text` through.

`rail` is catalog teaching. Zeus does not execute that verb until an engine change lands.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.x/min --base 7.x --out v2/base/base-7.x --no-set-base-id
python3 scripts/verify_base_pack.py --base 7.x
python3 scripts/diff_modes.py --base 7.x --fail-if-clone
```

Do not run `assemble_mode_prompts.py` on this pack. That script pulls the CORE overlay and can reintroduce the base-6.2 skinny.
