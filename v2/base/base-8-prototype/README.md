# base-8-prototype

Constitution morph of the base-7.4 pack. A new folder. The later cut is numbered **base-8.0**, and that folder is the catalog candidate. This folder stays. It is not a pin, not an embed, and not a suite.

| | |
| --- | --- |
| **BASE id** | `base-8-prototype` |
| **JSON** | [`min/chat_request_<mode>_base-8-prototype.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-8-prototype.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Report companions** | [`report_sink_schema.json`](report_sink_schema.json) · [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) (copied from base-7.4) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent** | `base-7.4` |
| **Design** | [CONSTITUION_DESIGN.md](../../../docs/CONSTITUION_DESIGN.md) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min`. Zeus embed stays **base-6.1** and **base-7.1**. |

Same 14 verbs as base-7.4, including `rail`. The morph keeps a 7.4 sentence that already matches a constitution statement and drops a sentence that only repeated one.

- One access statement. Later tools say "copy the list the plan names."
- `query_decomposition` records fast path or one probe. An `ex:` row is a spelling sample.
- Two intents that share a world are two chains in one `pipeline`.
- `order` takes `limit`. `project` does not.
- On a fast path the terminating pipeline may carry the summary shape. The facts come from the rows. A probe writes the facts after the probe returns.
- The card close and the walk-close "even when" clause stay on the plan. They are not copied onto `rail`, `return`, `find`, or `traverse`.

Search still has three examples. `set` still requires `id_kind`. The contract hash is the copied base-7.4 hash. This cut does not invent one.

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-8-prototype/min --base 8-prototype --out v2/base/base-8-prototype --no-set-base-id
python3 scripts/verify_base_pack.py --base 8-prototype
python3 scripts/diff_modes.py --base 8-prototype --fail-if-clone
python3 scripts/scan_catalogs.py
python3 scripts/chat_request_size.py
python3 scripts/constitution_exam.py
```

`--refresh-manifest` rewrites `status` toward scaffold and the note toward the scaffold sentence. Set `status` back to `prototype` after a refresh. Do not pass `--base 8` (that looks for a folder named `base-8`). Do not re-export without `--no-set-base-id` (that snaps `_lineage.base_id` back to `base-8`).
