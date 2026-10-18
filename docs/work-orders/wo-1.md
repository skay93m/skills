---
title: Work Order 1: Sprint 1 (v1.0.0 Style and Agile Baseline)
tags: [work-order, sprint-1, v1.0.0, style, agile]
type: work-order
---

# Work Order 1: Sprint 1 (v1.0.0 Style and Agile Baseline)

Work Order 1 packages Sprint 1 of repository v1.0.0 for autonomous, unattended execution by a Chief of Staff coordinator agent. The Chief of Staff executes each ticket sequentially, enforces deterministic pre-checks and bounded review loops, and logs all progress directly into this document.

> [!IMPORTANT]
> **Execution Mode**: Fully autonomous AFK.
> **Governing Protocol**: `docs/agents/coordinator-protocol.md`.
> **Review Ceiling**: Pass 0 plus up to 2 remediation loops (maximum 3 review runs per ticket).
> **Pruning Invariant**: Pre-configured prune points are strictly confidential to the Chief of Staff. Subagents receive only the pure GitHub ticket and specification.

## 1. Sprint Identity and Scope

- **Milestone**: `v1.0.0: Minimal Production Deploy`
- **Cadence**: Sprint 1 (Single session delivery)
- **Primary Deliverables**:
  1. Author and activate `skills/style/` enforcing British English, zero em dashes, and zero horizontal dividers.
  2. Refactor `AGENTS.md` for native GitHub Agile sprint workflows.
  3. Retire legacy maintenance code via Issue #114.
  4. Verify the 5-point CI release gate and cut release tag `v1.0.0`.

## 2. Sequential Ticket Execution Order

The Chief of Staff processes tickets sequentially on dedicated sprint branch `sprint-1` (branched from `origin/main`), merging into `main` via a single pull request once all tickets pass and the 5-point release gate is verified:

### Ticket 1: Issue #160
- **Title**: `[v1.0.0] Implement style skill and refactor AGENTS.md for Agile sprints`
- **Execution Target**: Author `skills/style/SKILL.md`, reference guides, tests, and refactor `AGENTS.md`.
- **Review Tier**: Standard (Deterministic pre-checks followed by unified Spec and Standards Reviewer).

### Ticket 2: Issue #114
- **Title**: `[v1.0.0] Retire superseded report-only maintenance code and spec text`
- **Execution Target**: Delete `scripts/knowledge_maintenance.py`, `tests/test_knowledge_maintenance.py`, and update specs.
- **Review Tier**: Standard (Deterministic pre-checks followed by unified Spec and Standards Reviewer).

### Ticket 3: Issue #162
- **Title**: `[v1.0.0] Verify 5-point CI release gate, packaging, and tag v1.0.0`
- **Execution Target**:
  1. Run 5-point CI release gate on `sprint-1`.
  2. Open release pull request from `sprint-1` into `main` (`gh pr create --base main --head sprint-1`).
  3. Merge pull request into `main` (`gh pr merge --admin --merge`).
  4. Check out `main`, verify clean git status, tag `v1.0.0` on `main`, and push tag (`git push origin v1.0.0`).
  5. Publish `docs/releases/v1.0.0.md` and close Milestone `v1.0.0: Minimal Production Deploy`.
- **Review Tier**: Core Release Gate (5-point automated CI checks plus release audit).

## 3. Pre-Configured Prune Points (Coordinator Exclusive Authority)

The Chief of Staff consults these designated boundaries only if Loop 2 review fails to converge:

| Ticket | Pre-Configured Prune Point (Non-Critical) | Essential Scope (Non-Negotiable) | Fail-Closed Behaviour |
| :--- | :--- | :--- | :--- |
| **#160** | If token ceiling check in `check-standard.py` blocks due to legacy skill count or reference files, prune token ceiling adjustment and defer explicitly to Issue #163. | Creation of `skills/style/`, British English enforcement, zero em dashes, zero horizontal dividers, `AGENTS.md` sprint refactor. | Fail closed to `ready-for-human` if any essential scope fails. |
| **#114** | None permitted. | Complete deletion of superseded maintenance code and green test suite. | Fail closed to `ready-for-human`. |
| **#162** | None permitted. | Clean pass across all 5 release gates and clean git working tree. | Fail closed, abort release tag. |

## 4. Living Execution Ledger

The Chief of Staff appends all status updates, subagent conversation IDs, verification results, and operational incidents below as tickets progress.

### Ticket Execution Log
- **Status**: Pending Dispatch
- **Dispatched At**: (Pending)
- **Completed At**: (Pending)

*(Chief of Staff: append entries below using the format: `[YYYY-MM-DD HH:MM] <Ticket / Action>: <Details>`)*

## Observations
- [decision] Package Sprint 1 into sequential Work Order WO-1 #sprint
- [requirement] Implement style skill and refactor AGENTS.md as Ticket 1 #style #agile
- [requirement] Retire superseded maintenance code under Issue #114 as Ticket 2 #cleanup
- [requirement] Execute 5-point CI release gate and cut v1.0.0 as Ticket 3 #release
- [rule] Pruning boundaries are strictly confidential to the Chief of Staff #safety

## Relations
- implements [[coordinator-protocol]]
- implements [[sprint-1-plan]]
- addresses [[issue-160]]
- addresses [[issue-114]]
- addresses [[issue-162]]
- defines [[glossary]]
