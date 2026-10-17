# Knowledge Report Example

## Metadata
- Run ID: run-20261017-020000
- Timestamp: 2026-10-17T02:00:00Z
- Project: sk-wiki
- Operator / Agent: wiki-ops-agent
- Operation: daily-reconciliation
- Status: succeeded

## Executive Summary
Completed daily knowledge reconciliation cycle. Processed 3 raw inbox sources in FIFO order, validated structural and semantic invariants across 42 notes, and applied 2 guarded mutations within allocated budgets.

## Ingest Queue
- Processed Sources: 3
- Remaining Queue: 0
- Mutation Budget Used: 2 / 10

## Structural & Semantic Lint Findings
| Category | Note Identifier | Severity | Finding Details | Recommended Action |
|---|---|---|---|---|
| Structural | `knowledge/distributed-systems` | Warning | Missing inbound index link | Add link to `knowledge/index.md` |
| Semantic | `source-notes/raft-consensus` | Info | Verified clean cross-references | None |

## Applied Mutations
| Action | Note Identifier | Path | Checksum Before | Checksum After |
|---|---|---|---|---|
| Create | `knowledge/distributed-consensus` | `knowledge/distributed-consensus.md` | `none` | `a1b2c3d4e5f6` |
| Edit | `knowledge/index` | `knowledge/index.md` | `f6e5d4c3b2a1` | `9876543210ab` |

## Ledger Audit Record
- Ledger Entry Appended: true
- Transaction Hash: `0123456789abcdef0123456789abcdef01234567`
