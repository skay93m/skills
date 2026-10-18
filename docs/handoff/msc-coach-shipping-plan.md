# Handoff: shipping msc-coach skills

Written 2026-10-18 at the end of a grill-with-docs and to-tickets session. Nothing has been implemented.

## Status

- The plan is agreed and ticketed. Parent: #146 "Ship msc-coach skills v1". Sub-issues: #147 to #154.
- Work starts only when the human says the msc-coach agent is ready. That signal is the human telling the skills agent, in conversation.
- The only ticket that can start before the signal is #147 (glossary). `GLOSSARY.md` has not been touched.
- Branch `refactor-ask-syafiq` was merged into `main` by the human. The local checkout may still be on that branch; switch to `main` and fetch before branching.

## Goal

Ship the finalised skills from the source repository `skay93m/msc-coach` into this repo so they install through `npx skills add skay93m/skills`. msc-coach is where the skills are developed. This repo only ships them. The human runs msc-coach sessions from the workspace using only the skills installed through `npx`.

## Decisions

- Out of scope: `mhel-coaching` workspace detection.
- `ask-syafiq` routing and count changes wait for the msc-coach skill manifest (#154). The "8 repositories" and "6 modules" counts, and the 100-line and 700-token budgets, are handled there.
- Copy from a pinned msc-coach commit on its GitHub `origin/main`, not from the local working tree at `../msc-coach`. Record the SHA on #146 and in the PR body.
- Use a fresh branch from `origin/main`, one PR, and the coordinator protocol (`docs/agents/coordinator-protocol.md`).
- Never overwrite an existing skill directory.
- Keep provenance and version fields. Fix only what the standard check flags. Report repo-side fixes back to msc-coach (#153).
- Gate: `python3 scripts/check-standard.py --base origin/main` shows 0 blocking and 0 non-blocking findings, and `pytest` passes. The `npx skills add skay93m/skills` check runs after merge, because it installs from the default branch.
- On the ready signal, count the skills myself. If the count is not 22 or `ask-coach` is missing, halt and report.
- No ADR: the decisions are easy to reverse.
- `docs/authorised-skill-repositories.md` does not apply. msc-coach is a source repo, not a third-party Authorised Skill Repository.

## Collision protocol

- A collision is an exact name match or a functional overlap. Report all of them to the human before anything is copied.
- Default resolution order: extend the existing skill, then merge and synthesise, then rename only if the two are functionally distinct. The human approves each case.
- The skills agent implements any change in this repo. msc-coach changes only msc-coach, and may propose and negotiate on #146.
- Non-colliding skills ship first (#150). Colliding ones follow after resolution (#151).
- Already suspected: msc-coach `academic-thinking-partner` overlaps this repo's `thinking-partner` and `academic-scholar`. The latter already adapts `thinking-partner`. Relay this to msc-coach early.

## Facts observed (2026-10-18)

- `../msc-coach/skills/` held 17 skills, not 22, so the finalised set is not there yet: academic-compaction, academic-review, academic-thinking-partner, active-retrieval, adversarial-examiner, analytical-read, blueprint, coach-orientation, coaching, final-audit, preview, session-end, session-start, slice-tickets, source-discover, supervision, syntopical-map.
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

## Merge policy (decided by the human)

- The agent may merge its own PRs, but only after it has spawned two adversarial reviewer subagents that each invoke `/code-review` on the PR, one on the Spec axis and one on the Standards axis, and every finding is resolved or explicitly dismissed.
- Mentioning `/code-review` in the policy is not a request to run it now. Run it per PR, at merge time.
- The permission classifier blocked a create-and-squash-merge earlier ("Merge Without Review"). The human has since added the `Bash(gh pr merge:*)` allow rule. The classifier is separate from the allow list and may still block a merge. If it does, stop and ask the human; do not work around it.
