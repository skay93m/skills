# Syafiq Kay Skills

Personal skills and adapters for Syafiq's agent environments.

This repository is the Syafiq-owned extension layer in a larger, centralised
skills installation. It is not a replacement for the upstream skill
repositories. Agents should use the golden configuration and the provenance
declared below before creating, copying, adapting, or overriding a skill.

## Upstream skill sources

The current golden configuration is recorded in
[`skills/sk-update/golden-skills.json`](skills/sk-update/golden-skills.json).
It points the local agent runtimes at these canonical sources:

| Source | Upstream repository or installation | Local canonical path |
| --- | --- | --- |
| Matt Pocock skills | [mattpocock/skills](https://github.com/mattpocock/skills) | `~/.agents/mattpocock-skills/skills/engineering` and `~/.agents/mattpocock-skills/skills/productivity` |
| Basic Memory skills | [basicmachines-co/basic-memory-skills](https://github.com/basicmachines-co/basic-memory-skills) | `~/.agents/basic-memory-skills` |
| Syafiq Kay skills | [skay93m/syafiq-kay-skills](https://github.com/skay93m/syafiq-kay-skills) | `~/.agents/syafiq-kay-skills/skills` |
| Agy built-ins | Agent-runtime installation | `~/.agents/agy-builtin-skills/skills` |

The repository names above are provenance pointers, not permission to add a
repository to the golden configuration. Only Syafiq may authorise additions to
that configuration.

## Extension policy

Before adding a skill, check whether an upstream source already provides the
capability. Personal work should normally be expressed as one of these,
listed from least to most divergent:

1. configuration or composition;
2. an adapter that delegates to the upstream skill and changes only the
   required interface or policy boundary;
3. a documented extension;
4. a fork or replacement, only when the upstream contract cannot support the
   requirement.

Every adapter or extension must identify its upstream source, preserve the
reason for divergence, and receive security, optimisation, duplication, and
public-surface review. Do not silently copy an upstream skill into this repo.

## Repository conventions

- `develop` is the development branch.
- Work is developed and reviewed on `develop`.
- Ready production changes are merged from `develop` into `main`.
- `main` is the production-ready branch.
- Skills should be small, composable, and progressively disclosed. Supporting
  scripts and references should be added only when they materially improve
  reliability or reduce repeated instructions.
- This repository must remain safe to publish: do not commit secrets, private
  Wiki content, personal information, local machine paths, private prompts, or
  internal URLs.

## Current skills

The `skills/` directory currently contains Syafiq-owned skills, including
onboarding, updates, Wiki governance, ingestion, semantic review, and
reconciliation. Read each skill's `SKILL.md` for its trigger and operating
boundary. The golden configuration identifies what is installed centrally; it
does not make every skill in this repository an upstream source for other
skills.

## Planned tooling

The command-line workflow is intentionally being discovered incrementally. The
roadmap includes human-controlled commands for onboarding, verification,
updates, healing drift, adding an authorised source, reinstalling a source,
and reviewing stale or unused skills. These commands are not yet the contract
of this repository and should not be inferred from `--help` output.

## Related knowledge

The detailed design rationale and open questions live in the Wiki. The
work-facing vision is the reference note
`references/personal-ai-engineering-vision`; its detailed synthesis is
`concepts/personal-ai-engineering-system`. This README records only the
repository-level operational context needed by an agent working here.
