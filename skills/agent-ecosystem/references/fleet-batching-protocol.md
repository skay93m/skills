# Fleet Batching Protocol & Lifecycle Management

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This specification details the subagent batching invariants, concurrency ceilings, queueing mechanics, and lifecycle cleanup rules for coordinating multi-agent fleets.

---

## 1. Concurrency Ceiling & Batch Limit Invariant

- **Hard Limit of Ten**: An orchestrator or coordinator must never spawn more than 10 subagents in a single `invoke_subagent` invocation.
- **Sequential Batch Queueing**:
  - When a task requires decomposing into more than 10 work units, the coordinator must divide the work into sequential batches of at most 10.
  - The coordinator must wait for the current batch to fully finish (all subagents in the batch reach idle or completed state) before dispatching the next batch.
- **No Concurrent Batch Sprawl**: Never run overlapping or unmonitored subagent batches.

---

## 2. Resource Exhaustion & Quota Handling

- **Error Detection**: A `RESOURCE_EXHAUSTED` (HTTP 429) status indicates model rate-limit saturation or token quota exhaustion.
- **Backoff Protocol**:
  - Do not immediately retry or relaunch failed workers when receiving quota errors.
  - Implement an exponential or bounded backoff delay before re-attempting failed requests.
  - Alert the operator if quota saturation persists across repeated retries.

---

## 3. Ephemeral Subagent Lifecycles

- **Immediate Cleanup**:
  - Subagents are ephemeral workers designed for targeted execution.
  - As soon as a subagent returns its completion report or goes idle, the coordinator must explicitly terminate or kill it.
  - Releasing resources immediately prevents memory bloat, context pollution, and zombie task retention.
- **Reactive Wakeup**:
  - Coordinators must rely on the system's reactive message delivery rather than executing continuous busy-wait polling loops.

---

## 4. Cross-Agent Handoff Protocol & Lifecycle

When transitioning control between coordinators, specialist agents, or across different runtime environments, agents must execute a durable handoff protocol to eliminate context degradation and unverified state transfers.

- **Handoff Procedure & Lifecycle Transition**:
  - When an agent finishes its scoped phase or prepares to yield control, it must halt further mutations.
  - The outgoing agent compiles a durable handoff document detailing all completed work, verified evidence, residual risks, and exact resumption instructions.
  - The incoming agent resumes by parsing the handoff document, validating the verification evidence, and executing the resumption prompt without repeating completed phases.
- **Storage Path Conventions**:
  - In code repositories, persist handoff records to `docs/handoff/<slug>.md`.
  - In persistent knowledge bases (Wiki), persist handoff records to `handoff/<slug>.md` and update the corresponding folder `index.md` and `log.md`.
- **Required Handoff Structure**:
  The handoff document must strictly match the structure defined in `agent-handoff.template.md`:
  - **Handoff Metadata**: Unique Handoff ID, timestamp, source agent/runtime, target agent/runtime, and task context boundary.
  - **Completed Objectives**: Bulleted list of verified milestones and concrete deliverables.
  - **Verification Logs & Evidence**: Results from standard checks (`check-standard.py`), unit/contract tests (`pytest`), and artifact integrity audits.
  - **Residual Risks & Open Blockers**: Explicit enumeration of unverified edges, technical debt, or open blockers (or "None").
  - **Resumption Prompt**: Concise, fenced prompt (up to two lines) ready to pass directly to the receiving agent.

