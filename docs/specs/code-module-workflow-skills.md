---
title: Code Module Workflow Skills Specification
tags: [spec, code-module, workflow, agile, chief-of-staff]
type: spec
---

# Code Module Workflow Skills Specification

This specification defines the roadmap and architecture for encapsulating Syafiq's Agile sprint delivery workflows directly into the `skills/code/` deep module. When the repository advances to authoring the `code` domain (under Issue #159), this document provides the exact scope, interface, and skill definitions to implement.

> [!IMPORTANT]
> **Architectural Seam**: While generic coding assistance and language paradigms delegate upstream to `mattpocock/skills`, Syafiq's opinionated delivery methodology (Dockets, Work Orders, and Chief of Staff AFK orchestration) must be encapsulated internally within `skills/code/`.

## 1. Context and Motivation

During the v1.0.0 bootstrap, the repository established a disciplined, autonomous execution model comprising:
1. **Dockets** (`docs/dockets/`): Deliberation packages reviewed and annotated asynchronously in Obsidian.
2. **Work Orders** (`docs/work-orders/`): Actionable execution orders with sequential ticket plans, living execution ledgers, and confidential prune points.
3. **Chief of Staff Protocol**: AFK autonomous delivery with deterministic pre-checks, a three-pass review ceiling, isolated scope pruning, automated rollback on `main`, and rate-limit backoff.

Currently, these workflows operate via documented markdown protocols. In Sprint 2, they must be converted into executable sub-skills and reference routines within the `skills/code/` deep module.

## 2. Target Component Breakdown within skills/code/

The `skills/code/` module will expose a lean, high-level interface in `SKILL.md` (under 100 lines and 700 tokens) with `disable-model-invocation: true`, backed by internal reference routines and scripts:

### Component 1: `code/docket` (Deliberation and Annotation)
- **Purpose**: Creates and manages deliberation dockets.
- **Responsibilities**:
  - Scaffolds new dockets (`docs/dockets/docket-<no>.md`) with `memory-notes` schemas.
  - Automatically parses inline annotations (`> agreed`, `> comment`) when triggered by "docket reviewed".
  - Synthesises findings and updates downstream specifications.

### Component 2: `code/work-order` (Execution Directive and Living Ledger)
- **Purpose**: Packages GitHub milestones and tickets into executable Work Orders.
- **Responsibilities**:
  - Scaffolds `docs/work-orders/wo-<no>.md` with ticket sequences and pre-configured prune points.
  - Guarantees that prune points remain confidential to the coordinator and are never leaked to implementer or reviewer subagents.
  - Maintains the living ledger by appending execution timestamps, subagent conversation IDs, verification results, and operational incidents.

### Component 3: `code/sprint-executor` (Chief of Staff AFK Orchestrator)
- **Purpose**: Executes a Work Order completely unattended (AFK).
- **Responsibilities**:
  - Enforces the bounded iteration model: Pass 0 plus up to 2 remediation loops (maximum 3 review runs per ticket).
  - Runs deterministic pre-flight checks (`pytest`, `scripts/check-standard.py`) prior to spawning any LLM reviewers.
  - Controls exclusive pruning authority on Loop 2 failures: spills pre-configured non-critical scope to follow-up issues, or fails closed to `needs-human` on essential criteria.
  - Executes automated `git revert` rollback on `main` if release CI checks fail.
  - Enforces 120-second backoff and serialization circuit breakers on HTTP 429 quota exhaustion.

### Component 4: `code/adversarial-review` (Two-Axis Staged Review Gate)
- **Purpose**: Tiered review dispatches.
- **Responsibilities**:
  - Gated by Stage 1 deterministic checks.
  - Standard tickets: single unified reviewer for specification and repository standards.
  - Interface tickets: dual reviewers (Spec and Architecture).
  - Codebase alignment evaluated at sprint planning and pre-merge.

## 3. Implementation Roadmap

1. **Sprint 1 (Current)**: Codify protocol in `chief-of-staff-sprint-execution-protocol.md`, establish `WO-1`, cut `v1.0.0`.
2. **Sprint 2 (Issue #159 & #164)**: Scaffold `skills/code/` deep module entrypoint and author the sub-skill reference files in `skills/code/references/`.
3. **Sprint 3**: Introduce CLI automation helpers in `scripts/` to automate docket parsing and Work Order ledger appending.

## Observations
- [decision] Encapsulate Docket, Work Order, and Chief of Staff workflows inside skills/code/ #architecture
- [requirement] Keep skills/code/SKILL.md under 100 lines and 700 tokens with disable-model-invocation: true #budget
- [technique] Delegate generic coding to mattpocock/skills while keeping workflow governance internal #deep-module
- [risk] Context leakage of prune points must be prevented programmatically by the work-order component #security

## Relations
- implements [[Chief of Staff Sprint Execution Protocol]]
- relates_to [[Work Order 1: Sprint 1]]
- relates_to [[Issue 159]]
- defines [[GLOSSARY]]
