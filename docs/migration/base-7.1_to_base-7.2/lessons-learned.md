# Lessons: base-7.1 → base-7.2

## What worked

- **New folder.** base-7.1 stays the measured pack and the Zeus embed. base-7.2 is the slot rule. The next tweak scaffolds another id.
- **One rule, not a pair matrix.** Producers publish `node_ids` and `doc_keys` when they have them. Consumers have typed slots. The model copies the list the next slot requires. A catalog sentence that names the previous verb ("always `node_ids` after find or hybrid") is the wrong `walk_path` seed. `from.src_keys` is doc keys even after find or hybrid.
- **FTS is the producer that leaves `node_ids` empty.** A node-id slot cannot follow an FTS step. `narrow_to` matches node ids only, so it cannot filter an FTS hit list by doc key.
- **Do not claim every producer fills both lists.** `set` copies the result onto only the declared `id_kind`. A `walk_path` aggregate row has no terminal node, so both lists are empty. Hybrid fills `node_ids` when the hit node has an id, and still writes `doc_keys`.
- **Keep the warning.** The pack still says `@step.ids` is node ids only. This hop does not ask Zeus to fall through to doc keys.
- **Leave the ranked example.** `find` → `order` `@cands.node_ids` → `project` `@ord.node_ids` is a legal chain. It is not a walk.
- **`verify_base_pack.py` and `diff_modes.py --fail-if-clone` before calling the pack ready.** Ten modes, none identical.

## What this release does not do

- Flip `CURRENT.json`. That pin stays base-1.
- Invent a production `contract_hash`. The copied hash stays.
- Run `assemble_mode_prompts.py`. That script can pull the base-6.2 skinny back in.
- Execute `rail`. The catalog can plan the call. The engine cannot run it yet.
- Run the 21-question suite. That comparison is still open.
- Swap the Zeus embed. The local 5.5TH tree still serves base-7.1 and also embeds base-6.1. The lab image still serves base-7.0.
- File a ticket. CR-40 stays To Do.

## Still open after the catalog is green

The 21-question suite on this pack, a Beelink image, and a `CURRENT.json` flip. Those are separate decisions. The wire did not change, so this hop does not add a Client parser story.
