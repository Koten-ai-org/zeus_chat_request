# base-8.0

Numbered name of the constitution morph that was `base-8-prototype-1`. Cut from base-7.4. **This folder is the released catalog (2026-11-21).** It is not the Zeus pin and not a suite result.

| | |
| --- | --- |
| **BASE id** | `base-8.0` |
| **JSON** | [`min/chat_request_<mode>_base-8.0.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-8.0.txt`](text/) |
| **Schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Example** | [`response_output_example.json`](response_output_example.json) |
| **Report companions** | [`report_sink_schema.json`](report_sink_schema.json) · [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) (copied from the prototype-1 cut) |
| **Lineage** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent** | `base-7.4` |
| **Hop** | [base-7.4 → base-8.0](../../../docs/migration/base-7.4_to_base-8.0/) |

## What this folder is

Same 14 verbs as base-7.4, including `rail`. The morph keeps a 7.4 sentence that already matches a constitution statement and drops a sentence that only repeated one. `query_decomposition` records fast path or one probe. The call ceiling stays 8.

`CURRENT.json` stays **base-1**. The Zeus embed stays **base-6.1** and **base-7.1**. The earlier folders [base-8-prototype](../base-8-prototype/) and [base-8-prototype-1](../base-8-prototype-1/) stay on disk. This folder is the numbered name of the second cut. Beelink may still list `base-8-prototype-1` until that image is rebuilt from these files.

Search still has three examples. `set` still requires `id_kind`. Each mode keeps the contract hash copied from its base-7.4 file. This cut does not invent one. `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp.

No 21-question suite has been run on this folder. The hypothesis page [../hypothesis_base-8-prototype.html](../hypothesis_base-8-prototype.html) is a prebuild of the earlier morph. It is not a result for base-8.0.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-8.0/min --base 8.0 --out v2/base/base-8.0 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 8.0
```

After `--refresh-manifest`, set MANIFEST `status` back to `constitution`. The refresh rewrites it toward scaffold.

```bash
python3 scripts/verify_base_pack.py --base 8.0
python3 scripts/diff_modes.py --base 8.0 --fail-if-clone
```

Do not run `assemble_mode_prompts.py` on this pack. Do not pass `--prototype-pack`.

## Next base

```bash
python3 scripts/new_base.py --from v2/base/base-8.0 --base <next-id>
```

That creates a new folder. It does not edit base-8.0 in place.
