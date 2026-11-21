# Lessons from chat_request changes

> **Doc status** · 2026-11-20 · a reading of the constitution exam, not a pack
>
> Source page: [../v2/base/constitution_exam.html](../v2/base/constitution_exam.html), written by `python3 scripts/constitution_exam.py`. Laws: [CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md).
>
> Each lesson is general. The base ids are the evidence. A lesson that names one tenant's rows does not belong here.

## Do not remove `query_decomposition` from the system text

It is the intent, and it is where the fast-path or probe suggestion is recorded. The turn's required four include it. A pack that never names it can still emit a pipeline and has nowhere to say why that pipeline was chosen.

Every scored base from base-1 through base-7.4 keeps the field in the system text. The exam never opens a "missing decomposition" miss. That is the evidence for leaving it where it is. Moving it into a hint, or into one mode only, makes it disappear on the turns that do not load that hint.

Source: constitution exam, `no_decomposition` never opens, base-1 through base-7.4.

## Do not treat a smaller file as a better pack

A character drop is a diet. It is not a result.

- base-4 loses 93 characters and fixes no check.
- base-6.2 loses 7,839 file characters and 4,127 system characters. It does clear two fights. The next train puts both fights back.
- base-7.2 grows 236 characters, open issues fall by one, and the 21-question pass falls from 20/21 to 16/21, net −4.

Score a diet by which statement it kept and which plan changed. A falling issue count is not accuracy.

Source: exam shrink section, base-4, base-6.2, base-7.2. Suite line on base-7.2.

## A fight you delete has to stay deleted

base-6.2 removes the `limit` on `project` and the summary written before the rows. base-7.x adds `rail` and the 8-round ceiling, and it also puts those two sentences back. They are still open on base-7.4.

Adding a verb or a ceiling is not a reason to restore a sentence an earlier diet removed. Close a fight once. Do not paste the warning onto another tool to keep it from coming back.

Source: exam, `project_limit` and `prewrite_summary` cleared at base-6.2, reopened at base-7.x, open on base-7.4.

## Do not paste one bind law onto every tool

Say the access rule once. A second copy on `find`, `traverse`, `order`, `pipeline`, or `return` is how the file grows without a new plan.

base-7.1 is the binding fix. It is also the base that introduces the repeated `@step.doc_keys` lines. Those copies are still open on base-7.4. The pass of base-7.1 against base-7.0 is net 0, so the copies did not buy accuracy.

Source: exam, `bind_copies` introduced at base-7.1, open on base-7.4. Suite line on base-7.1.

## Do not teach a parameter the schema does not have

That includes a mode example. The model copies the example.

base-5.1 introduces both a `project`/`get` `limit` sentence and a traverse example that uses `edge_types`. `traverse` takes `via`, one string. `project` has no `limit`. `order` does.

The `edge_types` examples stay until base-7.4 removes them. The project-limit sentence is removed on base-6.2 and returns on base-7.x. base-7.4 fixes the ranked example and leaves the prose.

Source: exam, `edge_types_example` from base-5.1 to base-7.3. `project_limit` from base-5.1, quiet on base-6.2, back at base-7.x.

## Do not omit a field the engine requires

`set` without `id_kind` is a call the server rejects. The schema taught that call from base-1 through base-7.3. base-7.4 puts `id_kind` on the required list.

A missing required field is not a shorter API. It is an invented call in the other direction: the model omits what the handler demands.

Source: exam, `set_id_kind` open base-1 through base-7.3, closed at base-7.4.

## Do not describe a last call that has no verb

`rail` is absent from base-1 through base-6.2. A hard fact in those packs has no legal tool, so the model invents a statement. The verb arrives at base-7.x.

Add the verb on its own hop when you can. The base-7.x hop that adds `rail` is the same hop that restores the project limit and the pre-written summary. One new tool does not have to reopen old fights.

Source: exam, `rail_missing` closed at base-7.x, same row that reopens `project_limit` and `prewrite_summary`.

## Do not bind `@alias.ids`

`@step.ids` is node ids only. A warning sentence that leaves `@fn.ids` or `@step.ids` in an example does not close the miss. The binds stay open from base-1 through base-7.3, across modes. base-7.4 closes them by changing the examples.

Do not add another "do not bind" line after the examples are gone. That line becomes the next copy.

Source: exam, `ids_bind` open base-1 through base-7.3, closed at base-7.4.

## Name the list a shape reads

`walk_path` with no `from.src_keys` seed is open from base-1 through base-7.1. base-7.2 states the seed and the issue closes.

Stating the list is not the whole result. base-7.2 is also the pass that drops four questions. A correct bind and a worse plan can be the same edit. Run the exam, then the suite.

Source: exam, `walk_seed_missing` closed at base-7.2. Suite line on base-7.2, net −4.

## State the 8-round ceiling once

It is missing from base-1 through base-6.2 and present from base-7.x on. A pack with no stop spends rounds on rediscovery. Say it in the plan. Do not repeat it on every verb.

Source: exam, `no_ceiling` closed at base-7.x.

## Keep search's three examples when you shrink the pack

Search is the verb the model invents inputs for. The three examples are full-text, hybrid plus `where`, and spatial. The count is wrong until base-5.3, and the big base-6.2 shrink does not reopen that miss.

A minify that cuts those examples puts the invented-input miss back. Cut a copy of a law before you cut a search example.

Source: exam, `search_examples` closed at base-5.3 and not reopened on base-6.2.

## A local miss gets one clause

base-7.3 adds the walk-close wording and 247 characters. The open-issue count does not change. The sentence was already the kind of copy the bind lesson names.

If the access rule already says the thing, edit that one statement. Do not add the story to `find`, `traverse`, the plan, and the pipeline key.

Source: exam, base-7.3 issue count unchanged from base-7.2.
