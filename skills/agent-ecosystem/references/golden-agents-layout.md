# Golden Agents Layout & Multi-Runtime Governance

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This specification defines the canonical Golden Agent layout architecture and distribution invariants across supported agent runtimes.

---

## 1. Golden Layout Architecture

To avoid configuration drift across heterogeneous AI environments, the personal computing environment establishes a single source of authority:

- **Authority Location**: The directory `~/.agents/` acts as the single source of truth for:
  - `skills/`: Authorized personal and upstream skill modules.
  - `rules/`: Fleet-wide behavioral rules, batching constraints, and safety guidelines.
  - `mcp.json`: Authorized Model Context Protocol (MCP) server definitions.
- **Runtime Projections**:
  - Client runtimes project from the golden layout via symlinks or managed synchronization.
  - Supported runtimes:
    - **Claude Code**: Reads configuration from `~/.claude/` projected from `~/.agents/`.
    - **OpenAI Codex**: Reads instruction sets and tool definitions projected from `~/.agents/`.
    - **Antigravity CLI**: Reads skills from `~/.gemini/antigravity-cli/` and repository root.
    - **Hermes**: Operates as a coordination agent executing standups and notification dispatch.

---

## 2. Invariant Rules for Agent Onboarding

- **Non-Destructive Onboarding**:
  - Onboarding and synchronization scripts must never execute destructive commands (such as deleting existing user directories like `~/.claude/skills` or `~/.agents/skills`).
  - Merges must occur additively with pre-flight conflict reporting.
- **Prohibition of Ad-Hoc Drift**:
  - Agents must not edit local runtime configurations directly without updating the authority in `~/.agents/`.
  - Drift detection checks run during regular ecosystem audits to flag out-of-sync projections.
