---
name: code
description: Gateway to engineering pipelines for TDD, specs, tickets, and code review, delegating to the upstream mattpocock/skills skills. Use when writing a spec, splitting tickets, practising TDD, or reviewing code.
disable-model-invocation: true
user-invoked: true
version: 1.0.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: code
---

# Code

Gateway for engineering pipelines. This module is an Overlay (see `GLOSSARY.md`): it names upstream skills and adds no delta yet. Upstream skills are used unchanged and are not copied here. Later sprints review and modify each referenced upstream skill.

## Pipelines

Source: `mattpocock/skills`. Install with `npx skills@latest add mattpocock/skills`.

| Intent | Upstream skill |
|---|---|
| Turn a conversation into a spec | `to-spec` |
| Split a spec into tickets | `to-tickets` |
| Triage incoming issues | `triage` |
| Implement a spec or ticket | `implement-spec`, `implement` |
| Test-driven development | `tdd` |
| Diagnose a hard bug | `diagnosing-bugs` |
| Review changes against standards and spec | `code-review` |
| Stress-test a plan against the domain model | `grill-with-docs` |
| Improve codebase architecture | `improve-codebase-architecture` |
| Write a pull request body | `pr` |

## Procedure

1. Match the request to one intent above.
2. Load the named upstream skill and follow it as written.
3. If the skill is not installed, give the install command and stop.
4. Do not paraphrase, copy, or edit upstream content.

## Boundaries

- The three-axis `code-review` refactor is deferred out of v1. Use the upstream `code-review` as it stands.
- Authorised sources are listed in `docs/authorised-skill-repositories.md`.
