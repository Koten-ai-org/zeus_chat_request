# Where the lines fight

> **Doc status** · snapshot **2026-11-20** · catalog **base-7.4** analytics · plus the scope brief Zeus appends on every turn, including every A/B turn
>
> Laws live in [CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md). This file is the current evidence that a sentence missed a law. It is not a license to edit the pack from here. When a fight is fixed, delete the row. Do not paste the repair onto another tool, and do not add the row to the constitution.

Each fight below is a local patch that never asked whether it still matched the access rule. A failed call produced a sentence. The same sentence was then pasted onto the next tool so the model could not miss it. The file got bigger. The goal did not get clearer.

## Fights

**The scope brief fights the pack on the walk seed.** The brief says find and hybrid results bind `@step.node_ids`, and not to put those in `src_keys`. The pack says a listed related type is `walk_path` with `from.src_keys` bound to `@step.doc_keys`, including when the seed row already shows that field. Find publishes both lists. The walk slot reads `doc_keys`. The brief tells the model to withhold the list the slot requires. Law 2, stated twice, in opposite directions. The A/B runner appends the brief after the pack, so the last sentence wins.

**The top-N rule fights the project schema.** The efficiency section says to `order`, then `project` or `get` with `limit: N`. `project` has no `limit` property, and the pipeline sentence says project ignores limit. `get` takes node ids only. The ranked example was fixed to cap `order`. The prose rule was not. Law 4.

**"Narrow" fights "narrow_to takes node ids only."** The plan says that with no hierarchy you stay on the same entity and narrow. The pipeline key says `narrow_to` takes node ids only, so it cannot follow an FTS step, because FTS leaves `node_ids` empty. A search-first question is told to narrow and told that narrow is illegal. Law 2.

**The typical chain over-applies the FTS case.** The plan says copy the list the next slot requires, and that FTS leaves `node_ids` empty. The pipeline sentence then says the typical chain is search, then project `@step.doc_keys`, with no strategy on it. That is the right bind after FTS. It is a standing order after every search, including hybrid, which is what a soft phrase is told to use. Law 2 got a shortcut, and the shortcut became the rule.

**The fast bet fights the evidence law.** Execution style says a terminating pipeline pre-writes `summary` and `query_decomposition` before seeing data. The evidence section and the `return` tool say fill Layer A from tool results and do not invent. Both are unconditional. The pre-write is legal only on `fast_path`, when the shape is already known and the facts arrive with the rows. Written as always-on, it tells the model to state facts it does not have yet. Law 6.

## Where the same law is copied

These agree with each other. They are the growth. One statement of the law is enough. The copies are why a later base gets bigger without meeting the goal.

| Law | How many times it is said in the analytics text |
| --- | --- |
| Copy `@step.node_ids` or `@step.doc_keys`. Do not bind `@step.ids`. | Plan, both execution lines, the terminate footer, `set` inputs, `order.ids`, and the pipeline key |
| A listed related type is still `walk_path` from `@step.doc_keys`, even when the seed row shows the field | Plan, access path, `find` WHEN NOT, `traverse` WHEN |
| At most 8 calls, and one pipeline is one of them | Plan budget, the hard-cap line, and the pipeline description |
| A browse ends on 10 or 20 cards unless the question asks for a related type | Goal, `rail` WHEN NOT, and `return` |
| Cheapest move that still follows the plan | Access-path heading and the verb-priority line |

The rail procedure is already the goal line and the `rail` tool: last call, hard fact, `name` copied from the brief, `binds` already in hand, no SQL. That pair is the same kind of copy. Do not add a third statement of it. The tool keeps the two fields. The essay stays once.

## Not a line fight

These are open, and they are not two sentences in the pack saying opposite things.

- `hints.*` is a hook in the catalog and is not injected on the live client. A universal law cannot live only in that hook.
- The 8-round session ceiling is the live law for every call. Analytics is a placeholder for a future Helios job. It does not raise that ceiling.
