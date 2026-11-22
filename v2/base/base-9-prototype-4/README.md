# base-9-prototype-4

Prototype pack for the constitution v2 empty-parent cut. An empty parent type does not stop a `scalar_ent` child `where`. A filled `relation` is `walk_path`, and `project` of that field is the card. Not the catalog pin. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-9-prototype-4` |
| **JSON** | [`min/chat_request_<mode>_base-9-prototype-4.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-9-prototype-4.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent scaffold** | `v2/base/base-9-prototype-3` |
| **Requirements (docs)** | [BIBLE.md](../../../docs/BIBLE.md) |
| **Roadmap** | [ROADMAP.md](../../../docs/ROADMAP.md) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Prompt assembly** | [PROMPT_ASSEMBLY.md](../../../docs/PROMPT_ASSEMBLY.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min` until you promote |

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-9-prototype-4/min --base 9-prototype-4 --out v2/base/base-9-prototype-4 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 9-prototype-4
python3 scripts/scan_catalogs.py
```

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/base-9-prototype-4 --base <next-id>
# NEVER diet a train in place — always new folder base-<next-id>/
```
