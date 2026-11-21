# Lessons: base-7.0 → base-7.1

## What worked

- **New folder.** base-7.0 stays immutable. base-7.1 is the binding fix. The next tweak scaffolds another id.
- **Parent is the working base-7.0 tree.** The diet is the bind sentences only. Plan, then call, `rail`, and the boolean / `one_of` teaching stay.
- **Name the list the verb actually writes.** An FTS `search` fills `doc_keys` and leaves `node_ids` empty. `find`, hybrid, and node-vector fill `node_ids`. `@step.ids` reads `node_ids` only. Teaching `@step.ids` as the preferred bind makes a later `project` run on an empty list. A terminating pipeline writes the summary on that same call, so the advisory `PIPELINE_AMBIGUOUS_IDS` cannot repair the turn.
- **Keep the warning.** The pack still says `@step.ids` is node ids only. This hop does not ask Zeus to fall through to doc keys.
- **`verify_base_pack.py` and `diff_modes.py --fail-if-clone` before calling the pack ready.** Ten modes, none identical.

## What this release does not do

- Flip `CURRENT.json`. That pin stays base-1.
- Invent a production `contract_hash`. The copied base-7.0 hash stays.
- Run `assemble_mode_prompts.py`. That script can pull the base-6.2 skinny back in.
- Execute `rail`. The catalog can plan the call. The engine cannot run it yet.
- Run the 21-question suite. That comparison is still open.
- Put the pack on the lab image. The local Zeus 5.5TH tree embeds base-6.1 and base-7.1. The served pin in that tree is base-7.1. The lab image still serves base-7.0 until a later deploy.

## Still open after the catalog is green

The 21-question suite, a Beelink image that embeds this pack, and a `CURRENT.json` flip. Those are separate decisions. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays open until they are asked for. The wire did not change, so this hop does not add a Client parser story.
