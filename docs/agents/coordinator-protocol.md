---
title: Coordinator & Subagent Protocol
tags: [coordinator, protocol, chief-of-staff, subagents, governance, afk]
type: protocol
---

# Coordinator & Subagent Protocol

This document defines the official Chief of Staff Coordinator & Subagent Working Protocol for all agent sessions (Claude, Codex, Antigravity) executing in this repository.

## 1. Core Principles

### Role Separation (Pure Coordinator Pattern)
The Parent or Primary Agent functions strictly as a Chief of Staff Coordinator:
- **No Direct Implementation**: The Coordinator never writes application or feature code, tests, or skill files directly in the parent context.
- **Pure Coordination**: The Coordinator's responsibilities are exclusively:
  - Scoping, decomposing, and prioritising issues and tasks.
  - Delegating discrete execution tasks to specialised subagents.
  - Managing subagent lifecycles and enforcing batch limits.
  - Orchestrating tiered staged verification and adversarial code reviews.
  - Dispatching fixes when defects are uncovered.
  - Synthesising final outcomes and executing git operations (branching, PR creation, landing, or roll-backs).
- **Context Preservation**: Keeping the primary context clean of transient implementation diffs and large test logs ensures deep reasoning capacity and clear architectural oversight.

### Sequential Ticket Flow on Dedicated Sprint Branch
- **Dedicated Sprint Branch**: Every sprint executes on a dedicated branch (for example: `sprint-1` branched from `origin/main`). Tickets land sequentially into this sprint branch.
- **Sequential Ticket Execution**: Tickets within a sprint are processed strictly sequentially (Ticket 1 to Land into sprint branch to Ticket 2 to Land into sprint branch).
- **Final Release Pull Request**: Once all sprint tickets are merged and the full 5-point CI release gate passes on the sprint branch, the sprint branch merges into `main` via a single verified pull request.
- **No Parallel Multi-Worktree Ticket Execution**: Processing separate tickets in parallel worktrees is abolished for unattended AFK sprints. This eliminates git index lock collisions (`fatal: Unable to create '.git/index.lock': File exists`) and headless semantic merge conflicts.
- **Run-to-Completion**: A ticket must complete its full lifecycle (planning, implementation, staged verification, fixer loop, verification, merge) before moving to subsequent work. This prevents work-in-progress sprawl and context dilution.

### Cost-Efficiency Tier
- Subagents handle heavy implementation, testing, review, and fixing tasks using cost-efficient models (`Model: "flash"` where supported, such as Gemini Flash, Flash Lite, or fast-tier models).
- Higher-tier reasoning models (`pro` or caller inheritance) are reserved for top-level coordinator orchestration, high-complexity architectural design, or when specifically mandated by the task.

### Batching and Lifecycle Cleanup
- **Subagent Batch Limit**: Never spawn more than 10 subagents in a single batch (strictly adhering to the subagent batching invariant).
- **Sequential Batches**: If a task requires more than 10 workers, queue them in sequential batches of at most 10, waiting for each batch to finish before launching the next.
- **Active Lifecycle Cleanup**: Subagents are ephemeral. The Coordinator must immediately terminate or kill idle or completed subagents before dispatching subsequent phases or new batches. This releases session resources, avoids quota exhaustion (`RESOURCE_EXHAUSTED` / 429), and eliminates zombie processes.

### Pruning Isolation and Integrity
- **Confidential Prune Points**: Pre-configured prune points live exclusively in Work Orders (`docs/work-orders/wo-<no>.md`) and are managed solely by the Chief of Staff Coordinator.
- **Subagent Isolation**: Implementer and reviewer subagents never see prune points or alternative scope boundaries. Subagents receive only the pure GitHub ticket and specification.
- **Moral Hazard Elimination**: Subagents must never have the incentive to fail repeatedly to force scope reduction. Essential acceptance criteria are strictly non-negotiable.

## 2. Phase-by-Phase Workflow

### Phase 1: Sprint Planning and Codebase Alignment
1. Review the sprint milestone, Work Order, and issues (`gh issue view`, specification documents).
2. Evaluate codebase alignment once at the sprint planning stage to verify cross-cutting architectural consistency.
3. Clarify scope boundaries, target file paths, constraints, and acceptance criteria for the target ticket.
4. Formulate a self-contained, explicit task prompt for an Implementation subagent.

### Phase 2: Implementation Delegation
1. Dispatch an Implementation Subagent (`flash` tier) with:
   - Defined task scope and strict file boundaries.
   - Deliverable specifications and edge-case requirements.
   - Verification instructions (`python3 scripts/check-standard.py`, `pytest`).
2. The Implementation Subagent performs edits, runs the test suite, confirms zero errors, and reports back via `send_message`.
3. The Coordinator reviews the completion report and inspects the git status and diff.
4. The Coordinator immediately terminates the Implementation Subagent before initiating review.

### Phase 3: Tiered Staged Verification
Verification is structured into two sequential stages:

#### Stage 1: Deterministic Local Checks
- The Coordinator or a light runner executes deterministic checks:
  - `python3 scripts/check-standard.py`
  - `pytest`
- If Stage 1 fails with any error, the Coordinator returns immediately to the implementer with the deterministic failure logs. Zero LLM review agents are spawned during Stage 1 failures.

#### Stage 2: Adversarial Code Review
Once Stage 1 is completely green, the Coordinator initiates Stage 2:
- **Standard Tickets**: A single unified reviewer (`flash` tier) audits both specification adherence and coding standards.
- **Core Interface or Protocol Modifications**: Dual specialised reviewers (`flash` tier) are dispatched in parallel:
  1. **Adversarial Spec Reviewer**: Hunts for omitted requirements, unhandled edge cases, interface drift, and missing assertions.
  2. **Adversarial Architecture and Standards Reviewer**: Audits architectural alignment, line budgets (100 lines for `SKILL.md`), single-level reference depth, lowercase kebab-case naming, British English spelling, zero em dashes, zero body horizontal dividers, and security hard-stops (`H1` to `H7`).
- **Review Finding Format**:
  - `BLOCKING [CHECK_ID] path/to/file:line`: Must be remediated before merge.
  - `NON-BLOCKING [CHECK_ID] path/to/file:line`: Advisory improvement or stylistic suggestion.

### Phase 4: Bounded Remediation Loop
1. **Review Ceiling**: Enforce Pass 0 plus up to 2 remediation loops (maximum 3 review runs total per ticket).
2. If blocking findings are reported in Pass 0 or Loop 1:
   - The Coordinator dispatches a dedicated Fixer Subagent (`flash` tier) with exact findings, files, lines, and remediation instructions.
   - The Fixer applies changes, runs deterministic tests, and reports back.
   - The Coordinator terminates the Fixer and dispatches verification re-review.
3. **Fail-Closed Boundary and Pruning Evaluation**:
   - If Loop 2 review still contains blocking findings, the ticket fails to converge.
   - The Coordinator evaluates the Work Order for pre-configured prune points before resetting any worktree:
     - If a pre-configured prune point is explicitly declared for that ticket in the Work Order, the Coordinator prunes only the declared non-essential criterion, defers it to its designated follow-up ticket, decorates the failing test with `@pytest.mark.skip(reason="Pruned to Issue #<n>")` to keep the sprint branch green, and re-verifies the remaining essential scope. Essential criteria are never pruned.
     - If no prune point is declared, or if essential scope has failed, the Coordinator halts the ticket immediately: resets the worktree, marks the issue `ready-for-human`, safely logs the incident into the Work Order, and moves to the next non-dependent ticket.
4. **Zero-Defect Gate**: No code lands on `main` with unresolved blocking findings or latent defects.

### Phase 5: Pre-Merge Codebase Alignment and CI Verification
1. Re-evaluate codebase alignment prior to merging into `main`.
2. Confirm the complete test suite passes cleanly across all modules (`pytest`, `python3 scripts/check-standard.py`).

### Phase 6: Sequential Landing and Automated Roll-Back
1. Open a pull request or merge the ticket directly to `main` as defined by the repository workflow.
2. Confirm `git status` is clean on `main`.
3. Execute the post-merge release gate on `main`.
4. **Automated Roll-Back Protocol**:
   - If the post-merge gate fails on `main`, the Coordinator must never attempt speculative autonomous hotfixing directly on the release branch.
   - The Coordinator immediately executes `git revert -m 1 HEAD` to roll back the offending ticket merge.
   - Re-verify that `main` returns to a clean green state.
   - Mark the offending ticket as `ready-for-human` with full diagnostic failure logs, and halt the release sequence.

## 3. Operational Resilience and Circuit Breakers

### HTTP 429 Rate Limit Circuit Breaker
- When an API invocation or subagent launch encounters `RESOURCE_EXHAUSTED` (HTTP 429):
  - Pause execution immediately for a 120-second backoff window using the `schedule` tool or timer.
  - Retry the operation after the backoff expires.
  - If rate limits persist after three successive backoff cycles, halt the sprint and write a durable handoff report.

### Subagent Watchdogs and Timeouts
- Every subagent dispatch must have an expected completion boundary (10 minutes for implementation, 5 minutes for review).
- If a subagent does not report completion within the boundary, the Coordinator uses `manage_task(Action='kill')` to terminate the hung worker, records a failure iteration, and cleans up task state.

### Context Preservation and Living Execution Ledger
- All execution progress, subagent IDs, verification logs, and operational events must be recorded into the active Work Order (`docs/work-orders/wo-<no>.md`).
- This ensures that if session compaction or disruption occurs, execution can resume without amnesia.

## 4. Documentation Integrity and Style Invariants

- **British English**: Use British English spelling consistently (prioritise, behaviour, organisation, synthesise, categorise, artefact).
- **Strictly Zero Em Dashes**: Never use em dashes. Use commas, colons, or parentheses instead.
- **Strictly Zero Body Horizontal Dividers**: Never insert horizontal rules in markdown bodies (only YAML frontmatter delimiters are allowed).
- **Markdown Line Budgets**: Adhere strictly to length limits, such as the 100-line limit on `SKILL.md` files.
- **Reference Depth**: Reference links must remain strictly one level deep from the parent skill. Never link a reference file to another reference file.
- **Path Hygiene**: Never commit hardcoded machine-specific user home paths. Always use repo-relative paths.
- **Privacy and Secrets**: Zero tolerance for credentials, API tokens, internal URLs, or private personal data.

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
