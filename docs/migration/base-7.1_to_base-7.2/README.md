# base-7.1 → base-7.2

| | |
| --- | --- |
| **From** | [`v2/base/base-7.1/`](../../../v2/base/base-7.1/) |
| **To** | [`v2/base/base-7.2/`](../../../v2/base/base-7.2/) |
| **Jira** | None. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays the parent bind bug and stays To Do. |
| **Wire** | Same. This hop changes which list the model copies into the next slot. |

base-7.1 stays the pack the 2026-11-20 suite measured, and the pack the local Zeus 5.5TH tree embeds. base-7.2 is a new folder cut from that tree.

## Why

base-7.1 named the bind from the previous verb: `@step.doc_keys` after FTS, `@step.node_ids` after find, hybrid, or node-vector. That second sentence is the wrong seed for `walk_path`. The engine accepts a doc key in `from.src_keys` and rejects a node id there. A node-id slot (`get`, hop, bfs, path, subgraph, `narrow_to`, analyze) is the other way around. One rule covers every pair: copy the list the next slot requires.

## Sentences

- `@step.node_ids` feeds get, hop, bfs, path, subgraph, `narrow_to`, and analyze.
- `@step.doc_keys` feeds `walk_path` `src_keys`.
- `project`, `order`, and `enrich` accept either list.
- FTS search leaves `node_ids` empty, so a node-id slot cannot follow it.
- `@step.ids` stays node ids only.

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-7.1 --base 7.2
python3 scripts/export_base_text.py --from v2/base/base-7.2/min --base 7.2 --out v2/base/base-7.2 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.2
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.2
python3 scripts/diff_modes.py --base 7.2 --fail-if-clone
```

Do not run `assemble_mode_prompts.py` on this pack.

## Docs

| Doc | Role |
| --- | --- |
| [GUIDE.md](GUIDE.md) | What stayed, what was added |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate |
| [lessons-learned.md](lessons-learned.md) | What this cut kept open |
| [OVERVIEW.md](../../../v2/base/base-7.2/OVERVIEW.md) | Pack delta |

## What this hop does not do

- Edit base-7.0 or base-7.1 in place.
- Flip `CURRENT.json`. That pin stays base-1.
- Invent a production `contract_hash`.
- Swap the Zeus embed. The served pin stays base-7.1.
- Make Zeus fall through from `@step.ids` to doc keys.
- Run the 21-question suite. That comparison is still open.
- File a new ticket.
