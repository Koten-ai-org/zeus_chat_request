# Migration hops (`base-X` → `base-Y`)

> **Archive** · each folder below is what that hop shipped. A line that says "13 verbs" is the catalog of that hop. It is not the current law. The current test is [CONSTITUION_DESIGN.md](../CONSTITUION_DESIGN.md). Do not rewrite a hop body to match a later law. Catalog candidate is **base-8.0**. `CURRENT.json` stays **base-1**.

**Last reviewed:** 2026-11-21  
**Purpose:** One folder per BASE upgrade. Living design stays in `docs/` root; ship packs stay in `v2/base/base-N/`.

## Naming (normative)

| Item | Pattern |
| --- | --- |
| Hop folder | `docs/migration/base-<FROM>_to_base-<TO>/` |
| Guide | `GUIDE.md` — what stayed / moved / added |
| Lessons | `lessons-learned.md` — recommended |
| **Required for real hops** | `RELEASE_CHECKLIST.md` — ship readiness (from template) |
| Optional | hop `README.md` — status + links |
| Template | [RELEASE_CHECKLIST_TEMPLATE.md](RELEASE_CHECKLIST_TEMPLATE.md) |

**AI playbook** always links hops as:

```text
docs/migration/base-X_to_base-Y/
```

See [BASE_AGENT_PLAYBOOK.md](../BASE_AGENT_PLAYBOOK.md) · root [AGENTS.md](../../AGENTS.md).

## Index of hops

| Jump | Path | Status |
| --- | --- | --- |
| base-1 → base-4 | [base-1_to_base-4/](base-1_to_base-4/) | Candidate pack on disk (`v2/base/base-4/`); pin still base-1 |
| base-4 → base-5 | [base-4_to_base-5/](base-4_to_base-5/) | Wire freeze pack `v2/base/base-5/` (pin still base-1); residual Zeus/Helios updated §10.1 |
| base-5 → base-5.1 | (folder Diff) | Mode overlays snapshot `v2/base/base-5.1/` |
| base-5 → base-5.2 | [base-5_to_base-5.2/](base-5_to_base-5.2/) | Dual gaps + **Zeus 0.6 / Helios 0.6 engine pin lessons** · pack `v2/base/base-5.2/` · [WISH_I_KNEW_DUAL.md](../WISH_I_KNEW_DUAL.md) |
| base-5.2 → base-5.3 | [base-5.2_to_base-5.3/](base-5.2_to_base-5.3/) | Skinny + world-model CORE + verb clarity · pack `v2/base/base-5.3/` · **not a wire break** |
| base-5.3 → base-6 | [base-5.3_to_base-6/](base-5.3_to_base-6/) | Soft `hints.*` inject contract · pack `v2/base/base-6/` · **additive only** · [HINTS.md](../HINTS.md) |
| base-6.1 → base-7.x | [base-6.1_to_base-7.x/](base-6.1_to_base-7.x/) | Working train · Plan, then call + `rail` · pack `v2/base/base-7.x/` · parent base-6.1 · **not** a wire break |
| base-6.1 → base-7.0 | [base-6.1_to_base-7.0/](base-6.1_to_base-7.0/) | Previous numbered ship · Plan, then call + `rail` · `CURRENT.json` stays base-1 |
| base-7.0 → base-7.1 | [base-7.0_to_base-7.1/](base-7.0_to_base-7.1/) | Binding fix · FTS `@step.doc_keys` · find/hybrid/node-vector `@step.node_ids` · [CR-40](https://kotenai.atlassian.net/browse/CR-40) · local Zeus pair base-6.1 + base-7.1 · `CURRENT.json` stays base-1 |
| base-7.1 → base-7.2 | [base-7.1_to_base-7.2/](base-7.1_to_base-7.2/) | Slot rule · copy the list the next slot requires · Zeus embed still base-7.1 · `CURRENT.json` stays base-1 |
| base-7.2 → base-7.3 | [base-7.2_to_base-7.3/](base-7.2_to_base-7.3/) | Walk close · a stored field on the seed does not replace `walk_path` · Zeus embed still base-7.1 · `CURRENT.json` stays base-1 |
| base-7.3 → base-7.4 | [base-7.3_to_base-7.4/](base-7.3_to_base-7.4/) | Call align · plan, tool text, and mode examples describe the same call · Zeus embed still base-7.1 · `CURRENT.json` stays base-1 |
| base-7.4 → base-8.0 | [base-7.4_to_base-8.0/](base-7.4_to_base-8.0/) | Constitution morph · numbered name of base-8-prototype-1 · catalog candidate · parent base-7.4 · Zeus embed still base-7.1 · suite not run · `CURRENT.json` stays base-1 |

## When you finish a new hop

1. Create `docs/migration/base-X_to_base-Y/`.  
2. Copy [RELEASE_CHECKLIST_TEMPLATE.md](RELEASE_CHECKLIST_TEMPLATE.md) → hop `RELEASE_CHECKLIST.md` and work every box.  
3. Add `GUIDE.md` (+ `lessons-learned.md`).  
4. Add a row to this index.  
5. Update [BASE_AGENT_PLAYBOOK.md](../BASE_AGENT_PLAYBOOK.md) jump table + comply cards.  
6. Update [COMPAT.md](../../COMPAT.md) + root [RELEASE_NOTES.md](../../RELEASE_NOTES.md).  
7. Scaffold pack via [CREATE_BASE.md](../CREATE_BASE.md) when Y is real catalogs.

## Not here

| Content | Where |
| --- | --- |
| Current requirements | [BIBLE.md](../BIBLE.md) |
| Future plan | [ROADMAP.md](../ROADMAP.md) |
| Version triples | [COMPAT.md](../../COMPAT.md) |
| Pack JSON/text | `v2/base/base-N/` |
