# Handoff: shipping msc-coach skills

Written 2026-10-18 at the end of a grill-with-docs and to-tickets session.

## Status

- #147 is implemented and reviewed on PR #155. Nothing from #148 onward has started.
- The plan is agreed and ticketed. Parent: #146 "Ship msc-coach skills v1". Sub-issues: #147 to #154.
- Work from #148 waits for the human's explicit ready signal, given in conversation to the skills agent. Do not infer it from msc-coach's repository state.
- Branch `refactor-ask-syafiq` was merged into `main` by the human. The local checkout may still be on that branch; switch to `main` and fetch before branching.
- #146 label swapped from `needs-triage` to `ready-for-human`. Done.
- Glossary terms **Source repository** and **Collision** are written in `GLOSSARY.md` (landing in PR #155). #147 closes when that PR merges.

## Goal

Ship the finalised skills from the source repository `skay93m/msc-coach` into this repo so they install through `npx skills add skay93m/skills`. msc-coach is where the skills are developed. This repo only ships them. The human runs msc-coach sessions from the workspace using only the skills installed through `npx`.

## Override of the coordinator protocol

Authorised by the human on 2026-10-18, for this plan only. It overrides Phase 6 of `docs/agents/coordinator-protocol.md`.

- All tickets #148 to #154 land as reviewed commits on PR #155, one integration PR, not one PR per ticket. PR #155 stays a draft until all its tickets are done.
- The agent does not merge PR #155. The human merges it once, because it lists collision decisions for approval.
- `--admin` and any other bypass are never used.
- Each ticket still gets the Spec and Standards adversarial reviews per Phases 3 and 4 of the protocol. Each reviewer posts its verdict as a PR comment whose first line is `<!-- adversarial-review: axis=<spec|standards> verdict=<pass|fail> sha=<head sha> -->`. Any new commit voids earlier verdicts.
- Shipping gate for this PR (a project criterion): `python3 scripts/check-standard.py --base origin/main` prints 0 blocking and 0 non-blocking findings, and `pytest` passes.

## Decisions

- Out of scope: `mhel-coaching` workspace detection.
- `ask-syafiq` routing and count changes wait for the msc-coach skill manifest (#154). The "8 repositories" and "6 modules" counts, and the 100-line and 700-token budgets, are handled there.
- Copy from a pinned msc-coach commit on its GitHub `origin/main`, not from the local working tree at `../msc-coach`. Record the SHA on #146 and in the PR body.
- Use one integration branch, `feat-msc-coach-shipping-plan` (PR #155), for every ticket.
- A msc-coach copy never replaces an existing skill directory. Extending or merging edits the existing skill in place via a reviewed change.
- Keep provenance and version fields. Fix only what the standard check flags. Report repo-side fixes back to msc-coach (#153).
- On the ready signal, count the skills myself. If the count is not the 22 stated in the msc-coach agent's ready message, or `ask-coach` is missing, halt and report.
- No ADR: the decisions are easy to reverse.
- `docs/authorised-skill-repositories.md` does not apply. msc-coach is a source repo, not a third-party Authorised Skill Repository.

## Collisions

- A collision is an exact name match or a functional overlap. Nothing is copied before the ready signal.
- After the ready signal, the agent applies the default resolution: try extend first, then merge and synthesise. Rename only for a pure name collision (an exact name match with no functional overlap). The agent lists every decision at the top of the PR body for the human to review at merge. This governs #149. #149 stays ready-for-human only for that review.
- msc-coach changes only msc-coach, and may propose and negotiate on #146. Every change in this repository is implemented by the skills agent.
- Non-colliding skills ship first (#150). Colliding ones follow after resolution (#151).
- Overlap suspicion (unverified): the 2026-10-18 snapshot listed `academic-thinking-partner`, which may overlap `thinking-partner` and `academic-scholar`. That name is gone from the later local tree, so recheck at #148 against the pinned SHA.

## npx checks

- #152 is verified before merge from the branch ref: `npx skills add skay93m/skills#<branch> --list` (verified 2026-10-18). The human's post-merge `npx skills add skay93m/skills` run is a final confirmation.
- #154 lands on PR #155 once the msc-coach manifest exists.

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
