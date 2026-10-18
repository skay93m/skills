# Coordinator & Subagent Protocol

This document defines the official Coordinator & Subagent Working Protocol for all agent sessions (Claude, Codex, Antigravity) working in this repository.

## 1. Core Principles

### Role Separation (Pure Coordinator Pattern)
The Parent or Primary Agent functions strictly as a **Coordinator Agent**:
- **No Direct Implementation**: The Coordinator never writes application/feature code, tests, or skill files directly in the parent context.
- **Pure Coordination**: The Coordinator's responsibilities are exclusively:
  - Scoping, decomposing, and prioritizing issues and tasks.
  - Delegating discrete execution tasks to specialized subagents.
  - Managing subagent lifecycles and enforcing batch limits.
  - Orchestrating adversarial code reviews.
  - Dispatching fixes when defects are uncovered.
  - Synthesizing final results and executing git operations (branching, PR creation, and landing).
- **Context Preservation**: Keeping the primary context clean of transient implementation diffs and large test logs ensures deep reasoning capacity and clear architectural oversight.

### Single Ticket Flow
- **Strict Focus**: The Coordinator focuses on one ticket or feature stream at a time from start to finish.
- **Parallel Work Limit**: At most two non-conflicting, fully independent task flows may run concurrently when explicit separation is guaranteed.
- **Run-to-Completion**: A ticket must complete its full lifecycle (planning → implementation → dual-axis adversarial review → fixer loop → verification) before moving to subsequent work. Completing a ticket does not discharge the whole-batch review in Phase 6 step 4(a). This prevents work-in-progress (WIP) sprawl and context dilution. Under one-PR delivery (Phase 6), a ticket is complete once its reviewed commits are on the integration PR; the batch's PR is merged once, after its last ticket.

### Cost-Efficiency Tier
- Subagents handle heavy implementation, testing, review, and fixing tasks using cost-efficient models (`Model: "flash"` where supported, such as Gemini Flash / Flash Lite or fast tier models).
- Expensive higher-tier reasoning models (`pro` or caller inheritance) are reserved for top-level coordinator orchestration, high-complexity architectural design, or when specifically mandated by the task.

### Batching & Lifecycle Cleanup
- **Subagent Batch Limit**: Never spawn more than 10 subagents in a single batch (strictly adhering to the subagent batching invariant).
- **Sequential Batches**: If a task requires more than 10 workers, queue them in sequential batches of at most 10, waiting for each batch to finish before launching the next.
- **Active Lifecycle Cleanup**: Subagents are ephemeral. The Coordinator must immediately terminate or kill idle or completed subagents before dispatching subsequent phases or new batches. This releases session resources, avoids quota exhaustion (`RESOURCE_EXHAUSTED` / 429), and eliminates zombie processes.

---

## 2. Phase-by-Phase Workflow

### Phase 1: Planning & Delegation Framing
1. Review the issue or feature requirement (`gh issue view`, specification documents).
2. Clarify scope boundaries, target file paths, constraints, and acceptance criteria.
3. Formulate a self-contained, explicit task prompt for an Implementation subagent.

### Phase 2: Implementation Phase
1. Dispatch an Implementation Subagent (`flash` tier) with:
   - Defined task scope and strict file boundaries.
   - Deliverable specifications and edge-case requirements.
   - Verification instructions (`python3 scripts/check-standard.py --base origin/main`, `pytest`, linter).
2. The Implementation Subagent performs edits, runs the test suite, confirms zero errors, and reports back.
3. The Coordinator reviews the completion report and inspects the git status and diff.
4. The Coordinator immediately terminates the Implementation Subagent before initiating review.

### Phase 3: Two-Axis Adversarial Code Review Loop
Every implementation must undergo a dual, concurrent adversarial review prior to merge approval. The Coordinator spawns two independent review subagents in parallel. Each reviewer applies one axis and runs `/code-review` on the change. A reviewer that cannot run it says so in its verdict and cannot pass. Each reviewer posts its verdict as a PR comment whose first line is exactly `<!-- adversarial-review: axis=<spec|standards> verdict=<pass|fail> sha=<head sha> -->`. Any new commit voids earlier verdicts. `verdict=pass` means zero BLOCKING findings from that reviewer on the current head.

1. **Adversarial Spec Reviewer**:
   - **Mission**: Relentlessly hunt for loopholes, unhandled edge cases, omitted spec constraints, subtle semantic drift from original intent, missing contract assertions, and latent regressions.
   - **Checklist**:
     - Did the implementation address all functional and non-functional requirements in the ticket?
     - Are error branches, empty states, and boundary conditions handled?
     - Did any public interface or contract inadvertently drift or break?
     - Are tests testing real edge cases or merely asserting happy paths?

2. **Adversarial Standards Reviewer**:
   - **Mission**: Relentlessly audit the code against repository standards (`sk-pr-review-standard`, `scripts/check-standard.py`, coding style, and architecture guidelines).
   - **Checklist**:
     - **Line Budgets**: Do skill files (`SKILL.md`) strictly obey the 100-line budget (`S4`)? Are other files concise and modular?
     - **Reference Depth**: Are markdown reference links strictly one level deep (`S5`), with zero nested chaining?
     - **Naming & Conventions**: Do files and directories follow lowercase kebab-case?
     - **Privacy & Security**: Are any secrets (`H1`), private note references (`H2`), personal information (`H3`), local user home paths (`H4`), or internal URLs (`H6`) exposed?
     - **Code Cleanliness**: Are errors typed and handled? Are imports cleanly organized without redundant dependencies?

3. **Finding Format**:
   Review findings must specify exact paths, line numbers, and severity:
   - `BLOCKING [CHECK_ID] path/to/file:line`: Must be remediated before merge.
   - `NON-BLOCKING [CHECK_ID] path/to/file:line`: Advisory improvement or stylistic suggestion.

### Phase 4: Fixer Loop
1. If **either** adversarial reviewer reports one or more `BLOCKING` findings:
   - The Coordinator dispatches a dedicated **Fixer Subagent** (`flash` tier).
   - The prompt provides the exact reviewer findings, files, lines, and instructions to resolve the defects.
   - The Fixer applies targeted changes, runs tests and standard checks, and reports back.
2. The Coordinator terminates the Fixer and dispatches verification / adversarial re-review.
3. The loop repeats until **0 blocking findings remain**.
4. **Zero-Defect Gate**: No pull request or branch may be merged with unresolved blocking findings or known latent defects. Latent defects are always BLOCKING.

### Phase 5: Whole-Product Adversarial Review
- At major milestone boundaries, multi-ticket epics, or release tags, the Coordinator triggers a holistic, whole-product adversarial audit.
- Audits end-to-end integration across modules, full test suite stability, architectural consistency, documentation completeness, and performance regressions across the entire repository.

### Phase 6: Landing & Merging
1. Verify git working directory and run full verification (`python3 scripts/check-standard.py --base origin/main`, `pytest`). The pass criterion for `check-standard.py` is 0 blocking and 0 non-blocking findings.
2. Push branch to remote repository.
3. Open a pull request using GitHub CLI (`gh pr create --draft`). A ticket batch may land as reviewed commits on one integration PR. The PR stays a draft while any of its tickets remain. Each ticket still completes Phase 3 and Phase 4 before the next starts. After the last ticket, both reviewers also review the whole batch (cumulative diff) on the final head.
4. The order is fixed:
   - (a) Both adversarial reviewers pass on the final head sha, covering the whole-batch review. The Coordinator confirms each verdict by comparing the marker sha with `gh pr view --json headRefOid`.
   - (b) Once all of the batch's tickets are done, mark the PR ready (`gh pr ready`).
   - (c) Merge with `gh pr merge --merge` only if the permission classifier (the Claude Code auto-mode safety check that can deny an action) and the repository ruleset allow it. Latent defects are always BLOCKING and must be fixed; only NON-BLOCKING style or clarity notes may be dismissed, with a stated reason. If the classifier or ruleset blocks the merge, stop and ask the human; do not work around it, and leave the PR ready for the human to merge once. A PR whose body lists decisions awaiting human approval (e.g. collision decisions) is never merged by the agent; it is left ready for the human. Never use `--admin` or other bypasses to defeat a permission or review denial.
5. After a merge, fast-forward local `main` (`git pull origin main`) and confirm `git status` is clean.

---

## 3. Documentation Integrity & Standards Invariants

- **Markdown Line Budgets**: Adhere strictly to length limits, such as the 100-line limit on `SKILL.md` files. Keep agent documentation concise, precise, and modular.
- **Reference Depth**: Reference links must remain one level deep from the parent skill. Never link a reference file to another reference file.
- **Path Hygiene**: Never commit hardcoded machine-specific user home paths. Always use repo-relative paths.
- **Privacy & Secrets**: Zero tolerance for credentials, API tokens, internal URLs, or private personal data.
- **Standard Checks Verification**: Always run `python3 scripts/check-standard.py --base origin/main` and `pytest` on every iteration to guarantee full compliance before landing changes.
