---
title: AGENTS
tags: [governance, agents, standards, agile]
type: root-policy
---

# AGENTS

Instructions and governing operational standards for all AI agents collaborating in this repository.

## Agile Sprint Framework

All planned feature development, refactoring, and maintenance work follow native GitHub Agile workflows:

- **Sprints**: Represented natively by GitHub Milestones (e.g. `v1.0.0: Minimal Production Deploy`). Every sprint defines an explicit objective, release gate, and bounded scope.
- **Epics**: High-level capability streams tracked as top-level GitHub issues with child sub-issues or `Part of #<parent>` task lists.
- **Issues**: Atomic units of work with unambiguous boundaries, verification criteria, and dependency declarations (`blocked_by`).
- **Execution Order**: Milestones execute sequentially on `main` to eliminate merge conflicts and branch drift.

## Deliberation and Execution Interfaces

Work shifts between two primary governing artefacts:

### Dockets (`docs/dockets/docket-<no>.md`)
- Prepared for human deliberation, architectural trade-offs, and asynchronous inspection in Obsidian.
- Deliberation is captured via inline human annotations (e.g. `> agreed`, `> comment`).
- When Syafiq indicates "docket reviewed" or "docket <n> approved", agents inspect the docket annotations and adopt the recorded decisions directly.

### Work Orders (`docs/work-orders/wo-<no>.md`)
- Authoritative operational directives packaging sprint tickets for autonomous Away From Keyboard (AFK) delivery.
- Specify sequential ticket order, pre-configured prune points, and a living execution ledger.
- Prune points are strictly isolated: subagents never see prune points, which remain under the exclusive authority of the Chief of Staff coordinator.

## Coordinator and Subagent Protocol

All multi-step tasks follow the Chief of Staff Coordinator Protocol detailed in `docs/agents/coordinator-protocol.md`:
- **Pure Coordinator**: The parent agent coordinates, delegates discrete execution to subagents, and synthesises outcomes without direct implementation in the parent context.
- **Model Tiers**: Implementer and reviewer subagents operate on cost-effective `flash` models; higher-reasoning tiers are reserved for top-level coordinator orchestration.
- **Batching Ceiling**: Never dispatch more than 10 subagents in a single batch.
- **Review Ceiling**: Standard tickets enforce Pass 0 plus up to 2 remediation loops (maximum 3 review runs total). If Loop 2 fails to converge, the ticket fails closed to human review.
- **Tiered Staged Verification**: Stage 1 deterministic checks (`pytest`, standard checker) gate Stage 2 adversarial reviews.
- **Resilience**: Rate limit circuit breaker (120-second backoff on HTTP 429) and automated git revert roll-back on `main` if post-merge checks fail.

## Style and Presentation Standards

Every document, comment, and code artefact produced must strictly adhere to the repository style rules:
- **British English**: Use British English spelling across all prose and identifiers (e.g. prioritise, behaviour, organisation, synthesise, artefact).
- **Strictly Zero Em Dashes**: Never use em dashes. Use commas, colons, or parentheses instead.
- **Strictly Zero Horizontal Dividers**: Never insert horizontal rules in markdown bodies (only YAML frontmatter delimiters are permitted).
- **Conciseness and Line Budgets**: Maintain strict modularity and respect skill line budgets (e.g. 100-line limit on `SKILL.md`).

## Domain and Documentation Standards

- **Single-Context Domain Model**: The glossary at `GLOSSARY.md` is the single source of truth for repository terminology. `CONTEXT.md` serves only as a redirect. See `docs/agents/domain.md`.
- **Authorised Skill Sources**: Permitted repositories are strictly documented in `docs/authorised-skill-repositories.md`.
- **Triage Labels**: Standard triage label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

## Context and Memory

This project integrates with the Basic Memory persistent memory app:
- Context is queried from the `sk-wiki` project in Basic Memory.
- Notes and persistent artefacts follow the `memory-notes` skill and schema conventions (YAML frontmatter, matching `# Heading`, semantic `[category]` observations, and wiki-link relations `[[target]]`).

## Observations
- [governance] Agile sprints are mapped to GitHub Milestones, Epics, and Issues #agile
- [workflow] Dockets govern human deliberation and Work Orders govern autonomous AFK execution #workflow
- [style] Repository mandates British English, zero em dashes, and zero body horizontal dividers #style
- [architecture] Chief of Staff enforces pure delegation, bounded review loops, and fail-closed isolation #protocol

## Relations
- governs [[coordinator-protocol]]
- governs [[issue-tracker]]
- governs [[domain]]
- defines [[GLOSSARY]]
- references [[authorised-skill-repositories]]
