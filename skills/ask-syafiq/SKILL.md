---
name: ask-syafiq
description: Master router skill providing rapid workspace detection across 8 repositories, intent-based routing to 6 deep modules, and execution phase boundary guidance. Use when routing requests, selecting deep modules, detecting repository context, or managing session transitions.
disable-model-invocation: true
user-invoked: true
version: 0.2.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: router
---

# Ask Syafiq

Master router skill providing workspace detection across 8 repositories, intent-based routing to 6 deep modules, and execution phase boundary guidance.

## Workspace Detection Matrix

Detect repository root heuristics before executing commands. Root indicators and full runbooks are in [workspace-matrix.md](references/workspace-matrix.md).

| Workspace | Primary Role |
|---|---|
| `skills` | Agent skills, deep modules, standards |
| `sk-wiki` | Compiled persistent knowledge base, Basic Memory |
| `awt` | Agile workflow tracker |
| `kos` | Kancil operating system|
| `syafiq-kay.github.io` | Public portfolio, essays, digital garden |
| `neko` | Desktop companion daemon, telemetry |
| `hermes` | Daily coordination agent, standup summaries |
| `archive` | Historical cold storage, deprecated records |

## Intent-Based Routing Table

Dispatch incoming requests to the appropriate domain module or pipeline phase. See [routing-table.md](references/routing-table.md) for full routing catalog.

| Domain | Skill | Intents / Triggers |
|---|---|---|
| `curate` | `wiki-ops` | Compiled knowledge, linting |
| `code` | `autonomous-scrum` | Agile engine, PO and Dev split |
| `setup` | `agent-ecosystem` | Fleet governance, subagents |
| `tutor` | `academic-scholar` | MSc prose, legal citations |
| `tutor` | `personal-cadence` | ADHD momentum, standups |
| `tutor` | `thinking-partner` | Socratic sparring |

### Upstream Engineering Pipeline
`/grill-me` -> `/to-spec` -> `/to-tickets` -> `/tdd` -> `/code-review` -> `/pr`

## Execution Phase Boundaries

Maintain bounded context and prevent state pollution across phase transitions:

- `Continue`: Iterate in place for bounded, cohesive steps.
- `/clear`: Clean conversation context when switching topics or repos.
- `/handoff`: Persist structured handoff note before context transition.
- `Subagent`: Delegate heavy or discrete execution tasks (strict <=10 batch limit).
- `/compact`: Compact context when token capacity fills.
