# Why these sentences are in base-7.0

Read this before adding, rewriting, or deleting a sentence in `chat_request_*.json` for `base-7.0` or `base-7.x`.

The catalog is an evolving prompt. A sentence that is true on every turn is paid on every turn, including scopes that never hit the problem. This file is the cost record: why the sentence is there, which scored run justified it, how many characters it adds, and when a later change should remove it instead of stacking another one.

Character counts are Python `len` of the added text. The report's `tk` figure is UTF-8 bytes ÷ 4, rounded up. It is not the model tokenizer. Costs below are per mode. Ten modes pay the same sentence.

Placement for an always-on verb rule is CORE (`messages[].content`) plus the verb card that would otherwise contradict it. `hints.*` is a Client paste after `rules{}`, for one scope or one arm, and it is excluded from the contract hash. Min packs omit `instructions`, `guidance`, and `masq`. See [HINTS.md](../../HINTS.md) and [PROMPT_RULE_PLACEMENT.md](../../PROMPT_RULE_PLACEMENT.md).

## How to judge the next sentence

1. Name the scored row: question id, what each pack called, and whether it met.
2. Find the row in the table below. If a sentence already covers that problem, do not add a second one.
3. If the miss is the question text or the harness, change `baseline/questions.json` (and `suite.lock.json`) or `baseline/run_ab.py`. That costs zero catalog characters.
4. A new sentence has to name the rows it can move and the rows it must leave alone. Pay the characters only when that trade is better than a question change.

## Sentences added for the 2026-11-18 travel gap

Source runs, both exit 0, Zeus `1.0.0-beta.3`, model `grok-4.7`:

- Full suite, before these sentences: [2026-11-18 report](../../../baseline/reports/2026-11-18_base-6_1_vs_base-7_0.html). base-6.1 met 16/22, base-7.0 met 12/22, net −4. Travel was 8/11 versus 3/11.
- Travel subset after the path-close law, eight questions where base-7.0 had missed: [travel-misses report](../../../baseline/reports/2026-11-18-travel-misses/2026-11-18_base-6_1_vs_base-7_0.html). Both packs met 3/8, net 0. The five full-suite regressions on that list were no longer regressions.

The gap was path choice. base-7.0 called `search` `fts` or `find` where the fixture wanted `search` `hybrid` or `traverse` `walk_path`. Return schema, `query_decomposition`, and `masq` were the same on both packs. Min packs have no `masq` object.

| Sentence | Where | Characters | Why it is there | Remove it when |
| --- | --- | --- | --- | --- |
| A related type on a WALK_PATHS chain closes with `traverse` `walk_path` from the seed ids. That close does not end on 10 or 20 cards. | Plan bullet, every mode | part of the +385 system total | 2026-11-18 travel walks (`travel-walk-state-counts`, `travel-beach-itinerary`) stopped on `find` or cards. The subset then walked state-counts on both packs. | A later run shows the walk rows meeting without it, or the sentence starts walks on questions whose target is `find`. |
| `find` is a same-entity GSI equality: a boolean, a name, or an id already in hand. A related type's name is not a `find` value. | Access-path `find` row, and `find` WHEN NOT | inside the +385, plus **70** on the `find` card | Both packs hunted a related type by `find` where that type's name was the value. | The access-path row and the card disagree, or a scored `find` question starts missing because the card over-blocks equality. |
| A soft phrase uses `strategy:hybrid`. `fts` is for a question that asks for full-text or a single indexed word. | Access-path `search` row, and `search` KEY | inside the +385, plus **108** on the `search` card | The old line said `` `strategy:fts` or `hybrid` ``. On `travel-pipeline-cards` and `travel-search-fts` that tie went to `fts`. The subset then hit both targets on both packs. `travel-search-fts` still asks for full-text, so `fts` stays legal. | A hybrid question starts missing, or an fts question starts calling hybrid. |
| `walk_path` from the seed ids when that related type is on a WALK_PATHS chain. | Access-path `traverse` row, and `traverse` WHEN | inside the +385, plus **53** on the `traverse` card | The traverse card still said "multi-hop after seeds exist," which the model satisfied with `find`. | The plan bullet and the card disagree. |
| A browse with no hard fact ends on 10 or 20 cards, unless the question asks for a related type on a WALK_PATHS chain. | Goal sentence, every mode. Replaces the shorter ending. | **67** | The shorter ending contradicted the plan bullet. On `travel-beach-itinerary` both packs returned beach hotels and landmarks and stopped. The question still asked which country each one is in. This clause is the contradiction removed, not a new hint block. It is not yet a scored win. | The next comparison shows no move on beach or the Bell Inn walks, and some `find` or card question gets worse. Then delete the clause and restore "A browse with no hard fact ends on 10 or 20 cards." The country-link question is no longer in the suite. |

System total for the path-close law before the goal clause: **+385** characters on every mode versus the base-7.0 text that shipped with Plan, then call. The goal clause is **+67** on top of that. Ten modes, so the clause is 670 characters of catalog text. One turn pays 67 of them.

The goal clause must stay quiet on questions that do not ask for a related type: free parking, the single indexed word, the beach hybrid search, and the ten-card pipeline. State counts and hotels-by-country already walked on the subset, so this clause is not there to move them.

## Kept out of the catalog

These were the same investigation. They do not belong in `chat_request*.json`.

| Problem | Change | Why it stays out of the prompt |
| --- | --- | --- |
| `travel-search-hybrid` on base-7.0 called hybrid inside one pipeline and the sample showed beach hotel cards. `verb_hit` was true. `met` was false. | `baseline/run_ab.py` `evidence_nonempty` counts `cards.rows`. | The method was already right. The harness only counted `items`, `rows`, `ids`, `node_ids`, and `src_keys`. A prompt sentence cannot change that. |
| `travel-walk-redbrook-country` and `travel-walk-city-hotels` spent the turn guessing the spelling Redbrook. The stored row is `hotel_21052`, name The Bell Inn. Redbrook is the city. | Question text now uses The Bell Inn. Expect is still `traverse` `walk_path`. `suite.lock.json` matches. | Beer "Where is 21A IPA brewed?" works because the words match the stored name. A prompt hint cannot invent the hotel's name. |
| `travel-walk-country-hotels` asked for hotels in the United Kingdom, then for hotels linked from that country. Both wordings landed on `find` Hotel where `country` is United Kingdom. | Removed from `baseline/questions.json` and `baseline/suite.lock.json`. The suite is 21 questions, 11 beer and 10 travel. | `find` Country returns no rows, and `walk_path` from Country `src_keys` `United Kingdom` along `Hotel.country` returns 0 rows. The string lives on the hotel. Inverse `walk_path` stays on `beer-walk-stone-beers`, `beer-walk-belgian`, and `travel-walk-city-hotels`. Put a Country → Hotel question back when Country documents exist: [CR-38](https://kotenai.atlassian.net/browse/CR-38). |

No dataset nouns were added to the pack. Hotel, beach, country, city, and beer stay in the question file.
