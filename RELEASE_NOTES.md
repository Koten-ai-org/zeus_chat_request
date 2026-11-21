# Release notes — zeus_chat_request

Published **Zeus V2 chat_request** catalogs for Zeus Client, Developer Helper MCP, demos, and coding agents.

| | |
| --- | --- |
| **Repo** | https://github.com/koten-ai/zeus_chat_request |
| **Format** | `zeus.chat_request.v2` |
| **Production pin** | **base-1** — `CURRENT.json` · `v2/min/` |
| **Candidate pack** | **base-5** wire line — `v2/base/base-5/` (last breaking freeze; not pin) |
| **Content train** | **base-8.0** — constitution morph, numbered name of base-8-prototype-1 ([v2/base/base-8.0/](v2/base/base-8.0/)). Parent **base-7.4**. The earlier folders base-8-prototype and base-8-prototype-1 stay. The local Zeus 5.5TH tree still serves **base-7.1** and also embeds base-6.1. `CURRENT.json` stays base-1. Suite not run. |
| **Prior content** | base-6.1 report stamps · base-6 soft `hints.*` · base-5.3 skinny/world-model · base-5.2 dual gaps · base-5.1 modes |
| **Prior candidate** | **base-4** — `v2/base/base-4/` |
| **Roadmap** | [ROADMAP.md](docs/ROADMAP.md) |
| **Modes** | [MODE.md](docs/MODE.md) · [work/RECREATE_MODE.md](work/RECREATE_MODE.md) |
| **Helios emit wishlist** | [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) |

---

## Unreleased (toward next tag)

### Highlights

- **base-8.0 constitution morph:** [`v2/base/base-8.0/`](v2/base/base-8.0/) — numbered name of [`v2/base/base-8-prototype-1/`](v2/base/base-8-prototype-1/), parent **base-7.4**, **additive** (not a wire break). `CURRENT.json` stays **base-1**. The local Zeus embed is still **base-6.1** and **base-7.1**. The earlier folders `base-8-prototype` and `base-8-prototype-1` stay. The 21-question suite has not been run. The lab image may still list `base-8-prototype-1` until it is rebuilt. An unpicked chat on that image still serves base-7.0.
  - The plan states the access rule once. `narrow_to` takes node ids only. `query_decomposition` records fast path or one probe. Two intents that share a world are two chains in one pipeline. A shared value is probed once. `project` has no `limit`; `order` takes `limit`.
  - Each mode keeps the contract hash copied from its base-7.4 file. The hash was not invented. `assemble_mode_prompts.py` was not run. `_base_meta.base_id` is still the inherited `base-6.1`. `contract.parent_base_id` is still the inherited `base-5.1` stamp.
  - `verify_base_pack.py --base 8.0` and `diff_modes.py --fail-if-clone` passed. `scan_catalogs.py` count is **200**. Open exam issues on base-8.0 are 0. That count is the gate, not accuracy.
  - Hop: [docs/migration/base-7.4_to_base-8.0/](docs/migration/base-7.4_to_base-8.0/)
- **base-7.4 call align:** [`v2/base/base-7.4/`](v2/base/base-7.4/) — cut from base-7.3, **additive** (not a wire break). `CURRENT.json` stays **base-1**. The local Zeus embed is still **base-6.1** and **base-7.1**. The 21-question suite has not been run on this pack.
  - The plan, the tool text, and the mode examples describe the same call. `narrow_to` follows node ids. The typical chain is `search` → `project` `@step.doc_keys`. `project` has no `limit`; the ranked example caps `order`.
  - Do not bind `@step.ids`; that name is node ids only. `set` requires `id_kind`. Search examples are unchanged. The contract hash was copied. `assemble_mode_prompts.py` was not run.
  - Analytics system growth versus base-7.3 is **+69** characters. File growth is **+677** characters on analytics. The token delta is not shared across modes. `verify_base_pack.py --base 7.4` and `diff_modes.py --fail-if-clone` passed. `scan_catalogs.py` count is **170**.
  - Hop: [docs/migration/base-7.3_to_base-7.4/](docs/migration/base-7.3_to_base-7.4/)
- **base-7.3 walk close:** [`v2/base/base-7.3/`](v2/base/base-7.3/) — cut from base-7.2, **additive** (not a wire break). `CURRENT.json` stays **base-1**. The local Zeus embed is still **base-6.1** and **base-7.1**. The 21-question suite has not been run on this pack.
  - A known stored value stays `find`, unless that value is the other end of a WALK_PATHS chain.
  - The related-type close is still `traverse` `walk_path` with `from.src_keys` `@step.doc_keys`, even when the seed row already shows that field.
  - The slot rule from base-7.2 stays. `@step.ids` stays node ids only. The contract hash was copied, not invented. `assemble_mode_prompts.py` was not run.
  - System growth versus base-7.2 is **+156** characters on every mode. Every mode file grows **+247** characters. The token delta is **+61** or **+62** (analytics **+61**). `verify_base_pack.py --base 7.3` and `diff_modes.py --fail-if-clone` passed. `scan_catalogs.py` count is **160**.
  - Hop: [docs/migration/base-7.2_to_base-7.3/](docs/migration/base-7.2_to_base-7.3/)
- **base-7.2 slot rule:** [`v2/base/base-7.2/`](v2/base/base-7.2/) — cut from base-7.1, **additive** (not a wire break). `CURRENT.json` stays **base-1**. The local Zeus embed is still **base-6.1** and **base-7.1**. One 21-question pass on 2026-11-20 scored base-7.1 20/21 vs base-7.2 16/21, net −4.
  - Copy `@step.node_ids` into a node-id slot: get, hop, bfs, path, subgraph, `narrow_to`, analyze.
  - Copy `@step.doc_keys` into `walk_path` `src_keys`.
  - `project`, `order`, and `enrich` accept either list. FTS search leaves `node_ids` empty, so do not `narrow_to` that step.
  - `@step.ids` stays node ids only. The contract hash was copied, not invented. `assemble_mode_prompts.py` was not run.
  - System growth versus base-7.1 is **+156** characters on every mode. `verify_base_pack.py --base 7.2` and `diff_modes.py --fail-if-clone` passed. `scan_catalogs.py` count is **150**.
  - Hop: [docs/migration/base-7.1_to_base-7.2/](docs/migration/base-7.1_to_base-7.2/)
- **base-7.1 binding fix (CR-40):** [`v2/base/base-7.1/`](v2/base/base-7.1/) — cut from the working base-7.0 tree, **additive** (not a wire break). `CURRENT.json` stays **base-1**. The local Zeus 5.5TH tree embeds **base-6.1** and **base-7.1**. The served pin in that tree is **base-7.1**. The lab image still serves base-7.0. The 21-question suite has not been run on this pack.
  - After an FTS `search`, bind `@step.doc_keys`. After `find`, hybrid, or node-vector, bind `@step.node_ids`. `@step.ids` stays node ids only.
  - Analytics ranked-list example uses `@cands.node_ids` and `@ord.node_ids`.
  - System growth versus base-7.0 is **+384** characters on nine modes and **+394** on analytics.
  - `verify_base_pack.py --base 7.1` and `diff_modes.py --fail-if-clone` passed. `scan_catalogs.py` count is **140**. `assemble_mode_prompts.py` was not run. The contract hash was copied, not invented.
  - Hop: [docs/migration/base-7.0_to_base-7.1/](docs/migration/base-7.0_to_base-7.1/)
  - Residual: 21-question suite · lab image · CURRENT pin. [CR-40](https://kotenai.atlassian.net/browse/CR-40) stays open.
- **base-7.0 content train (CR-35, CR-37):** [`v2/base/base-7.0/`](v2/base/base-7.0/) — previous numbered ship of [`v2/base/base-7.x/`](v2/base/base-7.x/), parent chain `base-7.x` ← `base-6.1`, **additive** (not a wire break). `CURRENT.json` stays **base-1**. The 21-question suite is net +2 with one Orange row still out. The France beach retest is a tie and does not replace that page.
  - **Plan, then call:** world, entry, path, goal, at most 8 calls. One drill-down is one pipeline.
  - New **`rail`** verb on all 10 modes: `name` from the SCOPE BRIEF, `binds` only, no SQL. Catalog teaching. Zeus does not execute `rail` yet.
  - **14 verbs** (base-6.1's thirteen plus `rail`). Required Layer A four unchanged.
  - Boolean and `one_of` rows: MINI-SCHEMA, `find`, and `where` teach the law. Tenant value lists stay on the entity map.
  - Prompt growth versus base-6.1 about **+3043 characters (~12%)** on every mode. The base-6.2 size cut is not the parent.
  - `verify_base_pack.py --base 7.0` and `diff_modes.py --fail-if-clone` passed.
  - Hop: [docs/migration/base-6.1_to_base-7.0/](docs/migration/base-6.1_to_base-7.0/)
  - Residual: stamped `rail` run · A/B books (CR-36) · Zeus vendor · CURRENT pin
- **base-6.2 content train (CR-34):** [`v2/base/base-6.2/`](v2/base/base-6.2/) — parent `base-6.1`, **content skinny only** (not a wire break):
  - CORE system diet: world-model / efficiency / Terminate compressed; Client `user`/`ip` enum out of model prompt
  - Tools diet: thinner `return` descriptions; `pipeline` terminating Layer A thin-refs `return` (no deep G2 trees)
  - **All 13 verbs** retained; required four + dual gaps + progressive-empty one-liner kept
  - Measured analytics min prefix (system+tools): ~**6.4k → ~4.8k tokens (~−25%)**
  - Hop: [docs/migration/base-6.1_to_base-6.2/](docs/migration/base-6.1_to_base-6.2/)
  - Residual: A/B books 6.1 vs 6.2 · optional Zeus vendor later
- **base-6.1 content train:** [`v2/base/base-6.1/`](v2/base/base-6.1/) — parent `base-6`, **additive only**:
  - Root report field **`user`**: `zeus_client` | `zeus` | `helios` | `admin` (product Client stamps `zeus_client`)
  - Root report field **`ip_address`**: IPv4 or IPv6 string when known (omit when unknown; never invent)
  - Client setting **`ai_process_result`** (bool, **default false**) — optional post-Zeus AI insight turn
  - Machine JSON: [`report_sink_schema.json`](v2/base/base-6.1/report_sink_schema.json) + example (stamps **not** on Layer A `response_output_*`)
  - Settings companion: [`settings_ai_process_result.example.json`](v2/base/base-6.1/settings_ai_process_result.example.json)
  - Thin CORE note: cheap default after tools; re-call only when Client enables insight; never invent `user` / `ip_address`
  - Hop: [docs/migration/base-6_to_base-6.1/](docs/migration/base-6_to_base-6.1/)
  - Client residual: **ZC-WISH-035**, **ZC-WISH-044** · Helios filter: **HEL-WISH-022** · Jira **CR-27** (pack) / **CR-28…30** (residual)
  - Client wishlist: stripped Helios Pri-3 bulk (locale/channel/market…); Helios SoT remains [HELIOS_WISHLIST…](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)
- **base-6 content train (CR-4):** [`v2/base/base-6/`](v2/base/base-6/) — parent `base-5.3`, **additive only** (not a wire break):
  - Soft **`hints.*`** inject contract — [docs/HINTS.md](docs/HINTS.md) (P0 path/fields/multipart; P1 hot_path; caps; multi-intent ≠ open)
  - Thin CORE note: hash-excluded hints after hard `rules{}` never replace jailbreak / company / MINI-SCHEMA
  - Retains base-5.3 world-model + verb clarity + dual gaps
  - Hop: [docs/migration/base-5.3_to_base-6/](docs/migration/base-5.3_to_base-6/)
  - Client runtime inject residual: **ZC-WISH-040**
- **base-5.3 content train (CR-26):** [`v2/base/base-5.3/`](v2/base/base-5.3/) — parent `base-5.2`, **not a wire break**:
  - World-model CORE blurb (AI-Ready overlay · MINI-SCHEMA shape · access path → verb · evidence-only Layer A)
  - Verb catalog clarity: all 13 tools WHEN/WHEN NOT/KEY aligned to Zeus `docs/API/V2`
  - **P0:** `order` uses `by: "field:<name>"` + `asc` (system no longer teaches `direction`)
  - `search` properties include `timeout_ms`, `where`, `seed_node_id`; `describe` gains `include`
  - Dual gaps from base-5.2 retained
  - Hop: [docs/migration/base-5.2_to_base-5.3/](docs/migration/base-5.2_to_base-5.3/)
- **Pack trains = snapshot folders (CR-25):** full trees for pull + JSON Diff — not in-place `content_train`:
  - [`v2/base/base-5/`](v2/base/base-5/) — wire freeze (objects, `app_output`; no mode overlays)
  - [`v2/base/base-5.1/`](v2/base/base-5.1/) — CORE + MODE_OVERLAY system prompts
  - [`v2/base/base-5.2/`](v2/base/base-5.2/) — dual gaps (`data_gaps` + design [WISH_I_KNEW_DUAL.md](docs/WISH_I_KNEW_DUAL.md))
  - [`v2/base/base-5.3/`](v2/base/base-5.3/) — skinny + world-model + verb clarity
  - [`v2/base/base-6/`](v2/base/base-6/) — soft hints contract
- **base-5.1 modes:** Author under `work/mode_overlays/`; `assemble_mode_prompts.py --base 6` for this train; `diff_modes.py --fail-if-clone`.
- Pin remains **base-1**. Zeus **0.6.15+** vendors **base-5.3** ([ZE-273](https://kotenai.atlassian.net/browse/ZE-273)); base-6 is candidate until Client inject + optional engine pin.
- Hop docs: [docs/migration/base-4_to_base-5/](docs/migration/base-4_to_base-5/), [base-5.2_to_base-5.3](docs/migration/base-5.2_to_base-5.3/), [base-5.3_to_base-6](docs/migration/base-5.3_to_base-6/).
- Docs/process: AI playbook, COMPAT, RELEASE_CHECKLIST, `verify_base_pack.py`, `new_base.py`.

### Breaking changes (opt-in **base-5**)

> **Pin is still base-1.** These apply when you **opt in** to base-5 catalogs.

| Breaking change | Who is affected | Mitigation |
| --- | --- | --- |
| **`business_rules_triggers` is an object** `{ rule_id: bool }` (not `boolean[]`) | Clients/parsers assuming array indexes | Parse object; missing key = false; dual-read arrays ≤1 Client release |
| **Inject `rules` is an object** `{ id: text }` | Clients building parallel arrays | Use named keys; merge/freeze per PROMPT_SETTINGS |
| **Optional `app_output`** on terminate | Strict tool schema rejecting unknown props | Allow optional object; validate against Client `output_request` |
| **`output_request` fields need type + description** | Type-only maps | Client renders descriptions into prompt; reject type-only |
| **Filename `*_base-5.json`** | Loaders only knowing `v2_min` or base-4 | Accept `base-N` pattern from COMPAT / manifest |
| **New stamp required** for any production use of base-5 | Anyone copying scaffold hashes | Hub verify/stamp only |

### Breaking changes (opt-in **base-4** / prototypes — still valid)

> Breakage when opting into base-4 (or base-2-prototype) vs base-1 pin only.

| Breaking change | Who is affected | Mitigation |
| --- | --- | --- |
| **Filename pattern** | Loaders that only glob `*_v2_min.json` | Accept `*_base-N.json` |
| **`return` / pipeline params grow** (recommended Layer A) | Strict unknown-property clients | Treat extra props optional; required four unchanged |
| **Terminate contract rewritten (base-4)** | Hash comparisons to base-1 system text | New stamp after opt-in |
| **Prototype packs are not production stamps** | Copying `contract.hash` from trees | Hub stamp only |

**Non-breaking for base-1 pin consumers:**  
`v2/min/` and `CURRENT.json` remain base-1; existing `*_v2_min.json` paths and the **required four** terminate fields are unchanged on that pin.

### base-4 (`v2/base/base-4/`)

| Item | Detail |
| --- | --- |
| Files | `min/chat_request_<mode>_base-4.json` · `text/chat_request_<mode>_base-4.txt` |
| Diet | Single `## Terminate (Layer A)` table + example (merged old Evidence-loop + Layer A essays) |
| Layer A required | `summary`, `query_decomposition`, `decomposition`, `confidence` |
| Layer A recommended | `policy_action`, `subject_confidence`, `jail_break_attempt`, `wish_i_knew`, `business_rules_triggers`, refs |
| Docs | [BIBLE.md](docs/BIBLE.md) · [BASE_1_TO_BASE_4_GUIDE.md](docs/migration/base-1_to_base-4/GUIDE.md) · [lessons-learned.md](docs/migration/base-1_to_base-4/lessons-learned.md) · [MULTI_ROUND_CLIENT.md](docs/MULTI_ROUND_CLIENT.md) · [JAILBREAK_POLICY.md](docs/JAILBREAK_POLICY.md) |
| Schema | [response_output_schema.json](v2/base/base-4/response_output_schema.json) |
| Helios | Aligns with wishlist **cost law**; does **not** add Pri-1 Helios fields as always-on AI emits (see ROADMAP) |

### base-3-prototype

- Indented text packs for diet/edit; generator [`scripts/export_base_text.py`](scripts/export_base_text.py).

### base-2-prototype

- Design fork introducing extended Layer A fields and base-N naming (historical / Diff).

### Inspector / tooling

- [`scripts/scan_catalogs.py`](scripts/scan_catalogs.py) — mode parse for `*_base-N.json` and `*_cus_*`.
- [`index.html`](index.html) — multi-BASE dropdown labels; Help for base-1 vs base-4; **one page** (no `index-base-4.html`).

### Docs

- [ROADMAP.md](docs/ROADMAP.md) — base-5+ **and** Helios HEL-WISH sequencing  
- [PROMPT_ASSEMBLY.md](docs/PROMPT_ASSEMBLY.md), [simple_layout.txt](docs/simple_layout.txt), [base_layout.txt](docs/base_layout.txt)  
- [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) — structured Requests (HEL-WISH-001–021)

### Helios (roadmap alignment — not all shipped in catalogs)

| Horizon | Helios focus (see ROADMAP) |
| --- | --- |
| base-5 | Pri-1 cheap spine on **Zeus/Client** (003, 008, 013, 014, 007, 009) + Layer A reliability |
| base-6 | Norms / geo_norm / multi_part / deployment slice (001, 002, 012, 016, …) + G2 Layer A discipline |
| base-7+ | Product events 018/019, stamp/Workbench, pin promote; AI-heavy 010 off hot path |

### Upgrade notes (opt-in base-4)

```bash
# Inspector
python3 scripts/scan_catalogs.py
docker compose up   # http://localhost:3333/index.html — Diff base-1 vs base-4

# Client (sketch)
# 1. Load v2/base/base-4/min/chat_request_<mode>_base-4.json
# 2. Accept extra return properties; validate required four
# 3. Map policy_action / business_rules_triggers when present
# 4. Stamp on Hub before production — do not use prototype/candidate hashes as prod
```

### Known limitations (unreleased)

- Production pin still base-1.  
- base-4 not Hub-stamped by default.  
- Helios Pri-1 report fields are **roadmap**, not all present in catalog JSON.  
- Text packs are not a substitute for stamped JSON in production.

---

## 0.1.0 — Initial public distribution

**Date:** 2026-07-16  
**Git:** `e342ebc` (`main`)

### Highlights

- First release of **integrator-facing** V2 **min** mode catalogs (no Zeus monorepo required).
- Sourced from Zeus engine generation path: `ai/V2/variants/min/` (`ai-snapshot --min`).
- Machine-readable **`manifest.json`** (mode, path, sha256, verb_count, template contract metadata).
- Scripts to refresh from a local Zeus checkout.

### Catalogs included (10 modes)

| Mode | File |
| --- | --- |
| analytics | `v2/min/chat_request_analytics_v2_min.json` |
| auto | `v2/min/chat_request_auto_v2_min.json` |
| code | `v2/min/chat_request_code_v2_min.json` |
| custom | `v2/min/chat_request_custom_v2_min.json` |
| fraud | `v2/min/chat_request_fraud_v2_min.json` |
| open | `v2/min/chat_request_open_v2_min.json` |
| private | `v2/min/chat_request_private_v2_min.json` |
| regulated | `v2/min/chat_request_regulated_v2_min.json` |
| research | `v2/min/chat_request_research_v2_min.json` |
| tenant | `v2/min/chat_request_tenant_v2_min.json` |

Typical payload size: ~13–15 KB per mode (min profile). Verb surface: **13** verbs per catalog in this snapshot set.

### Repo layout (at 0.1.0)

```text
zeus_chat_request/
├── README.md
├── RELEASE_NOTES.md
├── manifest.json
├── scripts/
│   ├── sync-from-zeus.sh
│   └── refresh_manifest.py
└── v2/min/
    └── chat_request_*_v2_min.json
```

### Intended consumers

| Consumer | How to use |
| --- | --- |
| **Zeus Client** (`kotenai-zeus-client`) | Demo/offline templates; production still **stamp + `sync_chat_requests`** |
| **Developer Helper MCP** | `list_catalog_modes` / `fetch_chat_request` |
| **koten_docs** | Contracts / using-zeus-client |
| **Coding agents** | Clone or fetch by mode; never invent `contract_hash` |

### Critical rules (unchanged for all releases)

1. **Templates ≠ production stamps.** Your Hub verify/stamp is authoritative.  
2. Prefer live **`sync_chat_requests`** after ops stamps a scope.  
3. Do **not** hand-edit hashes to clear drift (409) — resync and re-pin.  
4. Engine full (non-min) snapshots remain under Zeus `ai/V2/` for Hub A/B; integrators start with **min** / base-N min trees.

### Related tracking

| Item | Link |
| --- | --- |
| Docs story | [KD-8](https://kotenai.atlassian.net/browse/KD-8) |
| Helper catalog tools | [ZDH-14](https://kotenai.atlassian.net/browse/ZDH-14) |
| Platform docs | [docs.koten.ai](https://docs.koten.ai/) |
| Generator | [koten-ai/Zeus](https://github.com/koten-ai/Zeus) `ai-snapshot --min` |
| Helios wishlist | [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) |
| Roadmap | [ROADMAP.md](docs/ROADMAP.md) |

### Upgrade / refresh procedure (base-1 pin)

```bash
go run . ai-snapshot --mode=all --api-version=v2 --min   # in Zeus
./scripts/sync-from-zeus.sh /path/to/Zeus
python3 scripts/refresh_manifest.py
python3 scripts/scan_catalogs.py   # inspector index
```

### Breaking changes (0.1.0)

None (initial release).

### Known limitations (0.1.0)

- No full (non-min) profile published yet — min only.  
- No use-case-specific catalogs in this tree yet.  
- Helper MCP can clone this repo; set `ZEUS_CHAT_REQUEST_DIR` to a local checkout if you prefer not to fetch. A `GITHUB_TOKEN` is only needed if the clone is private.  
