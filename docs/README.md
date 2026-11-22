# Documentation

> **Doc status** · last reviewed **2026-11-21** · `CURRENT.json` **base-1** · released catalog **base-8.0** (2026-11-21) (numbered name of **base-8-prototype-1**, parent **base-7.4**) · earlier folders **base-8-prototype** and **base-8-prototype-1** stay · Zeus 5.5TH built-ins still **base-6.1** and **base-7.1** (served pin **base-7.1**, local tree) · suite not run · version matrix: [COMPAT.md](../COMPAT.md)


Educational and design docs for **zeus_chat_request**.  
Catalog **JSON packs** live under `v2/base/base-N/` (not here). Production pin is still **base-1** until promote.

## The test

[CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md) is the test a sentence about how to call Zeus must pass. Each other file owns one job. A recipe, a traffic card, a wire diagram, or a hop archive is not a second law.

| Doc | Job |
| --- | --- |
| [CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md) | The test for base-8.0. Goal, suggestion, seven laws. |
| [CONSTITUION_DESIGN_v2.md](CONSTITUION_DESIGN_v2.md) | Closed spec. Common rail, exact call, vague chain. Not the base-8.0 gate. Empty-seed cut is base-9-prototype-6, parent base-9-prototype-5. Not the pin. |
| [QUERY_DECOMPOSITION.md](QUERY_DECOMPOSITION.md) | The first reading of the submitted string. Intent, entity, shape, suggestion, and why, written once beside the queries. |
| [CHAT_REQUEST.md](CHAT_REQUEST.md) | File anatomy and the hash. |
| [BIBLE.md](BIBLE.md) | Ownership matrix for the base-4 and base-5 wire. |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Byte order. |
| [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) | Which surface, after the sentence passes. |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Control plane and named rules. |
| [MODE.md](MODE.md) | Engine mode hooks. Catalog mode is tone, not the suggestion. |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | Day-one recipes. They follow the constitution. |
| [OPTIMIZATION.md](OPTIMIZATION.md) | After-traffic rails. The catalog name is `rail`. |
| [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md) | Older speed theory. `fast_pass` / `scout` / `thorough` are retired names. |
| [HINTS.md](HINTS.md) | Hash-excluded soft inject. Not live yet. |
| [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score and hooks. Hints cannot replace it. |
| [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) | The two gap channels. |
| [LESSONS_LEARNED.md](LESSONS_LEARNED.md) | Reading of the exam. Not a law. |
| [CONTRIDICTION_FIGHTS.md](CONTRIDICTION_FIGHTS.md) | Snapshot of the current pack's fights. Not a law. |
| [migration/](migration/README.md) | Hop archives. What that hop shipped. |

## Layout (where things go)

| Location | Put here | Do **not** put here |
| --- | --- | --- |
| **`docs/`** | The constitution, then one job per file: anatomy, wire, placement, recipes, archives | Per-mode catalog JSON. A second call law. |
| **`docs/migration/base-X_to_base-Y/`** | **Hop archives** (GUIDE + lessons) for each upgrade | Living design that still evolves |
| **`docs/CREATE_BASE.md`** | Process to cut a new `base-N` pack | — |
| **`v2/base/base-N/`** | **Ship pack:** `min/`, `text/`, `MANIFEST.json`, `response_output_*.json`, short `README.md` / `OVERVIEW.md` | Long design essays (those stay in `docs/`) |
| **`samples/`** | Generic terminate samples (not pack-specific) | BASE diet docs |
| **Root `AGENTS.md`** | Short AI entry | Full checklists (those live in the playbook) |

```text
docs/
  CONSTITUION_DESIGN.md        ← the test (filename spells CONSTITUION)
  BASE_AGENT_PLAYBOOK.md       ← AI: comply with base-X / upgrade X→Y
  BIBLE.md · PROMPT_* · RULES_* · ROADMAP · …
  CREATE_BASE.md
  migration/
    README.md
    base-1_to_base-4/          ← GUIDE.md + lessons
    base-4_to_base-5/          ← archive; index is migration/README.md

v2/base/base-N/                ← pack only (min, text, MANIFEST, Layer A schemas)
AGENTS.md                      ← repo root: agent start here
COMPAT.md                      ← Zeus × BASE × zeus_client
```

## Start here

| Doc | Topic |
| --- | --- |
| [CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md) | **The test** — goal, suggestion, seven laws |
| [../AGENTS.md](../AGENTS.md) | **AI entry** — hard rules + where to go |
| [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) | Comply with base-X · upgrade X→Y (checklists) |
| [CHAT_REQUEST.md](CHAT_REQUEST.md) | File anatomy, hash, contract stamp |
| [BIBLE.md](BIBLE.md) | Ownership matrix for the base-4 / base-5 wire (set/unset/change) |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Byte order |
| [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) | Which surface, after the sentence passes |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings bag · rule merge · Client policy · security |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules + `output_request` (type + description) |
| [ROADMAP.md](ROADMAP.md) | Living plan. Released catalog is base-8.0 (2026-11-21). |
| [CREATE_BASE.md](CREATE_BASE.md) | Scaffold a new `base-N` pack. Exam before a suite. |
| [migration/README.md](migration/README.md) | All BASE upgrade hops |
| [migration/RELEASE_CHECKLIST_TEMPLATE.md](migration/RELEASE_CHECKLIST_TEMPLATE.md) | **BASE bump release checklist** (copy per hop) |
| [migration/base-4_to_base-5/RELEASE_CHECKLIST.md](migration/base-4_to_base-5/RELEASE_CHECKLIST.md) | Filled checklist for base-5 |
| [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score + named rules + hooks |
| [LESSONS_LEARNED.md](LESSONS_LEARNED.md) | Reading of the constitution exam. Not a law. |
| [CONTRIDICTION_FIGHTS.md](CONTRIDICTION_FIGHTS.md) | Snapshot of fights in the candidate pack. Not a law. |
| [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) | Middleman multi-round |
| [INSPECTOR.md](INSPECTOR.md) | One `index.html` for multi-BASE |
| [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | Helios emit requests (cost-aware) |
| [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) | **zeus_client** backlog (base-5 floor → base-6+) |
| [MODE.md](MODE.md) | **Modes** — engine hooks vs catalog tone. Tone is not the suggestion. |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | **Day-one recipes.** Bind the list the next slot requires. `project` has no `limit`. |
| [OPTIMIZATION.md](OPTIMIZATION.md) | **After traffic.** The catalog name is `rail`. The executor is still the named-query route. |
| [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md) | **Older speed theory.** `fast_pass` = fast path, `scout` = probe, `thorough` = a richer fast path. |
| [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) | The two gap channels. Law 6 already names them. |
| [../work/RECREATE_MODE.md](../work/RECREATE_MODE.md) | **Plan** — restore mode overlays into system prompt (`messages[].content`) |
| [../images/assembled_prompt.svg](../images/assembled_prompt.svg) | Assembled prompt diagram |
| [../images/zeus-pachinko-shaping.svg](../images/zeus-pachinko-shaping.svg) | Older drawing of the funnel. The catalog name is `rail`. [OPTIMIZATION.md](OPTIMIZATION.md) |
| [../images/opt-staples.svg](../images/opt-staples.svg) | Older drawing. Names retired. See the constitution. |
| [../images/opt-order-vs-waste.svg](../images/opt-order-vs-waste.svg) | Shrink bag → ORDER vs List fan-out |
| [../images/opt-question-class.svg](../images/opt-question-class.svg) | Older drawing. `known_goal` = fast path. `open_ended` = probe. Out of corpus = a gap. |
| [../images/opt-execution-shapes.svg](../images/opt-execution-shapes.svg) | Older drawing. A probe is one look, not a third product. |
| [../images/opt-bind-vs-list.svg](../images/opt-bind-vs-list.svg) | Bind the list the next slot requires. `@step.ids` is node ids only. |
| [../images/opt-pick-and-clocks.svg](../images/opt-pick-and-clocks.svg) | Older drawing. The session ceiling is 8 rounds. |
| [../images/opt-retrieve-shape.svg](../images/opt-retrieve-shape.svg) | Older drawing. The catalog has 14 verbs. The engine public set is still 13. |

## Migration hops

The index is [migration/README.md](migration/README.md). Each folder is an archive of what that hop shipped. It is not the current law.

## Packs on disk

| Path | Topic |
| --- | --- |
| [../v2/base/base-8.0/](../v2/base/base-8.0/) | Released catalog, 2026-11-21. Numbered name of base-8-prototype-1. Parent base-7.4. Not the pin. |
| [../v2/base/base-7.4/](../v2/base/base-7.4/) | Call-align parent of base-8.0. |
| [../v2/base/base-8-prototype-1/](../v2/base/base-8-prototype-1/) | Working folder this candidate was named from. Stays on disk. |
| [../v2/base/base-8-prototype/](../v2/base/base-8-prototype/) | Earlier constitution morph. Not the candidate. Not the pin. |
| [../v2/base/base-4/](../v2/base/base-4/) | Wire-era pack the Bible describes. |

## Version matrix

| Doc | Role |
| --- | --- |
| [../COMPAT.md](../COMPAT.md) | **SoT** — Zeus engine × chat_request BASE × zeus_client |

## Root (not under docs/)

| Doc | Why at root |
| --- | --- |
| [../README.md](../README.md) | Project entry + diagram |
| [../RELEASE_NOTES.md](../RELEASE_NOTES.md) | Releases + breaking changes |
| [../COMPAT.md](../COMPAT.md) | Version matrix (three products) |
