# base-7.2 overview

| | |
| --- | --- |
| **BASE id** | `base-7.2` |
| **Parent** | `base-7.1` |
| **JSON** | `min/chat_request_<mode>_base-7.2.json` |
| **Text** | `text/chat_request_<mode>_base-7.2.txt` |
| **Status** | Numbered slot-rule fix. Not a wire break. `CURRENT.json` stays base-1. |

## What changed

The pack no longer picks the bind from the previous verb.

- Copy `@step.node_ids` into get, hop, bfs, path, subgraph, `narrow_to`, and analyze.
- Copy `@step.doc_keys` into `walk_path` `src_keys`.
- `project`, `order`, and `enrich` accept either list.
- FTS search leaves `node_ids` empty, so do not `narrow_to` that step.
- The ranked-list example stays `find` → `@cands.node_ids` → `@ord.node_ids`.

`@step.ids` remains the node-id alias.

## Unchanged

- 14 verbs, including `rail` (`name` plus `binds`). Zeus still does not execute `rail`.
- Required Layer A four: summary, query_decomposition, decomposition, confidence.
- Envelope `_format: "zeus.chat_request.v2"`.
- Copied contract hash. This cut does not invent one.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.2/min --base 7.2 --out v2/base/base-7.2 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.2
```
