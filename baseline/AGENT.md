# Agent notes — baseline A/B report

Run the chat-request comparison from the **zeus_chat_request** repo root and let `baseline/report_bundle.py` write the HTML. Do not hand-edit `baseline/reports/*.html`. A repeatable report is the same section order, columns, colors, and verdict rule, filled with that run's rows.

Human lab notes stay in [README.md](README.md). This file is the run and page contract.

## Do not

- Invent a verdict, a score, or a "supports switching" line. Those come from `side_met` and `justification`.
- Print or commit `baseline/.env`, API keys, or basic-auth passwords. Process env wins over the file. Confirm key names only.
- Reuse the beer login for travel. Beer is `ZEUS_USER_BEER` / `ZEUS_PASS_BEER`. Travel is `ZEUS_USER_TRAVEL` / `ZEUS_PASS_TRAVEL`.
- Overwrite the comparison HTML when a turn has an empty `session_id`. The runner exits 3 and skips `write_bundle`. Keep the previous HTML.
- Float the CDN. Pico CSS is `2.0.6`. Apache ECharts is `5.6.0`. No `@latest` and no unversioned `/pico@2/`.
- Patch Zeus, pull or commit `zeus_client_python`, or commit this repo unless the user asks.
- Run `assemble_mode_prompts.py` or `--refresh-manifest` on a pack under test.
- Treat `--out` as the evidence file. `--out` is the raw trace. The evidence pair is the HTML plus the sibling JSON under `baseline/reports/`.
- Edit a question `id`, `scope`, `collection`, `text`, `expect`, or `evidence_required`. `--self-check` compares those fields with `baseline/suite.lock.json`. Change both files only when the user asks for a new suite. Notes may record a new probe. An `answer` anchor may be added without a lock change. It does not change the API verdict.
- Add or rewrite a system or verb sentence in a pack under test without reading [PROMPT_SENTENCES.md](../docs/migration/base-6.1_to_base-7.0/PROMPT_SENTENCES.md). That file is why each added sentence is there and what it costs. A miss that is the question text or the harness stays out of the catalog JSON.
- Pass `--id` on a comparison. That writes a short report and replaces the full stem.
- Run `--preview-report` onto `2026-10-21_base-6_1_vs_base-7_x`. Preview writes `--reports-dir`, which defaults to `baseline/reports`.
- Paste the CR-35 paragraph into a later pair. The renderer writes that story only for labels `base-6.1` and `base-7.x`.
- Add `template_report.html`. `render_html` is the template. Every HTML file carries a hidden `report-contract` comment.
- Remove the shared provider budget gate, or shrink a prompt so it fits a cap. The gate sleeps until the 60-second window has room. A request that cannot fit stops the run. Caps are in [README.md](README.md).
- Add a sleep between questions to ride out `050010`, `050015`, or `050016`. The client retries that same model call. `Retry-After` is the wait. Otherwise the wait is 5s, then 10s, then 20s. See [README.md](README.md).
- Share one Zeus login across the questions in a pack. Zeus force-closes `X-Zeus-Session` on the 21st tool call. `ask()` drops the cached login before each question ([CR-39](https://kotenai.atlassian.net/browse/CR-39)). A new Hub session id does not reset that counter. HTTP 400 stays in the score. Orange stays a turn whose last HTTP is 400 or higher.

## Run

Working directory is the repo root. The client is the sibling checkout, not a Homebrew install.

```bash
cd /path/to/zeus_chat_request
PYTHONPATH=../zeus_client_python/src \
  ../zeus_client_python/.venv/bin/python -u baseline/run_ab.py --self-check
```

Self-check must print `report verdict check ok` and `self-check ok` before a full run. It does not call Zeus or the model.

Full comparison of the current packs:

```bash
PYTHONPATH=../zeus_client_python/src \
  ../zeus_client_python/.venv/bin/python -u baseline/run_ab.py \
  --pack-a v2/base/base-6.1/min/chat_request_analytics_base-6.1.json \
  --label-a base-6.1 \
  --pack-b v2/base/base-7.x/min/chat_request_analytics_base-7.x.json \
  --label-b base-7.x \
  --provider xai \
  --questions baseline/questions.json \
  --report-date YYYY-MM-DD \
  --reports-dir baseline/reports \
  --out /tmp/chat_request_client_full.json
```

| Flag | Rule |
| --- | --- |
| `--label-a` / `--label-b` | Page title and column headers. Dots become underscores in the file stem. `base-6.1` and `base-7.x` write `base-6_1_vs_base-7_x`. |
| `--report-date` | `YYYY-MM-DD` prefix. Pass it. The default is the machine's today, which can move under a long run. |
| `--questions` | `baseline/questions.json`. Beer has 11 questions and travel has 11: find, search fts, search hybrid, pipeline, narrow_to, and walk_path. `travel-uk-beach-pipeline` is the vague-chain qualification: United Kingdom is `find` where `country` is United Kingdom, and beach is a hybrid `search` whose `narrow_to` is present. `narrow_to: true` in an expect means that field is present and non-empty. The step alias is not scored. `travel-walk-country-hotels` is out until Country documents exist ([CR-38](https://kotenai.atlassian.net/browse/CR-38)). Do not drop another row to balance a score. `baseline/suite.lock.json` is that suite. |
| `--provider` | Overrides `LLM_PROVIDER`. Known names and their URLs are in [README.md](README.md). Default `xai`. `LLM_MODEL` is the model id. `LLM_BASE_URL` overrides the table. |
| Zeus | `ZEUS_URL`, then `GET /version`. Do not copy that URL into another tool's defaults. |

One `run_turn` per question per pack, `rewind=true`, durable `/v2/session`. Beer-sample and travel-sample run at the same time, each on its own runtime. Each question drops that runtime's cached Zeus login before the turn. Questions inside one scope stay in order. The two packs still run one after the other. A log line `{label} running together: beer-sample, travel-sample` marks each pack. Wall time follows the slower scope, twice (once per pack), rather than all 44 turns in series. Judge the log line `EXIT:0`, not a wrapper shell that echoes the code. A progress line looks like `base-6.1 beer-find-style hit=… session=sess_…`. `session=MISSING` is a failed run.

Done means all of these:

1. Log contains `EXIT:0` and `wrote baseline/reports/<stem>.html`.
2. The sibling `<stem>.json` is beside it.
3. Every finished turn has a non-empty `session_id`.
4. The HTML contains the pinned Pico and ECharts URLs, `<h2>Summary</h2>`, the chart ids below, and the hidden `report-contract` comment.

## Next pair

The next comparison is the previous pack against the new pack. Today the previous pack is `base-7.x`. The new pack is whatever base id exists under `v2/base/{label}/`. The test and the page stay the ones in this file.

Keep all of these:

- `baseline/questions.json` and `baseline/suite.lock.json`. Twenty-two questions, beer then travel: eleven beer, eleven travel. `travel-uk-beach-pipeline` qualifies the vague chain. Country → Hotel comes back with [CR-38](https://kotenai.atlassian.net/browse/CR-38).
- One `run_turn` per question per pack, `rewind=true`, durable `/v2/session`. Beer and travel at the same time, each on its own runtime and login. Each question drops the cached Zeus login before the turn. Questions inside one scope stay in file order. Packs stay sequential.
- The verdict rule, columns, colors, marks, charts, and CDN pins below.
- The provider and model of the previous report, unless the user changes them. The finished run was `xai` and `grok-4.7`. The page prints both. A model change is not a pack change. Pass `--provider` or `--model` only to override `baseline/.env`.
- The shared LLM budget gate. Beer and travel share it. It sleeps, it does not shrink the prompt, and it refuses a request larger than the per-request or per-minute cap. Leave that gate in place.
- A new `--report-date`. Do not reuse `2026-10-21` for a new pair. That stem is the finished base-6.1 vs base-7.x report.

Replace `base-8.something` with the real directory name. The label and the filename use that same id. `--self-check` must pass first. Do not pass `--id`.

```bash
PYTHONPATH=../zeus_client_python/src \
  ../zeus_client_python/.venv/bin/python -u baseline/run_ab.py \
  --pack-a v2/base/base-7.x/min/chat_request_analytics_base-7.x.json \
  --label-a base-7.x \
  --pack-b v2/base/base-8.something/min/chat_request_analytics_base-8.something.json \
  --label-b base-8.something \
  --questions baseline/questions.json \
  --report-date YYYY-MM-DD \
  --reports-dir baseline/reports \
  --out /tmp/chat_request_client_full.json
```

`base-7.x` and `base-8.something` write `YYYY-MM-DD_base-7_x_vs_base-8_something.html` and the sibling `.json`. Done is the same four checks as above. The new page has the same sections. Its "What changed in the text" states the system-message delta and any tools added or removed. It does not include the CR-35 story. Size is measured from the two analytics files when both are on disk.

## HTML page, top to bottom

`render_html` is the only writer. Section order:

1. **Title.** `{label-a} vs {label-b}`.
2. **Run line.** Date, Zeus version, provider, model, `zeus_client.run_turn` version.
3. **Summary.**
   - Justification and the score line: each pack `met/total`, `better:worse`, net = better − worse. An Orange row is named on the score line and stays out of that net. A held-out row does not produce a "supports using" line.
   - Suite sums of chart hits and rounds, plus the question ids that moved the score. Row totals stay off this line. A chart hit of 1 with an empty required result still counts in the hit sum and does not count as met.
   - **Answer anchors and plan length.** A second paragraph. It does not change better, worse, or the justification. An anchor is the question's `answer` object: `contains` means every listed document id and field showed up, and extra documents stay; `closed` means the returned ids are a non-empty subset of that list, so an id outside the list misses. Questions without `answer` are not checked. `answer` is not part of `suite.lock.json`. Plan length is the model round where the anchor first showed up, summed only on questions both sides agreed. It is not wall-clock speed. The rounds column stays the full turn.
   - **Suggestion.** A third paragraph. It counts the label recorded on `query_decomposition`: fast path, probe, or not recorded. Analytics and both are named only when a finished turn recorded them. Scout is stored as probe. A return that only names intent and entity is not recorded. A finished side with no stored label is not recorded. This paragraph does not change better, worse, or the justification.
   - **What changed in the text.** For labels `base-6.1` and `base-7.x`, this is the CR-35 story: Plan then call, the search / pipeline / return rewrites, and `rail`. Any other pair whose analytics files are both on disk gets the system-message delta, the verb counts, and the tools added or removed. A missing file says the pack text was not measured. Do not add a causal claim the function does not print.
   - **What in that text shows up in the score.** One bullet per better or worse row: question id, verdict, what each pack called, rounds, rows. No better or worse rows means the added text did not move the score. The walk_path sentence under those bullets is part of the CR-35 story and is not written for a later pair.
   - **Size.** The pack table is measured at render time from `v2/base/{label}/min/chat_request_analytics_{label}.json`. The history of those counts is `v2/base/chat_request_size.csv`. The same command then writes `v2/base/chat_request_size.html` with those rows baked into a static script (see [CREATE_BASE.md](../docs/CREATE_BASE.md)). Open the file. It does not fetch the CSV. Do not hand-copy this section into either file, and do not hand-edit the page. Each cell shows characters, then `tk` on the next line. `tk` is the pack-viewer budget: UTF-8 bytes ÷ 4, rounded up. It is not the model's tokenizer. Rows: analytics file, system message, `search` / `pipeline` / `return` tool JSON, `rail` when either pack has it, the prose-and-tool sum, and the JSON-wrapping remainder. The same character delta on every mode file that exists is one sentence. When the token delta is the same too, that sentence includes it. When rounding makes the token delta differ by a token, the sentence says both numbers. When `scope_briefs` carries `full_chars`, Size continues with the live suffix, one column per dataset: scope brief, mini-schema, walk paths, and the full injection. A following table adds that suffix to each pack's system message. The suffix is the same document for both packs. A report without those counts omits the injection tables. The older `chars` field is the UTF-8 byte length of the scope-brief slice plus the mini-schema slice. Walk paths are the next heading, so they are outside that field.
4. **Hub pointer.** Session lists `session_id`. Inspector and Analysis open a hop `req_id`. `chat_id` is `ab-{date}-{label}-{question-id}` with the label slug (`base-6.1` → `base-6-1`).
5. **Hits, rounds, and rows.** Reading guide, then four suite charts: `chart-suite-hits`, `chart-suite-rounds`, `chart-suite-rows`, `chart-suite-http`. The HTTP chart counts every call at 200, 400, 500, and any other status that showed up. Each scope has the same four charts. If ECharts fails to load, `#chart-note` says the tables still list the three numbers.
6. **Better, worse, and the score.** The definitions below, the hoppy-citrus hybrid rule, the score, the justification again, the suite tally, then the scope-brief provenance (sha12 and client version). The sizes are in Size. Brief text is not stored. An older evidence file without the split still prints the combined byte count and says walk paths are the next heading.
7. **One section per bucket** (`beer-sample`, then `travel-sample`). Scope name, tally, score, four charts `chart-{bucket}-hits|rounds|rows|http`, the empty-hit sentence when that scope has a hit of 1 with 0 rows, then the table.

### Table columns

| Column | Contents |
| --- | --- |
| Question | Question id and the chat string |
| Target API | `expect.all_of` (and `any_of` when present) as verb, shape, strategy, entity type. `(rows required)` when `evidence_required` is true |
| Each pack | Large **hit**, **rounds**, and **rows** first, then the called verbs. A Zeus call whose HTTP status is not 200 wears a badge: orange when Zeus rejected the request, red when Zeus failed the call. The badge names the status, the verb, and the round. It does not change better or worse. When the question has an answer anchor, the next line is `answer agree · plan N`, `answer miss`, or `answer not in sample`. A finished turn shows `suggestion` when the return recorded fast path, probe, analytics, or both. Then HTTP, `session_id`, and `chat_id` in smaller type. When that HTTP is 400 or higher, the line names the source: `LLM`, `Zeus`, or `koten_converter (FUTURE)`. The word `pipeline` is a yellow mark. The word `fts` is an orange mark when the target was hybrid and this side did not call hybrid |
| Versus {label-a} | `better`, `worse`, `both hit`, `both missed`, `Orange`, or `not run`. `both hit` and `both missed` are the old `same` split in two. The score still counts both as same. Orange is a turn that ended on HTTP 400 or higher and stays out of better and worse. An earlier 400 on a turn that ends at 200 stays in the HTTP chart and leaves the verdict on the target-API rule |
| Why | The sentence from `verdict_pair`, or the re-test sentence when the row is Orange |
| Notes | The question fixture note |

A pack cell's hit is `verb_hit` (1 or 0). Rounds are model turns. Rows are the largest `sample.row_count` on that turn, not a sum of hops. A missing side is an em dash. A finished turn with no sample rows shows 0.

Pipeline steps are flattened before scoring. `params` win over the same field on the step. `walk_path` matches `traverse` with `shape` `walk_path`, not a verb named `walk_path`. `rail` is not posted. The client records HTTP 0 when the model calls it.

### Verdict and Why colors

Meeting the target is `verb_hit`. When the question sets `evidence_required`, the Zeus body must also be non-empty. An empty body is not met. A travel 403 does not fail a pack whose evidence is optional and whose verb matched. Rows from a different verb do not count. On "Find hoppy citrus beers" the target is `search hybrid`. That row is worse when the previous pack calls hybrid and the new pack calls fts, find, or set, even when both are HTTP 200 and both returned beers.

| Cell | Class | Color | When |
| --- | --- | --- | --- |
| Versus | `better` | `#21d15a` | New pack met the target and the previous pack did not |
| Versus | `worse` | `#ff2d2d` | Previous pack met the target and the new pack did not |
| Versus | `both hit` / `both missed` | `#8e99a4` | Both met the target, or neither did. The words differ. The grey is the same |
| Chart hint | under that scope's charts |  | A hit of 1 with 0 rows: the verb was called and the stored list was empty. Shown only on a scope that has such a row |
| Versus | `not-run` | `#ffe08a` | A side never reached the model. Left out of the score |
| Versus | `retest` | `#ff8a1e` | The column says Orange. A pack cell ends on HTTP 400 or higher. The row is held out of better and worse until a re-test. The source on the cell is LLM, Zeus, or koten_converter (FUTURE) |
| Why | `why-one` | `#ffe14a` | Exactly one side met the target |
| Why | `why-retest` | `#ffe0c2` | The row is Orange. The sentence names the HTTP status and the source |
| Why | `why-neither` | `#ff8a1e` | Both sides ran and neither met the target |
| Why | none | page background | Both met the target |

Chart series: first pack `#3d5a80`, second pack `#2a9d8f`. Charts do not change the verdict. Extra rows do not flip a row to better.

### Locked assets

```text
https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css
https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js
```

`<html>` carries `data-theme="light"`. Keep both URLs as those exact strings inside `PICO_CSS` and `ECHARTS_JS`.

The first thing inside `<body>` is an HTML comment that starts with `report-contract: baseline/AGENT.md`. It restates the frozen suite, the section order, the versus words, and the CR-35 limit. Browsers do not show it. It is there so the next run can read the page without a second template.

## Evidence JSON

Same stem, `.json` beside the HTML. It is the view `write_bundle` writes: score, tallies, justification, per-scope rows, each side's calls, HTTP status, row sample, `chat_id`, `turn_id`, `session_id`, and hop `req_id` values. It does not store the API key, the password, or the scope-brief text. It can store the injection character, byte, and tk counts per dataset.

## Change the page without a new model run

Style, summary wording, and colors belong in `baseline/report_bundle.py`. After the edit, run `--self-check`, then render the existing evidence file:

```bash
../zeus_client_python/.venv/bin/python - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "baseline")
import report_bundle
stem = "YYYY-MM-DD_base-6_1_vs_base-7_x"
path = Path("baseline/reports") / f"{stem}.html"
view = json.loads(path.with_suffix(".json").read_text())
path.write_text(report_bundle.render_html(view))
path.with_suffix(".json").write_text(json.dumps(view, indent=2, ensure_ascii=False) + "\n")
PY
```

`render_html` applies the Orange rule from each side's stored turn HTTP. Write the sibling JSON after that render when a verdict moves, so the evidence file matches the page. The calls stay. A change to how `verb_hit` is computed still needs a new run, because the stored calls are not re-scored. Open the HTML and confirm the Summary, the four suite charts (`chart-suite-hits`, `chart-suite-rounds`, `chart-suite-rows`, `chart-suite-http`), one yellow Why cell when a row is better or worse, one orange Why cell when both missed, and an Orange Versus cell when a pack ended on HTTP 400 or higher. A run with no worse row does not show a red Versus cell. The red rule still has to be in the stylesheet.
