# base-7.1 overview

| | |
| --- | --- |
| **BASE id** | `base-7.1` |
| **Parent** | `base-7.0` |
| **JSON** | `min/chat_request_<mode>_base-7.1.json` |
| **Text** | `text/chat_request_<mode>_base-7.1.txt` |
| **Jira** | [CR-40](https://kotenai.atlassian.net/browse/CR-40) |
| **Status** | Numbered binding fix. Not a wire break. `CURRENT.json` stays base-1. |

## What changed

The pack no longer tells the model to bind `@step.ids`.

- An FTS `search` is bound with `@step.doc_keys`.
- `find`, hybrid, and node-vector are bound with `@step.node_ids`.
- The analytics ranked-list example (`find` → `order` → `project`) uses `@cands.node_ids` and `@ord.node_ids`.

`@step.ids` remains the node-id alias. This pack does not ask Zeus to fall through to doc keys.

## Unchanged

- 14 verbs, including `rail` (`name` plus `binds`). Zeus still does not execute `rail`.
- Required Layer A four: summary, query_decomposition, decomposition, confidence.
- Envelope `_format: "zeus.chat_request.v2"`.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.1/min --base 7.1 --out v2/base/base-7.1 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.1
```
