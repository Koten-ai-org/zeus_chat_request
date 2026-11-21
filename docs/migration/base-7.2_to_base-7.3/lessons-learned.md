# Lessons: base-7.2 → base-7.3

## What worked

- **New folder.** base-7.2 stays the measured slot-rule pack. base-7.3 is the walk close. The next tweak scaffolds another id.
- **Diet the sentence that lost.** The slot rule was already telling the model to bind `walk_path` from `@step.doc_keys`. The 2026-11-20 losses were the model never calling the walk. "A known stored value stays `find`" was the sentence that won for country and city.
- **One clause, not a new paragraph.** The close, the access-path line, and the `find` and `traverse` descriptions now say the walk still runs when the seed row already shows that field.
- **Leave the ranked example.** `find` → `order` `@cands.node_ids` → `project` `@ord.node_ids` is a legal chain. It is not a walk.
- **Leave the 21A miss in the scorer.** Replaying the base-7.2 pipeline returned `place.items` with city and state. The runner does not count a pipeline step alias. That is not a catalog sentence.
- **`verify_base_pack.py` and `diff_modes.py --fail-if-clone` before calling the pack ready.** Ten modes, none identical.

## What this release does not do

- Flip `CURRENT.json`. That pin stays base-1.
- Invent a production `contract_hash`. The copied hash stays.
- Run `assemble_mode_prompts.py`. That script can pull the base-6.2 skinny back in.
- Execute `rail`. The catalog can plan the call. The engine cannot run it yet.
- Run the 21-question suite on base-7.3. The base-7.2 page is the reason for this diet. It is not a score for this pack.
- Swap the Zeus embed. The local 5.5TH tree still serves base-7.1 and also embeds base-6.1. The lab image still serves base-7.0.
- File a ticket. CR-40 stays To Do.

## Still open after the catalog is green

The 21-question suite on this pack, a Beelink image, and a `CURRENT.json` flip. Those are separate decisions. The wire did not change, so this hop does not add a Client parser story.
