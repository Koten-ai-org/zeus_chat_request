# base-9-prototype-6 overview

| | |
| --- | --- |
| **BASE id** | `base-9-prototype-6` |
| **Parent** | `base-9-prototype-5` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **JSON** | `min/chat_request_<mode>_base-9-prototype-6.json` |
| **Text** | `text/chat_request_<mode>_base-9-prototype-6.txt` |
| **Status** | Prototype. Not the catalog pin. `CURRENT.json` stays base-1. Zeus embed stays base-6.1 and base-7.1. The full 22-question suite has not been run. |

## What changed

Cut from base-9-prototype-5. The diet is the empty-seed reading.

- A parent `find` that returns nothing is not a seed. Its `doc_keys` stay off `src_keys`.
- An empty list is not a selector. `from` needs `doc_key`, a non-empty `src_keys`, or a `where`.
- That rejection stays on the call. It does not become `wish_i_knew`.
- With no spelling in the question, a `scalar_ent` child is a `find` of the child. `project` of the parent field is the card. The parent walk waits until that `find` returns keys.
- An `entity_fk` child still has no key to copy.

## Measured

Not a full suite. On 2026-11-22, grok-4.7, Zeus 1.0.0-beta.3, against base-8.0:

- `beer-walk-belgian` and `travel-walk-state-counts`: 1/2 versus 1/2, net 0. Belgian both hit the inverse of `Beer.brewery_id`. The hotels row did not reach the model on this pack (`050016`).
- `travel-walk-city-hotels`: 1/1 versus 1/1, net 0. Both called `walk_path`. The city hop returned no rows. The stored row is The Bell Inn.

Pages: `baseline/reports/2026-11-22-worse-two/` and `baseline/reports/2026-11-22-city-walk/`.

## Unchanged

- A list of the child in each parent still fills `relation` and walks the inverse when the parent `find` returns keys.
- An empty parent still does not stop a `scalar_ent` child `where` when the question names a spelling.
- `query_decomposition` stays on the planning call. `summary`, `decomposition`, and `confidence` stay on the answer `return`.
- 14 verbs, including `rail`. Zeus still does not execute `rail`.
- Contract hashes copied from base-9-prototype-5. The hashes were not invented. Analytics stays `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp. `_lineage.parent_base_id` is `base-9-prototype-5`. `_base_meta.prototype` stays false.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9-prototype-6/min --base 9-prototype-6 --out v2/base/base-9-prototype-6 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9-prototype-6
```

After a refresh, set MANIFEST `status` back to `prototype`, `parent_source` back to `v2/base/base-9-prototype-5`, and `prototype` true on each catalog. The refresh rewrites all three. Do not pass `--prototype-pack`. That flag would name the folder `base-9-prototype-6-prototype`.
