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

Detect repository root heuristics before executing commands. See [workspace-matrix.md](references/workspace-matrix.md) for full runbooks.

| Workspace | Primary Role | Root Indicators |
|---|---|---|
| `skills` | Agent skills, deep modules, standards | `skills/`, `docs/standards/`, `scripts/new-skill.py` |
| `sk-wiki` | Compiled persistent knowledge base, Basic Memory | `raw/`, `compiled/`, `AGENTS.md`, `log.md` |
| `awt` | Agile workflow tracker | `awt.db`, `sprints/`, `issues/`, `schema.sql` |
| `kos` | Kancil operating system| `daemons/`, `kernel/`, `systemd/`, `kos.conf` |
| `syafiq-kay.github.io` | Public portfolio, essays, digital garden | `_posts/`, `_layouts/`, `index.html`, `assets/` |
| `neko` | Desktop companion daemon, telemetry | `neko/`, `telemetry/`, `daemon.py`, `mood.json` |
| `hermes` | Daily coordination agent, standup summaries | `hermes/`, `standups/`, `notifications/`, `bot.py` |
| `archive` | Historical cold storage, deprecated records | `archive/`, `cold-storage/`, `manifest.json` |

## Intent-Based Routing Table

Dispatch incoming requests to the appropriate domain module or pipeline phase. See [routing-table.md](references/routing-table.md) for full routing catalog.

| Domain | Skill | Intents / Triggers |
|---|---|---|
| `knowledge` | `wiki-ops` | Compiled knowledge engine, Basic Memory compliance, linting |
| `scrum` | `autonomous-scrum` | Standalone AWT agile engine, PO vs Dev boundary, Event 0 |
| `ecosystem` | `agent-ecosystem` | Fleet governance, golden config, subagents (<=10), handoffs |
| `scholarship` | `academic-scholar` | KCL MSc Mental Health/Ethics/Law, student prose, legal citations |
| `cadence` | `personal-cadence` | ADHD momentum, Jibun Techo projections, Hermes standups |
| `cognition` | `thinking-partner` | Oxford tutorial Socratic sparring, concept stress-testing |

### Coaching Handoff (`/ask-coach`)
If `skills/ask-coach/SKILL.md` exists or `/ask-coach` is installed, route coaching, MSc study, viva, supervision, and session start or end intents to `/ask-coach` (22-skill coaching set, own router). Not a seventh deep module: do not pick a coaching command here. Without it, use `academic-scholar`.

### Upstream Engineering Pipeline
`/grill-me` -> `/to-spec` -> `/to-tickets` -> `/tdd` -> `/code-review` -> `/pr`

## Execution Phase Boundaries

Maintain bounded context and prevent state pollution across phase transitions:

- `Continue`: Iterate in place for bounded, cohesive steps.
- `/clear`: Clean conversation context when switching topics or repos.
- `/handoff`: Persist structured handoff note before context transition.
- `Subagent`: Delegate heavy or discrete execution tasks (strict <=10 batch limit).
- `/compact`: Compact context when token capacity fills.
