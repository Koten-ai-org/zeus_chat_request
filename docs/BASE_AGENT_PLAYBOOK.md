# BASE agent playbook — comply & upgrade

> **Call law** · [CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md) is the test a sentence about how to call Zeus must pass before a checklist places it. This file is procedures. Catalog candidate is **base-8.0**. `CURRENT.json` stays **base-1**. Zeus embed stays **base-6.1** and **base-7.1**.
>
> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · candidate pack **base-5** · prior candidate **base-4** · version matrix: [COMPAT.md](../COMPAT.md)

**Audience:** coding agents (and humans) changing **catalogs**, **Zeus engine**, or **zeus_client** for a given `base-N`.  
**Not:** a second Bible or Roadmap — **procedures + checklists** only. Depth lives in linked SoT docs.

| Entry | Link |
| --- | --- |
| Short start | [../AGENTS.md](../AGENTS.md) |
| Versions | [../COMPAT.md](../COMPAT.md) |
| Migration hops | [migration/README.md](migration/README.md) → `migration/base-X_to_base-Y/` |
| Scaffold pack | [CREATE_BASE.md](CREATE_BASE.md) |

---

## 0. Hard rules

1. Never invent production `contract_hash`.  
2. Pin last (`CURRENT.json`).  
3. BASE ≠ Zeus semver ≠ Client version.  
4. Pack = `v2/base/base-<id>/` (e.g. `base-5`, `base-5.1`) — **each train is a full folder**; design = `docs/`; hops = `docs/migration/…`. Never train-only via `content_train`.  
5. Required four always: `summary`, `query_decomposition`, `decomposition`, `confidence`.  
6. G2 admin never in chat UI; tool JSON is untrusted data.  
7. A sentence about how to call Zeus passes [CONSTITUION_DESIGN.md](CONSTITUION_DESIGN.md) before it is placed. [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) chooses the surface after that. A hop folder is an archive.

---

## 1. Detect which BASE you are on

| Signal | Where | Means |
| --- | --- | --- |
| Production pin | `CURRENT.json` → `base_id` | What prod clients should use |
| Pack present | `v2/base/base-N/` + `_lineage.base_id` | Catalogs on disk |
| Compat row | [COMPAT.md](../COMPAT.md) | Supported / candidate / design |
| Design only | [ROADMAP.md](ROADMAP.md) | Spec without pack (base-6+ themes until scaffolded) |

```text
Pin base-1  +  packs base-4 + base-5 on disk
→ production still base-1; trials may use base-4 or base-5 candidate; pin last
```

---

## 2. Comply with `base-X`

For each track (catalog / Zeus / Client), complete the checklist for **your target BASE**.

### 2.1 base-1 (production pin)

| Track | Must | Must not |
| --- | --- | --- |
| **Catalog** | Load `v2/min/` or `v2/base/base-1/min/`; `*_v2_min.json`; required four | Treat base-4 files as pin |
| **Zeus** | Stamp/hash path for min catalogs; Detective core four | Require base-4-only fields as hard fail on pin |
| **Client** | Bind contract; parse required four; multi-round `messages[]` | Invent hash; show admin scores in UI |

**SoT:** [CHAT_REQUEST.md](CHAT_REQUEST.md) · [COMPAT.md](../COMPAT.md)

### 2.2 base-4 (candidate pack)

| Track | Must | Must not |
| --- | --- | --- |
| **Catalog** | `v2/base/base-4/min/*_base-4.json`; one Terminate table; Layer A schema at pack root | Put long essays in the pack folder |
| **Zeus** | Accept extended `return` / terminating pipeline properties as **optional**; lineage `base_id`; loaders accept `*_base-N.json` | Break base-1 pin path |
| **Client** | Validate required four; map optional G2/G3; `business_rules_triggers` as **array** (index-aligned) if present; redaction G1 only for UI | Require object triggers (that is base-5) |

**SoT:** [BIBLE.md](BIBLE.md) · pack [response_output_schema.json](../v2/base/base-4/response_output_schema.json) · hop [migration/base-1_to_base-4/](migration/base-1_to_base-4/)

**Client quick list (base-4):**

- [ ] Parse recommended: `policy_action`, `subject_confidence`, `jail_break_attempt`, `wish_i_knew`, `business_rules_triggers[]`  
- [ ] Never put G2 in chat UI  
- [ ] Prefer `policy_action` → `message_*` chrome when brand inject present  

**Zeus quick list (base-4):**

- [ ] Return tool schema allows extra Layer A properties  
- [ ] Detective: required four; optional fields warn not fail (product choice)  
- [ ] Snapshot/publish can emit `base-4` lineage  

### 2.3 base-5 (**candidate pack** — last breaking train)

| Track | Must | Notes |
| --- | --- | --- |
| **Catalog** | Use **`v2/base/base-5/`**; object triggers + optional `app_output` in schema/tools | No array SoT |
| **Zeus** | Accept object triggers + optional `app_output`; optional Detective soft-require | Don’t require Helios Pri-1 on Layer A |
| **Client** | Settings bag; merge/freeze; **object** triggers; `output_request` type+description; policy table | Dual-read arrays **≤1 release** then **remove** |

**Law:** base-5 freezes the wire. **base-6+ must be additive/optional only** ([ROADMAP.md](ROADMAP.md) BASE change law).

**SoT:** pack [`v2/base/base-5/`](../v2/base/base-5/) · [ROADMAP.md](ROADMAP.md) · [RULES_OBJECT…](RULES_OBJECT_AND_OUTPUT_REQUEST.md) · [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · hop [migration/base-4_to_base-5/](migration/base-4_to_base-5/)

---

## 3. Upgrade `base-X` → `base-Y` (generic recipe)

Execute in order. Skip only if the hop folder says “design only” and you are not scaffolding yet.

```text
0. Copy docs/migration/RELEASE_CHECKLIST_TEMPLATE.md
     → docs/migration/base-X_to_base-Y/RELEASE_CHECKLIST.md  (phases A–G)
1. Read COMPAT.md + ROADMAP (for Y)
2. Read docs/migration/base-X_to_base-Y/  (GUIDE + lessons if present)
3. Scaffold pack (when Y is a real pack):
     python3 scripts/new_base.py --from v2/base/base-X --base Y
4. DIET Y deltas (Terminate table, Layer A schema, verb params, inject contracts)
     — scaffold copies parent wire; never ship undieted
5. Re-export text; refresh MANIFEST; scan_catalogs
6. VERIFY (P0):
     python3 scripts/verify_base_pack.py --base Y   # must OK before pack PR
6a. Size table, then the page:
     python3 scripts/chat_request_size.py
     # writes v2/base/chat_request_size.csv, then v2/base/chat_request_size.html from that CSV
7. Zeus engine: snapshot / PIN / Detective / loaders / return schema (see §5; often separate ticket)
8. zeus_client: parse/validate new fields; dual-read only if X→Y break and ≤1 release; redaction; policy table
9. Update COMPAT.md triples + feature table + RELEASE_NOTES.md
10. Ensure hop folder complete:
     GUIDE.md + lessons-learned.md + RELEASE_CHECKLIST.md
11. Update this playbook: §2 card for Y + §4 jump row
12. Inspector Diff: same mode base-X vs base-Y
13. Jira / CR board (Phase J): update base-Y epic, create residual
    zeus_client + Zeus stories, blocks pin epic — checklist §9
    Board: https://kotenai.atlassian.net/jira/software/projects/CR/boards/48
14. Client spike + Hub stamp BEFORE CURRENT.json pin flip
```

**Master checklist:** [migration/RELEASE_CHECKLIST_TEMPLATE.md](migration/RELEASE_CHECKLIST_TEMPLATE.md) · base-5: [migration/base-4_to_base-5/RELEASE_CHECKLIST.md](migration/base-4_to_base-5/RELEASE_CHECKLIST.md)

### 3.1 Where deltas live

| Y state | Primary delta source |
| --- | --- |
| Hop archived | `docs/migration/base-X_to_base-Y/GUIDE.md` |
| Design only | [ROADMAP.md](ROADMAP.md) + design docs linked from hop README |
| Scaffold only | [CREATE_BASE.md](CREATE_BASE.md) then fill GUIDE |

---

## 4. Jump table

| Jump | Migration path | Status | Comply card |
| --- | --- | --- | --- |
| base-1 → base-4 | [migration/base-1_to_base-4/](migration/base-1_to_base-4/) | Candidate pack | §2.1 → §2.2 |
| base-4 → base-5 | [migration/base-4_to_base-5/](migration/base-4_to_base-5/) | **Candidate pack** (breaking freeze shipped; pin still base-1) | §2.2 → §2.3 |
| base-5 → base-6+ | (add hop only if needed) | **Additive only** by default | No wire rename/remove |
| base-6.1 → base-7.0 | [migration/base-6.1_to_base-7.0/](migration/base-6.1_to_base-7.0/) | Previous numbered ship | No wire rename/remove |
| base-7.0 → base-7.1 | [migration/base-7.0_to_base-7.1/](migration/base-7.0_to_base-7.1/) | **Binding fix** (CR-40). Local Zeus pair base-6.1 + base-7.1. `CURRENT.json` stays base-1. | No wire rename/remove |
| base-7.1 → base-7.2 | [migration/base-7.1_to_base-7.2/](migration/base-7.1_to_base-7.2/) | **Slot rule.** Zeus embed still base-7.1. `CURRENT.json` stays base-1. | No wire rename/remove |
| base-7.2 → base-7.3 | [migration/base-7.2_to_base-7.3/](migration/base-7.2_to_base-7.3/) | **Walk close.** Zeus embed still base-7.1. `CURRENT.json` stays base-1. | No wire rename/remove |
| base-7.3 → base-7.4 | [migration/base-7.3_to_base-7.4/](migration/base-7.3_to_base-7.4/) | **Call align.** Zeus embed still base-7.1. `CURRENT.json` stays base-1. | No wire rename/remove |
| base-7.4 → base-8.0 | [migration/base-7.4_to_base-8.0/](migration/base-7.4_to_base-8.0/) | **Constitution morph.** Numbered name of base-8-prototype-1. Catalog candidate. Suite not run. Zeus embed still base-7.1. `CURRENT.json` stays base-1. | No wire rename/remove |

### 4.1 base-1 → base-4 (summary)

| Area | Delta |
| --- | --- |
| Catalog | `*_base-4.json`; one Terminate table; recommended Layer A on return tool |
| Zeus | Optional extra return properties; lineage |
| Client | Optional G2/G3; array triggers |

**Detail:** [migration/base-1_to_base-4/GUIDE.md](migration/base-1_to_base-4/GUIDE.md) · [lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md)

### 4.2 base-4 → base-5 (summary — **breaking**; take all wire pain here)

| Area | Delta |
| --- | --- |
| Catalog | Named `rules{}`; object triggers **only**; company_context; output_request |
| Zeus | Prefer not to grow always-on AI fields; Detective soft-require policy TBD |
| Client | Merge/freeze; settings bag; type+description → prompt; policy table; drop array dual-read ASAP |

**After this hop:** only additive/optional BASE changes until a new major is justified.

**Detail:** [ROADMAP.md](ROADMAP.md) · [RULES_OBJECT…](RULES_OBJECT_AND_OUTPUT_REQUEST.md) · [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · [migration/base-4_to_base-5/](migration/base-4_to_base-5/)

### 4.3 base-7.0 → base-7.1 (summary — additive)

| Area | Delta |
| --- | --- |
| Catalog | FTS `search` binds `@step.doc_keys`. `find`, hybrid, and node-vector bind `@step.node_ids`. `@step.ids` stays node ids only. |
| Zeus | Local 5.5TH tree embeds base-6.1 and base-7.1. Served pin in that tree is base-7.1. No fall-through from `@step.ids` to doc keys. |
| Client | No parser change. The wire is the same. |

**Detail:** [migration/base-7.0_to_base-7.1/GUIDE.md](migration/base-7.0_to_base-7.1/GUIDE.md) · [RELEASE_CHECKLIST.md](migration/base-7.0_to_base-7.1/RELEASE_CHECKLIST.md) · [CR-40](https://kotenai.atlassian.net/browse/CR-40)

### 4.4 base-7.1 → base-7.2 (summary — additive)

| Area | Delta |
| --- | --- |
| Catalog | Copy the list the next slot requires. Node-id slots take `@step.node_ids`. `walk_path` `src_keys` takes `@step.doc_keys`. `project`, `order`, and `enrich` accept either. |
| Zeus | The local 5.5TH embed is still base-6.1 and base-7.1. This pack is not that pin. |
| Client | No parser change. The wire is the same. |

**Detail:** [migration/base-7.1_to_base-7.2/GUIDE.md](migration/base-7.1_to_base-7.2/GUIDE.md) · [RELEASE_CHECKLIST.md](migration/base-7.1_to_base-7.2/RELEASE_CHECKLIST.md)

### 4.5 base-7.2 → base-7.3 (summary — additive)

| Area | Delta |
| --- | --- |
| Catalog | A known stored value stays `find`, unless it is the other end of a WALK_PATHS chain. The `walk_path` close still runs when the seed row already shows that field. `from.src_keys` stays `@step.doc_keys`. |
| Zeus | The local 5.5TH embed is still base-6.1 and base-7.1. This pack is not that pin. |
| Client | No parser change. The wire is the same. |

**Detail:** [migration/base-7.2_to_base-7.3/GUIDE.md](migration/base-7.2_to_base-7.3/GUIDE.md) · [RELEASE_CHECKLIST.md](migration/base-7.2_to_base-7.3/RELEASE_CHECKLIST.md)

### 4.6 base-7.3 → base-7.4 (summary — additive)

| Area | Delta |
| --- | --- |
| Catalog | The plan, the tool text, and the mode examples describe the same call. `narrow_to` follows node ids. `project` has no `limit`. Do not bind `@step.ids`. `set` requires `id_kind`. |
| Zeus | The local 5.5TH embed is still base-6.1 and base-7.1. This pack is not that pin. The live `WALK_PATHS` brief is unchanged. |
| Client | No parser change. The HTTP wire is the same. `set.id_kind` was already required by the engine. |

**Detail:** [migration/base-7.3_to_base-7.4/GUIDE.md](migration/base-7.3_to_base-7.4/GUIDE.md) · [RELEASE_CHECKLIST.md](migration/base-7.3_to_base-7.4/RELEASE_CHECKLIST.md)

### 4.7 base-7.4 → base-8.0 (summary — additive)

| Area | Delta |
| --- | --- |
| Catalog | Numbered name of the base-8-prototype-1 constitution morph. The plan states the access rule once. `narrow_to` takes node ids only. `query_decomposition` records fast path or one probe. Two intents that share a world are two chains in one pipeline. `project` has no `limit`. |
| Zeus | The local 5.5TH embed is still base-6.1 and base-7.1. This pack is not that pin. The lab image may still list `base-8-prototype-1`. |
| Client | No parser change. The HTTP wire is the same. Each mode keeps the contract hash copied from its base-7.4 file. |

**Detail:** [migration/base-7.4_to_base-8.0/GUIDE.md](migration/base-7.4_to_base-8.0/GUIDE.md) · [RELEASE_CHECKLIST.md](migration/base-7.4_to_base-8.0/RELEASE_CHECKLIST.md)

---

## 5. Zeus engine touchpoints (every BASE bump)

Search/update these **areas** in the Zeus repo (names vary; treat as checklist):

| Area | Why |
| --- | --- |
| AI snapshot / catalog generator | Emits min JSON + lineage `base_id` |
| PIN / publish to zeus_chat_request | What becomes pin vs candidate |
| Hash strip / `_hash_policy` | Contract stability |
| `return` / terminating `pipeline` tool JSON Schema | Must match pack `response_output_schema.json` |
| Detective / Layer A grading | Required four; optional field policy |
| Filename loaders | `*_v2_min.json` and `*_base-N.json` and customs |
| Compat / base_id warnings | Align with COMPAT.md (later hard gates) |
| Admin Workbench stamp | Production hashes only from Hub |

Do **not** invent Zeus Version bumps solely for docs; bump engine when behavior/schema requires it, then update COMPAT.

---

## 6. zeus_client touchpoints (every BASE bump)

| Area | Why |
| --- | --- |
| Catalog load path | min vs base-N filenames |
| Layer A parse + validate | Required four + optional fields for that BASE |
| G1/G2/G3 redaction | UI safety |
| Injects | company_context, rules shape, output_request |
| Multi-round | messages append, artifacts, Client clock |
| Policy table | base-5: triggers → flags → message_* |
| Package version | Bump only when behavior ships; update COMPAT Client column |

**Prioritized backlog (Requests):** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) (`ZC-WISH-*`, base-5 floor first).

---

## 7. Agent reading order

```text
1. AGENTS.md
2. COMPAT.md
3. This playbook (§2 or §3 only)
4. docs/migration/base-X_to_base-Y/ if upgrading
5. BIBLE / ROADMAP / RULES / SETTINGS as linked
6. v2/base/base-N/ pack
```

---

## 8. Anti-patterns

| Don’t | Do |
| --- | --- |
| Invent `contract_hash` | Hub stamp / sync |
| Flip CURRENT early | Client spike + Diff + stamp first |
| Put BIBLE inside pack folder | Link to `docs/` |
| Create `docs/base-4_to_base-5_guide.md` at root | Use `docs/migration/base-4_to_base-5/` |
| Mix base-4 array triggers with base-5 object API without dual-read | Document dual-read in COMPAT + Client |
| Copy Helios Pri-1 into always-on Layer A | Cheap Zeus/Client emits ([HELIOS wishlist](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)) |

---

## 9. Template — new hop `base-X` → `base-Y`

When a hop becomes real:

```bash
mkdir -p docs/migration/base-X_to_base-Y
cp docs/migration/RELEASE_CHECKLIST_TEMPLATE.md \
   docs/migration/base-X_to_base-Y/RELEASE_CHECKLIST.md
# fill RELEASE_CHECKLIST + GUIDE.md + lessons-learned.md
# update docs/migration/README.md index
# update this playbook §2 card + §4 jump table
# update COMPAT.md + RELEASE_NOTES.md
# scaffold: python3 scripts/new_base.py --from v2/base/base-X --base Y
```

Hop `GUIDE.md` should cover:

- [ ] Filename / lineage changes  
- [ ] Terminate / Layer A wire deltas  
- [ ] Client-breaking parse changes  
- [ ] Zeus-breaking schema / Detective changes  
- [ ] Hash / stamp impact  
- [ ] Pin readiness criteria  

Full ship bar: hop **`RELEASE_CHECKLIST.md`** (not GUIDE alone).

---

## 10. SoT map (do not duplicate)

| Topic | Canonical |
| --- | --- |
| Ownership set/unset/change | [BIBLE.md](BIBLE.md) §2 |
| Wire order / budget | [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) |
| Settings / policy table | [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) |
| Rules object / output_request | [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) |
| Jailbreak | [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) |
| Multi-round | [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) |
| Future BASE themes | [ROADMAP.md](ROADMAP.md) |
| Versions | [COMPAT.md](../COMPAT.md) |
| Pack scaffold | [CREATE_BASE.md](CREATE_BASE.md) |
