# base-7.4

Call-align diet on the base-7.3 pack. Sentences that disagreed now match the verb schemas. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-7.4` |
| **JSON** | [`min/chat_request_<mode>_base-7.4.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-7.4.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Report companions** | [`report_sink_schema.json`](report_sink_schema.json) · [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) (unchanged from base-7.3) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent** | `base-7.3` |
| **Hop** | [base-7.3 → base-7.4](../../../docs/migration/base-7.3_to_base-7.4/) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min`. This folder does not flip that pin. |

Same 14 verbs as base-7.3, including `rail`. The diet makes the plan, the tool text, and the mode examples describe the same call.

- `narrow_to` follows a step that published node ids. The typical chain is `search` → `project` `@step.doc_keys`.
- `hop`, `bfs`, `path`, and `subgraph` take node ids. `walk_path` still seeds `from.src_keys` from `@step.doc_keys`.
- `project` has no `limit`. The ranked example caps `order`.
- A browse ends on 10 or 20 cards, unless the question asks for a related type on a WALK_PATHS chain. `rail` and `return` say that too.
- Do not bind `@step.ids`. That name is node ids only.
- `set` requires `id_kind` (`node_ids` or `doc_keys`). The engine already rejected a call that omitted it.

Search examples are unchanged. The three search objects stay the parameter contract.

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-7.4/min --base 7.4 --out v2/base/base-7.4 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.4
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.4
python3 scripts/diff_modes.py --base 7.4 --fail-if-clone
```

After `--refresh-manifest`, set MANIFEST `status` back to `call_align`. The refresh rewrites it toward scaffold.

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/base-7.4 --base <next-id>
```

That creates a new folder. It does not edit base-7.4 in place.
