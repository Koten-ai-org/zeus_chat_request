# base-9-prototype-2 overview

| | |
| --- | --- |
| **BASE id** | `base-9-prototype-2` |
| **Parent** | `base-9-prototype-1` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **JSON** | `min/chat_request_<mode>_base-9-prototype-2.json` |
| **Text** | `text/chat_request_<mode>_base-9-prototype-2.txt` |
| **Status** | Prototype. Not the catalog pin. `CURRENT.json` stays base-1. Zeus embed stays base-6.1 and base-7.1. Suite not run. |

## What changed

Cut from base-9-prototype-1. The amendment on the v2 page is the only diet.

- `query_decomposition` is how the submitted string was understood: intent, entity, shape, suggestion, and why.
- It is required once on `find`, `search`, `pipeline`, and `rail`, beside the query those calls create.
- `summary`, `decomposition`, and `confidence` stay on the answer `return`, after the rows exist. `return` still requires `query_decomposition`, and the answer call copies the object already written beside the queries.
- A probe writes `query_decomposition` with the probe.

## Unchanged

- The vague chain skeleton, the four retired readings, and the three search examples.
- 14 verbs, including `rail`. Zeus still does not execute `rail`.
- Envelope `_format: "zeus.chat_request.v2"`.
- Contract hash copied from base-9-prototype-1, which was copied from base-8.0. The hash was not invented. Analytics stays `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp. `_lineage.parent_base_id` is `base-9-prototype-1`.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9-prototype-2/min --base 9-prototype-2 --out v2/base/base-9-prototype-2 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9-prototype-2
```

After a refresh, set MANIFEST `status` back to `prototype`, `parent_source` back to `v2/base/base-9-prototype-1`, and `prototype` true on each catalog. The refresh rewrites all three. Do not pass `--prototype-pack`. That flag would name the folder `base-9-prototype-2-prototype`.
