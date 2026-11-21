# base-8.0 overview

| | |
| --- | --- |
| **BASE id** | `base-8.0` |
| **Parent** | `base-7.4` |
| **JSON** | `min/chat_request_<mode>_base-8.0.json` |
| **Text** | `text/chat_request_<mode>_base-8.0.txt` |
| **Status** | Released catalog, 2026-11-21. Numbered name of `base-8-prototype-1`. `CURRENT.json` stays base-1. Embed stays base-6.1 and base-7.1. The earlier folder `base-8-prototype` stays. Suite not run. |

## What changed

The bytes are the second constitution morph of base-7.4, the folder that was `base-8-prototype-1`. The 7.4 sentences that already match a statement stayed. Copies came out in the same edit.

- The plan states the access rule once, and states that `narrow_to` takes node ids only. The pipeline tool does not repeat that sentence.
- `query_decomposition` records fast path when the question and the mini-schema already fill the plan. It records one probe when the question is vague, when the evidence size is unknown, or when a basic value may not be stored. Out of this dataset is a gap, not another search.
- Two intents that share a world are two chains in that one pipeline. A shared value is probed once. Zero stops every chain that needed it. The call ceiling stays 8.
- Ranked lists put `limit` on `order`, then `project` those ids. `project` has no `limit`.
- On a fast path the terminating pipeline may carry the decomposition and the summary shape. The facts come from the rows that return.

## Unchanged

- 14 verbs, including `rail` (`name` plus `binds`). Zeus still does not execute `rail`.
- Required Layer A four: summary, query_decomposition, decomposition, confidence.
- Envelope `_format: "zeus.chat_request.v2"`.
- Each mode keeps the contract hash copied from its base-7.4 file. `_base_meta.base_id` is still `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp.
- Search's three examples. `set.id_kind` required. The plan still says `from.src_keys` is `@step.doc_keys`.

The live Zeus scope brief is not in this pack. It still says find and hybrid results must not go in `src_keys`. No 21-question suite has been run. [../hypothesis_base-8-prototype.html](../hypothesis_base-8-prototype.html) is a prebuild of the earlier morph. The After column is empty. That page is not a result for base-8.0.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-8.0/min --base 8.0 --out v2/base/base-8.0 --no-set-base-id
python3 scripts/verify_base_pack.py --base 8.0
```

After `--refresh-manifest --base 8.0`, set MANIFEST `status` back to `constitution`. The refresh rewrites it toward scaffold. Do not pass `--prototype-pack`.
