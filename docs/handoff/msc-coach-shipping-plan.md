# Handoff: shipping msc-coach skills

Written 2026-10-18 at the end of a grill-with-docs and to-tickets session. #147 is implemented and reviewed on PR #155; nothing from #148 onward has started.

## Status

- The plan is agreed and ticketed. Parent: #146 "Ship msc-coach skills v1". Sub-issues: #147 to #154.
- Work starts only when the human says the msc-coach agent is ready. That signal is the human telling the skills agent, in conversation.
- The only ticket that can start before the signal is #147 (glossary). The glossary terms land in PR #155.
- Branch `refactor-ask-syafiq` was merged into `main` by the human. The local checkout may still be on that branch; switch to `main` and fetch before branching.

## Goal

Ship the finalised skills from the source repository `skay93m/msc-coach` into this repo so they install through `npx skills add skay93m/skills`. msc-coach is where the skills are developed. This repo only ships them. The human runs msc-coach sessions from the workspace using only the skills installed through `npx`.

## Decisions

- Out of scope: `mhel-coaching` workspace detection.
- `ask-syafiq` routing and count changes wait for the msc-coach skill manifest (#154). The "8 repositories" and "6 modules" counts, and the 100-line and 700-token budgets, are handled there.
- Copy from a pinned msc-coach commit on its GitHub `origin/main`, not from the local working tree at `../msc-coach`. Record the SHA on #146 and in the PR body.
- Use one integration branch, `feat-msc-coach-shipping-plan` (PR #155), for every ticket, and the coordinator protocol (`docs/agents/coordinator-protocol.md`).
- A msc-coach copy never replaces an existing skill directory. Extending or merging edits the existing skill in place via a reviewed change.
- Keep provenance and version fields. Fix only what the standard check flags. Report repo-side fixes back to msc-coach (#153).
- Shipping gate: for the msc-coach shipping PR, a project criterion (not a pre-existing rule), `python3 scripts/check-standard.py --base origin/main` must print 0 blocking and 0 non-blocking findings, and `pytest` must pass. These are the script's findings, separate from reviewer NON-BLOCKING notes. Phase 6 step 1 of `docs/agents/coordinator-protocol.md` lists the commands.
- On the ready signal, count the skills myself. If the count is not the 22 stated in the msc-coach agent's ready message, or `ask-coach` is missing, halt and report.
- No ADR: the decisions are easy to reverse.
- `docs/authorised-skill-repositories.md` does not apply. msc-coach is a source repo, not a third-party Authorised Skill Repository.

## Collision protocol

- A collision is an exact name match or a functional overlap. Collision decisions are listed at the top of the PR body before the batch is marked ready. Nothing is copied before the ready signal.
- After the human's ready signal for #148, the agent applies the default resolution order (authorised 2026-10-18). Before that signal, nothing from #148 onward starts. Order: try extend first, then merge and synthesise; rename applies only when the two skills are functionally distinct (a pure name clash). The human approves each case by reviewing the PR body list at merge. PR #155 is held for the human, per the protocol's Phase 6.
- msc-coach changes only msc-coach, and may propose and negotiate on #146. Every change in this repository is implemented by the skills agent.
- Non-colliding skills ship first (#150). Colliding ones follow after resolution (#151).
- Overlap suspicion (unverified): the 2026-10-18 snapshot listed `academic-thinking-partner`, which may overlap `thinking-partner` and `academic-scholar`. That name is gone from the later local tree, so recheck at #148 against the pinned SHA.

## Facts observed (2026-10-18)

- Snapshots of `../msc-coach/skills/` change as msc-coach evolves. An early one held 17 skills, a later one 21 (e.g. debrief, park, quiz, recall, think, viva-draft, viva-idea, compact-academic, supervision-debrief, supervision-prep), neither 22. Do not rely on either; count the pinned SHA at #148.
- `ask-coach` was not among them.
- No exact directory-name collisions with this repo's 38 skills at that time.
- Glossary precedent: a skill here that overlaps an Authorised upstream skill should extend it and record how it differs.

## Tickets

| # | Ticket | Label | Blocked by |
|---|---|---|---|
| 147 | Glossary: Collision and Source repository | ready-for-agent | none |
| 148 | Pre-flight check on msc-coach ready signal | ready-for-human | the human ready signal |
| 149 | Resolve collisions with msc-coach | ready-for-human | 148 |
| 150 | Ship the non-colliding msc-coach skills | ready-for-agent | 148 |
| 151 | Ship the held-back colliding skills | ready-for-agent | 149, 150 |
| 152 | Verify installation through npx | ready-for-human | 150 |
| 153 | Report repo-side fixes back to msc-coach | ready-for-agent | 150 |
| 154 | Update ask-syafiq routing and counts | ready-for-human | 150 and the msc-coach manifest |

Blocking edges are GitHub native dependencies, except the two external ones (ready signal, manifest), which are written in the ticket bodies.

## Resolved open items

- #146 label swapped from `needs-triage` to `ready-for-human`. Done.
- Glossary terms **Source repository** and **Collision** are written in `GLOSSARY.md` (landing in PR #155). #147 closes when that PR merges.

## One-PR delivery and merge (decided by the human, 2026-10-18)

- All tickets land as commits on PR #155, which stays a draft until its tickets are done.
- #149 collision decisions follow the Collision protocol above. The human approves them by reviewing the PR body list at merge.
- #152 is verified before merge from the branch ref: `npx skills add skay93m/skills#<branch> --list` (verified 2026-10-18). The post-merge `npx skills add skay93m/skills` run is a final human confirmation, not a gate on the PR.
- #154 lands on PR #155 once the msc-coach manifest exists.
- Work after #147 waits for the human's explicit ready signal. Do not infer it from msc-coach's repository state.

Review, verdict-comment and merge rules: see Phase 3, Phase 4 and Phase 6 of `docs/agents/coordinator-protocol.md`. Do not restate them here.
