# Migration hop: base-6.1 → base-7.0

| | |
| --- | --- |
| **From** | `base-6.1` |
| **Through** | [`base-7.x`](../base-6.1_to_base-7.x/) (working train id) |
| **To** | `base-7.0` |
| **Breaking wire?** | **No** — additive method on the base-6.1 catalog. One new verb: `rail`. |
| **Pack** | [`v2/base/base-7.0/`](../../../v2/base/base-7.0/) |
| **Jira** | [CR-35](https://kotenai.atlassian.net/browse/CR-35) · [CR-37](https://kotenai.atlassian.net/browse/CR-37) |
| **ROADMAP** | [§ base-7.x](../../ROADMAP.md) |

## Theme

base-6.2 reduced the base-6.1 prefix. That size cut was a performance regression, so this train does not parent on base-6.2 and does not diet.

1. Copy base-6.1 into `base-7.x`.
2. Add **Plan, then call** (world, entry, path, goal, at most 8 calls).
3. Add `rail` (`name` from the SCOPE BRIEF, `binds` only, no SQL).
4. Teach boolean rows and `one_of` rows in MINI-SCHEMA, `find`, and `where`. No tenant lists.
5. Cut the numbered folder `base-7.0` from `base-7.x`. Do not edit `base-7.0` in place for the next train.

Prompt growth versus base-6.1 is about **+3043 characters** (~12%) on every mode. That growth is the method plus `rail`.

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-7.x --base 7.0
python3 scripts/export_base_text.py --from v2/base/base-7.0/min --base 7.0 --out v2/base/base-7.0 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 7.0
python3 scripts/verify_base_pack.py --base 7.0
python3 scripts/diff_modes.py --base 7.0 --fail-if-clone
```

Do not run `assemble_mode_prompts.py` on this pack.

## Docs

| Doc | Role |
| --- | --- |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate |
| [lessons-learned.md](lessons-learned.md) | What this cut kept open |
| [PROMPT_SENTENCES.md](PROMPT_SENTENCES.md) | Why each added prompt sentence is there, and what it costs |
| [OVERVIEW.md](../../../v2/base/base-7.0/OVERVIEW.md) | Pack delta |

## Pin / engine

- `CURRENT.json` stays **base-1**. The central `v2/min` alias is unchanged.
- Zeus **5.5TH** embeds two built-in packs: **base-6.1** and **base-7.0**. The Workbench picker lists both. `ai/chat_request/PIN.json` `base_id` is **base-7.0**, so `GET /v1/ai/chat_request.json` and `chat_request_base_id` serve base-7.0 when the caller does not pick a file.
- Zeus does not execute `rail` until an engine change lands. The verb is in the catalog so the model can plan the last call.
- No Client API change is required for the system-text edit.

## Suite (2026-11-18)

The locked 21-question page, still on the old beach sentence, is base-6.1 **18/21** and base-7.0 **20/21**. Better 3, worse 1, same 16, Orange 1, net **+2**. The runner said: “base-7.0 is better on 3 question(s) and worse on 1. 16 question(s) are the same. Read the worse rows before treating this run as a promotion. 1 question(s) ended on an API error and stay out of the net until a re-test.”

The three gains are the exact IPA find, the Stone walk, and the Redbrook city walk. The Orange row is `beer-walk-beers-by-country` (last HTTP 400). The worse row was the open beach trip, which asked for a `walk_path` to a country string. That question is now “Plan a beach trip in France. Suggest hotels and landmarks.” Its one-question page is **1/1 vs 1/1, net 0**. The runner said that page does not show a reason to switch. It does not replace the 21-question net.

SQL++ on the live sample: `country = "France"` and the whole word beach is **0 hotels**. Coastal French hotels exist without that word (Nice 7, Cannes 1, Saint-Raphaël 1, Bonifacio 1, Saint-Florent 2). Landmarks: Dramont beach, and the Normandy American Cemetery because the content says Omaha Beach. On the France retest, base-6.1 named Nice and Cannes. base-7.0’s full-text `beach France` hits included Los Angeles, Carlsbad, and Argyll.
