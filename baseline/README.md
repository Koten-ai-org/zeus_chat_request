# Chat request A/B baseline

Agent run steps and the repeatable HTML contract are in [AGENT.md](AGENT.md). The next pack pair uses that same question file and the same page. The command shape is under **Next pair**.

Compare two `chat_request` packs against one Zeus version and one model. The question file says which verb each chat string should invoke. The locked suite is 22 questions, 11 beer and 11 travel. `travel-uk-beach-pipeline` is the vague-chain qualification: United Kingdom is a `find`, and beach is a hybrid `search` with `narrow_to` inside one pipeline. The runner sends each question through `zeus_client` `ZeusRuntime.agent.run_turn`, which opens a durable `/v2/session` and posts the model's tool calls with the trace headers Hub Debug needs.

This does not change the shared pin. Hotel and beer phrases stay in this folder.

## Dimensions recorded on every run

| Dimension | Where it comes from |
| --- | --- |
| Pack A / pack B | `--pack-a` and `--pack-b` (`_lineage.base_id`) |
| Model | `LLM_MODEL` in `baseline/.env`, or `--model` |
| Provider | `LLM_PROVIDER` in `baseline/.env`, or `--provider`. `LLM_BASE_URL` overrides the table below |
| Zeus version | `GET /version` on `ZEUS_URL` or `--zeus-url` |

## Run

Copy `example.env` to `baseline/.env` and fill the blanks. `.env.example` is the same template. `baseline/.env` is gitignored. A name already exported in the shell wins over the file. A flag wins over the file: `--provider`, `--base-url`, and `--model`.

`LLM_PROVIDER` selects the API. `LLM_MODEL` is that provider's model id. Put that provider's key in `LLM_API_KEY`. `LLM_BASE_URL` is optional and replaces the URL in the table. The example uses `LLM_PROVIDER=xai` and `LLM_MODEL=grok-4.7`.

Beer questions and travel questions run at the same time. Each scope has its own runtime and its own login. Each question drops that runtime's cached Zeus login before the turn, because the round cap is on `X-Zeus-Session`. Questions inside one scope stay in file order. The two packs still run one after the other. Both scopes share one provider budget, because they share one API key. The run prints one `pace` line with the caps it will enforce.

Beer questions use `ZEUS_USER_BEER` and `ZEUS_PASS_BEER`. Travel questions use `ZEUS_USER_TRAVEL` and `ZEUS_PASS_TRAVEL`. The runner does not reuse a beer session for travel.

The client is not installed into Homebrew Python. Use the sibling checkout's virtualenv and put its `src` on `PYTHONPATH`. `ZEUS_CLIENT_SRC` overrides that `src` directory.

```bash
export PYTHONPATH=../zeus_client_python/src
../zeus_client_python/.venv/bin/python baseline/run_ab.py \
  --pack-a v2/base/base-6.1/min/chat_request_analytics_base-6.1.json \
  --label-a base-6.1 \
  --pack-b v2/base/base-7.x/min/chat_request_analytics_base-7.x.json \
  --label-b base-7.x \
  --provider xai \
  --questions baseline/questions.json \
  --out /tmp/chat_request_ab.json
```

Each question calls `run_turn` with the local pack, `force_trace`, and `rewind=true`. The client posts `/v2/session`, then the verb hops, including pipeline. Beer and travel stay on separate logins (`password_env` is the variable name). The harness drops the cached login before the question so the 20-call cap starts over. If a turn finishes with an empty `session_id`, both scopes stop after the turn already in flight, and the runner does not overwrite the comparison HTML.

## Providers

The runner uses `zeus_client`'s OpenAI-compatible client. It sends `POST {base}/chat/completions` with a bearer token and tool calls. The base URL must not already end in `/chat/completions`. A provider that rejects tools will not drive the Zeus verbs.

Change provider by editing `baseline/.env`. A name that is not in this table works when `LLM_BASE_URL` is set to an OpenAI-compatible base.

| `LLM_PROVIDER` | Base URL | OpenAI chat completions | Documentation |
| --- | --- | --- | --- |
| `xai` | `https://api.x.ai/v1` | yes | [Chat completions](https://docs.x.ai/docs/guides/chat-completions) |
| `openai` | `https://api.openai.com/v1` | yes, this is the native API | [Chat](https://platform.openai.com/docs/api-reference/chat) |
| `groq` | `https://api.groq.com/openai/v1` | yes | [OpenAI compatibility](https://console.groq.com/docs/openai) |
| `together` | `https://api.together.xyz/v1` | yes | [OpenAI compatibility](https://docs.together.ai/docs/inference/openai-compatibility) |
| `fireworks` | `https://api.fireworks.ai/inference/v1` | yes | [OpenAI compatibility](https://docs.fireworks.ai/tools-sdks/openai-compatibility) |
| `openrouter` | `https://openrouter.ai/api/v1` | yes | [Quickstart](https://openrouter.ai/docs/quickstart) |
| `deepseek` | `https://api.deepseek.com` | yes | [API docs](https://api-docs.deepseek.com/) |
| `mistral` | `https://api.mistral.ai/v1` | yes | [API](https://docs.mistral.ai/api/) |
| `cerebras` | `https://api.cerebras.ai/v1` | yes | [Chat completions](https://inference-docs.cerebras.ai/api-reference/chat-completions) |
| `gemini` | `https://generativelanguage.googleapis.com/v1beta/openai` | yes, OpenAI-compatible layer | [OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai) |
| `perplexity` | `https://api.perplexity.ai/v2` | yes | [OpenAI compatibility](https://docs.perplexity.ai/docs/grounded-llm/openai-compatibility) |

A local server uses the same shape. Set `LLM_PROVIDER` to any name and `LLM_BASE_URL` to the server, for example `http://localhost:11434/v1` (Ollama), `http://localhost:1234/v1` (LM Studio), or `http://localhost:8000/v1` (vLLM). A local or unknown name uses the harness floor in the budget section.

## Provider budgets

Published numbers below were read on 2026-10-22. The provider console is the account number when it disagrees with this table. The code column is what the script enforces. Where a single published RPM, RPS, or TPM exists, the code number is 80% of that published number, rounded down (`max(1, published * 4 // 5)`). The harness floor is already the enforced ceiling and is not reduced again.

Beer and travel reserve against one 60-second window before each model call. The estimate is the same `tk` as the report: UTF-8 bytes of the messages and tools divided by 4, rounded up, plus `max_tokens` when the request sets it, otherwise 1,024. It is not the model's tokenizer. After the response, the script replaces that reservation with provider usage: prompt tokens plus completion tokens, or `total_tokens` when that is larger. Cached tokens are not subtracted.

The script does not shrink the prompt. A request larger than the per-request cap, or larger than the whole per-minute token cap, stops both scopes after the turn already in flight. The comparison HTML and JSON are not written. A request that can fit later sleeps until the window has room. The script does not enforce a daily or hourly cap. The script does not sleep between questions.

A provider response classified as `050010` (rate limit), `050015` (overload), or `050016` (unavailable) is retried on that same model call. The turn keeps the Zeus tool results it already has. When the provider sends a numeric `Retry-After`, that number of seconds is the wait. Without that header the wait is 5 seconds, then 10, then 20. Three extra attempts. The extra wait on one call stays inside 60 seconds. A header longer than the remaining budget ends the call instead of sleeping part of it. A timeout (`050005`) keeps the short transport backoff. The question scores **not run** only when those retries are exhausted and the turn never reached Zeus. A later model call that still fails after the retries stops the turn and the score uses the Zeus calls already made.

`LLM_TPM`, `LLM_RPM`, `LLM_RPS`, and `LLM_REQUEST_TOKENS` replace that one dimension. They are used as written. Set them below the console number. `0` blocks that dimension. Unset keeps the code column. The pace line looks like `pace provider=xai model=grok-4.7 rps=120 rpm=- tpm=40000000 request_tokens=- source=xai-tier0-80pct`.

The harness floor is RPM 60 and TPM 100,000, with no per-request cap. It is a code ceiling for providers that do not publish one RPM and one TPM this script can apply. It is not that provider's published rate.

| Provider | Published limit | Code restriction |
| --- | --- | --- |
| `xai` | [Rate limits](https://docs.x.ai/developers/rate-limits). Tier is cumulative spend since 2026-01-01. Tier 0 is $0. The console Models page is the account number. 429 when either cap is exceeded. Cached prompt tokens count toward TPM. No separate per-request token cap on that page. Tier 0: grok-4.7, grok-4.6, grok-4.5 are 150 RPS and 50M TPM. grok-4.3, grok-4.20-0309-reasoning, grok-4.20-0309-non-reasoning, and grok-build-0.1 are 37 RPS and 10M TPM. grok-4.20-multi-agent-0309 is 9 RPS and 2.5M TPM. | 80% of Tier 0. grok-4.7, grok-4.6, grok-4.5: RPS 120, TPM 40,000,000. The 37 RPS group: RPS 29, TPM 8,000,000. grok-4.20-multi-agent-0309: RPS 7, TPM 2,000,000. Any other xAI model id uses the grok-4.7 code row. No RPM and no per-request cap unless the env keys are set. |
| `groq` | [Rate limits](https://console.groq.com/docs/rate-limits). Developer-plan base for `openai/gpt-oss-120b` and `openai/gpt-oss-20b`: 30 RPM, 1K RPD, 8K TPM, 200K TPD. Other rows differ. The console Limits page is the account number. Higher limits exist for some workloads. | RPM 24 and TPM 6,400 for every Groq model id. A pack estimates above 6,400 tokens, so the runner stops before the first model call unless `LLM_TPM` and `LLM_RPM` are set to the console numbers. |
| `cerebras` | [Rate limits](https://inference-docs.cerebras.ai/support/rate-limits). Free trial for `gpt-oss-120b` and `qwen-3.8-27b`: 5 RPM, 30K uncached TPM, 90K total TPM, plus 1M TPH and 1M TPD. Developer pay-as-you-go is higher and per model. Any metric can trip first. The console Limits page is the account number. | RPM 4 and TPM 24,000 (80% of the uncached 30K), for every Cerebras model id. Set `LLM_TPM` and `LLM_RPM` when the console is the paid tier. |
| `deepseek` | [Rate limit](https://api-docs.deepseek.com/quick_start/rate_limit). Concurrency, not TPM. `deepseek-flash` is 2,500 and `deepseek-v4-pro` is 500, per account. 429 when concurrency is exceeded. | No RPM, RPS, or TPM. Two scopes sit under that concurrency cap. The shared gate still applies `LLM_TPM`, `LLM_RPM`, `LLM_RPS`, and `LLM_REQUEST_TOKENS` when they are set. |
| `openrouter` | [Limits](https://openrouter.ai/docs/api-reference/limits). A model id ending in `:free` is 20 RPM. Daily cap is 50 requests when fewer than 10 credits have been purchased, and 1,000 after that. Paid model ids have no OpenRouter plan RPM. Upstream provider limits apply. Extreme bursts can 429 from DDoS protection. | A model id ending in `:free`: RPM 16, no TPM. Any other model id: the harness floor. The daily cap is not enforced here. |
| `openai` | [Rate limits](https://platform.openai.com/docs/guides/rate-limits). Measured as RPM, RPD, TPM, TPD, and IPM. Some model families share one limit. The dashboard is the number. Usage tiers are spend qualifications, not one RPM or TPM. | Harness floor. This is not an OpenAI published rate. |
| `mistral` | [Usage limits](https://docs.mistral.ai/admin/billing-usage/usage-limits). RPS and TPM are enforced independently, plus tokens per month. That page does not print a free-tier TPM. The console Limits page is the number. | Harness floor. This is not a Mistral published rate. |
| `gemini` | [Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits). RPM, input TPM, and RPD, per project. The page does not print a free-tier number table. AI Studio is the account number. Paid tiers also have spend caps. | Harness floor. This is not a Gemini published rate. |
| `together`, `fireworks`, `perplexity` | Limits are per account and per model. This table does not print an RPM or TPM for them. The provider console is the number. | Harness floor until `LLM_TPM`, `LLM_RPM`, or `LLM_RPS` is set. |
| local or unknown | No published cap. | Harness floor, unless the env keys are set. |

`--self-check` scores a fake trace, exercises this gate with no network, and does not call the model.

A pass on the prompt is `verb_hit`. `evidence_nonempty` is a separate Zeus column. HTTP 403 or an empty travel scope does not, by itself, fail the pack.

## Report files

Each comparison writes two files with the same stem:

```text
baseline/reports/YYYY-MM-DD_base-6_1_vs_base-7_x.html
baseline/reports/YYYY-MM-DD_base-6_1_vs_base-7_x.json
```

The HTML file opens with a summary of what changed in the pack text, which rows moved the score, and the file-size delta. Below that are the two tables plus charts for hits, rounds, and rows. A hit of 1 means that pack called the target API. Rows are the largest Zeus result on that turn. Rounds are the model turns used. The page loads Pico CSS `2.0.6` and Apache ECharts `5.6.0` from jsDelivr. Those versions are pinned. The top of the file still defines better and worse and prints the score: each pack's met/total, the better:worse ratio, and the net (better minus worse). The charts do not change that verdict.

The JSON file is the evidence for those tables: the target API, the verdict, why, and for each pack the calls, the HTTP status, and a short preview of the rows Zeus returned. Each side also stores `chat_id`, `turn_id`, `session_id`, and the hop `req_id` values. Hub Debug → Session lists `session_id`. Inspector and Analysis open a `req_id` from that session. `chat_id` looks like `ab-2026-10-21-base-6-1-beer-find-style`. The file does not store the API key or the basic-auth secret.

The pack id on this branch is `base-7.x`. The date is the day of the run.

There are two tables, `beer-sample` and `travel-sample`. Each row is one question. The columns are the question, the API it should hit, what each pack called, a verdict, why, and the fixture note.

The verdict is the new pack compared with the previous pack:

| Verdict | Meaning |
| --- | --- |
| better | base-7.x called the target API and base-6.1 did not |
| worse | base-6.1 called the target API and base-7.x did not. Rows from another verb do not count |
| same | both called it, or neither did |
| not run | a model call is missing, so the row cannot justify a pack change |

Score is `met/total` for each pack, `better:worse`, and net = better − worse. A positive net means base-7.x covered more missed targets than it lost.

A hit is `verb_hit`. When the question says rows are required, an empty Zeus body is not a hit. The opening paragraph states whether the tally justifies switching packs. A file that is entirely `not run` does not.

`--preview-report` writes that shell, HTML and JSON, from `questions.json` and does not call the model. A real run overwrites both files after the model calls. `--out` is a separate raw trace and is not the evidence file.

The live `## SCOPE BRIEF`, including `## MINI-SCHEMA` and `## WALK_PATHS`, is merged inside `run_turn` (`ensure_scope_brief` keeps the local pack and splices the live suffix). The pack's own system text and verbs stay. The client virtualenv supplies `httpx`. The Size section lists that suffix per dataset: scope brief, mini-schema, walk paths, and the full injection, then the system message after the suffix is appended.

```bash
python3 baseline/run_ab.py --preview-report \
  --label-a base-6.1 \
  --label-b base-7.x \
  --report-date 2026-10-21
```

## Lab notes from the 0.9.19 probe

- Beer graph collection is `nodes`. Hybrid "hoppy citrus" and style equality `American-Style India Pale Ale` returned rows for `tester_beer`.
- FTS "lager" returned hits whose body was a `doc_key` only.
- `abort_if_empty` on a hybrid step aborted after 40 ids. The runner still records the status.
- Scope briefs reported `nodes_total: 0` while search returned rows.
- The same session could read the travel-sample brief and received 403 on travel data verbs. Travel evidence stays optional until a principal for that scope is used.
- `rail` is not posted. Zeus 0.9.19 has no such route. `zeus_client` rejects it before HTTP, and the harness records that call with HTTP 0.

## Walk path probes on 0.9.19

The pack's tool is `traverse` with `shape` `walk_path`. The scorer checks that pair. It does not require the path array. A name in the question may need a seed search before the walk, because the one-round-trip body already assumes a `doc_key`.

| Question | What the lab returned |
| --- | --- |
| Where is 21A IPA brewed? | One row: 21st Amendment Brewery Cafe, San Francisco, California. Beer key `21st_amendment_brewery_cafe-21a_ipa`, path `brewery_id`. |
| Beers by Stone Brewing | Inverse `Beer.brewery_id` from `stone_brewing_co`. `stone_brewing` is not the live key. |
| Beers from Belgian breweries | Forward walk from Beer with an empty `where` is HTTP 400. `Brewery` where `country` is `belgium`, then the inverse to Beer, returned rows. |
| Beers per Colorado brewery | `group_by` as an array is HTTP 400. `group_by` `brewery.name` is rejected (terminal-local only). `where` `state` `colorado` matched. |
| Beers by country | The demo body did not execute. Empty `where` is not a selector, and `group_by` must be a string. |
| Colorado trip | `find` returned 40 breweries and was truncated. City and state were absent on that projection. `get` metadata has the city. The City entity walk returned 0 rows. |

The comparison table and its evidence JSON go to `baseline/reports/`. The raw trace defaults to the `--out` path. Do not commit passwords. A `not run` pair may be kept so the table shape is visible before the first model run.
