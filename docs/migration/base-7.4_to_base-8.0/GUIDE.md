# GUIDE — base-7.4 → base-8.0

**Train:** constitution morph, numbered as base-8.0 · **Jira:** none · **Breaking wire:** No · **Date:** 2026-11-21

## What shipped

The working folder `v2/base/base-8-prototype-1` is now `v2/base/base-8.0`. The system text and the verb schemas are the same bytes as that prototype. The lineage id is `base-8.0`. The parent is `base-7.4`.

- The plan states the access rule once. `narrow_to` takes node ids only, so that sentence is not copied onto the pipeline tool.
- `query_decomposition` records fast path when the question and the mini-schema already fill the plan. It records one probe when the question is vague, when the evidence size is unknown, or when a basic value may not be stored.
- Two intents that share a world are two chains in one pipeline. A shared value is probed once. Zero stops every chain that needed it. The call ceiling stays 8.
- Ranked lists put `limit` on `order`. `project` has no `limit`.
- On a fast path the terminating pipeline may carry the decomposition and the summary shape. The facts come from the rows that return.

Nothing was renamed on the wire. Each mode keeps the contract hash copied from its base-7.4 file. `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp.

## What did not ship

- `CURRENT.json` stays base-1.
- The Zeus embed stays base-6.1 and base-7.1. The served pin in that tree stays base-7.1.
- The live scope brief still says find and hybrid results must not go in `src_keys`.
- Zeus still does not execute `rail`.
- No 21-question suite has been run. Open exam issues at 0 is the gate, not accuracy.

The earlier folder `base-8-prototype` stays. It is the first morph, not this pack. `base-8-prototype-1` stays so the Beelink image that embedded that name can be compared with this folder.
