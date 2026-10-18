---
name: curate
description: Gateway to knowledge operations and thinking partner work, delegating to the upstream basic-memory-skills and thinking-partner skills. Use when ingesting, searching, or maintaining notes in Basic Memory, or stress-testing a decision.
disable-model-invocation: true
user-invoked: true
version: 1.0.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: curate
---

# Curate

Gateway for knowledge operations and thinking partner work. This module is an Overlay (see `GLOSSARY.md`): it names upstream skills and adds no delta yet. Upstream skills are used unchanged and are not copied here. Later sprints review and modify each referenced upstream skill.

## Knowledge Operations

Source: `basicmachines-co/basic-memory-skills`. Install with `npx skills add basicmachines-co/basic-memory-skills`.

| Intent | Upstream skill |
|---|---|
| Write well-structured notes | `memory-notes` |
| Process unstructured input into entities | `memory-ingest` |
| Research a subject into an entity | `memory-research` |
| Reflect on recent activity | `memory-reflect` |
| Archive and move notes by status | `memory-lifecycle` |
| Search by frontmatter fields | `memory-metadata-search` |
| Manage schemas | `memory-schema` |
| Defragment memory files | `memory-defrag` |
| Track tasks | `memory-tasks` |
| Analyse literary text | `memory-literary-analysis` |

## Thinking Partner

Source: `mattnowdev/thinking-partner`. Install with `npx skills add mattnowdev/thinking-partner`.

| Intent | Upstream skill |
|---|---|
| Challenge assumptions and apply mental models | `thinking-partner` |

## Procedure

1. Match the request to one intent above.
2. Load the named upstream skill and follow it as written.
3. If the skill is not installed, give the install command and stop.
4. Do not paraphrase, copy, or edit upstream content.

## Boundaries

- Persistent writes go through the Basic Memory tools that the upstream skill names.
- Authorised sources are listed in `docs/authorised-skill-repositories.md`.
