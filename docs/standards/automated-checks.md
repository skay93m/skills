# Automated checks

Standard: `sk-pr-review-standard`, version `1.0.0-draft`. The mechanical checks of the standard run as a script on every pull request, so they do not depend on Sourcery's review rules. Sourcery keeps the checks that need judgement.

- Script: `scripts/check-standard.py` (Python standard library only).
- Workflow: `.github/workflows/standard-checks.yml`, run on pull requests to `develop` and `main`.
- Tests: `tests/test_check_standard.py`. Run them with `python3 -m unittest discover -s tests`.

## How it behaves

- It compares the pull request with its base and scans only the lines the pull request adds. Older problems in untouched lines are not reported.
- Each finding is an annotation on the exact file and line, labelled `BLOCKING [ID]` or `NON-BLOCKING [ID]`. A blocking finding makes the check red.
- The check is informational. The ruleset does not require it, so a red check never stops a merge. The owner reads the findings and decides.
- Skill checks run on skills the pull request adds or edits. S2 (name) applies when the skill is new or its name changes. S4 (100 lines) applies when the skill is new or the pull request adds lines to a file already over 100 lines.
- The checker and its tests quote the patterns they search for, so they are exempt from the pattern checks. Any change to them, to this document, or to the workflow is reported as `[STD]` so the owner reviews it in person.

## Checks

| ID | Severity | What it finds |
|---|---|---|
| H1 | Blocking | A secret or password value, a key block, a known token format, or a committed credential file |
| H2 | Blocking | A link or permalink into the owner's private notes |
| H3 | Blocking | An email address not already in the base branch, or a phone number |
| H4 | Blocking | A local user home path |
| H6 | Blocking | An internal host, a private network address, or a private session link |
| STD | Blocking | A change to the standard, to `.sourcery.yaml`, or to this checker, its tests or workflow |
| C5 | Blocking or non-blocking | A change to agent configuration; blocking when it adds a hook, command, tool or permission |
| C1 | Blocking | A mount of the Docker socket |
| C2 | Blocking | A download piped into a shell |
| C3 | Blocking | A write to a shell profile or to ssh or cloud credential folders |
| C6 | Non-blocking | A package installed without an exact version |
| C7 | Blocking or non-blocking | A third-party action pinned by tag or branch (blocking), or a GitHub-owned one (non-blocking) |
| C8 | Blocking | Text an outsider controls placed directly in a workflow script, or passed to `eval` |
| S1 to S6 | Blocking | Skill frontmatter, name, description, length, nested references and provenance |
| N5 | Non-blocking | `metadata.category` is missing |
| CUR | Non-blocking | The stamp's fresh-until date has passed |

## What stays with Sourcery

Sourcery's review rules keep the judged checks: description quality (N2), overlap with authorised upstream skills (N7), hidden or injected instructions (C4), and context cost (O1 to O5). Hard-stop H5 (pasted prompts and transcripts) is also left to Sourcery and to the owner, because a pattern cannot tell them apart from normal text.

GitHub secret scanning with push protection is on for this repository and blocks pushes that contain known secret formats.
