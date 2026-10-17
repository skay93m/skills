# Architecture Decision Record Example

## Metadata
- ADR ID: ADR-0014
- Title: Adoption of Read-Only SQLite State Engine with Transactional CLI Seams
- Date: 2026-10-17
- Status: Accepted
- Decision Type: Type 1 (One-Way Door)
- Primary Authors: Systems Architect & Autonomous Scrum Subagents

## Context & Problem Statement
Autonomous agile sprint workflows require reliable, fast, and multi-process state tracking for sprint goals, ticket lifecycles, and Event 0 verification gates. Prior proposals considered external PostgreSQL services, distributed key-value stores, and flat JSON ledgers. Flat files suffer from concurrent write corruption, whereas distributed databases introduce prohibitive operational overhead, container orchestration friction, and network failure modes for a single-developer repository.

## Decision Drivers & Constraints
- Zero external daemon dependencies (must function reliably offline on local workstations).
- Concurrency safety with atomic transactions.
- Strict prevention of rogue agent state modification (zero direct ad-hoc SQL writes).
- Low latency queries for terminal tools and subagent execution.

## Considered Architectural Options
| Option ID | Architectural Approach | Key Advantages | Disadvantages & Incurred Debt |
|---|---|---|---|
| Option A | Distributed PostgreSQL Daemon | Full SQL feature set, mature tooling | Heavy daemon requirement, breaks offline local CLI speed |
| Option B | Flat JSON / YAML State Files | Zero external tools, human readable git diffs | Race conditions on concurrent agent writes, file locking hazards |
| Option C | Embedded SQLite with Read-Only CLI Seams | Zero background daemon, ACID compliance, single file portable | Requires strict discipline to prevent raw ad-hoc write mutation |

## Decision Outcome & Chosen Strategy
### Decision
Adopt embedded SQLite (`awt.db`) as the state engine, strictly enforcing read-only URI querying (`file:awt.db?mode=ro`) for general queries while funneling all state mutations exclusively through validated transactional CLI commands.

### Justification & Tradeoff Calculus
Embedded SQLite delivers zero-daemon portability and sub-millisecond query performance. Restricting read operations to read-only SQLite modes prevents unintended schema drift or data destruction from rogue agent prompts, while CLI seams ensure all updates pass deterministic business logic validation and audit logging.

## Socratic Sparring Findings & Failure Mode Analysis
### Unstated Assumptions Challenged
- *Assumption*: "Subagents need direct SQL write access to quickly update task statuses."
  - *Challenge*: Allowing unconstrained direct write access inevitably leads to schema corruption, bypassed Event 0 gates, and unindexed foreign keys. Funneling writes through transactional CLI tools introduces negligible friction while eliminating data corruption.
- *Assumption*: "SQLite write locks will throttle parallel subagents."
  - *Challenge*: With subagent batch sizes capped at ten and writes restricted to discrete lifecycle milestones, WAL (Write-Ahead Logging) mode handles transactions in under 2ms, rendering lock contention practically non-existent.

### Pre-Mortem Deductions (Projected Failure Scenarios)
If this decision fails 12 months from now, the primary failure mode would be developers bypassing the CLI interface and manually executing SQLite commands directly against the database file. This is mitigated by establishing automated linters that flag raw SQLite write strings in codebase scripts.

## Consequences & Operational Impact
- **Positive Outcomes**: Fast local queries, zero external daemon requirements, rock-solid ACID transactions, easily backupable single database file.
- **Negative Incurred Costs**: Requires maintaining dedicated CLI wrappers for every state transition; cannot leverage server-based distributed replication without additional tooling.
- **Reversibility / Migration Plan**: If relational schema limitations are reached, SQLite tables can be exported via standard `.dump` commands and imported into PostgreSQL within two hours.
