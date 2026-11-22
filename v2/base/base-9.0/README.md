# base-9.0

Released catalog, 2026-11-22. Numbered name of the constitution v2 cut that was [`base-9-prototype-7`](../base-9-prototype-7/). Parent released catalog is [`base-8.0`](../base-8.0/). Not the `CURRENT.json` pin. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-9.0` |
| **JSON** | [`min/chat_request_<mode>_base-9.0.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-9.0.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent scaffold** | `v2/base/base-9-prototype-7` |
| **Spec** | [CONSTITUION_DESIGN_v2.md](../../../docs/CONSTITUION_DESIGN_v2.md) |
| **Requirements (docs)** | [BIBLE.md](../../../docs/BIBLE.md) |
| **Roadmap** | [ROADMAP.md](../../../docs/ROADMAP.md) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Prompt assembly** | [PROMPT_ASSEMBLY.md](../../../docs/PROMPT_ASSEMBLY.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min` until you promote |

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-9.0/min --base 9.0 --out v2/base/base-9.0 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9.0
python3 scripts/scan_catalogs.py
```

After `--refresh-manifest --base 9.0`, set MANIFEST `status` back to `constitution` and `parent_source` back to `v2/base/base-9-prototype-7`. The refresh rewrites both. Do not pass `--prototype-pack`.

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/base-9.0 --base <next-id>
# NEVER diet a train in place — always new folder base-<next-id>/
```
