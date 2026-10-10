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

### Phase 3: safe command contract
Document inputs, outputs, failure modes, and confirmation requirements for:
- `sk-onboarding`: initial machine setup.
- `skills verify`: read-only diagnosis.
- `skills update`: routine updates for authorised repositories.
- `skills heal`: explicit high-risk repair.
- `skills add <repo-url>`: proposal for adding an authorised repository.
- `skills reinstall <repo>`: explicit reinstall of one authorised repository.
- `skills review`: report stale, unused, duplicate or orphaned skills.
- `skills remove <skill>`: explicit removal after confirmation.

### Phase 4: onboarding
Revise `sk-onboarding` only after the contract is approved.

### Phase 5: verification
Implement `skills verify` as read-only diagnosis.

### Phase 6: routine update
Update only repositories already on the authorised list.

### Phase 7: healing and explicit repair
A future `skills heal` flow must inspect state, produce a repair plan, and wait for explicit human approval.

### Phase 8: repository and skill lifecycle
Future `add`, `reinstall`, `review`, and `remove` flows.

## Deferred Work
- The full CLI
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

## Open Decisions
- Exact implementation location for the `skills` CLI.
- Schema for `docs/authorised-skill-repositories.md`.
- Whether `golden-skills.json` is generated or validated.
- Exact onboarding behaviour by agent and operating system.
- Technical implementation of human confirmation.
- Whether `develop` also receives branch protection.
- Extension metadata and wrapper, overlay or copy model.
- Verification-report and handover-prompt format.
- Historical snapshot format.
- Final authorised repository list.
