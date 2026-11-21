# base-7.0 → base-7.1

| | |
| --- | --- |
| **From** | [`v2/base/base-7.0/`](../../../v2/base/base-7.0/) |
| **To** | [`v2/base/base-7.1/`](../../../v2/base/base-7.1/) |
| **Jira** | [CR-40](https://kotenai.atlassian.net/browse/CR-40) |
| **Wire** | Same. This hop changes the sentences the model copies into `ids`. |

base-7.0 stays as shipped. base-7.1 is a new folder cut from that working tree.

## Why

A full-text `search` writes hits on `doc_keys` and leaves `node_ids` empty. `@step.ids` reads `node_ids` only. base-7.0 told every mode to bind `@step.ids`, so a later `project` ran on an empty list. A terminating pipeline writes the summary on that same call, so the advisory `PIPELINE_AMBIGUOUS_IDS` cannot repair the turn.

## Sentences

- After an FTS `search`, bind `@step.doc_keys`.
- After `find`, hybrid, or node-vector, bind `@step.node_ids`.
- Do not teach `@step.ids` as the preferred bind.

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-7.0 --base 7.1
python3 scripts/export_base_text.py --from v2/base/base-7.1/min --base 7.1 --out v2/base/base-7.1 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.1
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.1
python3 scripts/diff_modes.py --base 7.1 --fail-if-clone
```

Do not run `assemble_mode_prompts.py` on this pack.

## Docs

| Doc | Role |
| --- | --- |
| [GUIDE.md](GUIDE.md) | What stayed, what was added |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate |
| [lessons-learned.md](lessons-learned.md) | What this cut kept open |
| [OVERVIEW.md](../../../v2/base/base-7.1/OVERVIEW.md) | Pack delta |

## What this hop does not do

- Edit base-7.0 in place.
- Flip `CURRENT.json`. That pin stays base-1.
- Invent a production `contract_hash`.
- Make Zeus fall through from `@step.ids` to doc keys.
- Run the 21-question suite. That comparison is still open.
