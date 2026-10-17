# Syafiq Kay Skills (`skay93m/skills`)

Personal skills, deep modules, and governance architecture for multi-agent workflows across Claude Code, Codex, Antigravity, and Hermes.

[![Release: v0.2.0](https://img.shields.io/badge/release-v0.2.0-blue.svg)](https://github.com/skay93m/skills/releases/tag/v0.2.0)
[![Tests: 316 passing](https://img.shields.io/badge/tests-316%20passing-brightgreen.svg)](https://github.com/skay93m/skills/actions)
[![Standard Checks: 0 violations](https://img.shields.io/badge/standard%20checks-0%20violations-success.svg)](https://github.com/skay93m/skills/actions)

---

## Operator Quickstart (Human First)

Get started with the skills ecosystem in three steps:

1. **Install the skills suite**:
   ```bash
   npx skills add skay93m/skills
   ```
   *To install a single deep module instead, specify `--skill <name>` (e.g. `npx skills add skay93m/skills --skill wiki-ops`).*

2. **Start any session with the master router**:
   Invoke `/ask-syafiq` in your agent prompt:
   > *"What workspace am I in, and how should we structure this session?"*

3. **Follow guided routing or invoke deep modules directly**:
   The master router automatically identifies your workspace (e.g., `skills`, `sk-wiki`, `awt`) and routes your intent to one of the 6 Deep Modules or into the 6-phase engineering pipeline.

> [!TIP]
> You never need to memorize individual skill names or parameters. Simply invoke `/ask-syafiq` or describe what you want to do in natural language. The router detects your repository context, validates execution boundaries, and dispatches to the specialized deep module.

---

## Operator Decision Matrix ("Which module do I reach for?")

When you have a specific goal, consult this matrix to reach for the right capability immediately:

| What do you want to accomplish? | Reach for | Domain / Engine | Quick Action / Invocation |
|---|---|---|---|
| **Starting a session / switching repos** | `ask-syafiq` | Master Router | `/ask-syafiq` or `"orient this session"` |
| **Managing ADHD momentum & daily schedule** | `personal-cadence` | `cadence` | `"plan daily cadence"` or `"morning brief"` |
| **Building code / engineering pipeline** | Upstream Pipeline | Multi-Agent Lifecycle | `/grill-me` $\to$ `/to-spec` $\to$ `/to-tickets` $\to$ `/tdd` $\to$ `/code-review` $\to$ `/pr` |
| **Evaluating hard architectural choices** | `thinking-partner` | `cognition` | `/grill-me` or `"challenge my architecture"` |
| **Writing postgraduate essays / legal research** | `academic-scholar` | `scholarship` | `"review legal argument"` or `"verify oscola citations"` |
| **Compiling wiki notes & running lints** | `wiki-ops` | `knowledge` | `"run knowledge lint"` or `"compile wiki"` |
| **Running agile sprints & ticket triage** | `autonomous-scrum` | `scrum` | `"plan sprint"` or `"check event 0 gates"` |
| **Managing fleet of agents & golden config** | `agent-ecosystem` | `ecosystem` | `"audit agent fleet"` or `"sync ~/.agents"` |

---

## Architecture Diagram

All incoming requests and session transitions route through `ask-syafiq` into the 6 bounded Deep Modules:

```text
                             [ ask-syafiq ]
                             (Master Router)
                                   │
     ┌──────────────┬──────────────┼──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼              ▼              ▼
[ wiki-ops ] [ autonomous-   [ agent-       [ academic-    [ personal-    [ thinking-
               scrum ]        ecosystem ]    scholar ]      cadence ]      partner ]
 (knowledge)   (scrum)       (ecosystem)   (scholarship)    (cadence)     (cognition)
```

---

## The 6 Deep Modules Catalog

Every deep module is a bounded, deterministic skill package complying with strict budgets ($\le 100$ lines, $< 700$ tokens), terminal references (depth 1), and explicit artifact contracts.

### 1. `wiki-ops`
- **Domain**: `knowledge`
- **Purpose**: Karpathy-style compiled knowledge engine for personal wiki and research operations. Ingests raw thoughts, compiles structured indexes, runs structural and semantic lints, and executes bounded note reconciliation.
- **Core Invariants**:
  - Basic Memory MCP compliance: All mutations occur through Basic Memory tools; direct filesystem writes under wiki paths are prohibited.
  - Prompt injection isolation: Raw source material is encapsulated in XML tags (`<source_content>`) to prevent instruction hijacking.
  - Additive artifact generation: Produces structured reports without destructive overwrite of raw inputs.
- **Artifact Contracts**: Produces `knowledge-report` ([`templates/knowledge-report.template.md`](skills/wiki-ops/templates/knowledge-report.template.md), [`examples/knowledge-report.example.md`](skills/wiki-ops/examples/knowledge-report.example.md)).
- **Direct Install**:
  ```bash
  npx skills add skay93m/skills --skill wiki-ops
  ```

### 2. `autonomous-scrum`
- **Domain**: `scrum`
- **Purpose**: Standalone AWT agile sprint engine enforcing automated sprint planning, backlog triage, ticket progression, and milestone burndown.
- **Core Invariants**:
  - Strict PO vs. Dev boundary: Agents acting as developers never modify acceptance criteria or self-approve ticket completion; Product Owner governance remains distinct.
  - Event 0 sprint gates: Strict pre-flight validation (dependency closure, spec completeness, test environment readiness) before any sprint starts.
  - Read-only SQLite state tracking: Tracks tasks, issues, and sprints deterministically in `awt.db`.
- **Artifact Contracts**: Produces `sprint-report` ([`templates/sprint-report.template.md`](skills/autonomous-scrum/templates/sprint-report.template.md), [`examples/sprint-report.example.md`](skills/autonomous-scrum/examples/sprint-report.example.md)).
- **Direct Install**:
  ```bash
  npx skills add skay93m/skills --skill autonomous-scrum
  ```

### 3. `agent-ecosystem`
- **Domain**: `ecosystem`
- **Purpose**: Fleet-wide governance for multi-agent environments across Claude Code, Codex, Antigravity, and Hermes, enforcing golden configurations and inter-agent coordination.
- **Core Invariants**:
  - Golden layout: Centralized synchronization through `~/.agents` golden directory structure.
  - Subagent batching ceiling: Strict limit of $\le 10$ concurrent subagents per batch; subsequent batches wait until the active batch completes.
  - Durable handoffs: Inter-agent handoffs and session completions are persisted to durable notes under `docs/handoff/<slug>.md`.
- **Artifact Contracts**: Produces `agent-handoff` ([`templates/agent-handoff.template.md`](skills/agent-ecosystem/templates/agent-handoff.template.md), [`examples/agent-handoff.example.md`](skills/agent-ecosystem/examples/agent-handoff.example.md)).
- **Direct Install**:
  ```bash
  npx skills add skay93m/skills --skill agent-ecosystem
  ```

### 4. `academic-scholar`
- **Domain**: `scholarship`
- **Purpose**: Postgraduate supervisory coaching and legal research scaffolding for King's College London (KCL) MSc in Mental Health, Ethics and Law.
- **Core Invariants**:
  - Student-authored prose invariant: Strict supervisory coaching, critique, and Socratic interrogation only; absolute ban on ghost-writing or model-authored prose.
  - Primary statutory authorities: Governed by UK mental health statutes (Mental Health Act 1983, Mental Capacity Act 2005) and Strasbourg / European Court of Human Rights (ECHR) jurisprudence.
  - Legal citation standard: Strict OSCOLA citation compliance for statutes, cases, and academic literature.
- **Artifact Contracts**: Produces `supervisory-feedback` ([`templates/supervisory-feedback.template.md`](skills/academic-scholar/templates/supervisory-feedback.template.md), [`examples/supervisory-feedback.example.md`](skills/academic-scholar/examples/supervisory-feedback.example.md)).
- **Direct Install**:
  ```bash
  npx skills add skay93m/skills --skill academic-scholar
  ```

### 5. `personal-cadence`
- **Domain**: `cadence`
- **Purpose**: Executive function and ADHD momentum coaching, daily energy alignment, time tracking, and coordination with ambient daemons.
- **Core Invariants**:
  - Jibun Techo 3-phase projections: Vertical timeline mapping covering Plan $\to$ Reality $\to$ Delta.
  - Hermes standups: Automated morning kickoff briefs and evening retrospective reconciliations.
  - Circadian energy mapping: Matching high-focus tasks to peak cognitive bandwidth and low-friction tasks to recovery troughs.
  - Neko companion coordination: Desktop companion status hooks and non-intrusive focus cycle nudges.
- **Artifact Contracts**: Produces `daily-cadence` ([`templates/daily-cadence.template.md`](skills/personal-cadence/templates/daily-cadence.template.md), [`examples/daily-cadence.example.md`](skills/personal-cadence/examples/daily-cadence.example.md)).
- **Direct Install**:
  ```bash
  npx skills add skay93m/skills --skill personal-cadence
  ```

### 6. `thinking-partner`
- **Domain**: `cognition`
- **Purpose**: Oxford tutorial Socratic sparring partner and cognitive challenger for stress-testing architectures, unmasking hidden assumptions, and formulating decision records.
- **Core Invariants**:
  - Adversarial interrogation before agreement: Relentlessly probes assumptions, edge cases, and second-order consequences.
  - Reversibility taxonomy: Explicit classification of Type 1 (irreversible, high-blast-radius) versus Type 2 (reversible, two-way-door) decisions.
  - Architecture Decision Records (ADRs): Formulates structured, auditable decision records documenting context, tradeoffs, and consequences.
- **Artifact Contracts**: Produces `concept-adr` ([`templates/concept-adr.template.md`](skills/thinking-partner/templates/concept-adr.template.md), [`examples/concept-adr.example.md`](skills/thinking-partner/examples/concept-adr.example.md)).
- **Direct Install**:
  ```bash
  npx skills add skay93m/skills --skill thinking-partner
  ```

### Master Router: `ask-syafiq`
- **Domain**: `general`
- **Purpose**: Rapid workspace detection across 8 repositories, intent-based routing to 6 deep modules, and execution phase boundary guidance.
- **Core Invariants**:
  - Workspace detection: Automatically identifies 8 canonical repositories (`skills`, `sk-wiki`, `awt`, `kos`, `syafiq-kay.github.io`, `neko`, `hermes`, `archive`) via root heuristics.
  - Intent routing: Dispatches requests directly to the corresponding deep module or pipeline phase.
  - Execution phase boundaries: Enforces context hygiene (`Continue`, `/clear`, `/handoff`, `Subagent`, `/compact`).
- **Direct Install**:
  ```bash
  npx skills add skay93m/skills --skill ask-syafiq
  ```

---

## Upstream Engineering Pipeline

All software engineering tasks follow a sequential, multi-agent delivery lifecycle designed to eliminate latent defects and ensure strict specification adherence:

```text
/grill-me  ──>  /to-spec  ──>  /to-tickets  ──>  /tdd  ──>  /code-review  ──>  /pr
```

1. **/grill-me (Socratic Stress-Testing)**: Relentless adversarial Socratic interview to interrogate requirements, expose implicit assumptions, discover failure modes, and align on boundaries before writing code.
2. **/to-spec (Formal Specification)**: Distill interview consensus and requirements into an unambiguous, bounded technical specification defining interface seams, data models, and acceptance criteria.
3. **/to-tickets (Atomic Work Decomposition)**: Decompose specifications into small, independent, test-driven implementation tickets with strict line budgets ($\le 100$ lines) and explicit acceptance gates.
4. **/tdd (Test-Driven Implementation)**: Implement tickets following the strict Red $\to$ Green $\to$ Refactor cycle: write failing test (Red), minimal implementation passing test (Green), and standards refactor.
5. **/code-review (Two-Axis Adversarial Review)**: Parallel adversarial review running two independent subagents:
   - **Standards Axis**: Verifies budgets ($\le 100$ lines, $< 700$ tokens), terminal references, security, and repository conventions.
   - **Spec Axis**: Verifies exact issue/spec requirement conformance with zero extraneous changes.
   Zero approval granted on latent defects.
6. **/pr (Pull Request Delivery)**: Construct high-fidelity pull requests containing structured change summaries, automated verification proofs, and risk assessments ready for human owner review and merge.

---

## Multi-Agent Runtime Installation

Skills in this repository are packaged for instant installation across all major agent runtimes using `npx skills`:

### Installation Commands

```bash
# Install the complete suite
npx skills add skay93m/skills

# Install individual deep modules
npx skills add skay93m/skills --skill ask-syafiq
npx skills add skay93m/skills --skill wiki-ops
npx skills add skay93m/skills --skill autonomous-scrum
npx skills add skay93m/skills --skill agent-ecosystem
npx skills add skay93m/skills --skill academic-scholar
npx skills add skay93m/skills --skill personal-cadence
npx skills add skay93m/skills --skill thinking-partner
```

### Supported Runtimes & Target Directories

| Runtime | Skill Installation Path | Discovery Mechanism | Execution Model |
|---|---|---|---|
| **Claude Code** | `~/.claude/skills/<skill>` | Direct folder resolution (`SKILL.md`) | Interactive CLI & subagent tools |
| **Codex** | `~/.codex/skills/<skill>` | Codex skill registry | Agent tool execution |
| **Antigravity (AGY)** | `~/.gemini/antigravity-cli/skills` or `~/.agents/skills` | Builtin / custom skill loader | Pair programmer & background subagents |
| **Hermes** | `~/.hermes/skills/<skill>` | Agent tool executor | Autonomous agent daemon |

> [!NOTE]
> **Self-Contained Packaging**: Every installed skill directory contains all required references (`references/`), templates (`templates/`), and examples (`examples/`). There are zero relative cross-package dependencies or broken links across modules.

---

## Safe Tombstone Policy (Migration Safety)

In `v0.2.0`, 26 legacy utility skills (`sk-*` and `task-assistant`) have been replaced with **Fail-Closed Safe Tombstones**:

- **Fail-Closed Behavior**: Every tombstone carries `disable-model-invocation: true` and executes zero mutations, zero shell commands, and zero filesystem writes.
- **Migration Guidance**: When invoked by existing agent workflows or historical prompts, the stub cleanly informs the agent that the capability has been retired and provides the exact `npx skills` replacement command for the successor deep module.
- **Retention Period**: Tombstones remain in place through `v0.3.0` to ensure backwards compatibility for existing agent prompts and configurations before full retirement.

---

## Developer & Contributor Guide

### Architectural Standards & Invariants

Every skill in this repository is governed by the Skill Manifest Standard (`docs/standards/skill-manifest.md`) and must strictly uphold:
- **Line Budget**: $\le 100$ lines for `SKILL.md`.
- **Token Budget**: $< 700$ estimated tokens for `SKILL.md`.
- **Terminal References**: Reference files in `references/` are 1-level deep from `SKILL.md` and must never link to other markdown reference files (`docs/standards/terminal-references.md`).
- **Artifact Contracts**: Modules producing user-facing or durable deliverables must provide declarative contracts with paired templates (`templates/`) and verified examples (`examples/`).

### Scaffolding New Skills

Scaffold new skills deterministically using declarative manifests:
```bash
python3 scripts/new-skill.py --manifest manifests/<name>.yaml
```

### Automated Quality Verification

Run the automated verification suite before submitting pull requests:

```bash
# Run comprehensive contract & unit test suite (316 tests)
pytest

# Run deterministic PR review standards (security, privacy, budgets, hygiene)
python3 scripts/check-standard.py
```

> [!IMPORTANT]
> All pull requests require 0 test failures (`pytest`) and 0 blocking findings from `scripts/check-standard.py` to maintain repository integrity.
