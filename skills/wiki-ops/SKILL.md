---
name: wiki-ops
description: Karpathy-style compiled knowledge engine enforcing Basic Memory MCP compliance, structural and semantic linting, and bounded reconciliation. Use when operating on persistent knowledge, ingesting sources, running knowledge lints, or reconciling notes.
disable-model-invocation: true
user-invoked: true
version: 0.2.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: knowledge
---

# Wiki Ops

Compiled knowledge engine enforcing Basic Memory MCP compliance, structural and semantic linting, and bounded reconciliation for `sk-wiki`.

## Operational Rules

1. **Pure Basic Memory MCP Invariant**:
   - Access and mutate persistent knowledge strictly via Basic Memory MCP tools (`read_note`, `write_note`, `edit_note`, `move_note`, `delete_note`, `list_directory`).
   - Direct filesystem mutations (`write_to_file`, `replace_file_content`, shell redirection) inside wiki directories are strictly prohibited.
   - Target project `sk-wiki` and enforce lowercase ASCII kebab-case note paths.

2. **Ingest Pipeline**:
   - Process inbox sources in FIFO order (oldest raw sources first).
   - Enforce mutation budget caps per run to prevent runaway churn.
   - Synthesize raw materials into modular concepts under `knowledge/` or `source-notes/`.

3. **Deterministic Structural & Semantic Linting**:
   - Verify root and domain folders maintain `index.md` and `log.md` with `bm_parse_semantics: false`.
   - Validate frontmatter schema, internal links, and naming conventions.
   - Zero meaning-changing automated repairs: flag ambiguous or broken semantics for human review.

4. **Rolling Report & Ledger Contract**:
   - Every ingest, lint, or reconciliation run generates a structured `knowledge-report` artifact.
   - Append durable run entries to the audit ledger in `operations/` to guarantee traceability.

## References

- [Basic Memory Contracts](references/basic-memory-contracts.md)
- [Reconciliation Policy](references/reconciliation-policy.md)

## Artifact Contracts

- Contract `knowledge-report`: [Template](templates/knowledge-report.template.md) and [Example](examples/knowledge-report.example.md).
