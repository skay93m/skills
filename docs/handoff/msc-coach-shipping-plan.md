# Handoff: shipping msc-coach skills

Written 2026-10-18 at the end of a grill-with-docs and to-tickets session.

## Status

- #147 is implemented and in review on PR #155 (closes on merge). Nothing from #148 onward has started.
- Parent: #146 "Ship msc-coach skills v1". Sub-issues: #147 to #154.
- Branch `refactor-ask-syafiq` was merged into `main` by the human. Switch to `main` and fetch before branching.

## Goal

Ship the finalised skills from the Source repository `skay93m/msc-coach` into this repo so they install through `npx skills add skay93m/skills`. msc-coach is where the skills are developed. This repo only ships them.

## Override of the coordinator protocol

Authorised by the human on 2026-10-18, for this plan only. It overrides Phase 6 of `docs/agents/coordinator-protocol.md`.

- All of #148-#154 land as reviewed commits on PR #155, kept as a draft until all are done. There is no separate PR per ticket.
- The agent never merges PR #155. The human merges it once, because it lists Collision decisions for approval.
- `--admin` and any other bypass are never used.
- Work from #148 waits for the human's explicit ready signal. Do not infer it from msc-coach's repository state.
- Collision decisions are listed at the top of the PR body and applied only after the ready signal.

## Review marker

Each reviewer's PR comment has the first line `<!-- adversarial-review: axis=<spec|standards> verdict=<pass|fail> sha=<head sha> -->`. Any new commit voids earlier verdicts.

## Shipping gate

For the msc-coach shipping PR (a project criterion): `python3 scripts/check-standard.py --base origin/main` prints 0 blocking and 0 non-blocking findings, and `pytest` passes.

## Tickets

Per-ticket requirements live in issues #146-#154 and their dated decision-update comments; where this note and a ticket differ, the ticket and its latest decision update govern.

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

Dependencies (blocked by) are GitHub native dependencies, except the two external ones (ready signal, manifest), which are written in the ticket bodies.

Note: #147 is implemented and in review on PR #155; it closes on merge.

## Facts

- Overlap suspicion (unverified): the 2026-10-18 snapshot listed `academic-thinking-partner`, which may overlap `thinking-partner` and `academic-scholar`. That name was gone from a later local tree.
- Glossary precedent: a skill here that overlaps an Authorised upstream skill should extend it and record how it differs.
