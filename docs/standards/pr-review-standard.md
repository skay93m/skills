---
title: Pull Request Review Standard
tags: [standards, review, pr, sourcery, quality, staged-verification]
type: standard
---

# Pull Request Review Standard

The canonical statement of `sk-pr-review-standard` for this repository. Tiered staged verification separates mechanical checks executed by deterministic scripts from qualitative checks evaluated by advisory reviewers (Sourcery and adversarial LLM subagents). The repository owner decides every merge.

## Identity

| Field | Value |
|---|---|
| `standard_id` | `sk-pr-review-standard` |
| `version` | `1.0.0-draft` |
| `status` | draft |
| Last reviewed | 2026-10-10 (set by the owner only) |
| Freshness period | one month (ISO 8601 `P1M`) |
| Fresh until | 2026-11-10 |
| Canonical location | this file, `docs/standards/pr-review-standard.md` |

Only the owner sets or changes the review date. An agent may point out that the freshness period has lapsed, but never refreshes the date.

## Purpose and Scope

- Verification follows a tiered staged structure:
  - **Stage 1 (Deterministic Checks)**: Automated scripts (`scripts/check-standard.py`, `pytest`) run first. Any failure immediately stops the gate without invoking LLM or advisory reviewers.
  - **Stage 2 (Advisory and Adversarial Reviews)**: Sourcery and specialised adversarial review subagents evaluate specification compliance, architecture, and code quality.
- Sourcery acts as an advisory reviewer. It recommends approve, comment, or request changes, explains its reasoning, and names exact findings. It never merges, and the owner has the final decision on every merge.
- The implementation covers this repository. A review covers the diff and the repository context it touches. It is not an audit of the whole repository.
- Existing problems in lines a pull request does not touch are not reported.
- The quality bar is identical whether an agent, the owner, or both authored the change.

## The Stamp

Each Sourcery review rule opens with this line:

`Standard sk-pr-review-standard v<version>, reviewed <date>, fresh until <date>.`

The stamp enables a review to declare which version of the standard it used. Sourcery quotes only the check that matched, so the stamp line itself does not appear in comments; the check ID does. The stamp in the dashboard must match the version in this file.

## Versioning

- **Major**: A blocking check is added, removed, or loosened.
- **Minor**: Non-blocking checks change.
- **Patch**: Wording only.
- A change that only describes repository settings or process, and changes no check, does not change the version.

Every version bump requires the owner's approval and a new review date.

## Currency Findings

| Finding | Severity |
|---|---|
| A missing or malformed stamp | Blocking |
| A stamp whose version differs from this file | Blocking |
| A lapsed freshness period | Non-blocking, with a comment recommending a re-review (check `CUR`) |
| A pull request that edits the standard, its checker, its tests, or its workflow | Non-blocking (check `STD`) |

## Findings and the Verdict

Every finding has a label and a check ID, in the form `BLOCKING [S4]` or `NON-BLOCKING [N2]`, and gives the file, the line, and a reason. The labels are text. They are not an automated merge block.

The owner maps them to a verdict:
- Any blocking finding: request changes.
- Only non-blocking findings: comment.
- No findings: approve, as the owner's decision.
- Insufficient evidence for a confident call: comment only.

Sourcery's setting to approve pull requests is active, and its approval is its own judgement. A blocking label does not stop it from approving, so the owner reads findings before every merge. GitHub auto-merge is disabled, and a ruleset on `main` requires a pull request with one approval. When Sourcery withholds approval, merging requires the owner's bypass, which is exceptional. To hand blocking findings to an agent, use `docs/standards/repair-prompt-template.md`.

## Hard-Stops

All seven are blocking, even in advisory mode.

| ID | Hard-stop |
|---|---|
| H1 | Secrets: keys, tokens, passwords, private keys, committed credential files |
| H2 | Links or permalinks into the owner's private notes, or pasted note bodies |
| H3 | Personal information (email addresses, phone numbers, account IDs) not already public in this repository |
| H4 | Local paths that name a user or a machine |
| H5 | Pasted system prompts, handoff text, or agent or session transcripts |
| H6 | Internal hosts, private network addresses, or private session links |
| H7 | An unresolved security finding from any reviewer, or a description that admits one |

## Style and Presentation Standard

Every pull request must conform to repository style rules:
- **British English**: All prose, identifiers, and documentation must use British English spelling (prioritise, behaviour, organisation, synthesise, artefact).
- **Strictly Zero Em Dashes**: Never use em dashes. Use commas, colons, or parentheses.
- **Strictly Zero Body Horizontal Dividers**: Never insert horizontal rules in markdown bodies (only YAML frontmatter delimiters are permitted).

## Pocock Skill Filter

Reviewers apply the Pocock Skill Filter to every added or changed skill. A skill that fails a pillar is a candidate for rejection or for an Overlay (see `GLOSSARY.md`).

- **Behavioural Delta**: The skill must change what a capable model does by default. Generic instructions the model already follows are a no-op and are rejected.
- **Upstream Overlap**: The skill must not duplicate an authorised upstream skill. Where upstream covers the need, use it unchanged and keep only the delta.
- **What We Care About**: The skill must encode Syafiq's own taste, doctrine, or non-default constraints that nobody else can supply.

## Check Registry

"Script" is `scripts/check-standard.py` (see [automated-checks.md](automated-checks.md)). "Sourcery" means a dashboard review rule (see [sourcery-rules.md](sourcery-rules.md)). "Owner" means the owner's own review.

| ID | What it checks | Severity | Where |
|---|---|---|---|
| H1 to H4, H6 | The hard-stops above that a pattern can find | Blocking | Script |
| H5, H7 | Pasted prompts and transcripts; open security findings | Blocking | Owner and Sourcery |
| STD | A change to the standard, its checker, tests, or workflow | Non-blocking | Script |
| CUR | The stamp's fresh-until date has passed | Non-blocking | Script |
| S1 | Frontmatter holds `name` and `description` | Blocking | Script |
| S2 | Name is kebab-case, at most three words, equals its directory, no "anthropic" or "claude" | Blocking | Script |
| S3 | Description at most 1,024 characters, has a "Use when" clause, no first or second person | Blocking | Script |
| S4 | `SKILL.md` at most 100 lines | Blocking | Script |
| S7 | `SKILL.md` estimated strictly under 700 tokens (characters divided by 4) | Blocking | Script |
| S5 | A reference file does not link to another reference file | Blocking | Script |
| S6 | Provenance in frontmatter: `metadata.origin`, `metadata.agent_involvement`, and `metadata.divergence` when the origin is an upstream | Blocking | Script |
| N1, N2, N4, N6 | Skill quality: name form, description quality, writing principles, fragile operations | Non-blocking | Sourcery |
| N5 | `metadata.category` is present | Non-blocking | Script |
| N7 | Overlap with an authorised upstream skill | Non-blocking | Sourcery |
| C1 to C3 | Docker socket mount, download piped into a shell, writes outside the repository | Blocking | Script |
| C4 | Hidden or injected instructions in text agents read | Blocking | Sourcery |
| C5 | A change to agent configuration | Blocking when it adds a hook, command, tool, or permission; otherwise non-blocking | Script |
| C6 | A package installed without an exact version | Non-blocking | Script |
| C7 | A third-party action pinned by tag or branch | Blocking (non-blocking for GitHub-owned actions) | Script |
| C8 | Outsider-controlled text used directly in a workflow script or passed to `eval` | Blocking | Script |
| O1 to O5 | Context cost: growth of always-loaded files, duplicated instructions, large default references, scripts that add nothing, generated filler | Non-blocking | Sourcery |

S2 applies when a skill is new or its name changes. S4 applies when a skill is new or a pull request adds lines to a file already over 100 lines.

## Changing the Standard

The standard changes only through a pull request that the owner approves. The checker reports any such change as `STD`, and the owner re-stamps it by setting a new review date and, where needed, a new version.

## Observations
- [standard] Establish canonical sk-pr-review-standard with tiered staged verification #standards #review
- [tiering] Stage 1 deterministic scripts gate Stage 2 qualitative advisory reviews #staged-verification
- [style] Mandate British English, zero em dashes, and zero body horizontal dividers #style

## Relations
- implements [[AGENTS]]
- relates_to [[automated-checks]]
- relates_to [[coordinator-protocol]]
- defines [[GLOSSARY]]
