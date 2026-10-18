---
name: setup
description: Minimal governance module for the agent fleet under ~/.agents and the subagent batch ceiling. Use when configuring the agent fleet or checking how many subagents may be dispatched.
disable-model-invocation: true
user-invoked: true
version: 1.0.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: setup
---

# Setup

Minimal governance module for the agent fleet. Grilling and implementation workflows are deferred to the next sprint.

## Agent Fleet

- Agent skills and shared configuration live under `~/.agents`.
- Authorised skill sources are listed in `docs/authorised-skill-repositories.md`. Only Syafiq changes that list.
- Fleet-wide behaviour follows `docs/agents/coordinator-protocol.md`.

## Subagent Batch Ceiling

- Dispatch 10 subagents or fewer in a single batch.
- Queue larger sets as sequential batches, and wait for each batch to finish.
- Terminate idle or completed subagents before the next batch.

## Boundaries

- This module does not define grilling or implementation workflows.
- Do not add or remove authorised repositories.
