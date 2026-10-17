# Product Owner vs Developer Role Boundaries

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This specification defines the strict operational boundaries, rights, and responsibilities governing Product Owner (PO) agents and Developer agents within autonomous agile workflows.

---

## 1. Principle of Role Separation

Maintaining a rigorous separation between specification authority (the PO) and implementation authority (the Developer) prevents subtle scope creep, untracked architecture drift, and self-serving test coverage.

---

## 2. Product Owner (PO) Authority & Responsibilities

- **Domain Scope**:
  - Authoring problem statements, feature specifications, and acceptance criteria.
  - Prioritizing backlog items, ordering sprint queues, and approving milestone boundaries.
  - Evaluating completed work against the original specification intent.
- **Strict Invariants**:
  - The PO agent never writes production application code, implementation patches, or skill entrypoints.
  - The PO evaluates pull requests along the Spec Axis during the two-axis code review loop.

---

## 3. Developer Authority & Responsibilities

- **Domain Scope**:
  - Designing modular code structures, writing automated tests, and implementing feature logic.
  - Following the Test-Driven Development (TDD) cycle: red (failing test) -> green (minimal code) -> refactor.
  - Ensuring strict compliance with repository standards, line limits, and reference invariants.
- **Strict Invariants**:
  - The Developer agent never modifies ticket acceptance criteria or expands functional scope without explicit PO sign-off.
  - If unexpected complexity or missing requirements arise during implementation, the Developer must stop and escalate back to the PO rather than making assumptions.

---

## 4. Conflict Resolution & Review Handoff

- **Two-Axis Review Separation**:
  - **Spec Axis Review**: Conducted by PO or dedicated spec reviewer subagent to confirm zero omissions and zero extraneous scope additions.
  - **Standards Axis Review**: Conducted by standards reviewer subagent to audit line budgets, reference depths, typing, and security hygiene.
- **Dispute Escalation**:
  - Disagreements between implementation mechanics and specification intent are referred to the human repository owner.
