# base-7.1

Binding fix on the base-7.0 Plan-then-call pack. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-7.1` |
| **JSON** | [`min/chat_request_<mode>_base-7.1.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-7.1.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Report companions** | [`report_sink_schema.json`](report_sink_schema.json) · [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) (unchanged from base-7.0) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent** | `base-7.0` |
| **Jira** | [CR-40](https://kotenai.atlassian.net/browse/CR-40) |
| **Hop** | [base-7.0 → base-7.1](../../../docs/migration/base-7.0_to_base-7.1/) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min`. This folder does not flip that pin. |

Same 14 verbs as base-7.0, including `rail`. The only diet is how a later step binds the previous step.

- After an FTS `search`, bind `@step.doc_keys`.
- After `find`, hybrid, or node-vector, bind `@step.node_ids`.
- `@step.ids` stays node ids only.

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.1/min --base 7.1 --out v2/base/base-7.1 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.1
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.1
python3 scripts/diff_modes.py --base 7.1 --fail-if-clone
```

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/base-7.1 --base <next-id>
# NEVER diet a train in place — always new folder base-<next-id>/
```
