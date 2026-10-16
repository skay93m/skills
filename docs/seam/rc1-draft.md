# Seam v0.1.0-rc.1 (draft)

**Draft, not ratified, no tag.** This file drafts what a first release candidate could say. It is not a release candidate, creates no tag and activates no binding. The owner decides whether any of it is adopted. The final ratified `seam-v0.1.0` release and the release of the mutation allowlist are the owner's decisions, not this document's and not an agent's.

## Basis and how to rebase

- Mirrors the seam draft on the `feat/109-go-live` branch at commit `c7efc6581f85aac6e91ff1b684981f6e8daa1242` (it contains the `feat/109-seam` work up to `3441ecf7d7229b7286ba3dfa78816de1bb7d0f7f`). Those files are not on `main` yet: `docs/seam/envelope.md`, `profiles.md`, `terms.md`, `tokens.md`, `profiles/knowledge-ingest-0.1.0.json`, `scripts/seam_conformance.py`, `tests/test_seam_conformance.py`.
- This draft sits beside them without editing them. When those files reach `main`, rebase this branch, then fold the changes in section 8 into `envelope.md` and `profiles.md` and delete the duplicated wording here.
- Profile files here use the same JSON format as `profiles/knowledge-ingest-0.1.0.json` and the suffix `-rc.1` so they do not collide with it.
- Wiki-specific identifiers, checksums, approvals and backend details stay private to the Wiki side. Examples below are synthetic.

## 1. Namespace

`com.syafiqkay.skills`, provisional until the owner confirms or replaces it. Extension keys use it as their reverse-DNS namespace.

## 2. Capability profiles

| Capability | File | Modes | Operation classes |
|---|---|---|---|
| `knowledge.lint` | `profiles/knowledge-lint-0.1.0-rc.1.json` | `report-only`, `propose-only`, `apply` | `read`, `write-report`, `propose-change`, `apply-change`, `delete` |
| `knowledge.ingest` | `profiles/knowledge-ingest-0.1.0-rc.1.json` | `report-only`, `propose-only`, `apply` | `read`, `write-report`, `propose-change`, `apply-change` |

- Both profiles list the unattended mode `apply`. They grant nothing: a run may use a class only when a human-approved grant exists, the mode permits it and the profile allows it.
- Deletion belongs to lint. `knowledge.lint` allows `delete` only so a grant limited to the allowlist in section 5 can exist. `knowledge.ingest` does not offer `delete`. No grant is drafted here.
- Both files declare `seam-versions: ["0.1.0"]` while breaking the 0.1.0 draft rules (see section 8). They are distinguished by file name only, and the capability version stays `0.1.0` because the existing checker accepts only `0.x.y`.
- `backend-constraint-tokens` name promises only (format from `tokens.md`, still "SW input needed"): `bc-exclusive-create`, `bc-expected-checksum`, `bc-readback-after-write`, `bc-no-blind-retry`, `bc-append-only-compile`, `bc-no-stored-trust`, `bc-snapshot-precondition`, and for lint also `bc-deletion-allowlist`. The mapping to a backend stays private.
- `conformance-status` is `not-tested`. `supported-extensions` is empty in this draft.

## 3. Guarded unattended envelope

An `apply` run under these profiles must follow every rule. A request that breaks one gives `status: refused` and `error-category: not-permitted`.

1. **Append-only compile.** Any note type may be compiled, but only by adding. Existing facts and claims are never rewritten. New evidence is added as a challenge or supersession.
2. **Exclusive-create.** A new note is created only if it does not exist. An existing note is never replaced by a create.
3. **Guarded edit.** An edit to an existing note is: read, presence check (skip if already applied), edit with an expected checksum, then readback.
4. **Overwrite is limited.** Only structural lint repairs (fix a link, remove an obsolete field, normalise a heading, repair a relation) may replace text, by guarded narrow edits. A whole-note overwrite is limited to the stale-index rewrite, guarded, keeping every still-valid entry.
5. **Readback.** Every write is read back and compared.
6. **No blind retry.** After a timeout or unclear failure, read the persisted state first. Retry at most once, and only if the change is absent.
7. **Deletion allowlist.** Section 5.
8. **No stored trust or status.** No note carries a trust, confirmation or authority field. Compiled wording is attributed and hedged, with no absolute claims. Operational run status on run records is a technical state, not trust.
9. **Provenance.** Every written note records its author, model and run reference.
10. **Index and log.** The log is append-only, one entry per run, with a presence check. The index is append-only except a guarded stale-index rewrite. If an index or log edit fails after the content write, the run records "index/log pending" and does not retry blindly.
11. **First-run limit.** While the owner's first-run limit holds, the only writes are the run's start marker and run record. The limit lifts when the owner says so or after an audit passes.

Checksums, permalinks and note content never cross the public seam (see the crossing rule in `envelope.md`). The guard values are private; only the tokens in section 2 are public.

## 4. Snapshot precondition

- The backend takes a daily automatic snapshot of the whole store on a published schedule, before the run window. The snapshot name is derived from the UTC date by a rule the Wiki side owns and keeps private.
- A scheduled run starts after the snapshot time plus a safety margin and aborts before any write if the UTC clock is earlier or unavailable. It derives the snapshot name from the UTC date it read, and records it.
- The run cannot create, list or verify snapshots. It must not claim that it did. An independent auditor checks that the snapshot exists and was taken before the run started, and flags the run if it is missing.
- Restoring from a snapshot is never done by a run or an auditor. It is a human action, by path.

## 5. Effective mutation policy

Effective permission = grant AND mode AND profile AND first-run scope. The release of any allowlist is the owner's decision.

| Class | Effective when | Limits |
|---|---|---|
| `read` | granted | none beyond the crossing rule |
| `write-report` | granted | operation records only |
| `propose-change` | granted and mode is `propose-only` or `apply` | additive proposals |
| `apply-change` | granted and mode is `apply` | section 3; first-run scope limit while it holds |
| `delete` (lint only) | granted for an allowlist rule and mode is `apply` | allowlist below only |

Deletion allowlist (each deletion recorded with rule and before-state; similarity score for duplicates only):
- (a) near-duplicate notes at least 95% identical in body, same source, canonical note kept and linked;
- (b) scratch notes created by the same run under a designated `scratch/` folder;
- (c) empty or malformed fixtures.

Everything else is human only: other deletions, restore, dismissing findings, architecture and schema changes, and seam ratification.

## 6. Extension rules

Extensions sit in one container, and an extension is identified by its namespace.

| Case | Outcome |
|---|---|
| Unknown, optional | Ignored. Not an error. |
| Unknown, required | `unsupported`; for rc.1, mapped to `invalid-request` (default applied) |
| Known, required, invalid | `invalid-request` |
| Known, optional, recognised but invalid | `invalid-request` |
| Any extension asks for a lower guarantee | Refused. No silent downgrade. |

An extension may not redefine or shadow a core field, add a vocabulary value or widen a grant. The name and value rules in `envelope.md` section 6 still apply. For rc.1 the container keeps flat `<namespace>.<name>` keys with scalar values; required extensions are deferred.

## 7. Open points, with defaults applied (owner to confirm)

- `unsupported` is not in the closed error-category list. Default applied: it maps to `invalid-request` in rc.1; a new value would be a breaking change.
- Required and optional markers, and a container keyed by namespace, are not in `envelope.md`. Default applied: keep flat scalar keys and defer required extensions.
- `seam_conformance.py` rejects any profile with the `apply` mode or the `apply-change` or `delete` classes, and rejects a `delete` grant. These profiles fail it by design. No test was added or changed.
- An rc suffix on versions is not accepted by the checker. Default applied: keep `0.1.0` values and tell the files apart by name; the checker change belongs on the `feat/109` branches, later.
- First run: default applied, no log or index entry.
- ADR 0002 says the next run aborts when a `-start` has no run note; the decisions record says the run records it and proceeds. This draft and the prompts follow the decisions record. Owner to confirm, and the ADR wording may need amending.
- Schedule in UTC. UK clocks change on 2026-10-25.
- Coordination: if the Wiki side creates schema notes while the first run or its audit window is open, the audit will flag them as unmanifested or out of scope.

## 8. Changes relative to the 0.1.0 draft on `feat/109-go-live`

- Adds `apply` and `apply-change` to the two profiles, and `delete` to the lint profile; the 0.1.0 draft says no profile may open them and no `delete` grant exists.
- Adds the knowledge.lint profile.
- Adds the guarded envelope, snapshot precondition and effective policy above.
- Changes the stance "initial knowledge.ingest is report-only and propose-only". Mutation-enabled execution was to need separate human-approved allowlists and Basic Memory adapter tests.
- Gates before any of this could be treated as a release candidate: an updated conformance suite, adapter tests against the backend, and a separate human release decision. None exists yet.
