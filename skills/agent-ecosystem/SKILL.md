---
name: agent-ecosystem
description: Heterogeneous agent fleet governance enforcing golden layout, subagent batching ceilings of ten, and durable cross-agent handoff contracts. Use when managing multi-agent fleets, onboarding agent runtimes, configuring golden layout, or coordinating agent handoffs.
disable-model-invocation: true
user-invoked: true
version: 0.2.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: ecosystem
---

# Agent Ecosystem

Heterogeneous agent fleet governance enforcing golden layout, subagent batching ceilings of ten, and durable cross-agent handoff contracts.

## Core Mechanics

1. **Golden Agent Layout Invariant**:
   - The canonical configuration authority resides in `~/.agents` (`skills/`, `rules/`, `mcp.json`).
   - Standard projections maintain consistency across supported runtimes (Claude Code, OpenAI Codex, Antigravity, Hermes).
   - Prohibit ad-hoc local mutations; all agent runtime changes must originate from the golden layout.

2. **Subagent Batching Ceiling of Ten**:
   - Enforce hard ceiling of strictly <= 10 concurrent subagents per `invoke_subagent` invocation.
   - Queue workloads sequentially in batches of at most 10: wait for the active batch to complete before launching the next.
   - Ephemeral subagent lifecycles: immediately terminate or kill idle/finished workers to prevent resource and quota exhaustion (429).

3. **Durable Cross-Agent Handoff Protocol**:
   - Transitions between coordinators, specialists, or runtimes require structured handoff contracts.
   - Handoff records document source/target runtimes, completed objectives, residual risks, verification logs, and the exact resume prompt.
   - All handoffs produce standard `agent-handoff` artifacts.

## References

- [Golden Agents Layout](references/golden-agents-layout.md)
- [Fleet Batching Protocol](references/fleet-batching-protocol.md)

## Artifact Contracts

- Contract `agent-handoff`: [Template](templates/agent-handoff.template.md) and [Example](examples/agent-handoff.example.md).
