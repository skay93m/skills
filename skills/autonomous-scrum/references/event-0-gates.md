# Event 0 Sprint Gates & Readiness Criteria

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This specification establishes the mandatory Event 0 pre-flight gate protocol required before activating any development sprint or epic in the Agent Work Tracker (AWT).

---

## 1. Purpose of Event 0

Event 0 represents the formal boundary between agile backlog grooming and active execution. No ticket may transition to in-progress status, and no developer agent may be dispatched, until all Event 0 gates pass with zero blocking findings.

---

## 2. Event 0 Readiness Checklist

Before activating a sprint, the Product Owner (PO) and coordinator agent must verify five core gates:

1. **Specification Completeness**:
   - Every ticket in the sprint backlog must have a clearly articulated problem statement, technical context, and explicit scope boundaries.
   - Ambiguous requirements or open design questions must be resolved during grooming prior to Event 0.

2. **Unambiguous Acceptance Criteria**:
   - Each ticket must define deterministic, testable acceptance criteria.
   - Acceptance tests must specify expected inputs, outputs, error conditions, and exit states.

3. **Dependency Graph Resolution**:
   - All prerequisite tickets, upstream API contracts, or external blockers must be satisfied.
   - Circular dependencies must be detected and decomposed into acyclic sequence paths.

4. **Test Environment & Harness Readiness**:
   - Baseline test suites (`pytest`, unit tests, lint checkers) must pass cleanly on the base revision.
   - CI workflows and required local mock fixtures must be confirmed functional.

5. **Budget Allocation & Scope Caps**:
   - Token budgets, line-count budgets (<= 100 lines for skills), and subagent concurrency limits (<= 10 workers) must be explicitly recorded for each ticket.

---

## 3. Gate Evaluation Protocol

- **Binary Decision**: Gates evaluate strictly to `PASS` or `FAIL`. Partial or conditional passes are forbidden.
- **Fail-Closed Gatekeeper**: If any ticket fails a gate, the entire sprint activation halts. The offending ticket must be remediated or deferred back to the product backlog.
- **Audit Record**: The evaluation result, timestamp, and gate checklist are preserved in the sprint kickoff record.
