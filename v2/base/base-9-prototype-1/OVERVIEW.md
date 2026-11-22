# base-9-prototype-1 overview

| | |
| --- | --- |
| **BASE id** | `base-9-prototype-1` |
| **Parent** | `base-8.0` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **JSON** | `min/chat_request_<mode>_base-9-prototype-1.json` |
| **Text** | `text/chat_request_<mode>_base-9-prototype-1.txt` |
| **Status** | Prototype. Not the catalog pin. `CURRENT.json` stays base-1. Zeus embed stays base-6.1 and base-7.1. Suite not run. |

## What changed

Cut from base-8.0, not from base-7.4 and not from `v2/min`. base-8.0 already carries the coverage this page keeps: the access rule said once, the probe on an `ex:` spelling, the 8-round ceiling, three search examples, and `project` with no `limit`. The diet removes the four readings v2 retired.

- Each soft facet is its own `query_text`. Two facets do not fold into one string.
- The turn stops on the last set, on zero rows, or on a named gap. A wide first page is not the end state.
- The pipeline tool's one example is the vague chain: hybrid search, `narrow_to` hybrid search, `project`. A stored equality is a `find` in front of that chain, not a `where` on the first hybrid.
- The planning call emits that skeleton and does not carry Layer A. The answer call's `return` writes summary, query_decomposition, decomposition, and confidence after the rows exist.
- Search keeps three single-call examples. The hybrid example is one facet and has no `where`.

The analytics mode overlay no longer shows find, then order, then project as its example. Top-N ranking stays in the system rule, with `limit` on `order`.

## Unchanged

- 14 verbs, including `rail`. Zeus still does not execute `rail`.
- Required Layer A four, on `return`.
- Envelope `_format: "zeus.chat_request.v2"`.
- Each mode keeps the contract hash copied from its base-8.0 file, which was copied from base-7.4. The hash was not invented. Analytics stays `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp. `_lineage.parent_base_id` is `base-8.0`.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9-prototype-1/min --base 9-prototype-1 --out v2/base/base-9-prototype-1 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9-prototype-1
```

After a refresh, set MANIFEST `status` back to `prototype` and `parent_source` back to `v2/base/base-8.0`. The refresh rewrites both. Do not pass `--prototype-pack`. That flag would name the folder `base-9-prototype-1-prototype`.
