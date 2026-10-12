---
name: sk-task
description: >-
  Use when running Hermes' conversation-first morning standup over canonical Wiki Tasks: review existing Tasks and verified planning links, agree one focus and next action with Syafiq, then record a dated Commitment only after explicit confirmation.
metadata:
  origin: "basicmachines-co/basic-memory-skills memory-tasks/SKILL.md @ 6d2b1d426d0dacf020aef45f029768c9d8c1e5e5"
  agent_involvement: full
  category: planning
  divergence: >-
    Adapter, not a fork: upstream task methodology is read and kept; only I/O and policy are overridden.
    Wiki Tasks in Basic Memory Cloud stay canonical (upstream status values and the active state do not apply),
    and this skill adds a confirmation-gated morning standup that upstream lacks.
    Issue 42 holds the specification and issue 46 the first ticket.
---

# sk-task (Adapter): morning standup

## 1. Ingest upstream methodology

Read the upstream `memory-tasks` skill in the Basic Memory skills repository (`~/.agents/basic-memory-skills/memory-tasks/SKILL.md`; if absent, read it read-only from its repository). Keep its method for creating, inspecting, resuming, updating, completing, blocking, abandoning and pre-compaction flush. Never copy or edit it.

## 2. I/O and policy override

- Read and write Tasks only through Basic Memory Cloud tools on the Wiki project. Wiki Task meaning and state are canonical.
- Follow the Wiki `schema/task` note, not the upstream example schema. Its statuses are `todo`, `doing`, `blocked`, `parked`, `done`, `abandoned`; never use `active`. Search with lowercase `note_types=["task"]`.
- GitHub stays authoritative for repository-linked operational state. Do not mirror its issues as Task copies.
- Treat upstream `priority` as source data, not a settled Wiki priority.
- Use only existing fields, notes, verified relations and Syafiq's direct answers for capacity and execution evidence. No calendar, email or shift lookups.

## 3. Standup flow

This is a conversation, not a report. Do not write while talking.

1. Read `todo`, `doing`, `blocked` and `parked` Tasks: description, steps, current step, context, blockers, owner, parent Task, Project.
2. Follow only explicit Task to Project to plan relations. Read each linked note before citing it.
3. Ask Syafiq about today's capacity and what actually happened recently. Use his answers and any recorded execution evidence; never assume either.
4. Offer a short list of candidates. A `blocked` or `parked` Task is shown with its blocker and is never offered as ready work. Ask for the unblock instead.
5. Explain the context path with the source of each link: daily focus, weekly plan, monthly plan, yearly plan, life direction.
6. Agree one focus Task and one concrete next action through discussion. Syafiq decides; do not choose for him.

## 4. Gaps and conflicts

Name every missing, stale, ambiguous, conflicting or blocked item and its source. Distinguish "not found in the indexed notes" from "does not exist". Never invent a link, create a horizon note, repair a relation, reconcile conflicting fields, or substitute a quarterly plan or multi-year sketch for a monthly or yearly one. A link explains context only; it authorises nothing.

## 5. Confirm, then record

Before any write, state in one message the Task, the date, the next action and exactly what will change, then ask for explicit confirmation. Silence, "maybe" or an answer to a different question is not confirmation.

A Commitment is a Task with an explicit owner, next action, time boundary and review point. Record the dated Commitment on the existing Task only when the Task note already follows a supported convention that can hold it safely. Use a targeted `edit_note`, then read the note back. If none exists or it is ambiguous, write nothing and report the smallest decision needed from Syafiq; do not invent a field, section format or storage rule.

The write never creates a Task, and never changes status, priority, `impact`, `due`, strategic standing or any planning note.

## 6. Out of scope

Daytime check-ins, scheduling and replanning belong to a later ticket. Weekly, monthly and yearly review workflows are also out of scope.

Synthetic examples: `references/standup-examples.md`. All examples and fixtures stay synthetic.
