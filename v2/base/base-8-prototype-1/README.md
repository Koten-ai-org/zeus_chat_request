# base-8-prototype-1

A second constitution morph of the base-7.4 pack. A new folder, cut again after [CONSTITUION_DESIGN.md](../../../docs/CONSTITUION_DESIGN.md) was updated. The numbered name of this cut is [base-8.0](../base-8.0/), and that folder is the released catalog (2026-11-21). The earlier folder [base-8-prototype](../base-8-prototype/) stays on disk. This folder stays. It is not a pin, not an embed, and not a suite.

| | |
| --- | --- |
| **BASE id** | `base-8-prototype-1` |
| **JSON** | [`min/chat_request_<mode>_base-8-prototype-1.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-8-prototype-1.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Report companions** | [`report_sink_schema.json`](report_sink_schema.json) · [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) (copied from base-7.4) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent** | `base-7.4` |
| **Call law** | [CONSTITUION_DESIGN.md](../../../docs/CONSTITUION_DESIGN.md) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min`. Zeus embed stays **base-6.1** and **base-7.1**. |

Same 14 verbs as base-7.4, including `rail`. The morph keeps a 7.4 sentence that already matches a constitution statement and drops a sentence that only repeated one.

- One access statement. Later tools say "copy the list the plan names." `narrow_to` takes node ids only, so it cannot follow an FTS step. That sentence stays on the plan.
- `query_decomposition` records fast path when the question and the mini-schema already fill the plan, or one probe when the question is vague, the evidence size is unknown, or a basic value may not be stored. An `ex:` row is a spelling sample. Out of this dataset is a gap.
- Two intents that share a world are two chains in one `pipeline`. A shared value is probed once. Zero stops every chain that needed it.
- `order` takes `limit`. `project` does not.
- On a fast path the terminating pipeline may carry the decomposition and the summary shape. The facts come from the rows. A probe writes the facts after the probe returns.
- The walk-close "even when" clause stays on the plan. It is not copied onto `find` or `traverse`.

Search still has three examples. `set` still requires `id_kind`. Each mode keeps the contract hash copied from its base-7.4 file. This cut does not invent one. `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp.

The hypothesis page [../hypothesis_base-8-prototype.html](../hypothesis_base-8-prototype.html) is a prebuild of the previous morph. It is not a result for this folder. The After column is empty. No 21-question suite has been run.

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-8-prototype-1/min --base 8-prototype-1 --out v2/base/base-8-prototype-1 --no-set-base-id
python3 scripts/verify_base_pack.py --base 8-prototype-1
python3 scripts/diff_modes.py --base 8-prototype-1 --fail-if-clone
python3 scripts/scan_catalogs.py
python3 scripts/chat_request_size.py
python3 scripts/constitution_exam.py
```

`--refresh-manifest` rewrites `status` toward scaffold and the note toward the scaffold sentence. Set `status` back to `prototype` after a refresh. Do not pass `--prototype-pack` (the id is already `8-prototype-1`). Do not pass `--base 8`. Do not re-export without `--no-set-base-id` (that snaps `_lineage.base_id`).
