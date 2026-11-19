# base-7.0

Numbered ship of the base-7.x Plan-then-call pack. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-7.0` |
| **JSON** | [`min/chat_request_<mode>_base-7.0.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-7.0.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Report companions** | [`report_sink_schema.json`](report_sink_schema.json) · [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) (unchanged from base-6.1) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent** | `base-7.x` ← `base-6.1` |
| **Jira** | [CR-35](https://kotenai.atlassian.net/browse/CR-35) · [CR-37](https://kotenai.atlassian.net/browse/CR-37) |
| **Requirements (docs)** | [BIBLE.md](../../../docs/BIBLE.md) |
| **Roadmap** | [ROADMAP § base-7.x](../../../docs/ROADMAP.md) |
| **Hop** | [base-6.1 → base-7.0](../../../docs/migration/base-6.1_to_base-7.0/) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Prompt assembly** | [PROMPT_ASSEMBLY.md](../../../docs/PROMPT_ASSEMBLY.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min`. This folder does not flip the pin. |

14 verbs. `rail` is `name` plus `binds`. Zeus does not execute `rail` yet. Boolean and `one_of` teaching points at the runtime MINI-SCHEMA. It does not copy a tenant's value lists into these files.

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.0/min --base 7.0 --out v2/base/base-7.0 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.0
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.0
python3 scripts/diff_modes.py --base 7.0 --fail-if-clone
```

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/base-7.0 --base <next-id>
# NEVER diet a train in place — always new folder base-<next-id>/
```
