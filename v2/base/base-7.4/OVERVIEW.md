# base-7.4 overview

| | |
| --- | --- |
| **BASE id** | `base-7.4` |
| **Parent** | `base-7.3` |
| **JSON** | `min/chat_request_<mode>_base-7.4.json` |
| **Text** | `text/chat_request_<mode>_base-7.4.txt` |
| **Status** | Call align. Not a wire break. `CURRENT.json` stays base-1. |

## What changed

The pack still uses the base-7.3 walk close and the base-7.2 slot rule. This hop removes sentences that described a different call than the schema.

- The pipeline typical chain is `search` → `project` `@step.doc_keys`. `narrow_to` only follows a step that published node ids.
- `traverse` names the two seeds: node ids for hop, bfs, path, and subgraph; `@step.doc_keys` for `walk_path`. It does not say "do not traverse after FTS."
- `get` runs after a step published node ids. FTS search leaves `node_ids` empty.
- `order.ids` accepts `@step.node_ids` or `@step.doc_keys`. The walk seed is not restated on that field.
- The ranked example puts `limit` on `order`. `project` has no `limit` parameter, and the engine ignores one.
- `rail` and `return` keep the related-type exception on the 10-or-20 card close.
- Mode examples that bound `@step.ids`, `edge_types`, or `limit` on `project` now use `shape`, `via`, `max_nodes`, and `@step.node_ids`.
- `set` requires `id_kind`.

`@step.ids` remains node ids only, and the text says not to bind that name. The search examples are unchanged.

## Unchanged

- 14 verbs, including `rail` (`name` plus `binds`). Zeus still does not execute `rail`.
- Required Layer A four: summary, query_decomposition, decomposition, confidence.
- Envelope `_format: "zeus.chat_request.v2"`.
- Copied contract hash `md5:5aacbf1d7a4d9d5de9436cdffbce050f`. This cut does not invent one.
- The walk close and the slot rule.

The live Zeus `WALK_PATHS` brief is not in this pack. It still says find and hybrid results must not go in `src_keys`.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.4/min --base 7.4 --out v2/base/base-7.4 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.4
```
