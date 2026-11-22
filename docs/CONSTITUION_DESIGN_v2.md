# Constitution v2

> **Doc status** · drafted **2026-11-21** · closed **2026-11-21** · standalone successor of [CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md) · design page, not a pack · v1 still gates **base-8.0** · the empty-seed cut is [base-9-prototype-6](../v2/base/base-9-prototype-6/), parent [base-9-prototype-5](../v2/base/base-9-prototype-5/) · `CURRENT.json` stays **base-1** · Zeus embed stays **base-6.1** and **base-7.1** · no suite
>
> A person cutting the next chat_request reads this page and does not need v1 open. v1 remains the test the already-cut base-8.0 pack was written against. This page is the spec for that next cut. Wall-clock time is measured on the pack, not edited again on this page.
>
> Amended **2026-11-21**. `query_decomposition` rides the call that creates the queries. That amendment is cut as [base-9-prototype-2](../v2/base/base-9-prototype-2/). [base-9-prototype-1](../v2/base/base-9-prototype-1/) still leaves it on the answer call. The reading is [QUERY_DECOMPOSITION.md](QUERY_DECOMPOSITION.md).
>
> Amended **2026-11-22**. A list of the child in each parent fills `relation` with that parent. That amendment is cut as [base-9-prototype-5](../v2/base/base-9-prototype-5/). [base-9-prototype-4](../v2/base/base-9-prototype-4/) still walks only a `relation` that is already filled.
>
> Amended **2026-11-22**. A parent `find` that returns nothing is not a seed. Its `doc_keys` stay off `src_keys`. That amendment is cut as [base-9-prototype-6](../v2/base/base-9-prototype-6/). [base-9-prototype-5](../v2/base/base-9-prototype-5/) still copies that empty list into `from`.
>
> The API table is the reference for `narrow_to`, the published list, and the next slot. It was read from the handlers on **2026-11-21**. `pipeline.go` and [Zeus `pipeline.md` §4.2](../../Zeus/docs/API/V2/pipeline.md) still describe every `narrow_to` as a post-filter. Hybrid, vector, find, get, and walk have moved past that. This page follows the handlers.

## The platform

A turn is four pieces. The 14 APIs are one of them.

| Piece | What it is |
| --- | --- |
| chat_request | How to read this world and which move to make. Hashed catalog, then the inject, then the question. |
| 14 APIs | The moves. `find`, `search`, `traverse`, `get`, `set`, `order`, `enrich`, `project`, `pipeline`, `analyze`, `describe`, `explain`, `return`, and `rail`. |
| hints | Patterns from past chat_requests for this scope: a common query shape, a user habit. They bias the first move. `hints.*` is not injected on the live client yet. |
| rails | An operator-pinned query for a question that has become common. One call returns the end state. It does not walk close, then closer, then closer. |

The end state of a data question is a list of real records. A travel ask ends as real hotels. A rail returns that list because the operator has already pinned the path. A narrowing chain builds that list when no rail is named.

## Goal

Take the question, see which shape it is, and use the tool that shape has.

A common question with a matching hint or a named rail is one fast call. An exact question is one `find` or one `search`. A vague question with two or more soft facets, and no rail, is one narrowing pipeline. The plan answers from evidence, or it stops on one of the three outcomes below.

Each `query_text` carries one facet of the user's words. The embedding does the approximation. The model does not add a synonym essay, and it does not fold two facets into one clause.

The same question, the same mini-schema, the same brief, and the same hints pick the same shape. Scores may move. The shape does not. The session ceiling is 8 rounds.

## Three shapes

| Shape | How you know | The tool | What you do not do |
| --- | --- | --- | --- |
| Common | A hint matches this ask, or the scope brief names a rail for it. | That hint's first move, or `rail` with the binds already in hand. | Do not build a `narrow_to` chain for a path the operator already pinned. |
| Exact | One stored equality, or one soft facet. | `find` for the equality. One `search` for the one facet. | Do not split one facet into several searches. |
| Vague | Two or more soft facets, and no rail is named. | One pipeline. First lens is the widest legal cut. Each later hybrid or node-vector search sets `narrow_to` to the previous `node_ids`. | Do not put every facet in one `query_text`. Do not spend a round per lens. |

Catalog mode sets tone. It does not pick the shape. Which suggestion runs the shape is the next section.

## Three outcomes

The world was handed over with the question. The plan probes or builds the call. Exactly one of these is true.

| Outcome | What is true | What the turn does |
| --- | --- | --- |
| Rows | The type is in the inject and the call returned records. | `summary` states those records. `wish_i_knew` is `[]`. |
| Zero rows | The type is in the inject, the call was legal, and the store returned nothing. | This is an empty answer. Say so. Stop. Do not start another chain to force rows. This is not a missing dataset. |
| `wish_i_knew` | The exception. The plan could not land on rows or on a clean zero. | At most three items. They stay out of `summary`. |

`wish_i_knew` has two causes that look alike and are not.

- The type or field is not in this world. `kind` is `schema`. The operator needs another dataset, or a field this scope does not have. `data_gaps` with `kind: schema` sits beside it so acquisition can see the hole.
- The world had a path and the plan did not use it. `kind` is `tool`. The question string and the query composition disagree. That is a composition miss. Repair it inside the ceiling when a round remains. Do not ask for a new dataset.

Two other kinds stay available. `rules` means a company rule the plan needed was absent. `message` means the user left out a value the plan cannot invent. `data` on `wish_i_knew` is for a value the turn lacked. A clean zero does not use it. A clean zero may set `data_gaps` to `kind: data` when the operator should collect more of a type that already exists.

An answerable question sends `wish_i_knew: []`. A `display` field is a mini-schema fact. Pick another verb, or name the gap once. A comparison the mini-schema cannot store, such as a maximum price, is not a soft facet. When the brief does not name a rail for it, the turn stops on `wish_i_knew`. It does not invent a search for the number.

## The suggestion

The fast path and the probe are suggestions recorded in `query_decomposition` when the shape is chosen. They are not a mode assigned before the question is read. The older names `fast_pass` and `scout` are these two. `thorough` is a richer fast path, not a third suggestion.

`query_decomposition` is how the submitted string was understood. It is the first step of the turn: the model writes that reading on the call that creates the queries, and a later reader sees the question, the reading, and the queries together. It is written once on the one `find`, the one `search`, the `pipeline`, the probe, or the `rail`.

The object is a row of short values. `intent` and `entity` are the core. `attribute`, `geo`, `audience`, `theme`, `occasion`, `price`, `dates`, `availability`, `rating`, `relation`, `parts`, and `other` are filled when the string signals them, and left empty when it does not. `shape`, `suggestion`, and `why` sit on that same row. A paragraph in one string is not a reading. A later store groups those values, orders them, puts them in a vector index, and searches them. The queries stored beside the row say which path that cluster took. The field table, the call each slot builds, and the loose join are [QUERY_DECOMPOSITION.md](QUERY_DECOMPOSITION.md).

The saved map is the gate. A stored spelling on an `entity`, `enum`, or active `boolean_map` row becomes `find`. A soft phrase becomes one `search` per phrase. A list of the child in each parent fills `relation` with that parent. It does not fill `attribute`. The back-walk under that parent is the chain. That filled `relation` is `walk_path` on the inverse. `project` of the field is the card. It is not the close. A null on that field in the first page does not replace the walk, and it does not become `wish_i_knew`. A parent `find` that returns nothing is not a seed. Its `doc_keys` stay off `src_keys`. An empty list is not a selector. The inverse hop starts on the parent. An empty parent has no key and no `where`, so that hop waits. A `scalar_ent` child with no spelling in the question is a `find` of the child. `project` of the parent field is the card. The parent walk waits until that `find` returns keys. `shape` is common, exact, or vague. It is not `group_by`. `Best` is an `order` after the bag exists. `Count` is `return` `count`. `price`, `dates`, `availability`, and a rating threshold are decision metrics: a comparison the row cannot store is a named rail when the brief has one, and `wish_i_knew` when it does not. A `display` row and a `skip` row do not become a `where`. The object names the reading. It does not copy the tool JSON, and it does not summarize the rows.

### Fast path

**Statement.** The shape is writable, and every equality value is known to be stored. Fill one pipeline from that shape and run it. Write every lens before any row comes back. Do not read a bag and then decide the next lens.

**Why.** A round per lens re-plans between hops. Reading the first page and stopping treats the wide cut as the end state.

**Goal.** The vague shape is one JSON. The exact shape is one call. The common shape is one rail.

### Probe

**Statement.** An `ex:` row is a spelling sample. It is not proof a value is stored, and a value missing from that row is not proof it is absent. When a basic value may not be stored, one probe of that value comes before any pipeline. Zero rows of that spelling, on the field that stores it, stop and name the gap. Some rows: the next round is the fast path, and the pipeline binds that value. An empty parent type does not stop a `scalar_ent` child. The spelling in the question is then the `where` on the child field that points at that parent. Zero rows of that child `where` stop and name the gap. Some of those rows make the next step the `walk_path` that chain lists. `wish_i_knew` for the empty parent does not cancel that `where`. An `entity_fk` child still stores a document key. An empty parent there is the gap, because there is no key to copy. A parent `find` that returns nothing is not a seed. Its `doc_keys` stay off `src_keys`. An empty list is not a selector. `from` needs `doc_key`, a non-empty `src_keys`, or a `where`. That rejection stays on the call. It does not become `wish_i_knew`. The inverse hop starts on the parent. An empty parent has no key and no `where`, so that hop cannot start. A `scalar_ent` child with no spelling in the question is a `find` of the child. `project` of the parent field is the card. The parent walk waits until that parent `find` returns keys.

**Why.** A pipeline built on a value the store does not have spends a round and returns nothing to inspect. A zero from that pipeline is easy to blame on the index. The probe separates "the value is not stored" from "the call was wrong." A parent with no documents is a gap on that type. A `scalar_ent` child still stores the spelling the question used. Stopping on the parent drops the walk the relation already named. Copying that empty `doc_keys` list into `src_keys` fails the step before the hop. The child rows still sit on the `scalar_ent` field.

**Goal.** One probe decides whether the funnel is worth building.

### Analytics

**Statement.** Analytics is the name reserved for a future Helios use of the Zeus API. It has no budget here. A question today is a fast path or a probe. The narrowing chain is the plan for those two suggestions. It is not a Helios budget. Grouping stored `query_decomposition` rows is a query on readings already written. It is not a longer turn.

**Why.** A long clock written as a live law lets an ordinary question spend past the ceiling. Helios is not that question yet. The facets exist so that later query is possible. They do not spend the ceiling on this turn.

**Goal.** The name stays reserved until a Helios job states its own budget.

### The second call

**Statement.** The planning call emits the filled skeleton and `query_decomposition`. The answer call is the next round. It fills `summary`, `decomposition`, and `confidence` from the rows. A rail whose binds are those ids is a further call, and only when the brief names the rail. The fast path does not use another call to invent the next lens.

**Why.** A price rail on the hotels that survived cannot be bound until those ids exist. The beach facet and the fun facet can be written up front, so they share the pipeline. Writing the summary on the planning call spends the clock before any row exists. How the question was understood is already known when the queries are written, so that reading rides the same call.

**Goal.** One short plan, with the reading beside the queries. One short answer after the rows. A further call only for a named rail that needs those ids.

## Done

The turn is done when the end state is in hand, or when it has stopped on zero rows, or when it has stopped on a named gap. A wide first page is not the end state. Rounds left over are not a reason to ask whether the call was right.

## Two operators

`narrow_to` is an input. On a read verb it means "run this lens inside these node ids." It is not the signal to keep going.

The keep-going signal is a binding. A step that publishes `node_ids` or `doc_keys` is an intermediate. The next step copies the list its slot requires.

| Signal | What it does |
| --- | --- |
| `narrow_to` | Restricts `find`, `search`, `traverse`, `get`, or `analyze` to node ids. |
| `@step.node_ids` / `@step.doc_keys` | The list the next slot copies. This is what continues the chain. |
| `abort_if_empty` | Mid-chain stop. This lens was required and it returned nothing. On a vague question that empty lens is a zero-row outcome for the chain. |
| Planning call | The skeleton, or the one query, plus `query_decomposition`. `summary`, `decomposition`, and `confidence` wait for the rows. |
| `return` | Turn stop. Not a step. |
| `rail` | Turn stop for a common or hard fact. One call. Not a step inside the pipeline. |

`previous_ids` is shorthand. The pipeline rewrites it to `narrow_to: "@<previous>.ids"`. `.ids` means `node_ids` only. After an FTS step that list is empty.

`set` is the boolean operator (`union`, `intersect`, `difference`, `xor`) on bags already in hand. It does not accept `narrow_to`.

## Kind bridge

A chain works when the list the step publishes is the list the next slot requires. `search` and `set` do not publish both kinds.

- Hybrid and node-vector `search`, and `find`, publish `node_ids`. When the hit carries a source key they also publish `doc_keys`. The next `narrow_to` binds `@step.node_ids`. A walk binds `@step.doc_keys`.
- FTS `search` publishes `doc_keys` and leaves `node_ids` empty. `narrow_to` matches `node.id` only, so it keeps nothing from that step.
- `set` publishes one list, the `id_kind` you declared. A `node_ids` set can feed `narrow_to`. A `doc_keys` set can feed `project`, `order`, `enrich`, or `walk_path`. `set` does not fill the other list and does not convert.
- `project`, `order`, and `enrich` accept either list. When they fetch, they write both `node_ids` and `doc_keys`. That fetch is the bridge from a doc-key bag to a node-id bag. `order` with `by: id` does not fetch. It sorts the tokens it was given and does not look up the missing half.

So hybrid → `narrow_to` hybrid → `project` is a chain. FTS → `set` of `doc_keys` → `narrow_to` is not. FTS → `project` on `@step.doc_keys` → `narrow_to` on that project's `node_ids` is the long way across.

## The 14 APIs

Pushdown means the allowlist is in the store query before `LIMIT`. Post-filter means the tool runs, then Go keeps hits whose `node.id` is in the list. Limits on hybrid, vector, and FTS clamp at 200.

| API | Role in the chain | `narrow_to` | Publishes | Next slot |
| --- | --- | --- | --- | --- |
| `find` | Equality lens. The wide cut when the mini-schema stores the value. The whole plan when the shape is exact. | Yes. `find_nodes` and `count_nodes` push down (`n.id IN $node_ids` before `LIMIT`). `selectivity`, `entity_mentions`, and `docs_sharing_entity` post-filter. | `node_ids` and `doc_keys` | `@step.node_ids` into `narrow_to`, `get`, hop. `@step.doc_keys` into `walk_path`. |
| `search` hybrid | Soft lens. The closer step on a vague question. One call on an exact soft facet. | Yes. Pushed into the ANN as `id IN $node_ids` before `LIMIT`. A residual `where` is applied after an over-fetch capped at 200. It is not inside that ANN clause. | `node_ids`, and `doc_keys` when the hit has a source key | `@step.node_ids` into the next `narrow_to`. |
| `search` vector / semantic, `target: nodes` | Same closer lens, or similarity from `seed_node_id`. | Yes. Same ANN pushdown. | `node_ids`, and `doc_keys` when the hit has a source key | `@step.node_ids` into the next `narrow_to`. |
| `search` vector / semantic, `target: entities` | Entity vector space. | Accepted, then post-filtered. Not in the pushdown list. A node-id allowlist does not match `entity_ids`. | `entity_ids` | No node-id slot. |
| `search` fts | Lexical lens. | Handler post-filter after the text query. The allowlist is not in the FTS query. The filter matches `node.id`, and these hits have none. | `doc_keys` only | `@step.doc_keys` into `project`, `order`, `enrich`, or `walk_path`. Not into `narrow_to`. |
| `search` spatial | Similarity from a seed. Experimental. | Accepted, then post-filtered. `find_similar_hybrid` is not pushed. | node hits when the flag is on | Not a default funnel step. |
| `traverse` | Move to a related type. The seed is `from` or `walk_path.from.src_keys` (`doc_keys`). | Yes, on the terminals. `related_to`, `expand_from`, `path_between`, `get_subgraph`, and `walk_path` push down. Walk compiles `NarrowTerminalIDs`. | `node_ids` and `doc_keys` | Either list, into the slot that list matches. |
| `get` | Hydrate by id. Own slot is `ids`, max 50. | Yes. Intersects those ids with the allowlist before the batch get. | `node_ids` | `project` on `@step.node_ids`. |
| `analyze` | Corpus job. | Accepted and post-filtered. The mapper strips the key. The jobs are not pushed. The filter helps only when the job returns `items[]` with `id`. | job-shaped | Not a funnel step. |
| `set` | Boolean compose of 2–8 bags. `id_kind` required. | Ignored. The verb reads `inputs`. | only the declared `id_kind` | `node_ids` into `narrow_to`. `doc_keys` into `project`, `order`, `enrich`, or `walk_path`. |
| `order` | Rank a bag. Own slot is `ids`. `limit` lives here. | Ignored. | both, when it fetched | `project` on either list. |
| `enrich` | Attach fields. Cardinality unchanged. Own slot is `ids`. | Ignored. | both, when it resolves | `project` on either list. |
| `project` | Shape the end-state cards. Own slot is `ids`. No `limit`. No `why_match_from`. | Ignored. | `node_ids` and `doc_keys` beside the rows | Last step inside the pipeline. |
| `pipeline` | The vague-question chain. Not a step. | Not a pipeline-level field. It sits on a step. | the steps named in `return[]` | Planning call. The skeleton, plus `query_decomposition` once beside it. |
| `return` | Answer envelope. Not a step. | No. | none | Stop. `summary`, `decomposition`, and `confidence` from the rows. |
| `describe` | Orientation when the inject is missing. | Ignored. | stats and types | Not a chain step. Do not call it when the inject is already in the turn. |
| `explain` | What a query means. | Ignored. | none | Not a chain step. |
| `rail` | Named-query execute for a common path or a hard fact. Not in `v2Verbs`. Not a pipeline step. | No. Binds are values already in hand, or ids the pipeline just returned. No SQL. | rows from the pinned statement | The whole call when the binds are already known. The next call when the binds are the ids this pipeline returns. |

## The vague chain

**Statement.** Two or more soft facets of the same entity, and no named rail, are one pipeline. The first lens is the widest legal cut. An equality the mini-schema stores is `find` when that value is known. Each later hybrid or node-vector search sets `narrow_to` to the previous `node_ids` and a smaller limit, and sets `abort_if_empty` when that facet is required. FTS feeds `project`, `order`, or `enrich` through `doc_keys`. The last step is `project`. The rows are the end state.

**Why.** One `query_text` asks one embedding to do every facet. A second search that is not inside the previous ids searches the world again. A doc-key bag passed to `narrow_to` comes back empty. A rail already pinned for this ask makes the chain a slower copy of a path the operator reviewed.

**Goal.** Close, then closer, in one call, on lists the engine actually joins, and only when no rail is named.

```json
{"as":"wide","verb":"search","params":{"strategy":"hybrid","entity_type":"<Type>","query_text":"<first facet>","limit":200},"abort_if_empty":true}
{"as":"closer","verb":"search","params":{"strategy":"hybrid","entity_type":"<Type>","query_text":"<second facet>","narrow_to":"@wide.node_ids","limit":40},"abort_if_empty":true}
{"as":"cards","verb":"project","params":{"ids":"@closer.node_ids","fields":["name"]}}
```

That shape is what a later pack teaches for two soft facets. A stored equality is a `find` step in front of it, not a `where` on the first hybrid. This page does not put the example in a pack.

## Hints and rails

**Statement.** A sentence true on the first turn for every tenant is core, next to the schema. A sentence true for one scope, one channel, one common ask, or one recent miss is `hints.*` or a line in that scope's brief. A hint may name the usual shape for that scope, including "this ask is the rail named in the brief." A hint sits after hard rules. It does not replace the mini-schema, the kind bridge, the jailbreak law, or the four terminate fields. A hint that becomes true for every tenant is promoted, and the hint is deleted.

A rail runs only when the brief names it. The model copies `name` from the brief and puts values it already holds into `binds`. It does not write SQL, and it does not invent a rail for a question the brief does not name. Until a question is that common, the vague shape uses the chain. The chain is how a path becomes common enough to pin.

**Why.** Writing a prepared statement for most questions is tens of thousands of rails. The chain covers the long tail. A rail covers the head. One scope's hot path pasted into the catalog is a paragraph every other tenant pays for. `hints.*` is still not on the live client, so a common pattern that exists only as a hint is invisible until that inject lands.

**Goal.** Vague questions narrow. Common questions skip the funnel. Exact questions stay one call.

## What a pack still carries

These are in force for a chat_request cut from this page. They are the base-8.0 coverage the short draft left on v1.

**The world is the inject.** Stay inside the scope brief, the mini-schema, and the walk paths that arrived with this turn. A field that is absent is not a fact. The catalog teaches how to read the inject. It does not name a tenant's entities.

**The mapping is the static world.** The saved entity map is fixed for the turn. It decides which types exist, which fields exist, and which verb a field can take. A row enters that world on Save. A new row is `skip` until then, and `skip` is absent. The model reads the kind on the mini-schema row. It does not remap a field. The Hub treatment name and the layer badges `attr`, `entity`, `edge`, and `list` stay on the operator screen. The catalog states this table once. It does not paste a tenant's paths into the prompt.

| Treatment | Row the model sees | What that row allows |
| --- | --- | --- |
| `skip` | absent | The field is not in this world. |
| `entity` | `scalar_ent`, `[gsi]`, `fk_to` the type hint | The stored string is an entity of that type. Equality uses the stored value. An empty parent does not replace that spelling. A zero-row parent is not `src_keys`. With no spelling in the question, `find` the child. |
| `entity_fk` | `entity_fk`, `[gsi]`, `fk_to` the type hint | The value is a document key. The hop is `walk_path` when that chain is on `WALK_PATHS`. |
| `numeric_facet` | `number`, `[gsi]` | Equality on the number. A range the row cannot store is `wish_i_knew`. |
| `searchable_text` | `text_fts`, `[fts]` | A soft phrase is `search`. It is not a `where` equality. |
| `display` | `display`, `[none]` | The value may appear on a card. It is not a `where` key. |
| `entity_per_element` | `array_of_ent` | Each element of the array is an entity. |
| `entity_per_key` | `map_of_ent` | Each key of the object is an entity. |
| `boolean_map` | `boolean` when the list is on. Otherwise `scalar_ent` with `ex:` | The closed list below, and only when the row is `boolean`. |
| `enum` | `string` with `one_of` | The closed list below. |

The document key has its own static treatment: `skip`, `whole`, `split`, or `regex`. That choice decides whether the key itself mints entities. A type the map did not mint is absent. A string stored on a hotel is not a Country document until the map says it is.

**A closed list on a row is the whole set.** `boolean_map` and `enum` are the two rows above. The catalog does not name those treatments, and it does not paste a tenant's spellings. A `boolean` row accepts `where` true, false, or one spelling from that row. The server matches the stored strings `"true"` and `"false"`. A `one_of` row is the whole set: copy one listed string. A value outside that set is rejected. An `ex:` trailer is a sample. It is not that set.

**Copy the list the next slot requires.** The kind bridge and the API table are that rule. `@step.ids` is node ids only. `set` requires `id_kind`. Node-id slots take `@step.node_ids`. `walk_path` `from.src_keys` takes `@step.doc_keys` when that list has keys. An empty list is not a selector. `project`, `order`, and `enrich` accept either.

**The schema is the parameter list.** A field the schema does not have is not taught in prose, in an example, or in a hint. `project` has no `limit`. `order` does. Search keeps three single-call examples, full-text, one hybrid facet, and spatial, because that verb is the one the model invents inputs for. Those examples do not combine an equality and a phrase. `narrow_to` is pipeline-only. It is not a field on a standalone `search`. The chain example lives on the pipeline tool only.

**Terminate from evidence.** The turn ends as one Layer A object.

- `query_decomposition` is how the submitted string was understood. The fields and the loose join are in [The suggestion](#the-suggestion) and in [QUERY_DECOMPOSITION.md](QUERY_DECOMPOSITION.md). It is written on the call that creates the queries.
- `decomposition` is the data plan: targets, predicates, and output, grounded in the mini-schema. It is written on the answer call, after the rows exist.
- `summary` and `confidence` (`high`, `med`, or `low`) are the user-facing close. They are written on the answer call. Facts in `summary` come from tool results or the brief.
- Those four are required. Three of them wait for rows.
- A probe writes `query_decomposition` with the probe. It writes the other three after the probe returns, and only to stop. It does not also write the funnel.

**The same question, schema, brief, and hints pick the same shape.** Catalog mode may change the tone. A hint may pick the rail or the first lens. Neither may change the kind bridge or the four required fields. Row ids may change when the store changes. The shape of the plan does not.

**The ceiling is 8 rounds.** A vague question is one planning round. That round carries the queries and `query_decomposition`. The answer is the next short round. A rail whose binds are already known is one round, and that round carries `query_decomposition`. A rail that needs the pipeline's ids is the round after the answer. The rounds under the ceiling are repair around that plan, not one lens per call.

## Where a sentence goes

This page is for the person cutting the pack. The model does not receive it. The model receives one skeleton on the pipeline tool and fills the slots: the equality value, each facet's words, the limits. It fills `query_decomposition` once beside that skeleton, or beside the one exact call. An exact question stays one small call. The system text does not narrate the gates on this page. The search tool does not repeat the chain. Placement of a sentence that passes the review is still [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md). Wire order is still [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md).

**No fight.** A new sentence that names a different verb, list, or parameter than a statement on this page does not go in. Edit the one statement.

**No copy.** A statement is said once. A second copy on another tool does not go in. The tool schema still lists its fields.

## Dropped

These sentences are retired. A pack cut from this page does not carry them, including where base-8.0 still says them.

- "One clause" applied to the whole question. Each soft facet is its own `query_text`. The user's words for that facet pass through. Two facets do not fold into one string.
- "Stop when the inputs are in hand" read as stop after the first page. The wide cut is not the end state. The turn stops on the last set, on zero rows, or on a named gap.
- `find`, then `order`, then `project` as the only pipeline the model sees. That shape ranks a bag already in hand. The vague pipeline is the chain example above.
- Hybrid plus `where` as the way to combine a stored equality and a phrase. The equality is a `find`. The phrase is a later `search` with `narrow_to`. A residual `where` on hybrid is not that cut.

## Engine bounds

Stated once. A later sentence does not repeat them.

- Hybrid, vector, and FTS limits clamp at 200.
- Hybrid `where` is a residual filter after the ANN, not a pushdown.
- FTS `narrow_to` does not see doc keys.
- `{via, into}` is rejected. `narrow_to` is an id list.
- `rail` is outside the step list. `pipeline` and `return` are not steps.
- `previous_ids` binds `.ids`, which is node ids only.
- `set` publishes one kind. It does not convert.
- `hints.*` is not injected on the live client yet.

## Review a sentence against this page

```text
Sentence:
Which shape does it serve?  common | exact | vague | all | none
Which outcome does it serve?  rows | zero | wish_i_knew | all | none
Adds a lens, a binding, a stop, or a gap kind?  lens | binding | stop | gap | none
Publishes the list the next slot requires?  yes | no
Uses narrow_to on a doc-key bag?  yes → do not add it
Tells a named rail to also build the chain?  yes → do not add it
Calls a clean zero a missing dataset?  yes → do not add it
Puts the whole question in one query_text?  yes → do not add it
Writes the whole question into one query_decomposition string?  yes → do not add it
Turns a price, date, availability, or rating comparison into a where?  yes → do not add it
Stops the turn after the first page?  yes → do not add it
Teaches hybrid where as an equality plus a phrase?  yes → do not add it
Gives analytics a budget?  yes → do not add it
Names a tenant, a city, or a sample row?  yes → hint, not this page
Paraphrases a boolean or one_of spelling, or pastes a tenant's list into the catalog?  yes → do not add it
Teaches a verb the row's kind does not allow, or a field the map did not declare?  yes → do not add it
Names a Hub layer badge, or a row that has not been Saved?  yes → do not add it
Stops on an empty parent while the scalar_ent child can take the spelling?  yes → do not add it
Fills relation and then only projects that field?  yes → do not add it
Puts each parent on attribute, then searches and projects?  yes → do not add it
Turns a null on the first page into wish_i_knew and skips the walk?  yes → do not add it
Binds a zero-row parent doc_keys as src_keys?  yes → do not add it
Uses a shape other than common, exact, or vague?  yes → do not add it
Fights the table, the suggestion, or the three outcomes?  yes → edit that section, do not add a second sentence
Copies a sentence already on this page?  yes → do not add it
```

A sentence that fails this review does not go into the next pack.

## Next pack

The empty-seed cut is `v2/base/base-9-prototype-6`. Parent is base-9-prototype-5. base-9-prototype-5 still copies a zero-row parent into `src_keys`. The each-parent cut is `v2/base/base-9-prototype-5`. Parent is base-9-prototype-4. The empty-parent cut remains `v2/base/base-9-prototype-4`, parent base-9-prototype-3. The call-rule cut remains `v2/base/base-9-prototype-3`, parent base-9-prototype-2. `v2/base/base-9-prototype-1` stays, and it still leaves `query_decomposition` on the answer call. `CURRENT.json` stays base-1. The Zeus embed stays base-6.1 and base-7.1. This page is not the pack.

The model text is the skeleton and the slot fill. An exact question stays one small call. A vague question is the chain example, with a `find` in front when the first cut is a stored equality. This page's gates stay here.

`query_decomposition` is on the planning call, beside the queries. It is the short facet row, including `dates`, `availability`, `rating`, and `relation` when the string signals them. A comparison with no named rail is `wish_i_knew`, not a `where`. An empty parent does not stop a `scalar_ent` child `where`. A list of the child in each parent fills `relation`, and that walk is the close. `project` of the field is the card. A null on the first page does not replace the walk. A parent `find` that returns nothing stays off `src_keys`. With no spelling in the question, a `scalar_ent` child is a `find` of the child, and the parent walk waits until that find returns keys. `summary`, `decomposition`, and `confidence` are the answer call after the rows. [base-9-prototype-6](../v2/base/base-9-prototype-6/) is that cut. [base-9-prototype-5](../v2/base/base-9-prototype-5/) is the each-parent cut. It still copies a zero-row parent into `src_keys`. [base-9-prototype-4](../v2/base/base-9-prototype-4/) still walks only a `relation` that is already filled. The empty-parent cut remains [base-9-prototype-4](../v2/base/base-9-prototype-4/). [base-9-prototype-3](../v2/base/base-9-prototype-3/) still stops on zero probe rows and does not say that `project` is the card. [base-9-prototype-2](../v2/base/base-9-prototype-2/) still names only `intent`, `entity`, `shape`, `suggestion`, and `why` on the tool line. [base-9-prototype-1](../v2/base/base-9-prototype-1/) still keeps all four on the answer call.

Wall clock is measured on that pack, against base-6.1, on the same questions. Record seconds for the planning call and for the answer call. The one-facet questions have to keep the short planning call. The 2026-11-21 report at [baseline/reports/2026-11-21_base-7_2_vs_base-8-prototype.html](../baseline/reports/2026-11-21_base-7_2_vs_base-8-prototype.html) counts rounds, 59 against 68, and has no seconds. Analytics system text there is 2,475 tokens on base-6.1 and 3,251 tokens on base-8.0. A larger prompt is not the clock.

The plan test is the five questions, plus the empty parent, the filled relation, and the list per parent. A named rail whose binds are already in hand stays one `rail`. An exact equality stays one `find`. A two-facet question with no rail changes from one `search` to `search`, then `narrow_to` `search`, then `project`. An equality known only as an `ex:` spelling is one probe, then that fast path. A type the mini-schema does not have stops on `wish_i_knew` `kind: schema` and does not invent the type. An empty parent of a `scalar_ent` child is that child's `where`, then `walk_path` when the chain is listed. A list of the child in each parent fills `relation` with that parent and walks the inverse. `project` of the field is the card. A null on the first page does not replace that walk. A parent `find` that returns nothing stays off `src_keys`. With no spelling in the question, a `scalar_ent` child is a `find` of the child, and the parent walk waits until that find returns keys.
