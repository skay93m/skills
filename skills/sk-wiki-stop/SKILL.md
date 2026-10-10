---
name: sk-wiki-stop
description: Close a Wiki work period safely by persisting resumable state, verifying
  no unsafe loose ends remain, identifying restart points, and stopping without inventing
  new work.
---

# Wiki stop

## Purpose

End a Wiki work period cleanly and reproducibly.

This skill is for intentional closure, such as ending the day, deliberately stopping a long Wiki session, or proactively stopping when an agent is approaching a context, token or usage limit. Do not wait for forced truncation or loss of continuity when there is enough capacity to persist state safely. It does not perform maintenance, reopen linting, advance projects, or search for additional work merely because time remains.

Use triage for bootstrap and mid-work restart/handoff discipline. Use this skill when the goal is to verify that the current work can safely stop.

## Stop principle

Closure means:

1. authorised work is either complete or durably represented as resumable work;
2. completed Tasks and Projects do not falsely appear underway;
3. unfinished work has a clear durable restart point;
4. no known write is left unverified or in an ambiguous state;
5. the agent does not create optional work merely to make closure feel comprehensive.

A future possibility, improvement or idea is not a blocker to stopping.

## Procedure

### 1. Recover current work state

Read the current Wiki contract and triage procedure, then retrieve only the Tasks, Projects and control notes materially changed or worked on during the current work period.

Do not run whole-Wiki maintenance or lint merely to close the session.

### 2. Verify completed work

For each work item completed during the period:

- confirm the durable note exists;
- confirm its lifecycle state reflects its own acceptance condition;
- confirm any material mutation already claimed as complete was read back or otherwise verified;
- ensure later or downstream work is not being used to keep a completed Task artificially open.

Do not retrospectively re-audit completed work unless evidence of a specific problem exists.

### 3. Persist unfinished work and continuation anchor

If work is genuinely unfinished and resumable:

- reuse the existing Task or Project when one already represents it;
- ensure it carries enough context, current state and next authorised step for a fresh session;
- use the lifecycle status that describes its actual state;
- verify the persisted handoff;
- make the Task or Project the explicit continuation anchor for the next session.

An existing Task or Project is the preferred continuation anchor. If useful thread state is not adequately represented in durable Wiki objects, use the upstream `memory-capture` skill to synthesise it into one coherent note, and make that capture the anchor, linked from the relevant Task or Project where one exists. Do not duplicate what `memory-capture` does, and do not create a capture merely because a session is ending when durable state is already sufficient.

The next session should use the upstream `memory-continue` skill to reconstruct context from the Task, Project or capture anchor and its relations rather than relying on chat history. Prefer the specific Task or Project as the starting point; use broader recent activity only when no durable anchor exists.

If stopping because context, token or usage headroom is getting low, perform this step early enough to write and verify the anchor safely. Do not consume the remaining headroom on optional cleanup before preserving resumability.

Do not create speculative Tasks for optional ideas that can remain ordinary future possibilities.

### 4. Check for unsafe loose ends

A stop blocker exists only when one of these is true:

- a write outcome is unknown;
- an authorised mutation was started but not safely completed or bounded;
- current lifecycle state materially contradicts known work state;
- resumable work would otherwise depend on chat history or model memory, with no durable anchor suitable for `memory-continue`;
- a transient failure rule or stronger governance rule requires unresolved state to be recorded before stopping.

Ordinary backlog, pending human decisions, future roadmap phases, deferred design work and optional improvements are not stop blockers if they are already represented appropriately.

### 5. Maintain chronology only when warranted

Append to an existing log only when the work period produced a meaningful chronological milestone that is not already recorded.

Do not create an end-of-day diary entry merely because this skill ran.

### 6. Stop

Report exactly:

- **SAFE TO STOP** or the specific blocker;
- any correction made during closure;
- the small set of durable Tasks or Projects that are natural restart points.

After reporting **SAFE TO STOP**, do not continue with new Wiki work unless Syafiq explicitly starts it.

## Boundaries

- Do not run structural lint, semantic lint or wiki-maintenance as part of routine closure.
- Do not resolve optional pending decisions merely to empty the backlog.
- Do not rename, reorganise or clean notes unless a specific unsafe loose end requires it.
- Do not manufacture Tasks from every idea mentioned during the day.
- Do not run `memory-capture` by default. Use it only to fill a gap in durable state.
- Do not treat local Git/GitHub propagation as an MCP-only stop blocker unless reconciliation or CLI handoff is explicitly in scope.
- Historical observations may retain earlier statuses or instructions when clearly part of audit history; current frontmatter and current observations must not misrepresent live state.

