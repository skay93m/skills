---
title: Automated Checks
tags: [standards, checks, automation, scripts, verification, staged-verification]
type: standard
---

# Automated Checks

Standard: `sk-pr-review-standard`, version `1.0.0-draft`. Mechanical checks run as Stage 1 deterministic checks on every pull request and local iteration, gating Stage 2 advisory reviews. Sourcery and adversarial LLM subagents retain qualitative checks requiring judgement.

- Script: `scripts/check-standard.py` (Python standard library only).
- Test Runner: `pytest` or `python3 -m unittest discover -s tests`.
- Workflow: `.github/workflows/standard-checks.yml`, executed on pull requests to `main`.
- Tests: `tests/test_check_standard.py`.

## How It Behaves in Tiered Staged Verification

- **Stage 1 Gate**: `scripts/check-standard.py` and unit tests execute first. If any blocking check fails, the pipeline halts immediately and reports failure logs. Zero LLM review agents are dispatched.
- **Diff-Scoping**: The script compares the pull request with its base ref and scans only added lines. Pre-existing issues in untouched lines are not reported.
- **Severity Annotations**: Each finding produces an annotation on the exact file and line, labelled `BLOCKING [ID]` or `NON-BLOCKING [ID]`. A blocking finding produces an error annotation and an exit code of 1.
- **Skill Checks**: Evaluates skills added or edited in the pull request. S2 (naming) applies when a skill is new or its name changes. S4 (100 lines) applies when a skill is new or lines are added to a file already over 100 lines.
- **Exemptions**: The checker and its tests quote search patterns and are exempt from pattern checks. Any modification to them, this document, or workflow files is reported as `[STD]`.

## Checks

| ID | Severity | What it finds |
|---|---|---|
| H1 | Blocking | A secret or password value, a key block, a known token format, or a committed credential file |
| H2 | Blocking | A link or permalink into the owner's private notes |
| H3 | Blocking | An email address not already in the base branch (example domains exempt), or a phone number in international, US, or UK format |
| H4 | Blocking | A local user home path |
| H6 | Blocking | An internal host (with or without a scheme), a private IPv4 or IPv6 address, or a private session link |
| STD | Non-blocking | A change to the standard, to `.sourcery.yaml`, or to this checker, its tests, or workflow |
| C5 | Blocking or non-blocking | A change to agent configuration; blocking when it adds a hook, command, tool, or permission |
| C1 | Blocking | A mount of the Docker socket |
| C2 | Blocking | A download piped into a shell |
| C3 | Blocking | A write to a shell profile or to ssh or cloud credential folders |
| C6 | Non-blocking | A package installed without an exact version |
| C7 | Blocking or non-blocking | A third-party action pinned by tag or branch (blocking), or a GitHub-owned one (non-blocking) |
| C8 | Blocking | Text an outsider controls placed directly in a workflow script, or passed to `eval` |
| S1 to S6 | Blocking | Skill frontmatter, name, description, length, nested references, and provenance |
| N5 | Non-blocking | `metadata.category` is missing |
| CUR | Non-blocking | The stamp's fresh-until date has passed |

## Known Limits

Pattern checks are heuristics. Unusual phone numbers or esoteric secret formats can slip through; GitHub secret scanning with push protection provides vendor coverage. Secret assignments are flagged when values are quoted, are 16 or more characters, or contain digits, capitals, or symbols.

## What Stays with Advisory Review (Stage 2)

Advisory reviewers (Sourcery and adversarial subagents) retain judged checks: description quality (N2), overlap with authorised upstream skills (N7), hidden or injected instructions (C4), and context cost (O1 to O5). Hard-stop H5 (pasted prompts and transcripts) is also evaluated in Stage 2 because patterns cannot reliably separate them from legitimate documentation.

## Style and Presentation Standard

Deterministic and advisory checks enforce repository style invariants:
- **British English**: Consistent spelling across all documents and identifiers.
- **Strictly Zero Em Dashes**: Prohibit em dashes across all documentation.
- **Strictly Zero Body Horizontal Dividers**: Prohibit horizontal rules in markdown bodies.

## Observations
- [standard] Codify Stage 1 deterministic checks for sk-pr-review-standard #standards #automation
- [tiering] Stage 1 deterministic checks gate Stage 2 qualitative advisory reviews #staged-verification
- [style] Enforce British English, zero em dashes, and zero body horizontal dividers #style

## Relations
- implements [[pr-review-standard]]
- relates_to [[coordinator-protocol]]
- aligns_with [[GLOSSARY]]
