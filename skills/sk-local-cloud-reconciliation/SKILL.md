---
name: sk-local-cloud-reconciliation
description: Reconcile the Wiki between local Git main and Basic Memory Cloud using
  local and Cloud capture branches, a Git merge candidate, non-blocking review markers
  and a verified publication.
---

# Local and Cloud reconciliation

This is the current procedure for reconciling the Wiki project between local Git main and Basic Memory Cloud. It has eight steps and they run in order. Every Basic Memory command names the project explicitly with `--project wiki`.

## Step 1: Status and inventory

Require a clean worktree before starting. Run `bm cloud pull --project wiki --dry-run` and `bm cloud push --project wiki --dry-run` to inventory conflicts, Cloud-only files and local-only files. Stop on any transport failure.

## Step 2: Preserve baselines

Create a Cloud snapshot. Commit the intended local changes to main and record that commit as BASE.

## Step 3: Local capture

Create a `local-capture` branch from BASE. Protect the working directory from watchers while it is in use. Run `bm cloud pull --project wiki --on-conflict keep-local`. Verify the result and commit it on the branch.

## Step 4: Cloud capture

Create a `cloud-capture` branch from BASE. Run `bm cloud pull --project wiki --on-conflict keep-cloud`. Verify the result and commit it on the branch.

## Step 5: Git merge candidate

Create a branch from `local-capture`. Run `git merge --no-commit --no-ff <cloud-capture-branch>` to produce the merge candidate without committing it.

## Step 6: Structural and settled resolution

Automatically resolve every difference that is structural and meaning-preserving, and every semantic difference that a recorded decision has conclusively settled.

Treat `index.md` and `log.md` according to their distinct functions. Reconcile `index.md` by preserving current navigation intent and `log.md` by preserving append-only chronology. Recency may break ties only after those functions and all meaningful content are preserved.

## Step 7: Non-blocking unresolved semantics

For each genuinely unsettled semantic difference, insert the following structure at the disputed passage, as plain Markdown and not inside a code fence. Unresolved differences do not block the procedure.

````markdown
- [reconciliation-pending] <conflict-id>. Context: <Briefly explain the difference>. Question: <Specific question for Syafiq>.
> **Local** (`<commit-sha>`):
> (exact multiline text)
>
> **Cloud** (`<commit-sha>`):
> (exact multiline text)
````

## Step 8: Final publication and definition of done

Merge the resolved vault to main. Run `bm cloud pull --project wiki --dry-run` immediately before publication. Explicitly delete the removed files from Cloud, because push does not propagate deletions. Publish with `bm cloud push --project wiki --on-conflict keep-local`.

The definition of done is a final dry-run showing 0 conflicts, 0 Cloud-only files and 0 local-only files. Once that is verified, commit to Git.