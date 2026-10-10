# Pull request review standard

The canonical statement of `sk-pr-review-standard` for this repository. The mechanical checks run as a script on every pull request, Sourcery's review rules keep the checks that need judgement, and the repository owner decides every merge.

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

## Purpose and scope

- Sourcery acts as an advisory reviewer. It recommends approve, comment or request changes, explains its reasoning and names exact findings. It never merges, and the owner has the final say on every merge.
- The first implementation covers this repository. A review covers the diff and the repository context it touches. It is not an audit of the whole repository.
- Existing problems in lines a pull request does not touch are not reported.
- The quality bar is the same whether an agent, the owner or both wrote the change.

## The stamp

Each Sourcery review rule opens with this line:

`Standard sk-pr-review-standard v<version>, reviewed <date>, fresh until <date>.`

The stamp lets a review say which version of the standard it used. Sourcery quotes only the check that matched, so the stamp line itself does not appear in its comments; the check ID does. The stamp in the dashboard must match the version in this file.

## Versioning

- **Major**: a blocking check is added, removed or loosened.
- **Minor**: non-blocking checks change.
- **Patch**: wording only.
- A change that only describes repository settings or process, and changes no check, does not change the version.

Every bump needs the owner's approval and a new review date.

## Currency findings

| Finding | Severity |
|---|---|
| A missing or malformed stamp | Blocking |
| A stamp whose version differs from this file | Blocking |
| A lapsed freshness period | Non-blocking, with a comment recommending a re-review (check `CUR`) |
| A pull request that edits the standard, its checker, its tests or its workflow | Blocking until the owner re-stamps it (check `STD`) |

## Findings and the verdict

Every finding has a label and a check ID, in the form `BLOCKING [S4]` or `NON-BLOCKING [N2]`, and gives the file, the line and a reason. The labels are text. They are not a merge gate.

The owner maps them to a verdict:

- Any blocking finding: request changes.
- Only non-blocking findings: comment.
- No findings: approve, as the owner's decision.
- Not enough evidence for a confident call: comment only.

Sourcery's setting to approve pull requests is on, and its approval is its own judgement. A blocking label does not stop it from approving, so the owner reads the findings before every merge. GitHub auto-merge is off, and a ruleset on `develop` and `main` requires a pull request with one approval. Sourcery's approval satisfies that requirement, so a pull request Sourcery approves can be merged normally. The owner is the only person who merges, and reads the findings first. When Sourcery withholds approval, merging needs the owner's bypass, which is exceptional. To hand blocking findings to an agent, use [repair-prompt-template.md](repair-prompt-template.md).

## Hard-stops

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

## Check registry

"Script" is `scripts/check-standard.py` (see [automated-checks.md](automated-checks.md)). "Sourcery" means a dashboard review rule (see [sourcery-rules.md](sourcery-rules.md)). "Owner" means the owner's own review.

| ID | What it checks | Severity | Where |
|---|---|---|---|
| H1 to H4, H6 | The hard-stops above that a pattern can find | Blocking | Script |
| H5, H7 | Pasted prompts and transcripts; open security findings | Blocking | Owner and Sourcery |
| STD | A change to the standard, its checker, tests or workflow | Blocking | Script |
| CUR | The stamp's fresh-until date has passed | Non-blocking | Script |
| S1 | Frontmatter holds `name` and `description` | Blocking | Script |
| S2 | Name is kebab-case, at most three words, equals its directory, no "anthropic" or "claude" | Blocking | Script |
| S3 | Description at most 1,024 characters, has a "Use when" clause, no first or second person | Blocking | Script |
| S4 | `SKILL.md` at most 100 lines | Blocking | Script |
| S5 | A reference file does not link to another reference file | Blocking | Script |
| S6 | Provenance in frontmatter: `metadata.origin`, `metadata.agent_involvement`, and `metadata.divergence` when the origin is an upstream | Blocking | Script |
| N1, N2, N4, N6 | Skill quality: name form, description quality, writing principles, fragile operations | Non-blocking | Sourcery |
| N5 | `metadata.category` is present | Non-blocking | Script |
| N7 | Overlap with an authorised upstream skill | Non-blocking | Sourcery |
| C1 to C3 | Docker socket mount, download piped into a shell, writes outside the repository | Blocking | Script |
| C4 | Hidden or injected instructions in text agents read | Blocking | Sourcery |
| C5 | A change to agent configuration | Blocking when it adds a hook, command, tool or permission; otherwise non-blocking | Script |
| C6 | A package installed without an exact version | Non-blocking | Script |
| C7 | A third-party action pinned by tag or branch | Blocking (non-blocking for GitHub-owned actions) | Script |
| C8 | Outsider-controlled text used directly in a workflow script or passed to `eval` | Blocking | Script |
| O1 to O5 | Context cost: growth of always-loaded files, duplicated instructions, large default references, scripts that add nothing, generated filler | Non-blocking | Sourcery |

S2 applies when a skill is new or its name changes. S4 applies when a skill is new or a pull request adds lines to a file already over 100 lines.

## Changing the standard

The standard changes only through a pull request that the owner approves. The checker reports any such change as `STD`, and the owner re-stamps it by setting a new review date and, where needed, a new version.
