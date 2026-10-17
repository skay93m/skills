# Syafiq Kay Skills (`skay93m/skills`)

Personal skills and deep modules for multi-agent environments across Claude Code, Codex, Antigravity, and Hermes.

This repository provides modular, bounded, and deterministic agent capabilities adhering to the Skill Manifest Standard (`docs/standards/skill-manifest.md`). Every module is governed by strict line budgets ($\le 100$ lines), token budgets ($< 700$ tokens), terminal references (no reference chaining), and explicit artifact contracts.

---

## Architecture Overview (Work 2)

```
                            [ ask-syafiq ]
                            (Master Router)
                                  │
    ┌──────────────┬──────────────┼──────────────┬──────────────┬──────────────┐
    ▼              ▼              ▼              ▼              ▼              ▼
[ wiki-ops ] [ autonomous-   [ agent-       [ academic-    [ personal-    [ thinking-
               scrum ]        ecosystem ]    scholar ]      cadence ]      partner ]
 (knowledge)   (scrum)       (ecosystem)   (scholarship)    (cadence)     (cognition)
```

### Master Router: `ask-syafiq`
- **Domain**: General dispatch & context orchestration.
- **Capabilities**: Rapid workspace detection across 8 canonical repositories, intent routing into deep modules, execution phase boundary enforcement (`PLAN` $\to$ `VALIDATE` $\to$ `EXECUTE`).

### The 6 Deep Modules

1. **`wiki-ops` (`knowledge`)**:
   - Compiled knowledge engine for personal wiki and research operations.
   - Basic Memory MCP compliance, prompt injection isolation, structural and semantic linting, and additive artifact contracts.
2. **`autonomous-scrum` (`scrum`)**:
   - AWT agile engine for automated sprint management.
   - Strict Product Owner vs. Developer role boundaries, Event 0 sprint gates, read-only SQLite state tracking (`awt.db`), and sprint artifact contracts.
3. **`agent-ecosystem` (`ecosystem`)**:
   - Heterogeneous fleet governance across Claude Code, Codex, Antigravity, and Hermes.
   - `~/.agents` golden layout, subagent batching ceiling ($\le 10$ workers), cross-agent durable handoffs (`docs/handoff/<slug>.md`), and fleet audit contracts.
4. **`academic-scholar` (`scholarship`)**:
   - Postgraduate supervisory coaching and legal research scaffolding.
   - Strict student-authored prose invariant (supervisory feedback only, zero ghost-writing), primary statutory authorities (MHA 1983, MCA 2005), Strasbourg/ECHR jurisprudence, OSCOLA legal citations, and supervision memo contracts.
5. **`personal-cadence` (`cadence`)**:
   - Executive function and ADHD momentum scaffolding.
   - Jibun Techo 3-phase projections, Hermes standups, circadian energy mapping, Neko desktop companion integration, and daily review contracts.
6. **`thinking-partner` (`cognition`)**:
   - Oxford tutorial Socratic sparring method.
   - Assumption unmasking, failure mode analysis, Type 1 vs. Type 2 decision reversibility analysis, Architecture Decision Record (ADR) formulation, and decision log contracts.

---

## Upstream Engineering Pipeline

All software engineering tasks follow the sequential multi-agent delivery pipeline:

$$\text{/grill-me} \longrightarrow \text{/to-spec} \longrightarrow \text{/to-tickets} \longrightarrow \text{/tdd} \longrightarrow \text{/code-review} \longrightarrow \text{/pr}$$

1. **/grill-me**: Relentless adversarial Socratic interview to stress-test designs and surface ambiguities.
2. **/to-spec**: Distill requirements and interview consensus into a formal technical specification.
3. **/to-tickets**: Decompose specifications into bounded, test-driven implementation tickets.
4. **/tdd**: Test-driven implementation cycle (red $\to$ green $\to$ refactor).
5. **/code-review**: Two-axis adversarial code review (Standards Compliance + Spec Verification).
6. **/pr**: Pull request composition and release verification.

---

## Installation & Multi-Agent Packaging

Skills in this repository are packaged for instant installation across all major agent runtimes using `npx skills`:

### Install Entire Suite
```bash
npx skills add skay93m/skills
```

### Install Individual Deep Module
```bash
npx skills add skay93m/skills --skill wiki-ops
npx skills add skay93m/skills --skill autonomous-scrum
npx skills add skay93m/skills --skill agent-ecosystem
npx skills add skay93m/skills --skill academic-scholar
npx skills add skay93m/skills --skill personal-cadence
npx skills add skay93m/skills --skill thinking-partner
npx skills add skay93m/skills --skill ask-syafiq
```

### Supported Runtimes & Target Directories

| Runtime | Skill Installation Path | Discovery Mechanism |
|---|---|---|
| **Claude Code** | `~/.claude/skills/<skill>` | Direct folder resolution (`SKILL.md`) |
| **Codex** | `~/.codex/skills/<skill>` | Codex skill registry |
| **Antigravity (AGY)** | `~/.gemini/antigravity-cli/skills` or `~/.agents/skills` | Builtin / custom skill loader |
| **Hermes** | `~/.hermes/skills/<skill>` | Agent tool executor |

All skills are self-contained: installed skill directories contain all necessary `references/`, `templates/`, and `examples/` without relative cross-package dependencies.

---

## Safe Tombstone Policy (Migration Safety)

In `v0.2.0`, 26 legacy utility skills (`sk-*` and `task-assistant`) have been replaced with **Fail-Closed Safe Tombstones**:
- **Behavior**: Safe tombstones carry `disable-model-invocation: true` and execute zero mutations and zero shell commands.
- **Migration Guidance**: Each tombstone informs the agent of its retired capability and provides the direct `npx skills` command to install its successor deep module.
- **Retention**: Tombstones remain in place through `v0.3.0` to preserve backwards compatibility for existing agent prompts and workflows.

---

## Repository Standards & Quality Verification

- **Skill Manifest Standard**: Every deep module and the master router is defined by a declarative manifest in `manifests/` validated against `docs/standards/skill-manifest.md`.
- **Scaffolder Tool**: Run `python3 scripts/new-skill.py --manifest manifests/<name>.yaml` to deterministically scaffold new skills with terminal references and artifact contracts.
- **Automated Verification**:
  - `pytest`: Comprehensive unit and contract test suite (>300 tests).
  - `python3 scripts/check-standard.py`: Deterministic pr-review standard enforcement for security, privacy, and skill budgets.
