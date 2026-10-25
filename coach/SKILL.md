---
name: coach
description: Unified deep-module Life OS & Coaching workflow (Apex Tier 1 life-coach, Tier 2 specialist coaches study-coach, career-coach, finance-coach), covering Season Manifesto alignment, weekly Sunday sync, mid-season check, season transition, Superfocus task/journal distillation, and where-are-we amnesia recovery. Trigger on "life-coach", "weekly sync", "weekly align", "mid-season", "season transition", "where are we?", study, career, or finance requests.
---

# Coach: Unified Life OS & Deep-Module Coaching Workflow

This deep-module skill unifies apex Life OS orchestration (`life-coach`), specialist coaching operations (`study-coach`, `career-coach`, `finance-coach`), workspace lifecycle management, and boundary alignment across all domain vaults.

## Shared Coaching Boundary (Revision `3`) Invariants

1. **Knowledge Vault (`wiki`)**: The single target canonical **Knowledge Vault** for both durable cross-coach personal context and standalone subject/domain synthesis.
2. **Transitional Commonplace (`commonplace`)**: Transitional subject vault pending its roadmapped merge into `wiki`. Read existing subject material in `commonplace` and `wiki`; never duplicate transcripts.
3. **2-Tier Coaching Hierarchy (Tier 1 Apex `life-coach` & Tier 2 Specialist Coaches)**:
   - **Tier 1 — Apex Coach (`life-coach`)**: Operates directly over `wiki` (`projects/life-compass/current-season`, `journal/`, `inbox/`, `tasks/`), **Superfocus MCP**, and **all registered Specialist Coaches** (`active_coaches` in `current-season.md`, currently `study-coach`, `career-coach`, `finance-coach`, plus any future `<domain>-coach`). Also covers uncoached life domains (*Health*, *Family & Friends*, *Household*).
   - **Tier 2 — Specialist Coaches (`<domain>-coach`)**: Isolated domain workspaces in `coaches/<domain>-coach` (`study-coach`, `career-coach`, `finance-coach`, etc.).
4. **Superfocus**: Exclusive owner of goals, milestones, tasks, due dates, priority, scheduling, and backlog. Read-only by default; mutate only with explicit user authorization.
5. **Explicit Project Rule**: Every Basic Memory MCP or `bm` CLI call MUST pass `project="<project>"` explicitly (e.g. `project="wiki"`, `project="study-coach"`).
6. **Desktop-Only Lifecycle Gate (macOS / Windows)**: Session operations (`start`, `resume`, `work`, `close`) may run on both desktop and mobile via Basic Memory MCP. Lifecycle and architecture operations (`create`, `extend`, `align`) require local Meta-Repository and shell access on macOS (or Windows) and MUST be refused in mobile or cloud-only sessions.

## Coach Adapter Interface Table

| Specialist Coach | Primary Entry Note | Contract & Records | Standards & Governance |
|---|---|---|---|
| `study-coach` | `AGENTS.md`, `index.md` | `contract/`, `record/` | `standards.md` |
| `career-coach` | `AGENTS.md`, `index.md` | `contract/`, `record/` | `standards.md` (legacy: `career-coach.md`, `review-standards.md`) |
| `finance-coach` | `AGENTS.md`, `index.md` | `contract/`, `record/` | `standards.md` |

## Routing Table

Dispatch to exactly one reference workflow based on user intent:
- **`life-coach` | `weekly sync` | `weekly align` | `mid-season` | `season transition` | `where are we?` | `start` | `resume` | `work` | `close`**: Load [references/session.md](references/session.md).
- **`create` | `extend`**: Load [references/create.md](references/create.md).
- **`align`**: Load [references/align.md](references/align.md).
