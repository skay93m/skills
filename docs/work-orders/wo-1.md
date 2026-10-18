---
title: "Work Order 1: Sprint 1 (v1.0.0 Style and Agile Baseline)"
tags: [work-order, sprint-1, v1.0.0, style, agile]
type: work-order
---

# Work Order 1: Sprint 1 (v1.0.0 Style and Agile Baseline)

Packages Sprint 1 for autonomous AFK execution under `docs/agents/coordinator-protocol.md`. Scope, deliverables, and acceptance criteria live in the linked GitHub issues, not here.

## 1. Sprint Identity

- **Milestone**: `v1.0.0: Minimal Production Deploy`, Spec https://github.com/skay93m/skills/issues/157 
- **Branch**: `sprint-1` from `origin/main`; one release PR into `main` after the 5-point gate (Ticket 3)

## 2. Ticket Order

| Order | Issue | Review Tier |
| :--- | :--- | :--- |
| 1 | https://github.com/skay93m/skills/issues/160 | Standard |
| 2 | https://github.com/skay93m/skills/issues/114 | Standard |
| 3 | https://github.com/skay93m/skills/issues/162 | Core Release Gate |

## 3. Pre-Configured Prune Points (Coordinator Exclusive Authority)

The Chief of Staff consults these designated boundaries only if Loop 2 review fails to converge:

| Ticket | Pre-Configured Prune Point (Non-Critical) | Essential Scope (Non-Negotiable) | Fail-Closed Behaviour |
| :--- | :--- | :--- | :--- |
| https://github.com/skay93m/skills/issues/160 | If token ceiling check in `check-standard.py` blocks due to legacy skill count or reference files, prune token ceiling adjustment and defer explicitly to Issue https://github.com/skay93m/skills/issues/163. | Creation of `skills/style/`, British English enforcement, zero em dashes, zero horizontal dividers, `AGENTS.md` sprint refactor. | Fail closed to `ready-for-human` if any essential scope fails. |
| https://github.com/skay93m/skills/issues/114 | None permitted. | Complete deletion of superseded maintenance code and green test suite. | Fail closed to `ready-for-human`. |
| https://github.com/skay93m/skills/issues/162 | None permitted. | Clean pass across all 5 release gates and clean git working tree. | Fail closed, abort release tag. |

## 4. Living Execution Ledger

The Chief of Staff appends all status updates, subagent conversation IDs, verification results, and operational incidents below as tickets progress.

### Ticket Execution Log
- **Status**: Pending Dispatch
- **Dispatched At**: (Pending)
- **Completed At**: (Pending)

*(Chief of Staff: append entries below using the format: `[YYYY-MM-DD HH:MM] <Ticket / Action>: <Details>`)*

[2026-10-18 19:00] Ticket 1 (#160): Implemented and committed on sprint-1. Stage 1 green (check-standard 0 blocking, 316 passed). Pass 0 review: no blocking findings, 4 non-blocking advisories (glossary lacks Sprint/Epic/Ticket, two multi-point table cells in AGENTS.md, rule duplication). Also touched tests/test_npx_packaging.py for the 39-skill inventory.
[2026-10-18 19:10] Ticket 2 (#114): Implemented and committed. Deleted knowledge_maintenance.py, its test and orphaned fixture; spec marked retired by ADR 0002. Stage 1 green (240 passed). Pass 0 review: no blocking findings. No explicit tombstone added (absence fails closed); awaiting owner view.
[2026-10-18 19:15] Ticket 3 (#162): HALTED before release. Gate 4 fails: working tree has a pre-existing uncommitted change (docs/standards/pr-review-standard.md deleted, extensionless pr-review-standard untracked) that is not mine to discard. Gate 2 expectation of 317 tests no longer matches (240 after retiring the legacy suite). No PR, merge, or tag was made.

## Observations
- [decision] Package Sprint 1 into sequential Work Order WO-1 #sprint
- [rule] Pruning boundaries are strictly confidential to the Chief of Staff #safety

## Relations
- implements [[coordinator-protocol]]
- implements [[sprint-1-plan]]
- addresses [[issue-160]]
- addresses [[issue-114]]
- addresses [[issue-162]]
- defines [[glossary]]
