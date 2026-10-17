# Knowledge Reconciliation Policy & Ledger Specifications

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This specification governs bounded reconciliation, mutation budgeting, human-gated safety boundaries, and the rolling audit ledger across knowledge operations in `sk-wiki`.

---

## 1. Bounded Reconciliation & Ingest Rules

- **FIFO Queue Ordering**: Inbox items under `raw/` must be ingested in chronological order, processing the oldest raw sources first.
- **Mutation Budget Ceilings**:
  - Automated runs must enforce a strict mutation budget (maximum note creations, edits, or moves per cycle).
  - When the budget cap is reached, processing stops cleanly and remaining items stay queued for subsequent runs.
  - Runaway recursive link synthesis or graph sprawl is strictly blocked.

---

## 2. Human-Gated Operations

To prevent catastrophic knowledge loss or semantic distortion, high-impact operations are strictly human-gated:

- **Deletions (`delete_note`)**:
  - Automated deletion is restricted to exact duplicates (similarity score >= 0.95), transient scratch notes created within the same run, or empty fixture notes.
  - All other deletion requests must be flagged in the knowledge report for operator approval.
- **Schema & Index Mutations**:
  - Altering core metadata schemas or modifying root index structures requires human sign-off.
- **Supersession & Semantic Rewrites**:
  - Marking established foundational notes as deprecated or superseded requires human review.
  - Automated tools must not rewrite established conclusions or alter the meaning of recorded knowledge.

---

## 3. Rolling Report & Ledger Contracts

Every reconciliation, ingest, or linting run must leave an indelible audit trail:

- **Run Artifact**: Each execution compiles a structured report recording run timestamp, operator or agent identity, scanned notes, applied mutations, and flagged warnings.
- **Ledger Entries**:
  - Durable entries are appended to the operational log or ledger note.
  - Each entry records the run identifier, loaded revision hash, mutation count, and execution status (`succeeded`, `partial`, or `failed`).
- **Idempotence**: Re-running reconciliation on unchanged source trees must produce zero mutations and report cleanly with no state drift.
