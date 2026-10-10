# syafiq-kay-skills project plan

This is the recovered implementation plan for `syafiq-kay-skills`. It supersedes the mistaken direction to develop a Sourcery-specific PR-review standard. The implementation slice is waiting for the concurrent research on good skill design to complete. The separate skill-refactoring work is proceeding in parallel and is not a blocker. No implementation should begin until the research has been reviewed and any resulting policy decisions have been approved by Syafiq.

## Status

- [status] Waiting for research before implementation.
- [scope] Develop, validate and distribute Syafiq's custom agent skills while safely managing installation and machine configuration.
- [branch] Use `develop` for integration and ongoing development; promote production through a pull request from `develop` to `main`.
- [authority] Syafiq retains authority over repository additions, destructive changes, production merges and semantic or policy decisions.
- [current_slice] The first implementation slice is documentation-only and remains paused pending the research gate.
- [parallel_work] Skill refactoring is part of this project and proceeds in parallel while the research completes; it is not a blocker.

## Goal and branch model

- `develop` is the integration branch.
- Feature branches start from `develop` and merge back through pull requests.
- `main` is production-ready.
- A release pull request promotes `develop` to `main`.
- A hotfix branches from `main`, merges into `main`, then merges back into `develop`.
- Direct development on `main` or `develop` is not part of the agreed workflow.

## Intended repository architecture

```text
skills/
  <skill-name>/
    SKILL.md
    scripts/       # only when needed
    references/    # only when needed

docs/
  authorised-skill-repositories.md
  glossary.md
  roadmap.md
  standards/
    snapshots/    # later, if approved

.github/workflows/ # later
tests/             # later
```

Skills should have minimal `SKILL.md` files. Supporting references and scripts are added only when they materially improve reliability, reduce repetition or provide deterministic behaviour. Local extensions and personalisations of authorised upstream skills must record provenance and divergence. The machine-readable configuration should be derived from human-readable authority.

Current repository content includes `skills/sk-onboarding/SKILL.md`, `skills/sk-update/SKILL.md` and `skills/sk-update/golden-skills.json`. The current `sk-update` instruction invokes `skills update --heal`, which conflicts with the safer separation of verify, update and heal and must be revised only in a later authorised phase.

## Implementation sequence

### Phase 0: repository and branch baseline

Confirm the remote `main` and `develop` branches and the pull-request workflow. Branch protection is an external setup decision. Do not change skill behaviour in this phase.

### Phase 1: human-readable authority and vocabulary

Add:

- `docs/authorised-skill-repositories.md`
- `docs/glossary.md`
- `docs/roadmap.md`

The authorised-repository note must state that only Syafiq may add or remove repositories. The glossary must distinguish the Syafiq skills repository, an authorised skill repository and the `skills` CLI. The roadmap must record future commands and deferred work without implying that they already exist.

### Phase 2: authority projection and validation

Define how `docs/authorised-skill-repositories.md` relates to `skills/sk-update/golden-skills.json`. The intended direction is human-readable authority to machine-readable projection. Whether JSON is generated or only validated remains unresolved. Mismatches must be visible and automation must not silently expand the allowlist.

### Phase 3: safe command contract

Document, before implementing a CLI:

- `sk-onboarding`: initial machine setup.
- `skills verify`: read-only diagnosis.
- `skills update`: routine updates for authorised repositories.
- `skills heal`: explicit high-risk repair.
- `skills add <repo-url>`: proposal for adding an authorised repository.
- `skills reinstall <repo>`: explicit reinstall of one authorised repository.
- `skills review`: report stale, unused, duplicate or orphaned skills.
- `skills remove <skill>`: explicit removal after confirmation.

Each command needs defined inputs, outputs, failure modes and confirmation requirements.

### Phase 4: onboarding

Revise `sk-onboarding` only after the contract is approved. It should establish approved central configuration, verify required files, install or link only authorised repositories, detect legacy or duplicate installations, report proposed mutations and converge safely when rerun. It must never expand the allowlist or run unsupervised.

### Phase 5: verification

Implement `skills verify` as read-only diagnosis of missing or unexpected repositories, configuration mismatches, broken links, duplicate skills, stale versions, malformed configuration and divergence from the golden configuration. It should exit nonzero on drift, report exact failure modes and produce a reusable handover prompt. It must not install, delete, rewrite or heal.

### Phase 6: routine update

Update only repositories already on the authorised list. Report local and remote state and update results. Do not add repositories or perform broad cleanup.

### Phase 7: healing and explicit repair

A future `skills heal` flow must inspect state, produce a repair plan, wait for explicit human approval, apply only approved changes, verify the result and report failures. It must not perform automatic destructive repair.

### Phase 8: repository and skill lifecycle

Future `add`, `reinstall`, `review` and `remove` flows must use explicit targets, confirmation and report-driven behaviour. Bulk pruning is deferred.

## Security and human authority

Agents may run read-only diagnosis but must not silently mutate machine configuration. Onboarding requires explicit human invocation. Healing, reinstalling and removing require explicit target and confirmation. Adding a repository requires Syafiq's approval and the allowlist cannot be expanded by automation. Destructive cleanup must never use unrestricted directory deletion. Missing authority or ambiguous configuration must fail visibly. Hidden help text is not a security boundary; the enforceable controls are confirmation, scope, auditability and pull-request approval.

## Approved decisions

The following are already approved: the `main`/`develop` model; pull-request development and release; Syafiq as final production gate; security and optimisation review; minimal skills with optional references and scripts; avoidance of duplication with authorised upstream skills; a human-readable repository allowlist; machine-readable configuration derived from that list; read-only `skills verify`; separate update and heal operations; future add, reinstall, review and remove commands; explicit authority for repository additions; provenance and divergence metadata for extensions; research before synthesis; Syafiq approval for synthesis and canonical-note creation; currentness metadata using `last_reviewed_at` and optional `freshness_period`; stale standards being flagged rather than automatically blocking ordinary review; missing or unknowable standards blocking the relevant review; and capturing the workflow before formalising the eventual skill.

## Deferred work

Defer the full CLI, automated healing, automated repository addition, bulk pruning, currentness automation, research-compounding workflow, full ingestion/synthesis governance, upstream contribution workflow, custom Sourcery review standards, complex versioning and package distribution, and a broad test framework.

## Open decisions

- Exact implementation location for the `skills` CLI.
- Schema for `docs/authorised-skill-repositories.md`.
- Whether `golden-skills.json` is generated or validated.
- Exact onboarding behaviour by agent and operating system.
- Technical implementation of human confirmation.
- Whether `develop` also receives branch protection.
- Extension metadata and wrapper, overlay or copy model.
- Verification-report and handover-prompt format.
- Historical snapshot format.
- Final authorised repository list.

## First authorised implementation slice

After the research gate and any required approvals, the smallest first slice is documentation-only:

- `docs/authorised-skill-repositories.md`
- `docs/glossary.md`
- `docs/roadmap.md`

This slice does not authorise code, Wiki changes beyond this record, CLI behaviour, onboarding changes, commits or Sourcery-standard work.

## Research handoff protocol

- [decision] Commission Gemini only for bounded research tasks.
- [decision] Gemini must write its findings to a Google Doc saved in Google Drive, including sources and uncertainties.
- [handoff] Gemini returns a one-line prompt containing the Google Doc link.
- [boundary] The receiving agent reads and verifies the Google Doc before synthesising findings into the Wiki or repository.
- [authority] Synthesis, policy decisions and implementation remain subject to Syafiq's approval.

## Relevant Matt Pocock skills

- `engineering/research`: current research gate; investigate primary sources and capture findings in one Markdown file.
- `productivity/grilling`: resolve the open design decisions in numbered rounds after research returns.
- `engineering/codebase-design`: design the CLI and configuration seams using deep-module vocabulary once implementation design is authorised.
- `engineering/to-spec`: turn the approved plan and repository understanding into an implementation specification.
- `engineering/implement-spec`: later implementation workflow once a spec and task graph exist.
- `engineering/tdd`: build behaviour behind the agreed interfaces.
- `engineering/code-review`: review implementation against repository standards and the approved spec.
- `engineering/pr`: prepare the pull-request body and evidence.
- `productivity/handoff`: preserve resumable state when pausing or changing sessions.
