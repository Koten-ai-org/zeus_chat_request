# Query decomposition

> **Doc status** · written **2026-11-21** · the reading behind [CONSTITUION_DESIGN_v2.md](CONSTITUION_DESIGN_v2.md) § The suggestion · design page, not a pack · the each-parent cut is [base-9-prototype-5](../v2/base/base-9-prototype-5/), parent [base-9-prototype-4](../v2/base/base-9-prototype-4/) · the empty-seed cut is [base-9-prototype-6](../v2/base/base-9-prototype-6/), parent [base-9-prototype-5](../v2/base/base-9-prototype-5/) · the full probe statement and the `walk_path` guard are [base-9-prototype-7](../v2/base/base-9-prototype-7/), parent [base-9-prototype-6](../v2/base/base-9-prototype-6/) · the numbered name of that cut is [base-9.0](../v2/base/base-9.0/) · [base-9-prototype-1](../v2/base/base-9-prototype-1/) still leaves this object on the answer call · `CURRENT.json` stays **base-1** · the model does not receive this page

`query_decomposition` is the first step of a Zeus turn. The model reads the submitted string and writes how that string was understood. That object is what gets the turn started, and it is what a later reader uses to see the understanding beside the queries that understanding produced.

The call that creates the queries carries the object. There is no round spent only on the reading. The planning call emits the queries and this object together.

## The fields

The object is a row of short values. A paragraph stuffed into one string cannot be grouped, ordered, or indexed. The field list is the Layer A schema, copied with each pack as `response_output_schema.json`. Core is `intent` and `entity`. The other facets are filled when the string signals them, and left null when it does not.

| Field | What a later query groups on |
| --- | --- |
| `intent` | The verb of the ask. The values already used are short: `List`, `Best`, `Book`, `Count`. |
| `entity` | The type in this world. `Hotel`, `Beer`, `City`. |
| `attribute` | A field the ask named. A list of the child in each parent is `relation`, not this field. |
| `geo` | The place, when the string has one. |
| `audience` | Who it is for. |
| `theme` | The soft subject. Beach, fruit. |
| `occasion` | The event or season. |
| `price` | A price band the string stated, as text. A comparison the row cannot store is a decision metric: a named rail when the brief has one, and `wish_i_knew` when it does not. |
| `dates` | A when or a stay window, as text. The same class as `price`. |
| `availability` | An open, in-stock, or in-inventory signal. The same class as `price`. |
| `rating` | A number threshold, such as "above 4". Equality on a `numeric_facet` is `find`. A comparison is the same class as `price`. |
| `relation` | The other type, or the seed, of a hop. A list of the child in each parent fills this slot with that parent. The back-walk under that parent is the chain. The call is `walk_path` on the inverse. `project` of the field is the card. A parent `find` that returns nothing is not the seed. Its `doc_keys` stay off `src_keys`. With no spelling in the question, a `scalar_ent` child is a `find` of the child. The parent walk waits until that parent `find` returns keys. |
| `parts` | One mini-reading per goal when the string has several. |
| `other` | A leftover signal that is still a key, such as a coupon code the user typed. |

`shape`, `suggestion`, and `why` sit on the same object. They are the plan reading from [CONSTITUION_DESIGN_v2.md](CONSTITUION_DESIGN_v2.md). `shape` is common, exact, or vague. A list of the child in each parent fills `relation` and walks the inverse. It is not `group_by`, and it is not a `shape` value. A null on that field in the first page does not replace the walk, and it does not become `wish_i_knew`. A parent `find` that returns nothing stays off `src_keys`. An empty list is not a selector. With no spelling in the question, `find` the `scalar_ent` child, and the parent walk waits until that parent `find` returns keys. `suggestion` is fast path or probe. `why` is one sentence that ties the string to that shape. They do not replace the facets above.

A fast path means the shape is writable and every equality value is known to be stored, so the lenses are written before any row comes back. A probe means one basic value may not be stored. One cheap probe of that value comes first. Zero rows of that spelling, on the field that stores it, stop and name the gap. Some rows make the next round the fast path. An empty parent type does not stop a `scalar_ent` child. The spelling in the question is the `where` on the child field that points at that parent. Zero rows of that child `where` stop and name the gap. Some of those rows make the next step the `walk_path` that chain lists. `wish_i_knew` for the empty parent does not cancel that `where`. An `entity_fk` child still stores a document key. An empty parent there is the gap, because there is no key to copy. A parent `find` that returns nothing is not a seed. Its `doc_keys` stay off `src_keys`. An empty list is not a selector. `from` needs `doc_key`, a non-empty `src_keys`, or a `where`. That rejection stays on the call. It does not become `wish_i_knew`. The inverse hop starts on the parent. An empty parent has no key and no `where`, so that hop cannot start. A `scalar_ent` child with no spelling in the question is a `find` of the child. `project` of the parent field is the card. The parent walk waits until that parent `find` returns keys.

## What the facets are for

[BIBLE.md](BIBLE.md) marks this object **forward analytics**. The client keeps the reading. A store of readings is then an ordinary table:

- `GROUP BY` `intent`, `entity`, `geo`, `theme`, `audience`, `occasion`, or `price` counts which asks recur.
- `ORDER BY` those same keys ranks a cluster.
- A vector index on the reading puts nearby asks next to each other. Search finds them.
- The queries stored beside the reading say which Zeus path that cluster actually took. A cluster that keeps winning is the one that earns a named rail.

The live chat already paints the short values as chips. Confidence and policy are sibling Layer A fields. Intent, entity, and theme come out of this object. A Yelp turn "What cities have listings?" paints `List` and `City` and runs one `find` of `City`.

The Helios screens are the same row at volume. Compare stacks one intent, `Best` plus `Hotel` plus `family` plus `MX` plus `beach` plus `vacation` plus a price band, and ranks the candidates under it. The funnel counts readings as they move from entry, to interpreted, to a path, to candidates, to an action. Explore plots the readings on semantic axes with price as a third axis. Those screens are prototypes. The numbers on them are not a measured suite. The fields they read are the fields in the schema.

## What becomes a call

The saved entity map is the gate. A slot becomes a Zeus call only when a row can carry it. `display` and `skip` do not become a `where`.

| Slot | Call |
| --- | --- |
| `intent` `List` | Rows. |
| `intent` `Best` | `order` after the bag exists. The order key is a field the map stores. |
| `intent` `Count` | `return` `count`. |
| `intent` `Book` | The common path when the brief names that rail. |
| `entity` | `entity_type` on the call. |
| `geo`, `attribute`, or a closed spelling in `other` | `find` where that field equals one listed value, when the row is `entity`, `enum`, or an active `boolean_map`. |
| `theme`, `audience`, `occasion` | One hybrid `search` per phrase, then `narrow_to`. A phrase that is itself a closed list on the map is `find` instead. |
| `relation` | A list of the child in each parent fills this slot. `walk_path` on the back-walk inverse. `project` of the field is the card, not the close. A null on the first page does not replace the walk. A zero-row parent `find` stays off `src_keys`. An empty list is not a selector. With no spelling in the question, `find` the `scalar_ent` child. The parent walk waits until that parent `find` returns keys. An `entity_fk` child still has no key to copy. |
| A number that is equal | `find` on a `numeric_facet`. |
| `price`, `dates`, `availability`, `rating` as a comparison | A named rail when the brief has one. `wish_i_knew` when it does not. |

## The loose join

The object is written once, on the call that creates the queries: the one `find`, the one `search`, the `pipeline`, the probe, or the `rail`.

A later reader lines up three things:

1. The submitted string.
2. This object.
3. The queries that reading produced.

The object names that reading. It does not copy the tool arguments into itself. It does not summarize the rows. The rows do not exist yet on this call.

The answer call is `return` after the rows. It copies this same object. It fills `summary`, `decomposition`, and `confidence` from the rows. `decomposition` is the data plan grounded in the mini-schema. It is not this reading. A probe writes `query_decomposition` with the probe, and writes the other three only to stop.

[base-9-prototype-7](../v2/base/base-9-prototype-7/) carries the full probe statement and the `walk_path` guard. `from` needs `doc_key`, a non-empty `src_keys`, or a `where`. That rejection stays on the call. Zero rows of that child `where` stop and name the gap. An empty `entity_fk` parent is the gap, because there is no key to copy. The parent walk waits until that parent `find` returns keys. [base-9-prototype-6](../v2/base/base-9-prototype-6/) is the empty-seed cut. It still omits those four clauses and the `walk_path` guard. A parent `find` that returns nothing stays off `src_keys`. [base-9-prototype-5](../v2/base/base-9-prototype-5/) is the each-parent cut. A list of the child in each parent fills `relation` and walks the inverse. It still copies a zero-row parent into `src_keys`. [base-9-prototype-4](../v2/base/base-9-prototype-4/) is the empty-parent cut. It still walks only a `relation` that is already filled. An empty parent does not stop a `scalar_ent` child `where`. [base-9-prototype-3](../v2/base/base-9-prototype-3/) still stops on zero probe rows. [base-9-prototype-2](../v2/base/base-9-prototype-2/) requires the object on `find`, `search`, `pipeline`, and `rail`. The answer `return` still requires all four fields and copies the object already written. [base-9-prototype-1](../v2/base/base-9-prototype-1/) still leaves all four on the answer call.

## A reading of one question

Submitted string: "Show hotels in the United Kingdom whose descriptions sound like a beach."

```json
{
  "intent": "List",
  "entity": "Hotel",
  "geo": "United Kingdom",
  "theme": "beach",
  "shape": "vague",
  "suggestion": "fast path",
  "why": "United Kingdom is a stored country. Beach is one soft facet. No rail is named."
}
```

That reading is one pipeline. The first step is `find` where `country` is United Kingdom. The next step is a hybrid `search` whose `query_text` is beach and whose `narrow_to` is the find's `node_ids`. The last step is `project`. The words in `why` are the reading. The tool arguments stay on the steps.

One soft facet and no stored equality stays exact: one `search`, and `query_decomposition` sits on that call. "What beers are made from fruits?" is that shape. The reading names Beer and one facet. It does not become a pipeline.

## Seeing the reading

Hub Debug → Sessions → Analysis looks for `query_decomposition` on a call named `return`, or on a `pipeline` whose arguments already carry it. A pipeline that carries the object lights that check. A one-call `find` or `search` can carry the object on that call, and the checklist still shows it missing until the answer `return` copies it.

The narration toggle is AI on Zeus result. That toggle writes the prose after the rows. It does not write this object, and this object is not a second checkbox.

The catalog states the five fields in one sentence on the tool. This page stays with the person cutting the pack. It is not pasted into the system text.
