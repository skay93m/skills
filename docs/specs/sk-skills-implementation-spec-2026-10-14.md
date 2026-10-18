# sk-skills implementation specification (draft for owner review)

Source: Wayfinder map #79 (`skay93m/syafiq-kay-skills`), decision log comment 6179364318, and the resolution comments on #80 to #88. Date: 2026-10-14.
Status: DRAFT. This document is a specification only. It authorises no implementation.

Note on tooling: the `/to-spec` skill is not installed in this session. This document follows the shape of the existing specs (#42, #49, #50) by judgement, not by template.

## 0. Authority and non-authorisation

- Nothing in this spec authorises code, repository edits, skill installs or removals, worktree changes, Basic Memory or Wiki changes, a release, a tag, an activation, or implementation tickets.
- Syafiq keeps semantic, policy, provenance, deletion, allowlist, merge, release and ratification authority.
- Only explicitly confirmed decisions appear in sections 2 to 5. Anything else is in sections 6 to 9 and labelled.
- Confirmation means a dated quote of Syafiq in chat, recorded on GitHub (P14). Where a ticket records a correction, the re-confirmed text supersedes the earlier one (see section 10).

## 1. Scope and boundary

Two outcomes:

1. Move installation and discovery to a verified, pinned `npx skills` model across Claude, Codex and Antigravity CLI, with bounded retirement of stale installs.
2. Define the public, vendor-neutral seam between SS (sk-skills) and SW (sk-wiki).

SS and SW stay distinct projects. SW-only knowledge-layer decisions stay with SW. Wiki and Basic Memory material was read-only context and stays so.

## 2. Confirmed decisions: contract and ownership

### 2.1 Ownership (C1, #87)

- SS owns the public vendor-neutral seam contract.
- SW owns meaning, policy, the compatibility binding and backend constraints.
- The public contract never defines what knowledge means. It carries opaque references only.
- Syafiq ratifies, releases and keeps deletion authority.
- A role grants no permission.

### 2.2 Envelope (layer 1, C6 to C9, P1, P2, #84)

Every operation report carries:

| Field | Rule |
| --- | --- |
| `seam-version` | Separate machine-readable field. |
| `capability` | Separate field. |
| `capability-version` | Separate field. A combined label such as `knowledge.ingest@0.1.0` may appear in human summaries only. |
| run reference | Opaque, SW-generated per run, not derived from private content. |
| `status` | `succeeded`, `partial`, `failed`, `refused`. |
| `disposition` | `reported`, `proposed`, `applied`, `skipped`. |
| `approval-state` | `not-required`, `pending`, `approved`, `denied`. |
| `error-category` | `invalid-request`, `not-permitted`, `conflict`, `backend-unavailable`, `internal`. Empty when `status` is `succeeded`. |
| counts | Counts only. |
| `mutation-summary` | Counts of requested, granted, applied, refused, per operation class. No targets, no content. |
| extensions | Namespaced, see 2.4. |

- Vocabularies are closed. A new value needs a new seam version. Extensions cannot add values.
- `refused` means the operation was not allowed to run. `failed` means it ran and broke.
- Operation classes are closed: `read`, `write-report`, `propose-change`, `apply-change`, `delete`.
- The public envelope exposes only the run reference, closed values and counts. The full operation-run record stays private in SW.

### 2.3 Grants and mutation (P1, #84; C1, #87)

- A grant is a human-approved allowlist entry for one capability and one operation class.
- A mode, a role or passing tests grants nothing.
- The envelope names a grant only by an opaque grant reference. The grant record (who, when, scope) stays private in SW and in the GitHub approval.
- A request outside a grant gives `status: refused` and `error-category: not-permitted`. It fails closed.
- SW decides what applies inside a grant. SS reports requested, granted, applied and refused.
- Seam 0.1.0 defines no grant for `delete`. Deletion stays with Syafiq.

### 2.4 Extensions (C9, #84)

- Key form `<namespace>.<name>`, reverse-DNS namespace owned by its definer.
- Unknown extensions are ignored, never an error.
- Extensions cannot add vocabulary values, grant permission, or change core field meaning.
- Extensions obey the crossing rule in 3.1.

### 2.5 Capability profile (layer 2, P3 to P7, #84)

- A profile declares: supported seam version, `capability`, `capability-version`, execution modes, supported extensions, allowed operation classes, backend-constraint tokens, conformance status.
- Drafting a profile, or putting it in a release candidate, implies no active binding.
- First profile: `knowledge.ingest` 0.1.0. Modes are closed: `report-only`, `propose-only`, `apply`. Version 0.1.0 declares `report-only` and `propose-only` only. `apply` and `delete` are not in 0.1.0.
- Public (SS): seam contract, profile declarations, synthetic fixtures, generic adapter behaviour. A public adapter skill talks only to the seam.
- Private (SW): Basic Memory binding and mappings, permalinks and IDs, approval records, backend diagnostics, real fixtures. The Basic Memory specific adapter belongs to SW.
- Conformance has two layers. First, a capability-independent envelope and permission check against an abstract backend with synthetic data. Second, a private SW check of the `knowledge.ingest` binding against the real backend. Public status values: `not-tested`, `passed`, `failed`.
- Versioning: seam is `0.x`. A breaking change, including any closed-vocabulary change, bumps the minor number. Capability versions move independently. A profile states its supported seam range. Adding a capability does not change the seam version.

### 2.6 Lifecycle and release (P8 to P11, #85)

- Four stages: draft, release candidate, ratified release, activation.
- A release candidate `seam-v0.1.0-rc.N` is drafted only when Syafiq commissions it.
- A ratified release is an immutable tag `seam-v0.1.0` bound to a commit SHA recorded in Syafiq's approval.
- The approval artefact is a GitHub issue or pull request that Syafiq approves, naming the SHA. An agent may create the tag only after that approval is recorded.
- SW's private compatibility record points at the GitHub approval and never replaces it.
- Activation of a Wiki binding is a separate decision from ratification. SS and SW agreement is never ratification.
- `seam-v*` tags and repository `v*` tags are separate families.
- A release contains no private binding and no fixtures with real data.
- No implementation and no Basic Memory mutation starts before the activation decision.

### 2.7 Installation model (C2, #81)

- The Skills CLI, pinned as `npx skills@1.7.2`, global (`-g`), lock-controlled, is the only installer.
- One authoritative source per group:

| Group | Source |
| --- | --- |
| Matt Pocock skills | `mattpocock/skills` |
| Basic Memory skills | `basicmachines-co/basic-memory-skills` |
| SS skills | `skay93m/sk-skills` (after the rename; `skay93m/syafiq-kay-skills` until then) |
| Antigravity skills | CLI target `~/.gemini/antigravity-cli/skills/` |

- Antigravity's live target is only `~/.gemini/antigravity-cli/skills/`, holding only CLI-made symlinks tracked by the lock file. Accepted on read-only evidence; no live test was run.
- Hand-made symlinks are outside the model and count as unowned.
- A skill with no lock entry and no known source is untouched until Syafiq names its owner.
- Other `~/.gemini` skill paths are out of the model.
- `thinking-partner` (C5, #43): adapt as pinned upstream plus a small local extension. Nothing is installed or authorised by that decision.

### 2.8 Repository projection (C3, #82)

- The top-level `skills/` folder stays the one place the CLI scans.
- Skill directory names are unchanged and each `SKILL.md` `name` matches its directory. No `sk-` prefix rule. Renaming the four unprefixed skills (`daily-knowledge-maintenance`, `knowledge-ingest`, `knowledge-lint`, `task-assistant`) is a separate later choice.
- The repository will be renamed from `syafiq-kay-skills` to `sk-skills`. The rename is implementation work, not done.
- Not added to the repository: plugin manifest, `skills-lock.json`, `.agents/skills/` or `.claude/skills/` copies.
- The seam contract has no separate package. A folder without a `SKILL.md` is not installed by the CLI.
- Provenance stays in each skill's frontmatter.

### 2.9 Cleanup rules (C4, #83)

- Evidence gate for any removal: the manifest names path, type, owner and reason; a dry run shows what each host loses; anything not on GitHub or in the lock is backed up; Syafiq approves the exact operation. Approval of one path covers no other path.
- Permanent deletion is run by Syafiq himself.
- Clones are kept until a CLI install is verified on Claude, Codex and Antigravity. Order: CLI install, verify, then remove links.
- Backups exist in `~/.agents-retired-backups/` (tarball of `agy-builtin-skills`; link lists for the Antigravity Kensho and `memory-*` links and for the four Matt Pocock link sets).

### 2.10 Ledger and resume (P12 to P14, #86)

- GitHub is authoritative. Design lives in the map tickets and the decision log.
- Every log row has an ID, decision, status (proposed, confirmed, superseded), evidence link and date. Superseded rows stay visible and name their replacement.
- Before the next question, read the #79 body, the log and the latest comment on the open ticket.

### 2.11 Roadmap placement (#88)

Findings are facts; the tracker changes are not approved (see section 9).

- #2 remains the parent roadmap. #79 is the next priority route inside it.
- Independent lanes continue: task-assistant (#42, #44 to #47, #55 family), knowledge maintenance (#49 and children), email (#50, #51, PR #78), and #77.
- Deferred, out of scope: #3 to #13.

## 3. Privacy and default-deny boundaries (confirmed, C1 and #87)

### 3.1 Crossing rule

Default-deny. Only these cross the public seam:

- the closed vocabulary values;
- SW-generated opaque references, not derived from private content;
- counts;
- capability tokens.

### 3.2 Always private

Checksums (not even as hashes), Basic Memory permalinks and IDs, Drive identifiers, source and evidence content, query and answer content, approval records, mutation targets and before/after content, backend diagnostics.

### 3.3 Further rules

- Public fixtures are synthetic only.
- Anything else crosses only if Syafiq approves promoting it into the public contract.
- Meaning-changing and policy changes are never automatic.
- A request/grant mismatch fails closed with a structured error.

## 4. Mandatory gate: clean development baseline (#89)

#89 is open and unresolved. It is a mandatory pre-implementation gate. It is not completed work, and no procedure is yet decided.

Facts recorded so far (#88, #83):

- The working tree had 18 changes (modified, untracked, one staged deletion, including `GLOSSARY.md`). All are user-owned by default.
- The local clone is on `develop` with unpushed commits, so it differs from `main` (29 skills on `main`, 32 locally).
- Evidence-bearing locations that must not be treated as disposable: `/tmp/syafiq-kay-skills-integration` (branch `integration/daily-maintenance-full-pass`), eight Codex worktrees named `syafiq-kay-skills`, `/tmp/syafiq-kay-skills-pr48`, `syafiq-kay-skills-persistence-safety` (detached HEAD), `~/.claude/skills/synced` (unowned), stray nested entries in the Matt Pocock clone.
- `~/.hermes/config.yaml` points at `~/.agents/syafiq-kay-skills`. Moving or renaming this checkout breaks Hermes unless the config is updated.

What #89 must still define (from its ticket text): the inventory; user-owned versus route-related work; recoverability; what is committed, moved to a branch or worktree, retained or untouched; and verification evidence for a clean start. Nothing may be cleaned, reset, staged, committed, reformatted or moved without separate explicit approval of the exact operation.

Rule for this spec: all implementation tickets, the repository rename, and every cleanup step stay blocked until #89 is resolved and approved.

## 5. Implementation scope (proposed, not authorised; for review)

This is the work the confirmed decisions imply. It is a description, not a ticket list.

A. Installation migration: CLI installs from the three sources; verification per host; then manifest removals one exact operation at a time.
B. Repository: rename; update `README.md`, `GLOSSARY.md`, `docs/roadmap.md`, issue text, the Hermes path.
C. Seam contract in SS: envelope, vocabularies, extension rules, `knowledge.ingest` 0.1.0 profile, synthetic fixtures, abstract-backend conformance check, generic adapter skill.
D. Glossary terms (proposed in #87, not added): public seam, compatibility binding, opaque reference, mutation grant, seam ratification. Added via `/domain-modeling` after approval.
E. Release candidate and ratification: only when commissioned, per 2.6.

Out of scope here: the SW binding, Basic Memory mutation, activation.

## 6. Deferred release and activation matters

- Commissioning any `seam-v0.1.0-rc.N`: not commissioned.
- Ratified `seam-v0.1.0` tag and its approving issue or PR: not created.
- Activation of any Wiki binding: not decided. Needs its own decision.
- Timing of the repository rename relative to the first install and first release (#82): undecided.
- A later seam version adding a narrow `delete` class: deferred until deletion propagation is settled.
- `apply` mode for `knowledge.ingest`: deferred beyond 0.1.0.
- Repository `v0.1.0` (#65) versus `seam-v0.1.0`: families stay separate; #65 is not part of this map.

## 7. Unresolved or unverified matters

- ChatGPT: the CLI has no ChatGPT target. How ChatGPT and its launchers find local skills is unverified. The #88 constraint stands.
- Antigravity app: the CLI writes `~/.gemini/antigravity/skills/` but docs say the app reads `~/.gemini/config/skills/` (#80 risk 3). This does not affect Antigravity CLI.
- `~/.gemini/config/skills.json` and `~/.agents/skills.json` as discovery mechanisms: not verified. Behaviour of `agy` with a missing source is untested.
- `skills` 1.7.2 versus `main`: the research used `main`. Re-verify against tag 1.7.2 before implementation.
- GitHub redirect after rename, CLI behaviour with the renamed source, and pinned-ref syntax (`owner/repo#ref`): all untested.
- Existing lock entries that record the old source need a read-only check (#83).
- The extension namespace `com.syafiqkay.skills` is provisional.
- The grant record format and the opaque grant reference format: not specified beyond "opaque".
- Format of capability tokens and of `backend-constraint tokens`: not specified.
- The `thinking-partner` pin, local extension content and security review result: held in #43; not restated here.
- `kensho-system` has no link in Antigravity and is out of scope.
- The first #79 body lists "Not yet specified" items as history; some wording in #79 still reads as pending.

## 8. Items still requiring explicit approval

1. This specification itself. It was not approved. P12 says the implementation-ready spec comes after Syafiq approves it.
2. Each of the six cleanup manifest entries (#83), exact operation by exact operation. None is approved. Entry 1 (`agy-builtin-skills`) has intent recorded ("delete it") and a backup, but Syafiq runs the command himself and the config entries (2 and 3) need their own approval.
3. Entry 4 (36 Kensho and `memory-*` links): intent recorded, operation not approved.
4. Entry 5 (four Matt Pocock link sets) and entry 6 (Basic Memory clone and its two config entries): listed, not approved, preconditioned on verified CLI installs.
5. The repository rename and the Wiki project note slug change (separate Wiki approval).
6. The #88 tracker changes (1 to 6): comments on #2, #43, #3, #6, #12; the `sk-task` versus `task-assistant` edit pass; deferred-set review incl. #9; tag families note. Also the canonical task-adapter name.
7. Closing #79. Not to be done unless instructed.
8. The #89 procedure and each operation inside it.
9. Creation of implementation tickets, after this spec is approved and #89 is resolved.

## 9. Corrections and supersession history

- #81, #82 and #87 each had a first resolution that was later flagged "approval unverified", reopened, then re-confirmed with quoted words. The re-confirmed text is authoritative. Amendments: #81 adds "CLI-made symlinks only" and the `sk-skills` source after #82; #82 adds the rename to `sk-skills`.
- #87's re-confirmed scope covers ownership and privacy only. Its earlier section 4 and the deletion-token and ingest-profile lines were void until #84 and #85 re-decided them. They are now covered by P1, P4 and P8 to P11.
- No decision-log row is marked superseded (P1 to P14 reviewed with "approved P1 to P14, no changes", 2026-10-14).
