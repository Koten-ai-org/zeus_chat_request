# base-9.0 overview

| | |
| --- | --- |
| **BASE id** | `base-9.0` |
| **Parent** | `base-8.0` |
| **Bytes from** | `base-9-prototype-7` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **JSON** | `min/chat_request_<mode>_base-9.0.json` |
| **Text** | `text/chat_request_<mode>_base-9.0.txt` |
| **Status** | Released catalog, 2026-11-22. Numbered name of `base-9-prototype-7`. `CURRENT.json` stays base-1. Embed stays base-6.1 and base-7.1. The earlier base-9-prototype folders stay. |

## What changed

The bytes are the constitution v2 probe-statement cut, the folder that was `base-9-prototype-7`. v1 still gates base-8.0. This pack follows [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md).

- `from` needs `doc_key`, a non-empty `src_keys`, or a `where`. That sentence is on the decisive call, the probe bullet, and the `walk_path` field.
- That rejection stays on the call. It does not become `wish_i_knew`.
- Zero rows of that child `where` stop and name the gap.
- An empty `entity_fk` parent is the gap, because there is no key to copy.
- The parent walk waits until that parent `find` returns keys.
- A stored spelling is `find`. A soft phrase is one `search`. A list of the child in each parent fills `relation` and walks the inverse.
- `query_decomposition` is written once beside the queries. The answer `return` copies that object and still requires `summary`, `decomposition`, and `confidence`.

## Unchanged

- 14 verbs, including `rail`. Zeus still does not execute `rail`.
- Required Layer A four: `summary`, `query_decomposition`, `decomposition`, `confidence`.
- `policy_action`, `jail_break_attempt`, `subject_confidence`, `wish_i_knew`, `business_rules_triggers`, and `data_gaps` stay on `return`. Hints still do not replace jailbreak and company law.
- Envelope `_format: "zeus.chat_request.v2"`.
- Each mode keeps the contract hash copied along the prototype chain. The hashes were not invented. Analytics stays `md5:5aacbf1d7a4d9d5de9436cdffbce050f`.
- `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp. `_lineage.parent_base_id` is `base-8.0`.

The 2026-11-22 full suite measured these bytes as base-9-prototype-7 against base-8.0: 16/22 versus 18/22, better 2, worse 0, net +2, three questions not run. That run used the question lock from before the Paris split. The current lock has not been run.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9.0/min --base 9.0 --out v2/base/base-9.0 --no-set-base-id
python3 scripts/verify_base_pack.py --base 9.0
```

After `--refresh-manifest --base 9.0`, set MANIFEST `status` back to `constitution`. The refresh rewrites it toward scaffold. Do not pass `--prototype-pack`.
