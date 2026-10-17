# Lint model

## Finding fields (recorded in the run note, `## Lint Operation`)
| Field | Rule |
|---|---|
| `finding_id` | `<run-id>-LF<seq>`, identifies one occurrence |
| `recurrence_key` | slug or hash of `check:target_entity:rule_key`; identical across runs for the same problem |
| `check` | `orphan_pages`, `concepts_without_page`, `missing_cross_references`, `contradictions`, `stale_claims`, or a supporting check |
| `disposition` | `open`, `repaired`, `deferred`, `escalated`; `dismissed` only by a person |
| `decided_by` | the run ID for an automatic repair |
| `target` | permalink of the note concerned |
| `themed_issue_pointer` | `operations/issues/<theme-key>` for escalated findings |

Disposition values are fixed at run time. Later decisions live in the themed issue note, never in the run note.

## Repair table
| Check | Automatic | Action |
|---|---|---|
| `orphan_pages` | yes | guarded typed relation + guarded index entry; return a log line for the orchestrator's single run log entry |
| `concepts_without_page` | yes | minimal stub by exclusive-create, `derived_from` its source |
| `missing_cross_references` | yes | reciprocal link |
| `contradictions` | no | additive `[issue]` observation, escalate |
| `stale_claims` | no | additive `[issue]` observation, escalate |

An `[issue]` observation looks like `- [issue] contradiction: <short neutral description> (run: [[<run-id>]])`. It states what was observed with hedged wording and never asserts which side is right.

## Themed issue notes
- Path `operations/issues/<theme-key>`; the key is a short kebab-case theme (for example `contradictions`, `stale-claims`, `schema-drift`, `missing-index-policy`).
- First occurrence: exclusive-create. Later occurrences: presence check on the `recurrence_key`, then one guarded appended line anchored on text read in the same run.
- Human decisions are written in the themed note by a person.
- The latest-run listing of `operations/` excludes this subfolder.

## Duplicate deletion checks
Compare normalised bodies (frontmatter excluded) for notes from the same source. The ratio must be computed by a real tool; if none is available, defer the deletion and never estimate a score. At a ratio of 0.95 or more [proposal], keep the canonical note, make sure the other note's incoming relations reach the canonical one, record `similarity_score`, re-read the checksum immediately before deleting, delete only if it equals the recorded `before_checksum`, and record it. Below 0.95, raise a deferred finding.

A fixture is a note with no substantive body that is zero-byte or has unparseable frontmatter. A note with body content and bad frontmatter or a schema failure gets a structural repair or a finding, never a deletion.

## Order of work
Check the changed notes first, then the oldest queued concerns, within the budget. A failed item never blocks unrelated checks. Incomplete reads block any claim of completeness.
