---
status: proposed
---

# Four-Domain Gateway and Style Architecture with Upstream Delegation

The repository collapses from a sprawling catalog of 60+ flat skills into a strict **4+1 Deep Module Architecture**: a single master gateway (`ask-syafiq`), 4 user-invoked action domains (`curate`, `code`, `tutor`, `setup`), and an ambient shared presentation and artifact foundation (`style`). Common coding and knowledge operations delegate directly to upstream authoritative repositories, while personal skills house uncopyable domain taste and non-negotiable invariants.

## Context

Over successive development sprints, the repository accumulated 62 skill folders, including 26 legacy skills, 6 historical deep modules, 5 loose knowledge-maintenance utilities, and 22 flat coaching skills imported from `skay93m/msc-coach` via PR #155. This caused:
1. **Severe Namespace Sprawl**: Agent discovery menus and `npx skills add` were flooded with internal procedural micro-steps (`preview`, `quiz`, `think`, `session-start`, `session-end`).
2. **Quality & Budget Failures**: PR #155 breached the mandatory 700-token ceiling across 11 to 17 skills, resulting in a BLOCKING standards review failure.
3. **Prompt Sediment & No-Ops**: Generic instructions that foundation models already obey by default paid a permanent context tax without changing agent behavior.

## Decision

1. **Root Directory Invariant (Exactly 6 Folders)**:
   The root of `skills/` exposes only 6 directories:
   - `skills/ask-syafiq`: Master Diagnostic Gateway and Fallback Router. **The only model-invoked router** (`disable-model-invocation: false`).
   - `skills/curate`: User-invoked (`/curate`). Owns personal wiki operations and Karpathy-style knowledge compounding.
   - `skills/code`: User-invoked (`/code`). Owns the software engineering lifecycle and agile sprint tracking (AWT).
   - `skills/tutor`: User-invoked (`/tutor`). Owns KCL MSc legal scholarship (OSCOLA), supervisory coaching, Socratic sparring, and ADHD daily cadence.
   - `skills/setup`: User-invoked (`/setup`). Owns agent fleet governance (`~/.agents`), golden symlink sync, subagent batch ceilings ($\le 10$), and onboarding.
   - `skills/style`: Ambient Shared Foundation (`user-invoked: false`, `disable-model-invocation: false`). Serves as the Shared Kernel across all skills, housing ubiquitous language, anti-verbosity rubrics, and shared artifact templates.

2. **Upstream Delegation & Code Review Enhancement**:
   - `curate` demotes custom maintenance engines and delegates common knowledge operations to upstream `basicmachines-co/basic-memory-skills`.
   - `code` delegates standard TDD, code review, spec, and ticket pipelines to upstream `mattpocock/skills`, while **refactoring `code-review` into three parallel subagents** (Spec compliance, Codebase architectural integration, and Standards conformance) to eliminate architectural drift.
   - Personal skills strictly focus on uncopyable taste, statutory doctrine, and non-default constraints.

3. **External Governance & Submodule Refactoring (`msc-coach`)**:
   - The 22 flat coaching skills from `skay93m/msc-coach` are withheld from the root `skills/` namespace.
   - A request is transmitted to `skay93m/msc-coach` to refactor its package into an encapsulated submodule with internal references fitting within the 700-token ceiling, for ingestion under `skills/tutor/workflows/coaching/`.

4. **Fail-Closed Tombstones with Zero-PII Telemetry**:
   - All legacy and demoted skills remain as passive, fail-closed tombstones with zero scripts and zero mutations.
   - Tombstones redirect callers to `ask-syafiq` and trigger an anonymous, zero-PII metadata counter event on GitHub to track revival demand without logging user prompts or code.

5. **`style` as an Ambient Companion Peer-Dependency**:
   - Modular installs via `npx skills add skay93m/skills --skill <name>` automatically bundle `style` as a companion peer dependency, guaranteeing shared templates and ubiquitous language are always present.

## Considered Options

1. **Retain the 60+ Flat Skills in Root**: Rejected. Floods global slash menus, inflates agent startup context, causes namespace collisions, and permanently fails the 700-token budget gate.
2. **Retain the 6 Legacy Deep Modules (`wiki-ops`, `autonomous-scrum`, etc.)**: Rejected. The 6-domain classification fractured related activities (`scholarship` and `cognition` were separated from knowledge; `cadence` was separated from tasks; `autonomous-scrum` was separated from engineering). The 4 action verbs (`curate`, `code`, `tutor`, `setup`) provide a cohesive, MECE taxonomy.
3. **Four Action Domains + Master Gateway + Shared Foundation (Chosen)**: Establishes a minimal public surface, isolates internal procedures behind deep seams, and delegates generic engineering to established upstream maintainers.

## Consequences

- Existing tests asserting the 60-skill catalog or legacy 6-module taxonomy will fail until retargeted in lockstep with the Phase 4 implementation.
- Consumers using old slash commands (`/wiki-ops`, `/autonomous-scrum`, `/preview`) are intercepted by safe tombstones and redirected to `/ask-syafiq`.
- PR #155 will be closed in favor of an upstream submodule issue on `skay93m/msc-coach`.
- Scaffolding tools (`new-skill.py`) and standard checkers (`check-standard.py`) must be updated to validate the new domain enum and token limits.

## Superseding note (2026-10-18)

This note supersedes earlier text above, which is left unaltered. Four changes apply:

1. Tombstones are replaced by outright deletion of retired skills. Safe tombstones and revival demand counters are dropped.
2. The three-axis `code-review` refactor is deferred out of v1. `code` uses an Overlay on the upstream skills for now.
3. `tutor` ships empty in v1. The `msc-coach` submodule is not ingested yet.
4. `setup` ships minimal in v1.
