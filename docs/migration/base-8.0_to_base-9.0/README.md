# base-8.0 → base-9.0

| | |
| --- | --- |
| **From** | [`v2/base/base-8.0/`](../../../v2/base/base-8.0/) |
| **To** | [`v2/base/base-9.0/`](../../../v2/base/base-9.0/) |
| **Bytes** | [`v2/base/base-9-prototype-7/`](../../../v2/base/base-9-prototype-7/) |
| **Wire** | Additive. Not a wire break. |
| **Date** | 2026-11-22 |

base-8.0 stays the v1 constitution morph. base-9.0 is a new folder. It is the numbered name of the constitution v2 cut that was `base-9-prototype-7`. The catalog was released on 2026-11-22. That release is not the `CURRENT.json` pin. The earlier folders `base-9-prototype-1` through `base-9-prototype-7` stay.

`CURRENT.json` stays **base-1**. The Zeus embed stays **base-6.1** and **base-7.1**. v1 still gates base-8.0. This pack follows [CONSTITUION_DESIGN_v2.md](../../CONSTITUION_DESIGN_v2.md).

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-9.0/min --base 9.0 --out v2/base/base-9.0 --no-set-base-id
python3 scripts/verify_base_pack.py --base 9.0
python3 scripts/diff_modes.py --base 9.0 --fail-if-clone
```

Do not run `assemble_mode_prompts.py`. Do not invent a contract hash.

## Related

| Doc | Role |
| --- | --- |
| [GUIDE.md](GUIDE.md) | What the cut changed |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Gate for this hop |
| [lessons-learned.md](lessons-learned.md) | What this hop does not prove |
| [OVERVIEW.md](../../../v2/base/base-9.0/OVERVIEW.md) | Pack delta |

- The 2026-11-22 full suite measured these bytes as base-9-prototype-7 against base-8.0: 16/22 versus 18/22, better 2, worse 0, net +2, three questions not run. That lock predates the Paris split. The current lock has not been run.
- A falling exam issue count is not accuracy. The v1 exam is open 0 on base-9.0. That page is not the v2 gate.
