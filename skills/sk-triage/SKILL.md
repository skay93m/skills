---
name: sk-triage
description: Mandatory TCREI startup for Wiki sessions and catch-up alignment with
  a human restart gate for ongoing unaligned sessions.
---

# Triage: TCREI session protocol

## Purpose and triggers

Every agent working with the Wiki must load this skill at session start after reading `AGENTS.md` and the root `index.md` via Basic Memory MCP. Apply Task, Context, References, Evaluate and Iterate to every non-trivial task. For a simple task, keep the record proportionate but retain retrieval, scope and verification checks.

## Session alignment and human restart gate
A new session reads the current contract and this skill before substantive work, then explicitly states Stage 1 (Task) and Stage 2 (Context) findings before implementation, opening that statement with the revision checksum of `AGENTS.md` as returned by that read, so that Syafiq can check at a glance that the current version was loaded. Complete References and Evaluate before entering Iterate. Iterate contains the authorised modifications and verification; the protocol does not require modifications before the preflight is complete.

If an ongoing session has not yet aligned with this skill, pause its substantive work immediately. Read the current contract and this skill, recover the authorised goal and completed actions from the conversation, retrieve relevant Wiki decisions, and record the five-stage alignment status. Distinguish already-completed work from proposed work; never claim that earlier actions passed checks retrospectively. Identify conflicts, unverified changes, errors and remaining gaps without silently expanding scope or undoing prior work.

Before stopping for the human restart gate, persist the handoff in a durable, discoverable Wiki object in `handoff/<slug>.md` with `type: handoff`. Use its context and observations to record the goal, sources, completed work, verification, unresolved gaps and exact next authorised step. Never persist handoffs in `tasks/` or temporary OS directories. Read the persisted object back and verify that it contains enough context for a fresh session to resume without relying on chat history or model memory.

Once the handoff has been persisted and verified, give the human a concise handoff that names the exact Wiki path or permalink to resume. Then STOP and explicitly ask the human to start a new session. Do not resume the original task, create a new session automatically, or delegate continuation. A subsequent message in the same session is not a new session unless the human explicitly changes this requirement.

The new session must load the current contract and this skill itself, then retrieve the named persisted handoff object and verify relevant current state before continuing. The handoff is continuation context, not proof that prior work was correct or that external state is still current. If the named object cannot be found or is insufficient to resume safely, stop and report the continuity failure rather than reconstructing state from memory. An already-aligned ongoing session need not repeat the catch-up restart gate merely because it reads this skill again.

## Operating principles

- Never assume novelty. Query existing knowledge before re-deriving logic or creating entities.
- Respect settled architecture and policy unless Syafiq explicitly authorises a change.
- If a command, tool or test fails, diagnose it and make at most one corrective attempt. If that fails, stop and report the exact error and affected state. Do not reset the allowance by switching tools or transport. Stricter stop rules in AGENTS, including immediate stop on Cloud 502/503/gateway or transport failure, take precedence.
- Triage does not grant authority for unrelated mutations, external communications or publication.

## 1. Task (T)

State the concrete goal in one or two sentences: what changes, for whom, and what counts as done. State the required operational role and the authorised scope. Explicitly identify ambiguity rather than silently guessing.

## 2. Context (C)

Query the Wiki before assuming novelty. Retrieve relevant decisions, existing entities and recent activity where it bears on the task. Record what to build on, decisions to respect and gaps that justify new work.

Use project-scoped Basic Memory MCP search and read tools when operating through MCP, explicitly selecting the Wiki project. Use an available recent-activity tool or a bounded relevant log excerpt when recent changes matter.

## 3. References (R)

List concrete inputs: repository paths, memory permalinks, documentation and explicit human directives. Identify established patterns and relevant tests to reuse. Label anything not grounded in those inputs as an assumption.

## 4. Evaluate (E)

Before modifying files or notes, check:

- Duplication: search for existing entities and prefer targeted section edits to parallel copies.
- Conflict: compare the plan with recorded decisions. If a conflict is not resolved by explicit human authority, halt and ask for clarification.
- Destination: verify the actual project and location. Do not write to workspace `main` when Wiki is intended.
- Completion evidence: define the exact checks appropriate to the change, including direct note readback, structure and metadata checks, or relevant tests, lint and type checks for code.

## 5. Iterate (I)

Execute authorised changes incrementally. Prefer targeted edits or appends over wholesale replacement. Reserve overwrite for deliberate, authorised re-synthesis; create new notes without overwriting existing ones.

Apply the one-corrective-attempt limit and stricter failure gates. Confirm written notes with direct Basic Memory reads and check their identity, intended content, frontmatter and Markdown structure. Record non-obvious findings or decisions under `## Observations` on the relevant note, respecting the graph-silent index/log contract.

Report Context findings, changes, evidence and unresolved `[gap]` items. If this was catch-up alignment in an ongoing unaligned session, provide the handoff and stop at the human restart gate.
