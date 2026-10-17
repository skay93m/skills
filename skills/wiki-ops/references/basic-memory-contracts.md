# Basic Memory Contracts & Tool Call Constraints

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This specification defines the mandatory invariants, tool call constraints, and project rules for operating on persistent knowledge via the Basic Memory Model Context Protocol (MCP) server.

---

## 1. Project Invariants

- **Canonical Project**: All persistent knowledge operations must explicitly specify `project: "sk-wiki"`. Cross-project bleed or targeting unverified projects is prohibited.
- **Strict File Naming**:
  - File identifiers and note paths must strictly use lowercase ASCII kebab-case (`example-concept.md`).
  - Never use spaces, CamelCase, Title Case, or underscores in note titles or file paths.
  - Exempt reserved root files: `AGENTS.md`, `index.md`, and `log.md`.
- **Root and Subdirectory Governance**:
  - Every root directory must contain an `index.md` (`type: index`, `bm_parse_semantics: false`).
  - Every root directory must contain a `log.md` (`type: log`, `bm_parse_semantics: false`).
  - Indexes list directory contents and navigation trees; logs record chronological mutation events.

---

## 2. Tool Call Constraints

All interactions with `sk-wiki` must use the approved Basic Memory MCP tools. Direct filesystem mutations or shell writes are strictly prohibited.

| Tool Name | Allowed Context | Constraints & Guardrails |
|---|---|---|
| `read_note` | Reading existing notes | Requires valid `identifier` and `project: "sk-wiki"`. Fails safely if note is absent. |
| `write_note` | Creating new notes | Requires `identifier`, `project`, and `body`. Must fail if note exists unless explicit overwrite is enabled. |
| `edit_note` | Modifying existing notes | Performs surgical edits via exact string replacement or section replacement. |
| `move_note` | Renaming or relocating notes | Atomic rename/move within the project. Updates inbound references when supported. |
| `delete_note` | Deleting notes | **Human-Gated**: Requires explicit operator authorization. Limited to duplicate or scratch notes. |
| `list_directory` | Navigating folder trees | Inspects directories within `sk-wiki` to discover unindexed or newly created notes. |

---

## 3. Mutation Hygiene & Safety Guards

- **Guarded Writes**: Prefer transactional or checksum-verified updates (`checksum_read`, `guarded_overwrite`) when supported by the store adapter.
- **Exclusive Create**: New note creation must not silently overwrite existing knowledge assets.
- **Frontmatter Preservation**: Edits to body text must never corrupt or accidentally strip YAML frontmatter blocks.
- **Fail-Closed Policy**: If a tool call fails or returns ambiguous results, the operation must halt immediately without attempting guessing heuristics.
