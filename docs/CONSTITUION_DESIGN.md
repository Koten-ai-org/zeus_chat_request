# Constitution for a chat_request

> **Doc status** · drafted **2026-11-20** · named **2026-11-21** · design page, not a pack · catalog candidate is **base-8.0**, the numbered name of **base-8-prototype-1** (parent **base-7.4**) · the earlier folders **base-8-prototype** and **base-8-prototype-1** stay on disk · `CURRENT.json` stays **base-1** · Zeus embed stays **base-6.1** and **base-7.1** · suite not run
>
> This page is the test a new or edited sentence must pass. It does not edit a pack, flip a pin, or raise the live 8-round ceiling. Placement of a sentence that passes the test is still [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md). Wire order is still [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md). The older speed theory is [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md). The current pack's fights and copies are [CONTRIDICTION_FIGHTS.md](CONTRIDICTION_FIGHTS.md). That file is a snapshot. It is not another law.
>
> Each core idea is stated once. A specific dataset story belongs in a hint or in the fights snapshot, not in a law.

## Goal

Take the question, extract the intent or intents, and navigate that world with the 14 public APIs. The plan answers from evidence, or it stops and says why it cannot.

Accurate means the verb, the bindings, and the parameters match the schema, and every fact came from a tool or from the inject. Fast means the fewest rounds that still do that. The session ceiling is 8 rounds. It is the Zeus limit, not a pile of rounds to spend looking.

## Done

A turn is done when the plan has run, or when it has stopped on a named gap. Rounds left over are not a reason to ask "was I right?"

## The 14 APIs

`describe`, `explain`, `get`, `find`, `set`, `order`, `enrich`, `project`, `traverse`, `pipeline`, `search`, `analyze`, `return`, and `rail`. `rail` runs only when the scope brief names one. `rail` is a catalog name. The engine's public verb list is still the other thirteen. The call is the named-query execute route the rail tool already describes. There is no `/rail` route, and `named_query` is not a fifteenth catalog verb.

Eight of them navigate and shape data, and a normal question starts there. `search` and `find` locate rows. `get` loads a node. `traverse` walks a relation. `pipeline` runs a multi-step plan in one round. `project` and `order` shape and rank a list already in hand. `rail` closes a hard fact the brief already names.

The other six stay in the catalog so a parameter is not invented. `describe` and `explain` are information calls: what exists, and what a query means. `return` is the answer envelope, not a fetch. `set`, `enrich`, and `analyze` work a set already in hand. They are not the way in.

## Two intents, one pipeline

One message can hold more than one intent. Each intent is a chain. Chains that share a world go in one `pipeline` `steps` list. Independent steps run in that same call. There is no array of pipelines. `pipeline` is not itself a step. The step list caps at 8.

A shared value is probed once, under the probe suggestion below. Zero stops every chain that needed it. Rows are followed by one pipeline with those chains bound to that value. A second pipeline call is only for a later intent that cannot be written until an earlier chain's rows have been read. The fast path does not do that read.

## What this page is

A turn arrives as three parts. They are not the same object.

1. The hashed catalog: messages, verb schemas, and the terminate object. Zeus stamps that hash. An author does not invent one.
2. The inject, outside the hash: the scope brief, the mini-schema, the walk paths, company rules, and hints.
3. The question.

The catalog teaches how Zeus is shaped, how to move, and how to terminate. The inject is one dataset. It is not copied into the catalog. File anatomy, the hash policy, and which key owns which field stay in [CHAT_REQUEST.md](CHAT_REQUEST.md) and [BIBLE.md](BIBLE.md). This page does not repeat them. The read order below is these three parts, then Layer A.

This page answers one question: does this sentence help the same question become the same plan?

Every law below has three lines. **Statement** is the words a later edit must still match. **Why** is the failure it stops. **Goal** is the piece of the goal above that it serves. An exception is allowed only when it is an engine fact. An exception for one pair of verbs means the access law is incomplete, or the sentence is a hint for one dataset.

## Where a sentence goes after it passes

[PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) says which surface. [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) says byte order. A recipe in [BEST_PRACTICES.md](BEST_PRACTICES.md) or a traffic card in [OPTIMIZATION.md](OPTIMIZATION.md) is not a second law. [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md) is the older speed theory. [BIBLE.md](BIBLE.md) is the ownership matrix for the base-4 and base-5 wire. A hop under [migration/](migration/README.md) is what that hop shipped. It is not the current law.

## Prevention

These apply to the catalog and to any brief appended on the same turn.

**No fight.** A new sentence that names a different verb, list, or parameter than a statement already on this page does not go in. Edit the one statement until there is a single instruction.

**No copy.** A statement is said once. A second copy on another tool does not go in. The tool schema still lists its fields. The essay does not repeat.

## The suggestion

The fast path and the probe are suggestions made inside `query_decomposition`, after the intent is extracted. They are not a mode assigned before the question is read. The decomposition records which suggestion it is taking, and why. Analytics is not a live choice.

An `ex:` row is a spelling sample. It is not proof a value is stored, and a value missing from that row is not proof it is absent. That is why a probe asks the store. A pipeline sent first that returns zero has spent a round and still needs another request. A zero from that pipeline is also easy to blame on the index. The probe separates "the value is not stored" from "the call was wrong."

Catalog mode (`analytics`, `code`, `fraud`, and the rest) sets tone: noise, hop flavor, how the summary sounds. It does not pick the suggestion. A fraud question can still be a fast path. The older names `fast_pass` and `scout` are these two suggestions. `thorough` is a richer fast path, not a third suggestion. A question whose plan is already writable is the fast path. The older class name is `known_goal`. A question whose evidence size is unknown, or whose value may not be stored, is the probe. The older class name is `open_ended`. Out of this dataset is a gap. It is not a third suggestion.

### Fast path

**Statement.** When decomposition extracted a lot of the question and the mini-schema fills or finds most of the plan, suggest the fast path. Fill one pipeline from that intent and run it. Do not probe. Do not read the rows to decide whether the call was right.

**Why.** This suggestion has no second pass. Confidence has to be in the extraction before the call. Spending the remaining rounds on a finished pipeline turns a known plan into a search.

**Goal.** A plan the prompt can already fill becomes one pipeline, run once.

### Probe

**Statement.** When decomposition finds the question vague, or finds that a basic value may not be stored, suggest one probe of that value before any pipeline. Zero rows: stop and name the gap. Some rows: the next round is the fast path.

**Why.** The pipeline is the expensive call. Building it on a value the store does not have spends a round and returns nothing to inspect. The probe is the cheap question. It is not the answer.

**Goal.** One probe decides whether a pipeline is worth building.

### Analytics

**Statement.** Analytics is the name reserved for a future Helios use of the Zeus API. It has no budget here. A question today is a fast path or a probe.

**Why.** A long clock written as a live law lets an ordinary question spend past the ceiling. Helios is not that question yet.

**Goal.** The name stays reserved until a Helios job states its own budget.

A hint may name a usual suggestion for one scope. It may not change the access rule.

## base-8.x

base-8.x is this page applied to base-7.4. It is a new folder. It keeps a 7.4 sentence that already matches a statement. It does not start from an empty prompt. A sentence that serves no statement comes out in that same edit.

The numbered pack is [v2/base/base-8.0](../v2/base/base-8.0/). It is the same cut as [v2/base/base-8-prototype-1](../v2/base/base-8-prototype-1/), named base-8.0. Parent is base-7.4. The earlier folder [v2/base/base-8-prototype](../v2/base/base-8-prototype/) stays on disk. It is not this page. base-8.0 is the catalog candidate. `CURRENT.json` stays base-1. The Zeus embed stays base-6.1 and base-7.1. The suite has not been run.

A miss against ground truth has one cause. SQL++ on the small set is the ground truth. A shorter page from `limit` and `offset` is not by itself a miss. A SQL++ count on the order of 200 and a Zeus result of zero is a miss.

| Cause | What it looks like |
| --- | --- |
| LLM | The intent was read wrong, or a matching hint was ignored. |
| Pipeline | The plan looks legal and asks for the wrong list, the wrong field, or a parameter the schema does not have. |
| Zeus API | The call matched the ground-truth shape and the server returned the wrong set. |

A pipeline cause is a catalog bug. A Zeus API cause is an engine bug. The catalog is not patched to hide either one.

## The seven laws

### 1. The world is the inject

**Statement.** Stay inside the scope brief, the mini-schema, and the walk paths that arrived with this turn. Entities, attributes, edges, and concepts come from that inject. A field that is absent is not a fact. The catalog teaches how to read the inject. It does not name a tenant's entities.

**Why.** A tenant named in the catalog is inherited by every other tenant, and a missing type gets invented.

**Goal.** The plan is for this dataset, and the same catalog loads for every dataset.

### 2. One access rule

**Statement.** Copy the list the next slot requires.

- A stored equality is `find`. Soft language is `search`, one clause, the user's words unchanged.
- A related type on a listed walk path is `traverse` `walk_path`, and `from.src_keys` is `@step.doc_keys`.
- Node-id slots (`get`, hop, bfs, path, subgraph, `narrow_to`, `analyze`, and `set` with `id_kind` `node_ids`) take `@step.node_ids`.
- `project`, `order`, and `enrich` accept either list.
- `@step.ids` is node ids only.
- FTS search leaves `node_ids` empty, so a node-id slot cannot follow it until a step resolves those keys.
- `set` requires `id_kind` (`node_ids` or `doc_keys`). Every input array is that one kind.

**Why.** A special case per pair of APIs is an exception list. The model follows the last sentence it read, so two sentences for the same slot produce an empty step.

**Goal.** The same question picks the same verb and the same binding, and the call succeeds on the first try.

### 3. One drill-down is one pipeline

**Statement.** A drill-down is one `pipeline`, and that pipeline counts as one round. Shrink a set you already hold. Stop when the goal's inputs are in hand. The rounds under the ceiling are repair around that pipeline, not one hop per call, and not a second look at a finished fast path.

**Why.** A soft phrase, a filter, and a card are three steps and one plan. Issued as three rounds, the model re-plans between them.

**Goal.** A fast path finishes in one pipeline. A probe spends one round, then either one pipeline or a stop.

### 4. The schema is the parameter list

**Statement.** Every field the engine requires is in the verb schema, with its type and legal values. A field the schema does not have is not taught in prose, in an example, or in a hint. Search keeps three examples, full-text, hybrid plus `where`, and spatial, because that verb is the one the model invents inputs for. A skinny verb set for one channel is a custom catalog, not a deletion from the base.

**Why.** The model fills a parameter it has seen described. `project` has no `limit`. `order` does. `traverse` takes `via` (one string) and `max_nodes`. `set` without `id_kind` is an error.

**Goal.** The call is one the 14 APIs accept.

### 5. Universal goes in the catalog. One dataset goes in a hint

**Statement.** A sentence true on the first turn for every tenant is core, next to the schema. A sentence true for one scope, channel, arm, or recent failure is `hints.*` or a line in that scope's brief. Hints sit after hard rules. They never replace the mini-schema, the jailbreak law, or the required four terminate fields. A hint that becomes true for every tenant is promoted, and the hint is deleted.

**Why.** One scope's hot path in the catalog is a paragraph every other tenant pays for. A universal rule left only in a hint is invisible on the turns that send no hint. `hints.*` is still not injected on the live client.

**Goal.** The catalog stays the short universal plan. A dataset adds its patterns without changing anyone else's plan.

### 6. Terminate from evidence

**Statement.** The turn ends as one Layer A object.

- `query_decomposition` is the intent and the entity, plus the suggestion above and why.
- `decomposition` is the data plan: targets, predicates, and output, grounded in the mini-schema.
- `summary` and `confidence` (`high`, `med`, or `low`) are the user-facing close.
- Those four are required.
- A gap is `wish_i_knew` (at most three: `rules`, `message`, `schema`, `data`, `tool`) or `data_gaps` (schema, data, or index). An answerable question sends `[]`. Gaps stay out of `summary`.
- A `display` field is a mini-schema fact. Pick another verb, or name the gap once.
- Facts in `summary` come from tool results or the brief.

On a fast path, the pipeline may carry the decomposition and the summary shape in the same call that asks for the rows. The facts are filled from the rows that return. On a probe, write the facts after the probe returns. Do not invent rows to make the object look complete.

**Why.** The intent and the data plan are different objects. A gap is for the operator. A summary that states a fact the tools did not return is a guess.

**Goal.** The same question produces the same plan object. The user sees only evidence. A real gap is visible to the operator.

### 7. The same question, schema, and brief pick the same plan

**Statement.** The same question, the same mini-schema, and the same brief lead decomposition to the same suggestion, the same verb class, and the same bindings. Catalog mode may change the tone. A hint may bias the first move inside the suggestion. Neither may change the access rule or the required four. Row ids may change when the store changes. The shape of the plan does not.

**Why.** The question alone is not the input. Two schemas can make two legal plans for one sentence. The unit of a regression is a changed verb, a changed binding, or a parameter the schema does not have.

**Goal.** An edit is judged by the plan a known question still makes, and by the statement that plan serves. A smaller file, or fewer open checks, is not that judgment.

## Read order

The model reads the hashed catalog, then the tools, then the inject, then the question. It emits Layer A after the evidence.

| Order | Who owns it | What the model gets | Which law |
| --- | --- | --- | --- |
| 1 | Catalog | Overlay. Plan. Access rule. Evidence. Hint hook. Ceiling. Terminate table. Catalog-mode tone. | 1, 2, 3, 5, 6, and the suggestion |
| 2 | Catalog | Verb schemas, including search's three examples. | 4 |
| 3 | Inject | Scope brief, mini-schema, walk paths, company rules, `hints.*`. | 1 and 5 |
| 4 | User | The question. | 6 and 7 |
| 5 | Model, after tools | Layer A. | 6 |

## Review a sentence against this page

```text
Sentence:
Statement it serves: 1 | 2 | 3 | 4 | 5 | 6 | 7 | none
Suggestion it assumes: fast path | probe | analytics | all
True for every tenant on turn 1?  yes → catalog.  no → hint or brief.
Schema agrees?  yes | no (then fix the sentence, or fix the brief)
Fights a statement already on this page?  yes → do not add it.
Copies a statement already said once?  yes → do not add it.
Names a tenant, a city, or a sample row?  yes → hint or fights snapshot, not this page.
If we delete it, which known question changes verb or binding?
```

A sentence that fails this review does not go into a base-8.0 versus base-8.1 run.

The fights and the repeated copies in the current pack live in [CONTRIDICTION_FIGHTS.md](CONTRIDICTION_FIGHTS.md). A fixed fight is deleted from that file. It is not added here, and it is not pasted onto another tool.

## How to test this page

Score every base with the same checks, then read the progression before any base-8.0 versus base-8.1 suite.

```text
python3 scripts/constitution_exam.py
```

That writes [../v2/base/constitution_exam.html](../v2/base/constitution_exam.html). The page embeds the rows. Open the file. It does not need a web server. Do not hand-edit it. A new base is scored by running the command again.

The page shows what each base still breaks, what the next base fixed, which misses come back after a shrink, and which constitution statements are already enough. Read a drop in that count with law 7. The suite remains the ground-truth check in the base-8.x section, and only after this gate. The reading of that page is [LESSONS_LEARNED.md](LESSONS_LEARNED.md). Lessons stay there. They are not copied onto this page.

The guess for the first suite sits in [../v2/base/hypothesis_base-8-prototype.html](../v2/base/hypothesis_base-8-prototype.html). It is a prebuild of the comparison report: left base-7.2, right base-8-prototype-1. The shape is [../baseline/hypothesis/report_template.html](../baseline/hypothesis/report_template.html). The After column stays empty until that run exists. A later prototype copies the template. It does not rewrite the guess.
