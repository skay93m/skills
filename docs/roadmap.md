# Syafiq-Kay-Skills Roadmap

This document records future commands, planned phases, and deferred work for `syafiq-kay-skills`. It serves as the backlog migrated from the initial Wiki planning session.

## Status & Boundaries
- **Waiting for research before implementation.**
- **Scope:** Develop, validate and distribute Syafiq's custom agent skills while safely managing installation and machine configuration.
- **Authority:** Syafiq retains authority over repository additions, destructive changes, production merges, and semantic/policy decisions.
- **Current slice:** The first implementation slice is documentation-only and remains paused pending the research gate.

## Planned Implementation Sequence

### Phase 1: human-readable authority and vocabulary
- Add `docs/authorised-skill-repositories.md`
- Add `docs/glossary.md`
- Add `docs/roadmap.md` (this file)

### Phase 2: authority projection and validation
- Define how `docs/authorised-skill-repositories.md` relates to `skills/sk-update/golden-skills.json`.
  - **Decision:** `golden-skills.json` is the technical source of truth that gets validated against `docs/authorised-skill-repositories.md` to ensure programmatic updates remain aligned with human-readable authority.

### Phase 3-8: Re-evaluation due to CLI Suspension
- **Decision:** The custom `skills` CLI (e.g. `sk-onboarding`, `skills verify`) is currently **suspended**.
- All interaction with Basic Memory should occur exclusively via the Basic Memory MCP tools.
- CLI-specific workflows (onboarding, verification, updates, explicit repair) are deferred or need to be reimagined as Agent Skills rather than bash/CLI commands.
- **Onboarding:** Treat machine onboarding as non-existent. It still needs to be built and should feed into the prioritization matrix. Do not assume the machine is already configured.
- **Verification:** Not needed when interacting via MCP, as there is no local/cloud drift issue to resolve.
- **Human Confirmation:** Technical implementation is deferred while the CLI is suspended.

## Deferred Work
- The full CLI (Currently Suspended)
- Machine Onboarding (feeds into prioritization matrix)
- Automated healing
- Automated repository addition
- Bulk pruning
- Currentness automation
- Research-compounding workflow
- Full ingestion/synthesis governance
- Upstream contribution workflow
- Custom Sourcery review standards (partially addressed via dashboard)
- Complex versioning and package distribution
- Broad test framework

## Settled Decisions
- **CLI Implementation Location:** CLI is suspended. Interaction with Basic Memory is via MCP tools.
- **`golden-skills.json`:** Validated against `docs/authorised-skill-repositories.md` (JSON is the source of truth).
- **Human Confirmation:** Deferred while CLI is suspended.
- **Extension Metadata Model:** Stored directly in the YAML frontmatter of the custom skill's `SKILL.md` (e.g., `upstream_source` and `divergence_rationale`).
- **Branch Protection:** `develop` receives branch protection to ensure all code is reviewed before entering the development branch.
- **Verification & Handover:** Verification is not needed when using MCP tools since there is no local/cloud context drift.
- **Schema for `authorised-skill-repositories.md`:** Standard Markdown table (human-readable).
- **Final Authorised Repositories:** Matt Pocock skills, Basic Memory skills, Syafiq Kay skills, and Agy built-ins.
- **Onboarding Behaviour:** Treat as non-existent and needs to be built; feeds into prioritization. Cannot assume the machine is configured.
- **Historical Snapshots:** Naturally maintained by git history instead of cluttering Basic Memory or filesystems.

## Open Decisions
- (None! All frontier decisions are currently settled.)
