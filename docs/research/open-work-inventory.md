# Open work inventory against candidate scopes

Research for issue #118 (part of map #117). Facts only. No recommendation on scope names, repo layout, or what to defer.

Snapshot: 2026-10-17. Repo `skay93m/syafiq-kay-skills`. Baseline `origin/main` at `74a92bd`.

## Candidate scopes tested (not decided)

| Code | Candidate scope |
|---|---|
| KM | Knowledge maintenance and the seam |
| DP | Daily planning (task-assistant, Hermes standup, check-ins) |
| ET | Email triage |
| RG | Repo governance and install |
| none | Fits no candidate scope cleanly (see Misfit list) |
| meta | The scoping wayfinder itself (#117 to #123); not project work |

## Sources and method

- Issues: `list_issues` state OPEN (57 open, all read from the GitHub API, bodies read in full for the ones that matter; bodies of #55, #42, #90, #105, #109, #71, #79 and #2 were read only in their first ~2,500 characters, see "Not verified").
- PRs: `list_pull_requests` state open (3: #108, #111, #112). Bodies read in full.
- Branches: `git fetch origin`, then `git branch -r`, ancestry with `git merge-base --is-ancestor`, file lists with `git diff --name-status origin/main origin/<branch>`.
- Skills: `git ls-tree origin/main skills/` (29 directories) plus skills added only on unmerged branches.
- "State" uses the label on the issue. Blocked-by lines are quoted from the issue body, not from GitHub's dependency feature (not queried).
- Scope assignment rule used: the scope whose subject the item's own text is about. Where an item names two scopes in its own text, it is listed with both and also appears in the Misfit list.

Label meanings come from `docs/agents/triage-labels.md` (default vocabulary); `wayfinder:*` labels are map/ticket types, not triage states.

## Counts

- Open issues: 57 (10 deferred backlog `wayfinder:task` items, #3 to #13 minus closed #11; 3 older maps #2, #44, #79; 7 scoping-wayfinder items #117 to #123).
- `ready-for-agent`: 17 open issues (#42, #46, #47, #49, #50, #55 to #60, #63, #64, #65, #71, #77, #109). #109 carries the label but its body says "IMPLEMENTATION_AUTHORIZED: NO" and that the label is withheld until the owner comments; the label and the body disagree (see Misfit list, item 12).
- Open PRs: 3, all unmerged; #111 and #112 are drafts.
- Unmerged remote branches by commit count ahead of `origin/main`: 7 (`feat/109-seam`, `feat/109-tracking-and-wizard`, `feat/109-go-live`, `feat/ss-guarded-knowledge-skills`, `feat/ss-run-audit-seam-prompts`, `feat/ss-seam-rc-mode`, `docs/77-track-main-wording`). Two more remote branches exist but are fully contained in `main` by ancestry (`develop`, `feature/46-sk-task-morning-standup`).
- Skills on `main`: 29. Skills that exist only on unmerged branches: 2 (`seam-adapter`, `knowledge-run-audit`).

## 1. Open issues

State column: label, then the blocking statement quoted or summarised from the body.

### Knowledge maintenance and the seam (KM)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| #49 Specify modular Wiki knowledge maintenance skills | KM | Says `task-assistant` "remains independent" (DP). Names Gemini/Drive review path and Basic Memory Wiki as canonical store. Coordinated by #50, #51 (ET) and #55 (DP). | `ready-for-agent` |
| #55 Coordinate Hermes daily task check-ins and Wiki knowledge maintenance | KM + DP (straddles) | Its own text delivers "two independent vertical slices": Hermes task assistant (DP: #42, #46, #47) and daily knowledge maintenance (KM: #49). Children #56 to #60. | `ready-for-agent` |
| #57 Make daily knowledge maintenance executable | KM | Part of #55 (DP parent). Blocked by #49. | `ready-for-agent`; blocked by #49 |
| #59 Run controlled end-to-end verification | KM + DP (straddles) | Blocked by #56 (DP), #58 (DP), #57 (KM). Acceptance includes "knowledge maintenance cannot create or mutate a Commitment or alter Task meaning". | `ready-for-agent`; blocked by #56, #57, #58 |
| #60 Activate and monitor the approved schedules | KM + DP (straddles) | Activates Hermes task schedules (DP) and the 03:00 knowledge schedule (KM). Blocked by #59. | `ready-for-agent`; blocked by #59 |
| #63 Run the pinned report-only ingest/lint workflow | KM | Blocked by #62 (closed) and "owner merges PR #61" (PR #61 is closed; whether it merged was not verified). #110 says it also blocks on SW work (private). | `ready-for-agent`; blocker #62 closed, PR #61 closed |
| #64 Prove idempotency and failure isolation | KM | Blocked by #63. #110 lists it as blocked by SW work. | `ready-for-agent`; blocked by #63 |
| #65 Release v0.1.0 and activate the daily schedule | KM (also RG: semantic release, tag) | Blocked by #64 and PR #61. States Hermes standup/check-ins are "separate and not changed" (DP). Release/tag step overlaps RG. | `ready-for-agent`; blocked by #64 |
| #71 Extend daily maintenance to lint the complete Wiki with resumable coverage | KM | Part of #49. | `ready-for-agent` |
| #77 Replace mandatory-pin wording with track-main plus optional SHA override | KM | Wording in #49 body and the spec. Related PR #108, #106, #107, #113. | `ready-for-agent` |
| #106 Fix revision override precedence and record the loaded revision | KM | Edits `scripts/knowledge_maintenance.py`. Follow-up to #77/#49. Related #113. | `needs-triage` |
| #107 Remove stale mandatory-pin and develop wording | KM | Edits the three knowledge skills and the spec. Follow-up to #77. | `needs-triage` |
| #109 Go live: ChatGPT daily ingest/lint with a minimal SS/SW seam | KM | Related list: #49, #55, #57, #60, #63, #64, #65, #77, #90 to #99, #106, #107, PR #108. Depends on a private SW binding "outside this repository". Strand 1 (revision recording, wizard) is KM; strand 2 (seam) is KM-seam; wizard is an install/launcher script (RG-adjacent). | `ready-for-agent` label, but body says `IMPLEMENTATION_AUTHORIZED: NO` |
| #110 SW delegation pointer: seam knowledge.ingest 0.1.0 report-only | KM (seam) | External: SW session (private handoff note in the wiki project). Blocks #96 close, a live run, #63, #64, schedule. | `needs-info` |
| #113 Decide unattended-run policy: guarded model vs report-only go-live script and tracking main | KM | Blocks landing the #109 stack (PR #111 body). Owner decision. | `needs-triage` |
| #114 Retire superseded report-only maintenance code and spec text | KM | "Depends on" #113. | `needs-triage`; depends on #113 |
| #115 Land the stacked #109 branches into main in order | KM (branch landing) + RG (merge order, branch pruning) | Stack spans `feat/109-*`, PR #108, #111, #112 and `feature/46-sk-task-morning-standup` (DP). Also asks about pruning 11 local `worktree-agent-*` branches. | `needs-triage` |
| #116 Owner decisions pending on seam rc.1, ADR 0001 and the run-audit skill | KM (seam) | Relates PR #112, #84, #85, #109, #110. | `needs-triage` |
| #90 Specify sk-skills installation migration and the SS/SW seam | KM (seam) + RG (install) (straddles) | Single spec containing both outcomes of map #79. "Blocked by #89" (clean baseline); #89 was not read. | `needs-triage`; blocked by #89 |
| #91 Define the seam envelope and closed vocabularies | KM (seam) | Child of #90. Namespace `com.syafiqkay.skills` provisional. | `needs-triage`; IMPLEMENTATION_AUTHORIZED: NO |
| #92 Define the capability profile format and knowledge.ingest 0.1.0 profile | KM (seam) | Child of #90. Tokens come from #96. | `needs-triage`; IMPLEMENTATION_AUTHORIZED: NO |
| #93 Build the seam conformance check on synthetic data | KM (seam) | Child of #90. "Blocked until Syafiq applies `ready-for-agent` after A and B are accepted". | `needs-triage`; blocked |
| #96 Decide grant reference, capability token and backend-constraint token formats | KM (seam) | Child of #90. #110 says it cannot close before the SW work. Tickets A, B and the adapter wait on it. | `needs-info`; IMPLEMENTATION_AUTHORIZED: NO |
| #98 Draft the public SS adapter skill that speaks only the seam | KM (seam) | Child of #90. Branch `feat/109-seam` already contains `skills/seam-adapter` (commit message cites #98). | `needs-info`; IMPLEMENTATION_AUTHORIZED: NO |
| #9 Full ingestion/synthesis governance | KM (title only) | Body is "Deferred task from roadmap." Only the title supports the assignment. | deferred (`wayfinder:task`) |
| #8 Research-compounding workflow | KM or none (title only) | Body is the same one-liner. Title does not name a candidate scope. | deferred (`wayfinder:task`) |
| #7 Currentness automation | none (title only) | Body is the same one-liner. Could concern skills or Wiki notes; not stated. | deferred (`wayfinder:task`) |

### Daily planning (DP)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| #42 Specify the task-assistant adapter for Hermes daily planning | DP | Uses `sk-create-adapter` and upstream `memory-tasks` (RG: authoring and adapter conventions). Wiki Task schema in Basic Memory is shared with ET (#50 delegates task operations to `task-assistant`). | `ready-for-agent` |
| #44 Choose the Next Vertical Slice for memory-tasks (map) | DP | Child discovery map under #42; cites #40, #41, #2 (RG roadmap). | `wayfinder:map` |
| #45 Define the First Daily Standup Slice for memory-tasks | DP | Nested under #44. Reads GitHub for repo-linked task state and Basic Memory for personal tasks. | `wayfinder:grilling` |
| #46 Add the Hermes morning standup to the task-assistant adapter | DP | Part of #42. "Blocked by: None". `skills/task-assistant` already exists on `main` and branch `feature/46-sk-task-morning-standup` is fully contained in `main`; the issue is still open. | `ready-for-agent` |
| #47 Add task-aware daytime check-ins to the task-assistant adapter | DP | Part of #42. Blocked by #46. | `ready-for-agent`; blocked by #46 |
| #56 Connect and verify the Hermes morning standup | DP | Part of #55. Blocked by #46. | `ready-for-agent`; blocked by #46 |
| #58 Connect noon and evening task check-ins | DP | Part of #55. Blocked by #47. | `ready-for-agent`; blocked by #47 |

### Email triage (ET)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| #50 Specify email triage as a deep skill module | ET | Delegates task operations to `task-assistant` / `memory-tasks` (DP). Delegates source capture to knowledge-ingestion contracts (KM). Coordinate with `knowledge-review` (KM; this skill does not exist in `skills/`). Coordinate with #49. | `ready-for-agent` |
| #51 Refactor Inbox Zero automations into thin skill launchers | ET | "Coordinate with #49 and #50". Launchers reference a pinned revision of a GitHub-owned workflow (same pin/tracking question as KM #77, #113). Touches three live ChatGPT automations (07:00, 13:00, 19:00 Europe/London). No automation change authorised. | `needs-info` |

### Repo governance and install (RG)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| #2 Syafiq-Kay-Skills Roadmap & Deferred Backlog (map) | RG | Parent roadmap for everything else (#79 says "#2 stays the parent roadmap"). Its decisions include the `sk-task` adapter (DP) as first production skill. | `wayfinder:map` |
| #79 sk-skills Installation Migration and sk-wiki Seam Wayfinder (map) | RG (install) + KM (seam) (straddles) | Map text states two outcomes: install migration across Claude, Codex, Antigravity, and the SS/SW seam. | `wayfinder:map` |
| #94 Build the read-only install-state verification report | RG | Child of #90. Reads the global Skills lock and host skill directories. | `needs-triage`; IMPLEMENTATION_AUTHORIZED: NO |
| #95 Verify pinned Skills CLI 1.7.2 behaviour | RG | Child of #90. Running the CLI needs owner approval. | `needs-info`; IMPLEMENTATION_AUTHORIZED: NO |
| #97 Add repository projection checks for skills/ layout and provenance | RG | Child of #90. Checks `skills/` layout across all skills (every scope). | `needs-triage`; IMPLEMENTATION_AUTHORIZED: NO |
| #99 Plan the thinking-partner adaptation and glossary terms | RG (security gate, adapter) + KM (seam glossary terms) (straddles) | Child of #90. `thinking-partner` is not in `skills/` on `main` or the branches checked. Security gate is "#43's follow-on" (#43 not read). | `needs-info`; IMPLEMENTATION_AUTHORIZED: NO |
| #105 Specify sandcastle runs on the MacBook (AFK builds with review) | RG (agent workflow, review) | Part of #2. Targets `ready-for-agent` issues from all scopes (names #57, #63, #64, #71, all KM). Orchestration would live in a new private repo. | `needs-triage`; IMPLEMENTATION_AUTHORIZED: NO |
| #3 Machine Onboarding | RG | One-liner body. Title only. Overlaps `sk-onboarding` and `sk-cli-agent-onboarding` skills (see skills table). | deferred |
| #4 Automated healing | RG (title only) | One-liner body. #2's destination lists "healing" as deferred. | deferred |
| #5 Automated repository addition | RG (title only) | One-liner body. | deferred |
| #6 Bulk pruning | RG (title only) | One-liner body. Could also concern Wiki notes (KM); not stated. | deferred |
| #10 Upstream contribution workflow | RG (title only) | One-liner body. | deferred |
| #12 Complex versioning and package distribution | RG (title only) | One-liner body. Related to the `sk-skills` install model of #79. | deferred |
| #13 Broad test framework | RG (title only) | One-liner body. Tests currently exist for KM scripts (`tests/`). | deferred |

### Meta (the scoping wayfinder itself)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| #117 Project Scope Boundaries and Roadmap Order Wayfinder | meta | Names #2, #44, #79 as existing maps and #113 to #116 as owner decisions already filed. | `wayfinder:map` |
| #118 Inventory open work against candidate scopes | meta | Part of #117. | `wayfinder:research` |
| #119 Name the scopes and what each owns | meta | Part of #117. Not blocked. | `wayfinder:grilling` |
| #120 Decide what to roll back or defer | meta | Blocked by #118, #119. | `wayfinder:grilling` |
| #121 Define the interface between scopes and the agent-assignment rule | meta | Blocked by #119. | `wayfinder:grilling` |
| #122 Choose one repository or several | meta | Blocked by #119, #121. | `wayfinder:grilling` |
| #123 Choose the delivery order and milestones | meta | Blocked by #119, #120, #122. | `wayfinder:grilling` |

## 2. Open pull requests

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| PR #108 `docs/77-track-main-wording` | KM | Wording-only. Edits `docs/specs/daily-knowledge-maintenance.md` and `GLOSSARY.md` (glossary is single-context for the whole repo per `AGENTS.md`). Based on `main`, 3 commits ahead. Does not fully close #77. | Open, not draft |
| PR #111 `feat/ss-guarded-knowledge-skills` | KM | Contains all of `feat/109-go-live` (19 commits). Edits `GLOSSARY.md`. Open item 1 says `scripts/setup-chatgpt-ingest-lint.sh` contradicts it (decision #113). Merge `feat/109-go-live` first (body). 30 files. | Open, draft, "Not ready to merge" |
| PR #112 `feat/ss-run-audit-seam-prompts` | KM (seam) | Contains `feat/109-go-live` and `feat/ss-seam-rc-mode`. Changes `scripts/seam_conformance.py` (body: "safety-relevant", own review). Adds ADR 0001 (proposed), skill `knowledge-run-audit`, ChatGPT automation prompts A and B (not created anywhere). Decisions pending in #116. 30 files. | Open, draft, "Not ready to merge" |

## 3. Unmerged remote branches

"Ahead/behind" is against `origin/main` at `74a92bd`.

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| `origin/feat/109-seam` | KM (seam) | Adds `skills/seam-adapter`. Ancestor of `feat/109-go-live`. Not an ancestor of `feat/109-tracking-and-wizard`. | 5 ahead, 0 behind; no PR |
| `origin/feat/109-tracking-and-wizard` | KM (+ install wizard script) | Ancestor of `feat/109-go-live`. Touches the ChatGPT cutover wizard. | 7 ahead, 0 behind; no PR |
| `origin/feat/109-go-live` | KM | Contains the two branches above. Ancestor of the heads of PR #111 and PR #112. No PR of its own (#115). Changes `scripts/setup-chatgpt-ingest-lint.sh`, `GLOSSARY.md`, `docs/seam/*`, `docs/specs/email-triage-spec.md`, three knowledge skills. | 19 ahead, 0 behind; no PR |
| `origin/feat/ss-guarded-knowledge-skills` | KM | Head of PR #111. | 0 behind |
| `origin/feat/ss-run-audit-seam-prompts` | KM (seam) | Head of PR #112. | 0 behind |
| `origin/feat/ss-seam-rc-mode` | KM (seam) | Ancestor of the head of PR #112 (22 ahead of main includes go-live). No PR of its own. | 22 ahead, 0 behind |
| `origin/docs/77-track-main-wording` | KM | Head of PR #108. | 3 ahead |
| `origin/feature/46-sk-task-morning-standup` | DP | Not unmerged by ancestry: 0 ahead of `main`, 41 behind, fully contained in `main` (verified with `merge-base --is-ancestor`). #115 lists it as unmerged work "with no PR". Still exists on the remote. | 0 ahead, 41 behind |
| `origin/develop` | RG (branch hygiene) | Fully contained in `main` (0 ahead, 47 behind). `develop` was retired in commit `2d491fa` (cited in #107). Still exists on the remote. | 0 ahead, 47 behind |
| 11 local `worktree-agent-*` branches | RG (branch hygiene) | Local only in this checkout; not on the remote. #115 asks about pruning them. Their content was not inspected. | local branches |

## 4. Skill directories in `skills/`

Source: `origin/main` (29 directories) plus branch-only additions. Frontmatter and body of each `SKILL.md` were read for the first lines. Many skills carry no `description`.

### Knowledge maintenance and the seam (KM)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| `daily-knowledge-maintenance` | KM | Orchestrates `knowledge-ingest` and `knowledge-lint`. Wording being changed by #107, PR #108, PR #111, PR #112. | on `main` |
| `knowledge-ingest` | KM | Same. `sk-email-ingest` points at "knowledge-capture" and `sk-supervised-ingest` instead (ET). | on `main` |
| `knowledge-lint` | KM | Same. Referenced by `sk-index-governance`. | on `main` |
| `sk-index-governance` | KM | References `knowledge-lint`, `knowledge-maintenance` and two retired `sk-scheduled-*` names (stale cross-references). No frontmatter `description`. | on `main` |
| `sk-supervised-ingest` | KM | Referenced by `sk-email-ingest` (ET). No `description`. | on `main` |
| `sk-unsupervised-ingest` | KM | Bounded non-blocking ingestion of selected Wiki raw material. Relation to `knowledge-ingest` not stated in the files read. | on `main` |
| `sk-semantic-lint` | KM | Referenced by `sk-wiki-maintenance`. | on `main` |
| `sk-wiki-maintenance` | KM | Runs upstream Basic Memory maintenance skills one at a time; references `sk-semantic-lint`. | on `main` |
| `sk-local-cloud-reconciliation` | KM | Referenced by `sk-cli-agent-onboarding`. | on `main` |
| `sk-cli-agent-onboarding` | KM | Wiki-specific contract for CLI agents. Name says "onboarding" (cf. `sk-onboarding`, RG) but the description is Wiki note mutation and sync. | on `main` |
| `sk-triage` | KM | Mandatory startup for Wiki sessions. Not the same as email triage (ET). | on `main` |
| `sk-wiki-stop` | KM | Closes a Wiki work period. | on `main` |
| `seam-adapter` | KM (seam) | Absent from `main`. Present on `feat/109-seam`, `feat/109-go-live`, `feat/ss-guarded-knowledge-skills`, `feat/ss-run-audit-seam-prompts`. Corresponds to #98. | branch only |
| `knowledge-run-audit` | KM (seam) | Absent from `main`. Present only on `feat/ss-run-audit-seam-prompts` (PR #112). Runbook CLI steps marked unverified (#116). | branch only (PR #112) |

### Daily planning (DP)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| `task-assistant` | DP | Adapter over upstream `memory-tasks` (frontmatter `origin`, `category: planning`). Built with the `sk-create-adapter` pattern (RG). References `sk-planning` (not in `skills/`). Wiki Task schema shared with ET per #50. | on `main` |
| `sk-claude-weekly-review-prep` | DP (name only) | Stub: body is one line, "Stub for ...". No content shows its purpose. | on `main`, stub |
| `sk-claude-weekly-task-consolidation` | DP (name only) | Stub. | on `main`, stub |
| `sk-codex-weekday-morning-brief` | DP (name only) | Stub. Could be planning or an unrelated brief; not stated. | on `main`, stub |
| `sk-claude-techo-evening-pull` | DP (name only) | Stub. "Techo" is not defined in any file read (#42 mentions "Jibun Techo" as out of scope). | on `main`, stub |

### Email triage (ET)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| `sk-email-ingest` | ET | Says email triage and Wiki ingestion are "related but separate decisions". References `memory-tasks` (DP) and `sk-supervised-ingest` (KM). Target of #50 (rename proposed to `email-triage`) and #51. | on `main` |
| `sk-claude-daily-inbox-triage` | ET (name only) | Stub. Probably one of the three automations in #51; the stub does not say. | on `main`, stub |
| `sk-claude-inbox-triage-nudge` | ET (name only) | Stub. #51 says the evening run has "no interactive nudge"; link to this stub not verified. | on `main`, stub |

### Repo governance and install (RG)

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| `sk-create-adapter` | RG (authoring) | Used by `task-assistant` (DP) and `sk-wiki-teach`. Referenced by #42, #45, #46. | on `main` |
| `sk-onboarding` | RG | Enforces the `~/.agents` layout and removes legacy installs. Overlaps in subject with #94 and #79 install migration. | on `main` |
| `sk-update` | RG | Runs `~/.local/bin/skills` script; ships `golden-skills.json`. Overlaps with #79 install model (pinned Skills CLI). | on `main` |

### Fit no candidate scope cleanly

| Item | Candidate scope | Cross-scope dependencies | State |
|---|---|---|---|
| `sk-wiki-teach` | none | Adapter of the Matt Pocock teaching method into the Wiki (uses Basic Memory MCP). Not maintenance, planning, email or governance. | on `main` |
| `sk-writing-coach` | none | Reviews Syafiq's journal notes in the Wiki. | on `main` |
| `sk-claude-daily-writing-journal-seed` | none (name only) | Stub. Related to journal/writing by name. | on `main`, stub |
| `sk-claude-draft-energy-map` | none (name only) | Stub. #55 refers to "energy-reminder schedules" as separate from task check-ins, which suggests an energy topic outside DP; the stub gives no content. | on `main`, stub |
| `sk-hermes-energy-inventory-14-days` | none (name only) | Stub. Same energy topic. | on `main`, stub |
| `sk-hermes-daily-audit` | none (name only) | Stub. Hermes named, "audit" not defined. | on `main`, stub |

## 5. Cross-scope dependencies, collected

Each line names two scopes and the item(s) that carry the link, so the links are visible in one place.

| From | To | Carried by |
|---|---|---|
| DP and KM | together | #55 (parent of #56 to #60); #59 blocked by #56, #58 (DP) and #57 (KM); #60 activates both |
| ET to DP | task operations | #50 ("Delegate canonical non-repository task operations to `task-assistant`"); `sk-email-ingest` references `memory-tasks` |
| ET to KM | source capture and review | #50 (ingestion contracts, `knowledge-review`); `sk-email-ingest` references `sk-supervised-ingest`; `docs/specs/email-triage-spec.md` was edited on `feat/109-go-live` |
| ET to KM | pin/tracking model | #51 uses a pinned revision of a GitHub-owned workflow; KM has the same open question in #77, #113 |
| ET to ET/KM | coordination | #51 "Coordinate with #49 and #50" |
| DP to RG | adapter pattern | #42, #45, #46 require `sk-create-adapter` and upstream `memory-tasks` |
| DP and KM | shared Wiki and Basic Memory | #49 and #55 state the Wiki owns canonical knowledge and Tasks; #59 requires knowledge maintenance not to mutate Commitments |
| KM to RG | install and release | #65 (semantic release and tag); #109 (cutover wizard); `scripts/setup-chatgpt-ingest-lint.sh`; #79 and #90 (install migration and seam in one spec) |
| KM to RG | glossary | `GLOSSARY.md` is single-context for the whole repo (`AGENTS.md`); PR #108 and PR #111 edit it; #99 proposes seam terms |
| KM to private SW | external | #109, #110, #96: the private SW binding is outside this repository; its status was not verifiable |
| RG to all | skills layout | #97 checks `skills/` layout and provenance across every skill; #105 would run agents over `ready-for-agent` issues in every scope |
| Branch stack | KM + DP + RG | #115: `feat/109-seam` to `feat/109-tracking-and-wizard` to `feat/109-go-live` to PR #111 and PR #112; plus PR #108 and `feature/46-...` |

## 6. Items that fit no scope cleanly

1. #55, #59, #60: each names KM and DP work in one ticket. The parent's own text calls them "two independent vertical slices".
2. #79 and #90: one map and one spec containing both install migration (RG) and the seam (KM).
3. #99: contains a `thinking-partner` security gate and adaptation (RG-like) and seam glossary terms (KM-like).
4. #115: branch landing is KM; merge order, review assignment and branch pruning could be RG; one branch (`feature/46-...`) is DP.
5. #65 and #109: both include a release/tag or wizard step (RG-like) inside a KM outcome.
6. #7 Currentness automation, #8 Research-compounding workflow, #6 Bulk pruning: one-line bodies; the subject (skills, Wiki notes or the repo) is not stated.
7. Four stub skills whose name fits no candidate scope: `sk-claude-draft-energy-map`, `sk-hermes-energy-inventory-14-days`, `sk-hermes-daily-audit`, `sk-claude-daily-writing-journal-seed`. The other six stubs are placed in DP or ET by name only.
8. `sk-wiki-teach`, `sk-writing-coach`: Wiki-using skills that are not maintenance, planning, email or governance.
9. `sk-cli-agent-onboarding` and `sk-onboarding`: similar names, different subjects (Wiki mutation contract vs skills install layout).
10. #105 sandcastle: the workflow serves all scopes' `ready-for-agent` issues; repo placement is a new private repo.
11. `origin/develop`, `origin/feature/46-sk-task-morning-standup`, and the 11 local `worktree-agent-*` branches: repository hygiene, not tied to a scope; the first two are already contained in `main`.
12. #109 carries `ready-for-agent` while its body says the label is withheld; #91 to #99 correctly lack the label. Label/body mismatch recorded as a fact.
13. #117 to #123: meta items, outside every candidate scope by definition.

## 7. Not verified

- **Private SW state.** #109, #110, #96 depend on a private handoff note in the `wiki` project. Not read; "Basic Memory query" was not attempted.
- **GitHub native blocked-by relationships** were not queried. "Blocked by" is taken from issue body text only.
- **Bodies truncated in this pass.** For #2, #42, #55, #79, #90, #105, #109 and #71 only the first ~2,500 characters were read; sections beyond that (for example the full #90 user stories, the #2 decision list, the rest of #109's strands) could add dependencies not listed here.
- **Issues not read:** #43, #89, #84, #85 (referenced by open items; none appears in the open list; their state was not checked). #61 is a closed PR and #62 a closed issue; whether #61 was merged was not checked.
- **Comments** on all issues and on PRs were not read; decisions recorded only in comments (for example #79 comment 6179364318 and #109 owner comments) are not reflected.
- **Skill assignment by name.** Ten skills are stubs whose body is one line; their scope is inferred from the directory name only, or marked "none".
- **Skill content depth.** Only frontmatter and the first lines of each `SKILL.md` and `grep` of cross-references were read; full bodies of the long skills were not.
- **Local `worktree-agent-*` branches:** names counted only; contents not inspected.
- **Branch skill sets** other than the diffs listed (`seam-adapter`, `knowledge-run-audit`, edits to the three knowledge skills) were not enumerated for `feat/109-tracking-and-wizard` and `feat/ss-seam-rc-mode`.
- **No tests were run.** Test counts quoted by PR bodies (158, 172, 74) are the PR authors' statements.
