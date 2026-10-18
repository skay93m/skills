# Intent-Based Routing Table & Pipeline Specification

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This reference provides comprehensive routing guidelines, trigger phrases, intent mappings, and phase transition policies for the master router across all 6 deep modules and the upstream engineering pipeline.

---

## 1. Deep Module Dispatch Catalog

### 1.1 `wiki-ops` (Domain: `knowledge`)
- **Intent**: Karpathy-style compiled knowledge operations, persistent note lifecycle, Basic Memory backend compliance, and knowledge hygiene.
- **Trigger Phrases**:
  - "lint wiki", "check wiki consistency", "run knowledge lint"
  - "ingest note", "compile raw notes", "process inbox note"
  - "recompile indexes", "audit knowledge run", "verify basic memory"
- **Target Capabilities & Actions**:
  - Supervised and unsupervised ingest flows converting raw thoughts into structured knowledge notes.
  - Structural validation: enforces root folder index.md and log.md contracts, lowercase kebab-case naming, and frontmatter typing.
  - Semantic linting: verifies cross-references, detects orphan concepts, and flags stale claims.
  - Basic Memory tool governance: mandates read_note, write_note, edit_note, move_note, delete_note; blocks direct filesystem mutations.

### 1.2 `autonomous-scrum` (Domain: `scrum`)
- **Intent**: Standalone AWT agile project management, sprint planning, issue lifecycle progression, and strict role separation.
- **Trigger Phrases**:
  - "plan sprint", "start next sprint", "close current sprint"
  - "triage issue", "groom backlog", "refine ticket acceptance criteria"
  - "event 0 sprint gate", "check sprint burndown", "audit ticket status"
- **Target Capabilities & Actions**:
  - Enforces Product Owner (PO) versus Developer boundaries: developers implement features against fixed acceptance criteria; POs manage prioritization and scope.
  - Event 0 sprint gates: enforces rigorous pre-flight checks (dependency resolution, spec completeness, test environment readiness) prior to sprint kickoff.
  - SQLite state management: updates task statuses, links tickets to issues, and calculates velocity metrics deterministically.

### 1.3 `agent-ecosystem` (Domain: `ecosystem`)
- **Intent**: Fleet-wide agent governance, golden configuration maintenance in `~/.agents`, subagent batching constraints, and inter-agent handoff standards.
- **Trigger Phrases**:
  - "manage agent fleet", "audit agent config", "sync ~/.agents"
  - "spawn subagents", "batch subagents", "subagent resource limit"
  - "handoff to agent", "inter-agent protocol", "agent coordination"
- **Target Capabilities & Actions**:
  - Subagent batching invariant: enforces strict batch limit of <= 10 concurrent subagents; requires all subagents in a batch to complete before launching subsequent batches.
  - Golden configuration management: synchronizes skills, MCP servers, and environment rules across active agents.
  - Inter-agent handoffs: defines structured summary schemas, residual risk logging, and context handoff contracts between coordinators and specialists.

### 1.4 `academic-scholar` (Domain: `scholarship`)
- **Intent**: Academic research assistance, literature synthesis, bioethics reasoning, and scholarly coaching for the KCL MSc in Mental Health, Ethics and Law.
- **Trigger Phrases**:
  - "research mental health law", "analyze ethics case", "legal citation check"
  - "review essay argument", "synthesize academic literature", "oscola citation"
  - "statutory interpretation", "co-author critique", "bioethics deliberation"
- **Target Capabilities & Actions**:
  - Student-authored prose integrity: acts strictly as a tutor, sparring partner, and critical reviewer; ensures all final writing represents authentic student reasoning and expression.
  - Citation precision: formats and verifies legal and academic references (OSCOLA, Bluebook, Harvard styles).
  - Analytical depth: evaluates legal statutes (e.g. Mental Health Act, Mental Capacity Act) and bioethical principles (autonomy, beneficence, justice).

### 1.5 `personal-cadence` (Domain: `cadence`)
- **Intent**: Personal productivity governance, ADHD momentum support, Jibun Techo time tracking, Hermes standup coordination, and cognitive energy alignment.
- **Trigger Phrases**:
  - "morning brief", "evening review", "adhd momentum reset"
  - "draft energy map", "jibun techo pull", "weekly review prep"
  - "check cognitive bandwidth", "daily standup summary", "inbox triage nudge"
- **Target Capabilities & Actions**:
  - Energy-to-task pairing: matches scheduled work with operator energy cycles (deep focus vs administrative vs restorative).
  - Jibun Techo projections: maps daily vertical schedule allocations, tracks habitual consistency, and conducts weekly consolidation.
  - Momentum protection: provides low-friction starting steps, visual checklists, and executive function scaffolding for complex initiatives.

### 1.6 `thinking-partner` (Domain: `cognition`)
- **Intent**: Socratic intellectual sparring, concept stress-testing, architectural tradeoff probing, and Architecture Decision Record (ADR) formulation.
- **Trigger Phrases**:
  - "grill me", "stress-test this idea", "challenge my architecture"
  - "socratic sparring", "probe design tradeoffs", "formulate adr"
  - "find failure modes", "devils advocate", "explore second-order effects"
- **Target Capabilities & Actions**:
  - Oxford tutorial style dialogue: relentlessly questions implicit assumptions, probes edge conditions, and demands defensible justifications.
  - Tradeoff analysis: evaluates competing technical solutions across complexity, maintainability, and operational cost dimensions.
  - ADR generation: captures the final decision context, alternatives considered, consequences, and compliance obligations into standard ADR documents.

### 1.7 `/ask-coach` (Handoff, not a deep module)
- **Detect**: `skills/ask-coach/SKILL.md` exists in the skills repository, or `/ask-coach` is installed.
- **Intent**: Coaching and MSc study workflow: orientation, returning after a break, session start and end, supervision prep and debrief, viva, quizzes, academic review.
- **Trigger Phrases**:
  - "coach me", "where was I", "next coaching command", "start study session"
  - "prep supervision", "viva practice", "academic review", "end session"
- **Rule**: Hand off to `/ask-coach` and stop; it owns the 22 coaching skills and picks the command. This router never selects a coaching command itself.
- **Fallback**: If `/ask-coach` is absent, route to `academic-scholar` (1.4).
- **Counts**: The 6 deep modules and 8 workspaces are unchanged; `/ask-coach` adds neither.

---

## 2. Upstream Engineering Pipeline

For software development and architectural implementation, agents and operators progress sequentially through the six-phase upstream engineering pipeline:

```text
/grill-me  -->  /to-spec  -->  /to-tickets  -->  /tdd  -->  /code-review  -->  /pr
```

1. **Phase 1: `/grill-me` (Socratic Stress-Testing)**
   - Objective: Interrogate proposed requirements, identify unstated assumptions, discover edge cases, and align on core architecture.
   - Deliverable: Validated decision matrix and accepted design boundaries.

2. **Phase 2: `/to-spec` (Formal Specification Formulation)**
   - Objective: Synthesize the grill findings into a rigorous, unambiguous specification document.
   - Deliverable: Approved specification declaring system context, data models, interface seams, and explicit acceptance criteria.

3. **Phase 3: `/to-tickets` (Atomic Work Decomposition)**
   - Objective: Break down the specification into small, self-contained, independent implementation tickets.
   - Deliverable: Ordered ticket backlog in AWT with exact line budgets, clear scopes, and verification checklists.

4. **Phase 4: `/tdd` (Test-Driven Implementation)**
   - Objective: Implement ticket functionality following the Red-Green-Refactor cycle.
   - Deliverable: Failing test demonstrating absence of feature (Red), minimum implementation passing test (Green), and refactored code adhering to standards.

5. **Phase 5: `/code-review` (Two-Axis Adversarial Review)**
   - Objective: Evaluate pull request or branch changes along two orthogonal axes:
     - Spec Axis: Does the implementation satisfy all requirements and invariants in the issue/spec without extraneous changes?
     - Standards Axis: Does the implementation obey coding standards, budgets (<= 100 lines), terminal references, and security rules?
   - Deliverable: Adversarial review report with zero-approval on latent defects.

6. **Phase 6: `/pr` (Pull Request Delivery)**
   - Objective: Construct high-fidelity pull request documentation ready for human owner review and merge.
   - Deliverable: Structured PR description with summary of changes, verification evidence, and risk analysis.

---

## 3. Execution Phase Boundary Guidelines

When navigating long-running sessions, multi-repository tasks, or large implementation projects, operators and agents must observe explicit context management boundaries:

| Action / Command | Trigger Condition | Operational Effect |
|---|---|---|
| `Continue` | Cohesive, incremental steps within the same ticket and workspace. | Keeps conversational context active; proceeds immediately to next task sub-step without resetting state. |
| `/clear` | Context switching between unrelated repositories, tickets, or deep modules. | Erases active conversational window; starts with fresh context to eliminate state pollution and hallucinations. |
| `/handoff` | Session termination, shift handoff, or transitioning between distinct agent roles. | Generates and persists a structured handoff note capturing completed work, open blockers, and exact next steps. |
| `Subagent` | Heavy exploratory research, parallel file analysis, or CPU-intensive task runs. | Spawns background worker in isolated context (strictly <= 10 concurrent subagents); reports summarized findings back to coordinator. |
| `/compact` | Conversation context approaching token capacity limit during extended work. | Summarizes historical conversation context while preserving critical constraints and active task invariants. |
