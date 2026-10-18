---
title: Issue Tracker: GitHub
tags: [github, issues, agile, sprints, tracking]
type: reference
---

# Issue Tracker: GitHub

Issues and specifications for this repository live natively as GitHub issues. Use the `gh` CLI for all tracking and lifecycle operations.

## Agile Sprint Framework in GitHub

The repository tracks agile delivery natively using GitHub constructs:

- **Sprints as Milestones**: Each agile sprint or release cycle is represented by a GitHub Milestone (e.g. `v1.0.0: Minimal Production Deploy`). A milestone sets the delivery boundary, release criteria, and target cadence.
- **Epics**: High-level capability streams or architectural transitions are tracked as top-level issues. Epics hold task lists of child tickets or use GitHub sub-issues.
- **Issues (Sprint Tickets)**: Concrete, granular units of delivery. Every ticket must define clear file boundaries, functional requirements, and deterministic verification criteria.
- **Dependencies**: Native GitHub issue dependencies represent sequential blockers. Tickets declare blockers using `blocked_by` relationships.

## Interface: Issues, Dockets, and Work Orders

The agile framework coordinates three distinct artefacts:

### 1. Dockets (`docs/dockets/docket-<no>.md`)
- **Role**: Human deliberation, architectural trade-offs, and adversarial debate.
- **Surface**: Authored for asynchronous reading and inline annotation in Obsidian.
- **Workflow**: Syafiq reviews the docket and adds inline annotations (e.g. `> agreed`, `> comment`). Once Syafiq signals "docket reviewed" or "docket <n> approved", the agent adopts the annotated decisions.

### 2. Work Orders (`docs/work-orders/wo-<no>.md`)
- **Role**: Authoritative operational directives packaging sprint tickets for autonomous Away From Keyboard (AFK) delivery.
- **Contents**: Scope identity, sequential ticket execution order, pre-configured prune points, and a living execution ledger.
- **Pruning Isolation**: Pre-configured prune points remain strictly confidential to the Chief of Staff coordinator. Implementer subagents see only the pure GitHub ticket and specification.

### 3. GitHub Issues
- **Role**: The operational execution surface and public ledger of record.
- **Workflow**: Subagents are dispatched against specific issue numbers (`#160`, `#114`, `#162`). Completion reports, review findings, and merge links are posted directly to the relevant issues.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Sub-issue relationship**: `gh issue create --parent <parent> ...`, or `gh issue edit <parent> --add-sub-issue <child>` (`gh` 2.94+). Where native sub-issues are unavailable, declare `Part of #<parent>` at the top of the child body.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply or remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close an issue**: `gh issue close <number> --comment "..."`

Infer the repository from `git remote -v`; `gh` performs this automatically inside a clone.

## Pull Requests as a Triage Surface

**PRs as a request surface: no.** (Set to `yes` if external pull requests are treated as feature requests; `/triage` reads this flag.)

When set to `yes`, pull requests run through the same labels and states as issues, using `gh pr` equivalents:
- **Read a PR**: `gh pr view <number> --comments` and `gh pr diff <number>` for the diff.
- **List external PRs for triage**: `gh api --paginate 'repos/{owner}/{repo}/pulls?state=open' --jq '.[] | select(.author_association | IN("OWNER","MEMBER","COLLABORATOR") | not) | {number, title, author: .user.login, author_association, labels: [.labels[].name]}'`.
- **Comment, label, or close**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub shares one number space across issues and PRs. A bare `#42` may refer to either: resolve with `gh pr view 42` and fall back to `gh issue view 42`.

## Wayfinding Operations

Used by `/wayfinder`. The **map** is a single issue with child issues as tickets:

- **Map**: A single issue labelled `wayfinder:map`, holding Notes, Decisions-so-far, and Fog sections. Created via `gh issue create --label wayfinder:map`.
- **Child ticket**: An issue linked to the map as a GitHub sub-issue or task list item with `Part of #<map>`. Labels: `wayfinder:<type>` (`research`, `prototype`, `grilling`, `task`). Once claimed, assigned to the driving developer.
- **Blocking**: GitHub native issue dependencies represent the canonical, UI-visible blockers:
  `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`
  where `<blocker-db-id>` is the numeric database id (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, not the `#number` or `node_id`). GitHub reports `issue_dependencies_summary.blocked_by`. Where dependencies are not available, use `Blocked by: #<n>, #<n>` at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: List open children of the map, drop any with open blockers or an assignee; first in map order wins.
- **Claim**: `gh issue edit <n> --add-assignee @me`, the session's first write.
- **Resolve**: `gh issue comment <n> --body "<answer>"`, then `gh issue close <n>`, then append a context pointer (gist and link) to the map's Decisions-so-far.

## Observations
- [governance] Represent Agile sprints natively using GitHub Milestones, Epics, and Issues #agile #github
- [workflow] Dockets define deliberation, Work Orders define AFK dispatch, and Issues track execution #interface
- [dependencies] Manage blockers using native GitHub issue dependencies #dependencies
- [style] Enforce British English spelling, zero em dashes, and zero body horizontal dividers #style

## Relations
- implements [[AGENTS]]
- relates_to [[wo-1]]
- relates_to [[docket-1]]
- aligns_with [[GLOSSARY]]
- references [[triage-labels]]
