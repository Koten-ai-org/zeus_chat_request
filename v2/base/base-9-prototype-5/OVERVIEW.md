# base-9-prototype-5 overview

| | |
| --- | --- |
| **BASE id** | `base-9-prototype-5` |
| **Parent** | `base-9-prototype-4` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **JSON** | `min/chat_request_<mode>_base-9-prototype-5.json` |
| **Text** | `text/chat_request_<mode>_base-9-prototype-5.txt` |
| **Status** | Prototype. Not the catalog pin. `CURRENT.json` stays base-1. Zeus embed stays base-6.1 and base-7.1. Suite not run. |

## What changed

Cut from base-9-prototype-4. The diet is the each-parent reading.

- A list of the child in each parent fills `relation` with that parent. It does not fill `attribute`.
- The back-walk under that parent is the chain. The call is `walk_path` on the inverse. `project` of the field is the card, not the close.
- A null on that field in the first page does not replace the walk, and it does not become `wish_i_knew`.
- `shape` stays common, exact, or vague. It is not `group_by`.

## Unchanged

- An empty parent still does not stop a `scalar_ent` child `where`. An `entity_fk` child still needs the document key.
- `query_decomposition` stays on the planning call. `summary`, `decomposition`, and `confidence` stay on the answer `return`.
- 14 verbs, including `rail`. Zeus still does not execute `rail`.
- Contract hash copied from base-9-prototype-4. The hash was not invented. Analytics stays `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp. `_lineage.parent_base_id` is `base-9-prototype-4`. `_base_meta.prototype` stays false.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9-prototype-5/min --base 9-prototype-5 --out v2/base/base-9-prototype-5 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9-prototype-5
```

After a refresh, set MANIFEST `status` back to `prototype`, `parent_source` back to `v2/base/base-9-prototype-4`, and `prototype` true on each catalog. The refresh rewrites all three. Do not pass `--prototype-pack`. That flag would name the folder `base-9-prototype-5-prototype`.
