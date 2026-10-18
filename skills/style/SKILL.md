---
name: style
description: Mandatory ambient writing standard for Syafiq's repositories and sessions, requiring British English, zero em dashes, zero horizontal dividers, and clean markdown tables. Use when writing or reviewing any document, comment, code artefact, report, or chat reply.
disable-model-invocation: false
user-invoked: false
version: 1.0.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: governance
---

# Style

Ambient standard for every document, comment, code artefact, report, and chat reply produced in this repository or for Syafiq. Load it before writing. It overrides default habits.

## Mandatory Rules

1. **British English.** Spell prose and new identifiers in British English (prioritise, behaviour, organise, synthesise, artefact). Keep existing identifiers, YAML keys, upstream names, and quoted text unchanged.
2. **Zero em dashes.** Never use the em dash character, and do not substitute an en dash. Use a comma, a colon, or parentheses.
3. **Zero horizontal dividers.** In markdown bodies, chat replies, and reviews, never write a rule line made of three or more hyphens, asterisks, or underscores. Use a heading instead. YAML frontmatter delimiters are the only permitted exception.
4. **Clean tables.** Keep one point per cell. If a cell needs a second clause, split the row or use a bullet list.
5. **No emoji** in repository artefacts, unless a tool or instruction requires one, such as the attribution line on a pull request.
6. **Line budgets.** Keep documents concise and modular. Respect skill line budgets, such as the 100-line limit on `SKILL.md`.

## Vocabulary

Use the terms in `GLOSSARY.md`, the single source of truth. A sprint is a GitHub Milestone. An epic is a top-level issue with sub-issues. A ticket is an issue labelled `ready-for-agent`. Avoid the synonyms the glossary marks as avoid.

## Writing Checks

Before finishing, scan your output for:
- the em dash character and rule lines;
- US spellings such as color, behavior, organize, analyze, and catalog;
- table cells holding more than one point.

The Stage 1 checker (`scripts/check-standard.py`) blocks em dashes (W1), body dividers (W2), and US spellings (W3) on added lines, before any Stage 2 review runs. See `docs/standards/automated-checks.md`.

## References

- [Language rules](references/language-rules.md): spelling pairs, dash and divider replacements.
- [Markdown layout](references/markdown-layout.md): headings, tables, lists, and the visual document template.
- [Global agent setup](references/global-agent-setup.md): how global agent environments load this skill.
