---
title: "Work Order 2: Sprint 2 (v1.0.0 4+1 Architecture Delivery)"
tags: [work-order, sprint-2, v1.0.0, architecture, agile]
type: work-order
---

# Work Order 2: Sprint 2 (v1.0.0 4+1 Architecture Delivery)

Packages Sprint 2 for autonomous AFK execution under `docs/agents/coordinator-protocol.md`. Scope, deliverables, and acceptance criteria live in the linked GitHub issues, not here.

## 1. Sprint Identity

- **Milestone**: `v1.0.0: Minimal Production Deploy`, Spec https://github.com/skay93m/skills/issues/157
- **Branch**: `sprint-2` from `origin/main`; one release PR into `main` after the 5-point gate (release ticket https://github.com/skay93m/skills/issues/169)
- **Governing decision**: [ADR 0002](https://github.com/skay93m/skills/blob/main/docs/adr/0002-four-domain-gateway-and-style-architecture.md), with owner overrides: six-directory v1 catalogue, no tombstones, empty `tutor`, minimal `setup`
- **Supersedes**: Ticket 3 of WO-1 (https://github.com/skay93m/skills/issues/162), halted before release and replaced by the release ticket above
- **Curate upstream sources**: `basicmachines-co/basic-memory-skills` and `mattnowdev/thinking-partner`. Future work reviews and modifies each referenced upstream skill.

## 2. Ticket Order

Tickets land sequentially on `sprint-2`. Each completes its full lifecycle before the next begins.

| Order | Issue | Review Tier |
| :--- | :--- | :--- |
| 1 | https://github.com/skay93m/skills/issues/168 | Standard |
| 2 | https://github.com/skay93m/skills/issues/163 | Core, three-axis (Spec, Codebase, Standards) |
| 3 | https://github.com/skay93m/skills/issues/159 | Core, three-axis (Spec, Codebase, Standards) |
| 4 | https://github.com/skay93m/skills/issues/161 | Core, three-axis (Spec, Codebase, Standards) |
| 5 | https://github.com/skay93m/skills/issues/164 | Core Release Gate, three-axis (Spec, Codebase, Standards) |
| 6 | https://github.com/skay93m/skills/issues/169 | Core Release Gate, three-axis (Spec, Codebase, Standards) |

## 3. Pre-Configured Prune Points (Coordinator Exclusive Authority)

The Chief of Staff consults these designated boundaries only if Loop 2 review fails to converge:

| Ticket | Pre-Configured Prune Point (Non-Critical) | Essential Scope (Non-Negotiable) | Fail-Closed Behaviour |
| :--- | :--- | :--- | :--- |
| https://github.com/skay93m/skills/issues/168 | None declared. | Deterministic style checks in `check-standard.py`. | Fail closed to `ready-for-human`. |
| https://github.com/skay93m/skills/issues/163 | None declared. | Domain enum, `disable-model-invocation` rule, 700-token check. | Fail closed to `ready-for-human`. |
| https://github.com/skay93m/skills/issues/159 | None declared. | Four action domain entrypoints and their manifests. | Fail closed to `ready-for-human`. |
| https://github.com/skay93m/skills/issues/161 | None declared. | Gateway routing to the four domains and `style`. | Fail closed to `ready-for-human`. |
| https://github.com/skay93m/skills/issues/164 | None permitted. | Six-directory root with all tests passing. | Fail closed to `ready-for-human`. |
| https://github.com/skay93m/skills/issues/169 | None permitted. | Clean pass across all 5 release gates. | Fail closed, abort release tag. |

## 4. Living Execution Ledger

The Chief of Staff appends all status updates, subagent conversation IDs, verification results, and operational incidents below as tickets progress.

### Ticket Execution Log
- **Status**: Pending Dispatch
- **Dispatched At**: (Pending)
- **Completed At**: (Pending)

*(Chief of Staff: append entries below using the format: `[YYYY-MM-DD HH:MM] <Ticket / Action>: <Details>`)*

[2026-10-18 20:00] Ticket 1 (#168): Implemented, committed 7cb528f. Stage 1 green (247 passed, 0 blocking). Pass 0 review: no blocking findings. Non-blocking: working-tree mode uses two-dot diff (W1), fence handling ignores fence length (W2), unverified 'most capable' wording for opus in the protocol (P1).

## Observations
- [decision] Sprint 2 delivers the v1 six-directory catalogue with no tombstones, replacing the WO-1 release attempt #sprint
- [rule] Pruning boundaries are strictly confidential to the Chief of Staff #safety

## Relations
- implements [[coordinator-protocol]]
- implements [[adr-0002]]
- addresses [[issue-168]]
- addresses [[issue-163]]
- addresses [[issue-159]]
- addresses [[issue-161]]
- addresses [[issue-164]]
- addresses [[issue-169]]
- supersedes [[wo-1]]
