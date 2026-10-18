---
title: Session Focus Reset - Style-First Minimal v1.0.0 Deployment
type: proposal
status: active
date: 2026-10-18
tags:
  - thinking-partner
  - agile
  - sprint-planning
  - style
  - agents-md
---

# Session Focus Reset: Style-First Minimal v1.0.0 Deployment

> [!IMPORTANT]
> **Context**: Syafiq observed recurring digressions into hypothetical, complex workflows while immediate friction points (em dashes, horizontal dividers, American spelling) remained unresolved.
> **Mandate**: Reset the session goal to the single highest-leverage outcome achievable today: deploy the live `style` skill, codify the simple Milestone = Sprint Agile workflow in `AGENTS.md`, and cut `v1.0.0`.

## 1. Thinking-Partner Analysis: Why We Digressed

1. **The Speculative Generality Trap**:
   We spent substantial turns designing elaborate 3-stage contributor ingestion funnels, review consensus loops, and future governance models. In reality, no external contributor is waiting at the door. The immediate consumer is Syafiq.

2. **Unaddressed Daily Friction**:
   Every response from the agent contains micro-annoyances that violate Syafiq's personal taste:
   - Frequent use of em dashes.
   - Excessive horizontal dividers.
   - American English spellings instead of British English.

3. **Theory of Constraints (TOC) Realignment**:
   The highest leverage intervention is not a theoretical 6-domain architectural revolution. It is establishing the personal `style` skill so that every current and future agent writes with Syafiq's exact taste and voice.

## 2. Definition of Done (DoD) for Today

To achieve a clean, uncompromised deployment today, we reduce the scope to three atomic deliverables:

### Deliverable 1: Live `style` Skill (`skills/style/`)
- Author `skills/style/SKILL.md` (strictly under 100 lines).
- Codify mandatory presentation and language rules:
  - British English spelling (for example: prioritise, catalogue, behaviour, synthesise).
  - Strict ban on em dashes (use parentheses, colons, or commas instead).
  - Strict ban on horizontal dividers (`---`) in standard conversational output.
  - Clear heading hierarchies and visual spacing.
- Verify that `skills/style/` passes all mechanical standard checks.

### Deliverable 2: Refactor `AGENTS.md` for Agile Sprints via GitHub Milestones
- Update `AGENTS.md` to establish GitHub Milestones as the canonical Sprint container.
- Simple hierarchy:
  - **Milestone** = One bounded Sprint (for example: `v1.0.0: Minimal Production Deploy`).
  - **Spec** = The architectural requirement note (`docs/specs/`).
  - **Tickets** = Atomic GitHub issues with `ready-for-agent` labels.
- Persist this agile practice so all future agents follow it without debate.

### Deliverable 3: Cut Clean `v1.0.0` Release
- Retire superseded `knowledge_maintenance.py` scripts (Issue #114).
- Clean baseline on git `main` (satisfying Gate #89).
- Tag and publish release `v1.0.0`.
- Defer all other domain expansions (`curate`, `code`, `tutor`, `setup`) to Sprint 2 (`v1.1.0`).

## 3. Proposed Refactoring for `AGENTS.md`

```markdown
## Agile Workflow & Sprints

This repository operates on a simple, native GitHub Agile workflow:
1. **Milestones as Sprints**: Every sprint is tracked as an open GitHub Milestone (for example, `v1.0.0: Minimal Production Deploy`).
2. **Specifications (`docs/specs/`)**: Each milestone is governed by a specification defining user stories, acceptance criteria, and boundaries.
3. **Atomic Tickets**: Work is decomposed into small, independent GitHub issues labeled `ready-for-agent`. Agents execute one ticket at a time.
4. **Two-Axis Review Loop**: Every completed ticket requires independent Spec and Standards reviews before merging.

## Style & Presentation Standard

All agents must strictly load and comply with `skills/style/`:
- **British English**: Use British spelling throughout (for example: prioritise, organise, behaviour, colour).
- **No Em Dashes**: Never use em dashes. Use commas, colons, or parentheses instead.
- **No Horizontal Dividers**: Do not use horizontal dividing lines in chat responses or reviews. Use clear section headers instead.
- **Visual Markdown**: Use structured bullet lists and readable tables with one point per line.
```

## 4. Execution Sequence for Rest of Session

1. Refactor `AGENTS.md` with the Agile and Style rules.
2. Scaffold and commit `skills/style/` as our first production skill.
3. Execute Issue #114 (retiring superseded maintenance code).
4. Run test suite and standard checks.
5. Publish release `v1.0.0`.
