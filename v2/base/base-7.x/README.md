# base-7.x

Ship pack for chat_request catalogs. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-7.x` |
| **JSON** | [`min/chat_request_<mode>_base-7.x.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-7.x.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent scaffold** | `v2/base/base-6.1` (not base-6.2; that size cut regressed) |
| **Jira** | [CR-35](https://kotenai.atlassian.net/browse/CR-35) |
| **Requirements (docs)** | [BIBLE.md](../../../docs/BIBLE.md) |
| **Roadmap** | [ROADMAP.md](../../../docs/ROADMAP.md) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Prompt assembly** | [PROMPT_ASSEMBLY.md](../../../docs/PROMPT_ASSEMBLY.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min` until you promote |

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.x/min --base 7.x --out v2/base/base-7.x --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.x
python3 scripts/scan_catalogs.py
```

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/base-7.x --base <next-id>
# NEVER diet a train in place — always new folder base-<next-id>/
```
