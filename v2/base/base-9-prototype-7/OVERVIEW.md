# base-9-prototype-7 overview

| | |
| --- | --- |
| **BASE id** | `base-9-prototype-7` |
| **Parent** | `base-9-prototype-6` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **JSON** | `min/chat_request_<mode>_base-9-prototype-7.json` |
| **Text** | `text/chat_request_<mode>_base-9-prototype-7.txt` |
| **Status** | Prototype. Not the catalog pin. `CURRENT.json` stays base-1. Zeus embed stays base-6.1 and base-7.1. No suite has been run. |

## What changed

Cut from base-9-prototype-6. The diet puts the probe statement into the model text and puts the empty-list guard on `walk_path`.

- `from` needs `doc_key`, a non-empty `src_keys`, or a `where`. That sentence is on the decisive call, the probe bullet, and the `walk_path` field.
- That rejection stays on the call. It does not become `wish_i_knew`.
- Zero rows of that child `where` stop and name the gap.
- An empty `entity_fk` parent is the gap, because there is no key to copy.
- The parent walk waits until that parent `find` returns keys.
- The `query_decomposition` line on `find`, `search`, `pipeline`, and `rail` keeps the field contract. The walk essay stays on the decisive call and the probe bullet.

## Unchanged

- A parent `find` that returns nothing is still not a seed. Its `doc_keys` stay off `src_keys`. An empty list is still not a selector.
- The plan lines still say `from.src_keys` is `@step.doc_keys` when that list has keys.
- A list of the child in each parent still fills `relation` and walks the inverse when the parent `find` returns keys.
- An empty parent still does not stop a `scalar_ent` child `where` when the question names a spelling.
- `query_decomposition` stays on the planning call. `summary`, `decomposition`, and `confidence` stay on the answer `return`.
- 14 verbs, including `rail`. Zeus still does not execute `rail`.
- Contract hashes copied from base-9-prototype-6. The hashes were not invented. Analytics stays `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp. `_lineage.parent_base_id` is `base-9-prototype-6`. `_base_meta.prototype` stays false.
- The Layer A `relation` description now says the parent walk waits until that parent `find` returns keys. The example file is the copy from base-9-prototype-6.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9-prototype-7/min --base 9-prototype-7 --out v2/base/base-9-prototype-7 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9-prototype-7
```

After a refresh, set MANIFEST `status` back to `prototype`, `parent_source` back to `v2/base/base-9-prototype-6`, and `prototype` true on each catalog. The refresh rewrites all three. Do not pass `--prototype-pack`. That flag would name the folder `base-9-prototype-7-prototype`.
