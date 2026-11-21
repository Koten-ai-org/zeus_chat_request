# base-8-prototype overview

| | |
| --- | --- |
| **BASE id** | `base-8-prototype` |
| **Parent** | `base-7.4` |
| **JSON** | `min/chat_request_<mode>_base-8-prototype.json` |
| **Text** | `text/chat_request_<mode>_base-8-prototype.txt` |
| **Status** | Earlier prototype. The released catalog is base-8.0 (2026-11-21). `CURRENT.json` stays base-1. Embed stays base-6.1 and base-7.1. |

## What changed

Morphed from base-7.4 by [CONSTITUION_DESIGN.md](../../../docs/CONSTITUION_DESIGN.md). The 7.4 call-align sentences that already match a statement stayed. Copies came out in the same edit.

- The plan states the access rule once: node-id slots take `@step.node_ids`, `walk_path` `src_keys` take `@step.doc_keys`, and `project`, `order`, and `enrich` accept either. FTS leaves `node_ids` empty. Do not bind `@step.ids`.
- `query_decomposition` records the suggestion: fast path when the mini-schema fills most of the plan, or one probe when the question is vague or a basic value may not be stored.
- Two intents that share a world are two chains in that one pipeline. The call ceiling stays 8.
- Ranked lists put `limit` on `order`, then `project` those ids.
- A fast path may put the summary shape on the terminating pipeline and fills the facts from the rows that return.

## Unchanged

- 14 verbs, including `rail` (`name` plus `binds`). Zeus still does not execute `rail`.
- Required Layer A four: summary, query_decomposition, decomposition, confidence.
- Envelope `_format: "zeus.chat_request.v2"`.
- Copied contract hash `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- Search's three examples. `set.id_kind` required. The `walk_path` parameter still says `from.src_keys` is `@step.doc_keys`.

The live Zeus scope brief is not in this pack. It still says find and hybrid results must not go in `src_keys`. No 21-question suite has been run on this folder. The guess for that suite is [../hypothesis_base-8-prototype.html](../hypothesis_base-8-prototype.html). It is a prebuild of the comparison report: left base-7.2, right base-8-prototype-1. The After column is empty until the run exists.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-8-prototype/min --base 8-prototype --out v2/base/base-8-prototype --no-set-base-id
python3 scripts/verify_base_pack.py --base 8-prototype
```

After `--refresh-manifest --base 8-prototype`, set MANIFEST `status` back to `prototype`. The refresh rewrites it toward scaffold.
