---
name: autonomous-scrum
description: Standalone AWT agile sprint engine enforcing Product Owner versus Developer boundaries, Event 0 sprint gates, and read-only SQLite state tracking. Use when planning sprints, triaging issues, checking Event 0 gates, or reviewing sprint progress.
disable-model-invocation: true
user-invoked: true
version: 0.2.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: scrum
---

# Autonomous Scrum

Standalone AWT agile sprint engine enforcing Product Owner versus Developer boundaries, Event 0 sprint gates, and read-only SQLite state tracking.

## Core Mechanics

1. **Product Owner vs Developer Role Separation**:
   - Product Owner (PO) agents define requirements, formulate specifications, groom tickets, and set acceptance criteria.
   - Developer agents implement strictly against approved tickets, write tests, and resolve findings.
   - Developers must never alter ticket acceptance criteria or expand scope without PO approval; POs never author production implementation code.

2. **Event 0 Sprint Gates**:
   - Mandatory gate check before any sprint or milestone activation.
   - Requires 100% resolution of prerequisites: complete ticket specifications, unambiguous acceptance tests, verified dependency graphs, and CI environment readiness.
   - Any gate failure blocks sprint kickoff until defects are resolved.

3. **Read-Only SQLite State Tracking**:
   - Inspect sprint metrics, burndown status, and ticket states via read-only SQL queries against `awt.db`.
   - Prevent state corruption: state mutations occur solely through authorized transactional interfaces, never ad-hoc direct database writes.

4. **Lifecycle Progression**:
   - Sequential progression: Backlog Triage -> Event 0 Validation -> Active Sprint -> Dual-Axis Review -> Sprint Closure.
   - Sprint progress is documented in durable `sprint-report` artifacts.

## References

- [Event 0 Gates](references/event-0-gates.md)
- [Role Boundaries](references/role-boundaries.md)

## Artifact Contracts

- Contract `sprint-report`: [Template](templates/sprint-report.template.md) and [Example](examples/sprint-report.example.md).
