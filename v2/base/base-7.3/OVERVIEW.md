# base-7.3 overview

| | |
| --- | --- |
| **BASE id** | `base-7.3` |
| **Parent** | `base-7.2` |
| **JSON** | `min/chat_request_<mode>_base-7.3.json` |
| **Text** | `text/chat_request_<mode>_base-7.3.txt` |
| **Status** | Numbered walk-close diet. Not a wire break. `CURRENT.json` stays base-1. |

## What changed

The pack still uses the base-7.2 slot rule. This hop only decides when `find` is the wrong close.

- A known stored value stays `find`, unless that value is the other end of a WALK_PATHS chain.
- A related type on that chain still closes with `traverse` `walk_path`, and `from.src_keys` is `@step.doc_keys`, even when the seed row already shows that field.
- The `find` and `traverse` tool lines say the same thing. No new paragraph.

`@step.ids` remains the node-id alias. The ranked-list example stays `find` → `@cands.node_ids` → `@ord.node_ids`.

## Unchanged

- 14 verbs, including `rail` (`name` plus `binds`). Zeus still does not execute `rail`.
- Required Layer A four: summary, query_decomposition, decomposition, confidence.
- Envelope `_format: "zeus.chat_request.v2"`.
- Copied contract hash. This cut does not invent one.
- The slot rule: node-id slots take `@step.node_ids`, `walk_path` `src_keys` takes `@step.doc_keys`, and `project`, `order`, and `enrich` accept either.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.3/min --base 7.3 --out v2/base/base-7.3 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.3
```
