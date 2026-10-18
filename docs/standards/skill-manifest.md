# Skill Manifest Standard & Artifact Contract Specification

The canonical specification of the declarative YAML Skill Manifest schema and Artifact Contract for skills in `skay93m/skills`.

## Identity

| Field | Value |
|---|---|
| `standard_id` | `sk-skill-manifest-standard` |
| `version` | `0.1.0` |
| `status` | active |
| Last reviewed | 2026-10-17 |
| Freshness period | one month (ISO 8601 `P1M`) |
| Fresh until | 2026-11-17 |
| Canonical location | `docs/standards/skill-manifest.md` |

---

## 1. Overview & Purpose

Every skill in the `skills` repository is a deep module designed to give autonomous and interactive agents bounded, deterministic, and verifiable capabilities. To prevent architectural drift, unbounded prose, nested reference sprawl, and unverified file mutation, every skill is governed by a **Declarative Skill Manifest**.

The manifest acts as a pre-authoring contract that specifies:
1. Identity, purpose, ownership, and provenance.
2. Hard resource budgets (line and token ceilings for the entrypoint `SKILL.md`).
3. Disclosed terminal references and deterministic helper scripts.
4. Artifact contracts guaranteeing canonical templates and examples for persistent writes.
5. Router taxonomy metadata to register intents with the master router (`skills/ask-syafiq/SKILL.md`).

---

## 2. Skill Manifest Schema

A manifest is authored in declarative YAML (or JSON) and adheres to the schema below.

### 2.1 Schema Definition

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | `string` | **Yes** | — | Unique lowercase kebab-case identifier (max 3 words). Must match `^[a-z0-9]+(-[a-z0-9]+)*$` and equal the skill's directory name. |
| `description` | `string` | **Yes** | — | Concise purpose statement ($\le$ 1,024 characters). Must include a "Use when" clause and use third-person or verb-first phrasing (no first/second-person pronouns). |
| `version` | `string` | No | `"0.1.0"` | Semantic version string (e.g. `0.1.0`). |
| `owner` | `string` | No | `"skay93m"` | GitHub user or team handle responsible for the skill. |
| `provenance` | `string` | No | `"original"` | Upstream origin, issue reference, or author attribution. |
| `disable-model-invocation` | `boolean` | No | `true` | When `true`, prevents models from invoking the skill automatically without explicit human slash command. Default is `true` for personal skills. `false` is permitted only for the gateway (`ask-syafiq`) and presentation (`style`) modules; the scaffolder rejects it for every other skill. |
| `user-invoked` | `boolean` | No | `true` | Indicates whether the skill is intended for direct user slash invocation. |
| `triggers` | `list[string]` | No | `[]` | Natural-language utterances, prompts, or trigger keywords activating the skill. |
| `budgets` | `object` | No | `{}` | Resource ceilings for the skill entrypoint `SKILL.md`. |
| `budgets.line-budget` | `integer` | No | `100` | Maximum line count for entrypoint `SKILL.md` (strictly $\le 100$). |
| `budgets.token-budget` | `integer` | No | `700` | Maximum token budget for entrypoint `SKILL.md` (strictly $\le 700$). |
| `references` | `list[string]` | No | `[]` | Terminal markdown reference documents located in `references/`. Must obey the terminal reference rule. |
| `scripts` | `list[string]` | No | `[]` | Deterministic helper scripts located directly in `scripts/` without nested subdirectories or path traversal. |
| `artifacts` | `object` | No | `{}` | Persistent file and report production contract. |
| `artifacts.produces` | `boolean` | No | `false` | Whether the skill produces persistent notes, reports, or files. |
| `artifacts.contracts` | `list[object]` | Conditional | `[]` | Required if `artifacts.produces` is `true`. List of contract specifications. Each entry must define `name` (lowercase kebab-case), `template` (must end with `.template.md` or `.md` strictly under `templates/` without nested subdirectories or traversal), and `example` (must end with `.example.md` or `.md` strictly under `examples/` without nested subdirectories or traversal). |
| `router` | `object` | No | `{}` | Router dispatch configuration for `skills/ask-syafiq/SKILL.md`. |
| `router.domain` | `string` | No | `"general"` | Taxonomy domain: strictly one of `curate`, `code`, `tutor`, `setup`, `style`, or `general`. |
| `router.intents` | `list[string]` | No | `[]` | High-level intent descriptions registered in the master routing table. Must be non-empty strings. |

---

## 3. Structural Invariants

### 3.1 Terminal Reference Invariant (No Chaining)
- Reference files declared under `references/` must be terminal documents.
- A reference file is linked strictly **one level deep from `SKILL.md`**.
- Reference files must **NEVER** link or chain to other reference markdown files (`.md`).
- This invariant guarantees that agent context stays strictly bounded, preventing recursive reading loops.

### 3.2 Entrypoint Budgets
- Entrypoint `SKILL.md` must not exceed **100 lines** (Standard S4).
- Entrypoint `SKILL.md` token budget must not exceed **700 tokens**.
- Extended documentation, procedures, schemas, and checklists must be offloaded to terminal `references/`.

### 3.3 Provenance and Naming
- Skill name must be lowercase kebab-case at most 3 words, free of vendor labels (`anthropic`, `claude`).
- Frontmatter must supply provenance metadata (`metadata.origin`, `metadata.agent_involvement`, and `metadata.category`).

---

## 4. Artifact Contract Specification

Any skill that produces persistent files, reports, database records, or notes (i.e. `artifacts.produces: true`) MUST declare an Artifact Contract.

### 4.1 Contract Requirements
For every declared artifact contract `contract_name`:
1. **Canonical Template (`templates/<contract_name>.template.md`)**:
   - Defines the exact structural blueprint of the produced artifact.
   - Declares required frontmatter, headings, section order, and typed placeholder slots (e.g. `{{DATE}}`, `{{STATUS}}`, `{{EVIDENCE}}`).
   - Must be a non-empty relative path ending with `.template.md` (or `.md`), strictly located under `templates/` without nested subdirectories, and must not contain path traversal (`..`) or leading slashes.
2. **Concrete Example (`examples/<contract_name>.example.md`)**:
   - Demonstrates a realistic, fully instantiated instance of the template.
   - Must contain no unreplaced placeholder tokens.
   - Must avoid leaking confidential personal identifiers or real credentials.
   - Must be a non-empty relative path ending with `.example.md` (or `.md`), strictly located under `examples/` without nested subdirectories, and must not contain path traversal (`..`) or leading slashes.

### 4.2 Contract Schema

```yaml
artifacts:
  produces: true
  contracts:
    - name: "<contract-name>"
      template: "templates/<contract-name>.template.md"
      example: "examples/<contract-name>.example.md"
```

---

## 5. Router Registration Specification

The router configuration binds domain skills to the master router (`skills/ask-syafiq/SKILL.md`).

### 5.1 Domain Taxonomy
Taxonomy domains include:
- `curate`: Knowledge base operations, ingestion, and memory compounding.
- `code`: Engineering workflows: specification, tickets, TDD, and review.
- `tutor`: Syafiq's own teaching taste: legal doctrine, supervision debriefs, Socratic thinking, and daily cadence.
- `setup`: Agent fleet governance and configuration.
- `style`: Ambient presentation and writing standards.
- `general`: Anything that fits none of the above.

### 5.2 Routing Integration
When a skill declares a `router` block, the scaffolder (`scripts/new-skill.py`) appends or updates an entry in `skills/ask-syafiq/SKILL.md`:
```markdown
| Domain | Skill | Intents / Triggers |
|---|---|---|
| curate | [`knowledge-run-audit`](../knowledge-run-audit/SKILL.md) | Audit knowledge maintenance runs, inspect diffs |
```

---

## 6. Concrete Manifest Examples

### Example 1: Minimal Skill Manifest (`knowledge-run-audit.yaml`)

```yaml
name: knowledge-run-audit
description: Use when auditing a finished scheduled Wiki lint and ingest run against independent snapshot diffs.
version: 0.1.0
owner: skay93m
provenance: original
disable-model-invocation: true
user-invoked: true
triggers:
  - "audit knowledge run"
  - "verify maintenance run"
budgets:
  line-budget: 100
  token-budget: 700
references:
  - runbook.md
  - checks.md
scripts:
  - run-audit.sh
artifacts:
  produces: true
  contracts:
    - name: audit-report
      template: templates/audit-report.template.md
      example: examples/audit-report.example.md
router:
  domain: curate
  intents:
    - "Audit and verify knowledge maintenance run artifacts"
    - "Inspect run records and diffs"
```

### Example 2: Non-Artifact Skill Manifest (`thinking-partner.yaml`)

```yaml
name: thinking-partner
description: Use when stress-testing architectural decisions, exploring tradeoffs, and probing edge cases.
version: 0.1.0
owner: skay93m
provenance: original
disable-model-invocation: true
user-invoked: true
triggers:
  - "grill this plan"
  - "stress-test design"
budgets:
  line-budget: 100
  token-budget: 700
references:
  - questioning-heuristics.md
scripts: []
artifacts:
  produces: false
router:
  domain: tutor
  intents:
    - "Probe design assumptions"
    - "Stress-test technical proposals"
```
