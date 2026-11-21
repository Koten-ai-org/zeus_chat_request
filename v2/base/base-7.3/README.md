# base-7.3

Walk-close diet on the base-7.2 pack. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-7.3` |
| **JSON** | [`min/chat_request_<mode>_base-7.3.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-7.3.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Report companions** | [`report_sink_schema.json`](report_sink_schema.json) · [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) (unchanged from base-7.2) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent** | `base-7.2` |
| **Hop** | [base-7.2 → base-7.3](../../../docs/migration/base-7.2_to_base-7.3/) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min`. This folder does not flip that pin. |

Same 14 verbs as base-7.2, including `rail`. The diet is when `find` yields to `walk_path`.

- A known stored value stays `find`, unless that value is the other end of a WALK_PATHS chain.
- That related type still closes with `traverse` `walk_path`, even when the seed row already shows the field.
- `from.src_keys` stays `@step.doc_keys`. `@step.ids` stays node ids only.

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.3/min --base 7.3 --out v2/base/base-7.3 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.3
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.3
python3 scripts/diff_modes.py --base 7.3 --fail-if-clone
```

After `--refresh-manifest`, set MANIFEST `status` back to `walk_close`. The refresh rewrites it toward scaffold.

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/base-7.3 --base <next-id>
# NEVER diet a train in place — always new folder base-<next-id>/
