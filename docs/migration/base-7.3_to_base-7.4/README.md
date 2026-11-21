# base-7.3 → base-7.4

| | |
| --- | --- |
| **From** | [`v2/base/base-7.3/`](../../../v2/base/base-7.3/) |
| **To** | [`v2/base/base-7.4/`](../../../v2/base/base-7.4/) |
| **Kind** | Sentence align. The HTTP wire does not change. |
| **Pin** | `CURRENT.json` stays base-1. Zeus embed stays base-6.1 and base-7.1. |

base-7.3 stays the walk-close pack. base-7.4 is a new folder. The sentences that described a different call than the verb schema now describe the same call.

## Why

The base-7.3 plan was right in pieces and disagreed with itself in the places the model copies. The pipeline said both "do not narrow_to an FTS step" and "typical: search → narrow → project." `traverse` said expansion is from ids, and also that `walk_path` seeds `doc_keys`. The ranked example put `limit` on `project`, which has no limit parameter. Mode examples bound `@step.ids` and `edge_types`. `rail` and `return` dropped the related-type exception on the 10-or-20 card close. `set` omitted `id_kind`, which the engine already requires.

## What this hop does

- Align those sentences with the schemas. Search keeps its three examples.
- Do not edit base-7.0, base-7.1, base-7.2, or base-7.3 in place.
- Do not flip `CURRENT.json`, invent a contract hash, or run `assemble_mode_prompts.py`.
- Do not run the suite or file a ticket as part of this cut.

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-7.3 --base 7.4
python3 scripts/export_base_text.py --from v2/base/base-7.4/min --base 7.4 --out v2/base/base-7.4 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.4
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.4
python3 scripts/diff_modes.py --base 7.4 --fail-if-clone
python3 scripts/chat_request_size.py
```

Set MANIFEST `status` back to `call_align` after refresh.

## Read next

| Doc | Role |
| --- | --- |
| [GUIDE.md](GUIDE.md) | What stayed and what the sentences say now |
| [lessons-learned.md](lessons-learned.md) | What not to copy forward |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Gate for this hop |
| [OVERVIEW.md](../../../v2/base/base-7.4/OVERVIEW.md) | Pack delta |

## Still open

- The 21-question suite has not been run on base-7.4.
- The Zeus `WALK_PATHS` brief still says find and hybrid results must not go in `src_keys`. That line is outside this pack.
