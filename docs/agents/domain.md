---
title: Domain Docs
tags: [domain, glossary, adr, documentation, memory-notes]
type: reference
---

# Domain Docs

How engineering skills and autonomous agents consume and author this repository's domain documentation.

## Before Exploring, Read These

- **`GLOSSARY.md`** at the repository root, or
- **`GLOSSARY-MAP.md`** at the repository root if it exists: it points at one `GLOSSARY.md` per context. Read each one relevant to the topic.
- **`docs/adr/`**: read Architectural Decision Records (ADRs) that touch the area you are about to work in. In multi-context repositories, also inspect `src/<context>/docs/adr/` for context-scoped decisions.

`CONTEXT.md` at the repository root is a redirect to `GLOSSARY.md`. Older versions of the engineering skills read `CONTEXT.md` (upstream renamed it to `GLOSSARY.md` on 2026-08-15), so the stub enables both versions to find the glossary. Keep all terms in `GLOSSARY.md`; do not add terms to `CONTEXT.md`.

If any of these files do not exist, proceed silently. Do not flag their absence and do not suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions are resolved.

## File Structure

Single-context repository (standard layout):

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-guarded-unattended-mutation-profiles.md
│   └── 0002-four-domain-gateway-and-style-architecture.md
└── skills/
```

Multi-context repository (indicated by the presence of `GLOSSARY-MAP.md` at the root):

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          (system-wide decisions)
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  (context-specific decisions)
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## Memory-Notes Structure and Conventions

All domain documents, ADRs, specifications, and persistent notes must adhere to the `memory-notes` convention:

1. **YAML Frontmatter**:
   - `title`: Matches the top-level `# Heading` exactly.
   - `tags`: Lowercase kebab-case tags for indexing and discovery.
   - `type`: Semantic note type (e.g. `glossary`, `adr`, `standard`, `reference`, `protocol`, `docket`, `work-order`).
2. **Generous Context Body**:
   - Free-form markdown between the title heading and the Observations section.
   - Detail the problem, motivation, architectural trade-offs, and design rationale.
3. **Categorised Observations**:
   - Synthesise atomic facts in the form `- [category] Observation statement #tag`.
   - Examples of semantic categories: `[decision]`, `[requirement]`, `[risk]`, `[standard]`, `[convention]`, `[authority]`.
4. **Wiki-Link Relations**:
   - Relate notes using wiki-links in the form `- <relation_type> [[target-note]]`.
   - Filenames and directory paths must strictly adhere to lowercase ASCII kebab-case (`example-note.md`).

## Use the Glossary's Vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, or a test name), use the term as defined in `GLOSSARY.md`. Do not drift to synonyms that the glossary explicitly avoids.

If the concept you need is not in the glossary yet, that is a signal: either you are inventing language the project does not use, or there is a genuine gap to capture via `/domain-modeling`.

## Flag ADR Conflicts

If your proposal contradicts an existing ADR, surface it explicitly rather than silently overriding:

> Contradicts ADR-0001 (guarded unattended mutation profiles), but worth reopening because...

## Observations
- [domain] GLOSSARY.md at repository root provides the single source of truth for repository language #domain #glossary
- [structure] Require memory-notes structure across all domain docs, ADRs, and persistent notes #memory-notes
- [convention] Enforce lowercase kebab-case for file paths and wiki-links #conventions
- [style] Enforce British English spelling, zero em dashes, and zero body horizontal dividers #style

## Relations
- implements [[AGENTS]]
- aligns_with [[GLOSSARY]]
- references [[coordinator-protocol]]
