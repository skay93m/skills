---
title: Coordinator & Subagent Protocol
tags: [coordinator, protocol, chief-of-staff, subagents, governance, afk]
type: protocol
---

# Coordinator & Subagent Protocol

**First step: any agent following this protocol must load the `/chief-of-staff` skill before taking any other action.**

Fallback: if the skill is not listed or fails to load, read this document and `AGENTS.md` in full, record in the Work Order ledger that the skill was unavailable, and then follow this document as written.

Next, confirm `AGENTS.md` is in your context. If it is not, read it before acting.

This document defines the official Chief of Staff Coordinator & Subagent Working Protocol for all agent sessions executing in this repository.

## 1. Core Principles

### Role Separation
- The Coordinator never writes application code, tests, or skill files in the parent context. It scopes tasks, delegates to subagents, enforces batch limits, orchestrates verification and review, dispatches fixes, and performs git operations (branching, PRs, landing, roll-backs).

### Sequential Ticket Flow on Dedicated Sprint Branch
- Each sprint runs on a dedicated branch (for example `sprint-1` from `origin/main`). Tickets land into it strictly sequentially, each completing its full lifecycle (planning, implementation, verification, fixer loop, merge) before the next begins.
- No parallel multi-worktree ticket execution in unattended AFK sprints (avoids `.git/index.lock` collisions and semantic merge conflicts).
- When all tickets are merged and the full 5-point CI release gate passes on the sprint branch, merge into `main` via a single verified pull request.

### Model Tiers
- The Coordinator runs on `opus`, the most capable Claude Code tier, for orchestration and high-complexity design.
- Implementers, reviewers and fixers default to `sonnet`, which balances cost and capability. Use `haiku` only for mechanical, fully specified edits.
- Set the tier on each Agent tool dispatch with its `model` argument (`opus`, `sonnet` or `haiku`), unless the task mandates another tier.

### Batching and Lifecycle Cleanup
- Never spawn more than 10 subagents in one batch. Queue larger sets in sequential batches, waiting for each to finish.
- Terminate idle or completed subagents before dispatching the next phase or batch.

## 2. Phase-by-Phase Workflow

### Phase 1: Sprint Planning
1. Review the milestone, Work Order, and issues (`gh issue view`, specifications).
2. Check codebase alignment once for cross-cutting architectural consistency.
3. Fix scope boundaries, target paths, constraints, and acceptance criteria for the ticket.
4. Write a self-contained task prompt for an Implementation subagent.

### Phase 2: Implementation Delegation
1. Dispatch an Implementation Subagent (every subagent prompt, including reviewers and fixers, must tell it to read `AGENTS.md` first) with only the GitHub ticket and specification (never prune points, per `AGENTS.md`), plus task scope, strict file boundaries, edge-case requirements, and verification commands (`python3 scripts/check-standard.py`, `uv run --no-project --with pytest python -m pytest tests -q`).
2. The subagent edits, runs the suite, and returns its final report as the Agent tool result.
3. The Coordinator inspects the report, git status, and diff, then terminates the subagent before review.

### Phase 3: Tiered Staged Verification
- **Stage 1 (deterministic)**: run `python3 scripts/check-standard.py` and `uv run --no-project --with pytest python -m pytest tests -q`. On any failure, return the logs to the implementer and spawn no review agents.
- **Stage 2 (adversarial review)**, only once Stage 1 is green, following `docs/standards/pr-review-standard.md`:
  - Standard tickets: one unified reviewer audits specification adherence and coding standards.
  - Core interface or protocol changes: three parallel reviewers, one per axis (three-axis review):
    - Spec: an Adversarial Spec Reviewer for omitted requirements, edge cases, interface drift, and missing assertions.
    - Codebase: an Adversarial Codebase Reviewer for how the change fits the whole codebase, including duplicated modules, broken seams, and conflicts with existing conventions.
    - Standards: an Adversarial Standards Reviewer for `skills/style/SKILL.md`, `docs/standards/`, and the repository coding standards.
  - Findings are reported as `BLOCKING [CHECK_ID] path:line` (must fix before merge) or `NON-BLOCKING [CHECK_ID] path:line` (advisory).

### Phase 4: Bounded Remediation Loop
1. Review ceiling: Pass 0 plus up to 2 remediation loops (maximum 3 review runs per ticket).
2. On blocking findings in Pass 0 or Loop 1, dispatch a Fixer Subagent with exact findings, files, lines, and instructions. The Fixer applies changes, runs deterministic tests, and reports back. The Coordinator terminates it and dispatches a re-review.
3. If Loop 2 still has blocking findings, the ticket fails to converge. Check the Work Order for a declared prune point before resetting anything:
   - Declared for that ticket: prune only the named non-essential criterion, defer it to its follow-up ticket, mark the failing test `@pytest.mark.skip(reason="Pruned to Issue #<n>")`, and re-verify the remaining essential scope. Never prune essential criteria.
   - None declared, or essential scope failed: reset the worktree, mark the issue `ready-for-human`, log the incident in the Work Order, and move to the next non-dependent ticket.
4. No code lands on `main` with unresolved blocking findings.

### Phase 5: Pre-Merge Alignment
Re-check codebase alignment and re-run the full Stage 1 checks before merging.

### Phase 6: Landing and Automated Roll-Back
1. Open a pull request or merge the ticket as the repository workflow defines, and confirm `git status` is clean. The pull request body must contain a `Closes #<n>` line for every issue it lands, so GitHub closes those issues on merge.
2. Run the post-merge release gate on `main`.
3. If it fails, never hotfix speculatively on the release branch: run `git revert -m 1 HEAD`, confirm `main` is green again, mark the ticket `ready-for-human` with diagnostic logs, and halt the release sequence.

## 3. Operational Resilience

### HTTP 429 Circuit Breaker
- On `RESOURCE_EXHAUSTED` (HTTP 429), wait 120 seconds before retrying. After three successive backoff cycles, halt the sprint and write a durable handoff report.

### Subagent Watchdogs
- Each dispatch has a completion boundary: 10 minutes for implementation, 5 minutes for review.
- A subagent that has not reported within its boundary is stopped with `TaskStop`, its failure is recorded as an iteration in the ledger, and its task state is cleaned up.

### Living Execution Ledger
- Record progress, subagent IDs, verification logs, and operational events in the active Work Order so execution can resume after compaction or disruption.

## 4. Style and Standards

Follow the style rules in `skills/style/SKILL.md`, and the checks in `docs/standards/automated-checks.md`.

## Observations
- [governance] Codify Chief of Staff AFK execution protocol and Docket 1 adversarial review decisions #afk #governance
- [ceiling] Cap review loops at Pass 0 plus 2 remediation runs (max 3 runs total) before fail-closed quarantine #safety
- [verification] Tier verification into Stage 1 deterministic checks and Stage 2 adversarial reviews #efficiency
- [isolation] Keep prune points strictly confidential to Chief of Staff in Work Orders #integrity
- [resilience] Mandate 120-second backoff circuit breaker for HTTP 429 and automated git revert rollback on main #resilience
- [style] Enforce British English spelling, zero em dashes, and zero body horizontal dividers #style

## Relations
- implements [[docket-1]]
- governs [[wo-1]]
- governs [[AGENTS]]
- aligns_with [[GLOSSARY]]
- references [[pr-review-standard]]
- references [[automated-checks]]
