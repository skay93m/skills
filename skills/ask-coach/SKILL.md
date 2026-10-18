---
name: ask-coach
description: Use when seeking orientation, returning after a break, or routing to the next coaching command.
disable-model-invocation: false
metadata:
  origin: original
  agent_involvement: full
  category: router
---

# Ask Coach

This skill provides a fast, grounding workspace router and health check across all coaching skills. Work through the steps in order.

## Steps

### Health Check

Inspect the eight governing documents in the working directory: MISSION.md, USER.md, SOUL.md, RESOURCES.md, PARKING_LOT.md, ACADEMIC_STANDARDS.md, GLOSSARY.md, and AGENTS.md. If any document is missing, report the gap to the student and deliver a standard recommendation with primary command `/coach-setup`, rationale "Initialise missing governing documents in workspace.", zero alternatives, and stop immediately. Strictly never execute setup commands or write files directly.

### Read Workspace State

Read the tracker repository dynamically from RESOURCES.md under the GitHub Tracker section. If available, inspect open sprint issues using the GitHub CLI:

```bash
gh issue list -R <tracker repository> --label sprint-active --state open --json number,title
```

Inspect the latest handoff notes or Build Record in `docs/handoffs/` to identify the most recent completed activity, the active Atomic Target, and any recorded Landing Strip.

### Route Across All 22 Skills

Map the current workspace state to the corresponding coaching skill. This skill routes to downstream skills and never recommends `ask-coach` itself:
- `coach-setup`: Initialise or reconfigure the eight governing documents.
- `ask-coach`: Fast, grounding orientation, health check, or next command.
- `session-start`: Open a study block, set an Atomic Target, and run somatic check-in.
- `session-end`: Close a study block, review outputs, and record the handoff.
- `debrief`: Grounding check-in when emotionally stuck or overwhelmed.
- `park`: Capture a tangent into PARKING_LOT.md to resume study.
- `think`: Clarify academic argument logic or resolve conceptual confusion.
- `source-discover`: Record a source, format Zotero fields, and verify OSCOLA citations.
- `preview`: Set a tutor dossier or conduct four diagnostic preview questions.
- `analytical-read`: Challenge a Stance Anchor across three analytical rounds.
- `syntopical-map`: Map three to five conflicting sources across the Idea Compass.
- `recall`: Five-minute unprompted active retrieval sprint on a legal doctrine.
- `quiz`: Short Socratic diagnostic quiz on a taught module before writing.
- `blueprint`: Construct a one-page argument outline with Paragraph Functional Budget.
- `slice-tickets`: Slice an approved blueprint into fifteen-minute drafting tickets.
- `academic-review`: Review drafted prose or technical artefacts against standards.
- `final-audit`: Check a completed essay or dissertation for audit defects and verdict.
- `viva-idea`: Oral defence of a working thesis or idea before drafting.
- `viva-draft`: Viva-style interrogation and oral defence of completed draft prose.
- `compact-academic`: Lossless state snapshot before context compaction.
- `supervision-prep`: Prepare a one-page Briefing Memo before a supervision gate.
- `supervision-debrief`: Convert confirmed supervisor directives into tracker tickets.

### Deliver Recommendation

Recommend exactly one primary command with a one-line rationale, followed by at most two alternatives. Ground the advice in USER.md and SOUL.md posture. Recommend downstream skills only; never recommend `ask-coach`. Strictly never execute downstream skills or commands directly.
