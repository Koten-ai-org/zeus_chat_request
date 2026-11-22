# base-9-prototype-3 overview

| | |
| --- | --- |
| **BASE id** | `base-9-prototype-3` |
| **Parent** | `base-9-prototype-2` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **JSON** | `min/chat_request_<mode>_base-9-prototype-3.json` |
| **Text** | `text/chat_request_<mode>_base-9-prototype-3.txt` |
| **Status** | Prototype. Not the catalog pin. `CURRENT.json` stays base-1. Zeus embed stays base-6.1 and base-7.1. Suite not run. |

## What changed

Cut from base-9-prototype-2. The model-facing call rule is the only diet. The Hub treatment table, the layer badges, and Save stay on the constitution page.

- `query_decomposition` fills `attribute`, `geo`, `audience`, `theme`, `occasion`, `price`, `dates`, `availability`, `rating`, `relation`, `parts`, and `other` when the string signals them.
- A stored spelling is `find`. A soft phrase is one `search`. `relation` is `walk_path` when that chain is listed. `Best` is `order` after the bag exists. `Count` is `return` `count`. `display` and `skip` are not a `where`.
- A price, date, availability, or rating comparison is a named rail when the brief has one, and `wish_i_knew` when it does not.

## Unchanged

- `query_decomposition` stays on the planning call. `summary`, `decomposition`, and `confidence` stay on the answer `return`.
- The vague chain skeleton, the closed-list sentences, and the three search examples.
- 14 verbs, including `rail`. Zeus still does not execute `rail`.
- Contract hash copied from base-9-prototype-2. The hash was not invented. Analytics stays `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp. `_lineage.parent_base_id` is `base-9-prototype-2`.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9-prototype-3/min --base 9-prototype-3 --out v2/base/base-9-prototype-3 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9-prototype-3
```

After a refresh, set MANIFEST `status` back to `prototype`, `parent_source` back to `v2/base/base-9-prototype-2`, and `prototype` true on each catalog. The refresh rewrites all three. Do not pass `--prototype-pack`. That flag would name the folder `base-9-prototype-3-prototype`.
