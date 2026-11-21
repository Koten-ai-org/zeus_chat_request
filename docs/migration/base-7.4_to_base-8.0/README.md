# base-7.4 → base-8.0

| | |
| --- | --- |
| **From** | [`v2/base/base-7.4/`](../../../v2/base/base-7.4/) |
| **To** | [`v2/base/base-8.0/`](../../../v2/base/base-8.0/) |
| **Wire** | Additive. Not a wire break. |
| **Date** | 2026-11-21 |

base-7.4 stays the call-align pack. base-8.0 is a new folder. It is the numbered name of the constitution morph that was `base-8-prototype-1`. The catalog was released on 2026-11-21. That release is not the `CURRENT.json` pin. The sentences that already matched a constitution statement stayed. Copies came out in that same edit.

`CURRENT.json` stays **base-1**. The Zeus embed stays **base-6.1** and **base-7.1**. The earlier folders `base-8-prototype` and `base-8-prototype-1` stay on disk.

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-8.0/min --base 8.0 --out v2/base/base-8.0 --no-set-base-id
python3 scripts/verify_base_pack.py --base 8.0
python3 scripts/diff_modes.py --base 8.0 --fail-if-clone
```

Do not run `assemble_mode_prompts.py`. Do not invent a contract hash.

## Related

| Doc | Role |
| --- | --- |
| [GUIDE.md](GUIDE.md) | What the morph changed |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Gate for this hop |
| [lessons-learned.md](lessons-learned.md) | What this hop does not prove |
| [OVERVIEW.md](../../../v2/base/base-8.0/OVERVIEW.md) | Pack delta |

- The 21-question suite has not been run on base-8.0.
- A falling exam issue count is not accuracy.
