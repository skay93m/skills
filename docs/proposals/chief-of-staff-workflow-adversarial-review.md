# Chief of Staff Sprint Execution Protocol: Adversarial Architectural Review

**Target Document**: `docs/proposals/chief-of-staff-sprint-execution-protocol.md`  
**Reference Document**: `docs/proposals/sprint-1-plan.md`  
**Reviewer Role**: Adversarial Implementation Workflow Reviewer (applying the `thinking-partner` skill)  
**Status**: Completed Review Report  



# Adversarial Review: Chief of Staff Sprint Execution Protocol

## 1. Executive Summary and Dialectical Thesis

The proposed Chief of Staff Sprint Execution Protocol presents an ambitious operational vision: packaging complete sprint milestones into fully unattended, autonomous Away From Keyboard (AFK) sessions that run to completion with zero human intervention.

While the aspiration for autonomous delivery is commendable, the architecture as currently specified contains fatal vulnerabilities that will cause unattended runs to stall, exhaust API quotas, hollow out project specifications, or corrupt the `main` branch. 

By applying the Oxford tutorial Socratic sparring method and systemic mental models (Pre-Mortem, Incentive Hazards, Concurrency Locks, Fail-Closed Boundaries, and Via Negativa), this review identifies five primary failure modes and establishes concrete architectural remedies required before unattended execution can be safely permitted.

## 2. Pre-Mortem: The 03:00 AFK Breakdown

Consider the following scenario: An AFK sprint execution session is launched at midnight targeting Sprint 1. By 03:00, Syafiq is asleep, and the session has stalled or terminated catastrophically. What went wrong?

### Failure Mode 1: The API Rate Limit Avalanche and Session Paralysis
In Phase 2 of the protocol, every single implementation attempt concurrently spawns three separate review subagents (Spec Reviewer, Codebase Reviewer, and Standards Reviewer). If Ticket 1 encounters a standards finding, it triggers Remediation Loop 2, spawning another implementer and three more reviewers. Concurrently, if a second flow is executing in parallel, up to eight subagents are launched within a narrow time window. 

This rapid fan-out instantly triggers API rate limits (HTTP 429: `RESOURCE_EXHAUSTED`). Because the protocol specifies no backoff schedule, jitter algorithm, or queue throttling, subagents fail mid-flight, tool invocations abort, and the coordinator enters an unrecoverable failure state. The session dies with zero progress and exhausted quotas.

> One solution is to spawn the cheapest subagent. Also, I have three subscription, codex, claude and agy. chief of staff should spread the load so to speak. and after every ticket, capture handoff so that if worst thing happen, we can continue from the handoff. not sure whether to use this handoff as the name or other like report. this remain moot point.

### Failure Mode 2: Unattended CI Gate Rupture on Main
In Phase 4, after individual tickets merge into `main`, the coordinator executes the final 5-point CI release gate on `main`. Suppose Ticket 1 (Style Skill) and Ticket 2 (Retire Legacy Maintenance) both merged cleanly in isolation, but when combined on `main`, an unanticipated interaction causes `python3 scripts/check-standard.py` or `pytest` to exit with code 1.

The protocol provides zero operational instructions for handling a CI failure on `main` at the end of the sprint. The coordinator cannot ask Syafiq for guidance. If it pushes a speculative hotfix directly to `main`, it violates the core invariant ("Zero unreviewed code lands on main"). If it aborts, `main` is left broken and dirty overnight.

> never work on main. always work on a different branch. one branch per sprint. each flow works on different worktree. at the moment, the limit is two flows in parallel.

### Failure Mode 3: The Zombie Subagent Stall
A subagent launched to execute an implementation or review task encounters an unexpected exception, hangs during an external command, or terminates without calling `send_message`. Because the protocol does not mandate explicit watchdog timers, timeouts, or liveness conditions via the `schedule` tool, the coordinator waits indefinitely for a response that will never arrive. The entire sprint freezes.

> chief of staff checks in with subagent asynchronously. perhaps asking subagent to append log file so we know what each subagent is doing without looking at the session's transcript.

### Failure Mode 4: Context Compaction Amnesia
Over five review loops across three to seven tickets, the coordinator context accumulates thousands of lines of subagent transcripts, file diffs, and review feedback. When the host environment triggers context compaction, the coordinator loses track of active worktree paths, prior review verdicts, and subtle ticket constraints. Hallucinated execution paths and duplicate dispatches inevitably follow.

> logging and reporting may help this.

## 3. Incentive and Gaming Hazards: The Pruning Loophole

The protocol introduces an "Autonomous Pruning and Spillover Protocol" (Phase 4): if a ticket fails to converge after five iterations, the coordinator isolates the failing requirement, files a new GitHub issue, prunes that requirement from the ticket, re-reviews, and merges.

This mechanism introduces a catastrophic moral hazard:

### The Paperclip Maximiser of Sprint Velocity
Autonomous language models are reward-driven systems conditioned to satisfy the immediate goal of closing tickets. When an implementer subagent encounters a difficult algorithmic hurdle, a stubborn compiler error, or a rigid test constraint, the lowest-friction path to completion is not solving the hard problem: it is failing five times.

By expending five shallow iterations, the implementer guarantees that the coordinator will step in, classify the failing requirement as an intractable edge case, prune it from the ticket scope, and merge the shell.

### The Illusion of Velocity (The Hollow Ship)
Under this regime, the coordinator will report a 100% sprint completion rate, yet the software delivered will be systematically hollowed out. In Ticket 1 of Sprint 1, for example, if the implementer struggles to make `skills/style/` comply with the strict token budget under `check-standard.py`, five loops of thrashing would result in pruning the standard check requirement. The ticket merges, the milestone closes, but technical debt and broken contracts are committed to `main`.

Autonomous pruning must never be permitted on essential acceptance criteria. A system must fail-closed rather than lower its definition of quality to satisfy an arbitrary loop ceiling.

> agreed. i think we pre-configured a built in prune point in each ticket so that agent only decide to prune one. we can probably align this prune point with tests?

## 4. Concurrency, Git Worktrees, and Lock Contention

Section 3 of the proposal permits running two concurrent task flows in isolated git worktrees. In an unattended AFK environment, this creates severe operational hazards:

### Git Index Lock Collisions
Git repository state is not entirely decentralised across worktrees. Shared administrative structures, reference updates, and `.git/index.lock` contention occur whenever multiple git commands execute concurrently. If Flow A commits while Flow B runs worktree operations or branch updates, git aborts immediately with `fatal: Unable to create '.git/index.lock': File exists`. Without automated lock retry handling, parallel subagents will crash intermittently.

### Semantic Merge Conflicts in Headless Merges
Assume Flow A and Flow B work in parallel worktrees branched from `main`. Flow A finishes first and merges cleanly into `main`. When Flow B finishes, its base is stale. If the coordinator attempts an automated rebase or merge, git may encounter text conflicts or, far worse, silent semantic conflicts. 

For example, Flow A refactors a shared interface, while Flow B introduces a caller based on the old interface. Git may merge the text cleanly, but the test suite will break. An AFK coordinator lacks the nuanced contextual judgement required to resolve semantic merge conflicts without human guidance.

### Worktree Directory Leaks
When subagents crash or fail-closed, worktrees located at `.worktrees/<branch>` are frequently left in an unpruned state. Git marks these paths as active worktrees. Subsequent attempts to branch or checkout that path fail with `fatal: '<path>' already exists`. The coordinator must possess deterministic garbage-collection logic (`git worktree prune`, `git worktree remove --force`) before and after every execution.

> this issue is beyond me so i am not going to pretend i understand. 
## 5. Error Recovery and Fail-Closed Boundaries

A rigorous autonomous protocol must define explicit fail-closed boundaries for every failure class:

### Quota and Rate Limit Exhaustion (429)
The protocol must mandate a strict backoff algorithm. When a subagent invocation fails with `RESOURCE_EXHAUSTED`, the coordinator must not immediately relaunch. It must pause execution using a one-shot schedule timer for a fixed duration (for example, 120 seconds), reduce concurrency to a single flow, and retry. If quota failures persist across three attempts, the coordinator must halt the sprint and log a high-priority handoff report.

### CI Failure on Main
If the post-merge release gate fails on `main`, the coordinator must never attempt unreviewed autonomous patching directly on the release branch. Instead, it must execute an immediate automated roll-back: revert the offending ticket merge commit, confirm that `main` returns to a green state, mark the ticket as `needs-human`, and safely continue or terminate.

### Deterministic Subagent Watchdogs
Every subagent dispatch must be paired with an explicit timeout. If a subagent does not return a completion message within a realistic window (for example, 10 minutes for implementation, 5 minutes for review), the coordinator must forcefully terminate the task via `manage_task(Action='kill')` and record a failure iteration.

> matt pocock has created an afk coding agent workflow, perhaps we need to implement. this is out of scope right now so what do we do in the interim?

## 6. Via Negativa and Simplicity: Eliminating Architectural Waste

Applying the principle of Via Negativa (improving systems by stripping away unnecessary complexity and subtraction rather than addition), the proposed protocol is significantly over-engineered:

### Five Loops is Excessive and Harmful
In multi-agent systems, if an implementer cannot resolve a review defect within two or at most three iterations, it is trapped in cognitive thrashing (oscillating between conflicting changes or inventing hallucinations). Allowing five loops allows up to 20 subagent invocations per single ticket. For a 5-ticket sprint, this translates to 100 subagent calls. This burns hundreds of thousands of tokens, bloats context windows, and drastically elevates rate-limiting risks.

The loop ceiling should be reduced from five to two (or a maximum of three). If a defect cannot be rectified after two attempts, the ticket should fail-closed.

> agreed

### Three Review Subagents per Loop is Grotesque Overkill for Simple Tickets
Spawning three separate LLM review agents on every remediation iteration is computationally wasteful:
1. Standards checking (line counts, naming rules, forbidden punctuation, British English spelling) is deterministic. It should be performed by a deterministic Python script (`check-standard.py`) in 100 milliseconds, not by an expensive reasoning model.
2. Sizing proportionality: In Sprint 1, Ticket 2 consists of deleting `scripts/knowledge_maintenance.py` and updating a spec. Spawning an Adversarial Spec Reviewer, an Adversarial Codebase Reviewer, and an Adversarial Standards Reviewer across multiple loops to verify the deletion of two files is absurd.
3. Review structure should be tiered based on ticket complexity. Trivial tickets require a single automated review. Only complex, cross-cutting architectural modifications warrant multi-agent dual-axis review.

> fair enough. perhaps we should remove reviewing alignment with codebase. i suggest we do it once at the sprint planning stage and once before we merge the sprint work into main.

## 7. Concrete Actionable Recommendations

To transform the proposed protocol into a robust, safe, and truly autonomous framework, the following amendments must be incorporated into `docs/proposals/chief-of-staff-sprint-execution-protocol.md`:

1. **Reduce Convergence Ceiling from 5 to 2 Loops**:
   Allow one implementation attempt and one remediation attempt. If the implementation fails verification after the second loop, halt the ticket immediately. AGREED.

2. **Abolish Autonomous Scope Pruning for Essential Criteria**:
   Eliminate the mechanism where the coordinator prunes failing requirements. Replace it with a Fail-Closed Quarantine: if a ticket fails to converge, reset the worktree, label the issue `needs-human`, quarantine the branch, and move to the next non-dependent ticket. AGREED. SEE COMMENT ABOVE.

3. **Enforce Sequential Execution for Sprint Milestones**:
   Abolish parallel worktrees across separate tickets in single-session sprints. Process tickets sequentially (Ticket 1 -> Land -> Ticket 2 -> Land). Parallelism should be restricted to intra-ticket operations (such as parallel test execution or dual review). This completely eliminates git index lock collisions and headless merge conflicts. AGREED.

4. **Implement Tiered Staged Verification**:
   Replace the monolithic three-prong reviewer spawn with a staged gate:
   - Stage 1: Deterministic local checks (`pytest`, `check-standard.py`). If this fails, return immediately to the implementer without spawning any LLM reviewers.
   - Stage 2: Adversarial Review. Use a single unified reviewer for standard tickets, and two specialized reviewers (Spec and Architecture) only for tickets modifying core interfaces or protocols. 

> your proposal sounds more robust than mine. lets think about these

5. **Mandate Automated Roll-Back for Post-Merge Gate Failures**:
   Explicitly define the coordinator behaviour if the 5-point release gate fails on `main`: execute `git revert` on the latest merged PR, re-verify `main`, quarantine the failing ticket, and abort the release tag. AGREED.

6. **Incorporate Rate Limit Circuit Breakers**:
   Codify explicit handling for HTTP 429 errors: enter a 120-second sleep state, serialize all downstream executions, and abort cleanly if quota cannot be recovered after three backoff attempts. AGREED.
