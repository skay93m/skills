---
name: sk-cli-agent-onboarding
description: 'Wiki-specific contract for agents with a local shell and Git worktree:
  CLI note mutation, Git cadence, synchronisation and reconciliation.'
---

# CLI agent onboarding

This note applies to agents that work on the Wiki through a local shell and Git worktree, such as `agy`, `codex` and `claude` running in a parent workspace. It sits beside [[syafiq-kay/wiki/agents]], which remains the default contract for every agent and assumes access through the Basic Memory MCP tools. Agents that reach the Wiki only through MCP do not need this note. A CLI agent reads it during bootstrap, after the triage skill, and treats it as binding for all shell and Git work.

## Parent workspace routing

Agents running in a parent workspace also follow that workspace's own root `AGENTS.md` for workspace invariants, submodule mechanics and tooling. This note covers only the Wiki-specific CLI contract. Do not copy parent-only Git or runtime mechanics into the Wiki.

## Mutating notes

Do not create, edit or delete Markdown files inside the project submodules (`wiki/`, `kensho/`, `awt-bm/`, `kos-bm/`) with raw shell tools (`echo >`, `cat >`, `rm`, `touch`) or generic file-editing tools (`write_to_file`, `replace_file_content`) during routine note operations. Use the Basic Memory CLI instead:

- Create or update: `bm tool write-note --title <t> --folder <path> --project <name> ...`
- Read: `bm tool read-note <identifier> --project <name> ...`
- Search: `bm tool search-notes <query> --project <name> ...`
- Edit: `bm tool edit-note <identifier> --operation <op> --content <text> --project <name> ...`
- Delete: `bm tool delete-note <identifier> --project <name> ...`

Always supply `--project <wiki|kensho2|main>` for `bm tool` commands and `--name <cloud-project>` for `bm cloud` commands. A system architect may use direct filesystem operations for a specific migration or convergence task that Syafiq has explicitly authorised.

## Python tooling

Run every Python script, test runner and package command through `uv run`, for example `uv run pytest` or `uv run python script.py`. Never invoke unmanaged system Python or bare `pip`.

## Git commits and working state

Create a Git commit immediately after completing and verifying each discrete block of work, and never leave verified work uncommitted across conversation turns. Follow Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:` and so on), stage specific files explicitly, and never use `git add -A` or a bare `git add .`.

- **Main is the sole long-lived working branch.** Normal Wiki development and note operations happen directly on `main`. Branches are not the default workflow.
- **Clean worktree at turn start and turn end.** Every turn begins and ends clean. Intended, verified changes are committed and normally pushed to `origin/main` before the turn ends.
- **No partial or dirty handovers.** Do not leave modified files, staged changes, unresolved conflicts, untracked artefacts, WIP commits or stashes as handover state. A stash is never a persistent workflow mechanism.
- **Stop on pre-existing dirty state.** If the worktree is dirty at turn start, halt and report it without stashing, resetting, committing, overwriting or discarding work you did not create.
- **Revert uncompleted turn work.** If work cannot be completed safely within the turn, revert only the changes made during that turn, restore the initial clean state, and report `BLOCKED` or `REVIEW REQUIRED`.
- **Branches are tools, not destinations.** Temporary branches or worktrees are permitted only as disposable tools for isolated technical operations such as three-way merge simulation, historical comparison or deterministic merge experiments. Integrate the verified result into `main` or discard them, and never hand off a temporary branch as active workflow state.

## Reindexing

`bm reindex -p <project>` is an exceptional repair or verification operation, not routine cleanup. Before running it, state `Reindex reason: <specific demonstrated reason>`. Valid reasons are notes created, moved or deleted outside the active watch path with uncertain index freshness; known or suspected stale or orphaned index rows; recovery from an aborted or failed prior indexing run; explicit validation or benchmarking requirements; direct instruction from Syafiq; or inability to confirm correctness through cheaper direct inspection such as `bm tool read-note`. Never reindex merely after editing a note, committing or pushing Git, running dry-runs or pull and push, updating `AGENTS.md`, or when a prior reindex already covered the current state. If no concrete reason can be stated, do not reindex.

## Synchronising Git, GitHub and Cloud

Local Git commits and Basic Memory Cloud may diverge during development. GitHub is a shared remote verification surface, but remote branches do not reflect uncommitted local changes. A parity certificate is a point-in-time attestation, and any later local commit or Cloud write invalidates it. Moving Cloud state is always handled with pre-reconciliation snapshots, dry-run comparisons and explicit delta classification, never with blind `keep-local` or `keep-cloud` overwrites.

### Control plane notes

A change to a note marked `sync_class: immediate` must be committed to Git `main`, pushed to `origin/main` and propagated to Basic Memory Cloud within the same task, using the supported single-note mutation path available in the current environment. Publication is per note. Do not start full reconciliation or reindexing merely because a control-plane note changed, and do not use raw transport such as direct WebDAV calls unless explicitly commissioned. A Cloud failure during publication is handled by the Cloud Transient-Failure Rule in [[syafiq-kay/wiki/agents]].

### Knowledge plane notes

Notes outside the control plane need no same-task propagation. Full Git and Cloud convergence and point-in-time parity certificates are scheduled operations, normally run once daily.

### Publication protocol for a moving Cloud

Another agent or Syafiq may author notes in Cloud at the same time, so publication follows this order:

1. Take a fresh Basic Memory Cloud snapshot immediately before publication.
2. Run bidirectional dry-runs with `bm cloud pull --dry-run` and `bm cloud push --dry-run`.
3. Classify only the new deltas authored since the initial baseline snapshot.
4. Import and preserve genuine Cloud-authored additions (`IMPORT_CLOUD_ADDITION`).
5. Stop and report if a same-path note changed semantically in Cloud, rather than overwriting it blindly.
6. Publish only after a clean pre-publication race check shows zero unclassified deltas.

### Transient failures on the command line

The Cloud Transient-Failure Rule in [[syafiq-kay/wiki/agents]] applies to `bm cloud pull`, `bm cloud push`, WebDAV and any equivalent command-line Cloud operation, and the failing command is the operation to record.

## Lint prerequisites

Parity must be established before a full production lint run, and before any semantic sweep. Any lint mutation creates a fresh Git delta and invalidates active parity certificates until they are re-sealed. The structural and semantic lint tiers themselves are defined in [[syafiq-kay/wiki/agents]].

## Reconciliation procedure

Active reconciliation follows [[wiki/skill/local-cloud-reconciliation]]. Control-layer notes retain current instructions only. Resolve deterministic structural differences and settled semantic differences automatically. Preserve unsettled alternatives only at the disputed passages in one review-ready note, and synchronise that same note without waiting for semantic decisions. Report file parity and semantic review separately.

## Observations

- [decision] Syafiq directed on 2026-10-04 that MCP is the default way for agents to interact with the Wiki and that CLI-specific guidance lives in this note rather than in AGENTS.
- [scope] This note holds shell, Git, GitHub and `bm cloud` mechanics moved out of AGENTS without changing their substance.
- [gap] Local Git and GitHub copies of this note do not exist until a CLI agent propagates it, because it was created through Cloud MCP.

## Relations

- relates_to [[syafiq-kay/wiki/agents]]
- relates_to [[syafiq-kay/wiki/skill/triage]]
- relates_to [[wiki/skill/local-cloud-reconciliation]]
