# base-7.2 → base-7.3

| | |
| --- | --- |
| **From** | [`v2/base/base-7.2/`](../../../v2/base/base-7.2/) |
| **To** | [`v2/base/base-7.3/`](../../../v2/base/base-7.3/) |
| **Jira** | None. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays the parent bind bug and stays To Do. |
| **Wire** | Same. This hop changes when `find` yields to `walk_path`. |

base-7.1 stays the pack the local Zeus 5.5TH tree embeds. base-7.2 stays the slot-rule pack the 2026-11-20 suite measured. base-7.3 is a new folder cut from that tree.

## Why

On the 2026-11-20 full pass, base-7.1 met 20/21 and base-7.2 met 16/21, net −4. Three of the losses were travel questions where base-7.2 answered with `find`, `get`, or `project` and never called `walk_path`. Country and city are stored on the hotel, and the pack already says a known stored value stays `find`. That sentence was winning over the walk close. The beer 21A loss was the scorer missing a pipeline step alias; Zeus had returned the rows. This hop does not change the scorer.

## Sentences

Existing lines only. No new paragraph.

- A known stored value stays `find`, unless that value is the other end of a WALK_PATHS chain.
- A related type on a WALK_PATHS chain closes with `traverse` `walk_path`, and `from.src_keys` is `@step.doc_keys`, even when the seed row already shows that field.
- The same clause is on the access-path line and on the `find` and `traverse` tool descriptions, so those lines do not contradict the close.

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-7.2 --base 7.3
python3 scripts/export_base_text.py --from v2/base/base-7.3/min --base 7.3 --out v2/base/base-7.3 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.3
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base 7.3
python3 scripts/diff_modes.py --base 7.3 --fail-if-clone
python3 scripts/chat_request_size.py
```

Do not run `assemble_mode_prompts.py` on this pack. After `--refresh-manifest`, set status back to `walk_close`.

## Docs

| Doc | Role |
| --- | --- |
| [GUIDE.md](GUIDE.md) | What stayed, what was added |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate |
| [lessons-learned.md](lessons-learned.md) | What this cut kept open |
| [OVERVIEW.md](../../../v2/base/base-7.3/OVERVIEW.md) | Pack delta |

## What this hop does not do

- Edit base-7.0, base-7.1, or base-7.2 in place.
- Flip `CURRENT.json`. That pin stays base-1.
- Invent a production `contract_hash`.
- Swap the Zeus embed. The served pin stays base-7.1.
- Make Zeus fall through from `@step.ids` to doc keys.
- Run the 21-question suite on base-7.3.
- File a new ticket.
