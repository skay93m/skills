---
name: sk-semantic-lint
description: Evidence-first Wiki semantic lint that surfaces meaning, truth, authority
  and consistency issues for human judgement without autonomously changing meaning.
---

# Semantic lint

## Purpose

Find problems of meaning, truth, consistency, authority and provenance in the Wiki, then make them easy for Syafiq to judge.

Semantic lint does not decide what Syafiq means. Syafiq owns epistemic judgement, meaning and policy. The agent retrieves evidence, compares claims, identifies tensions, tests authority, asks critical questions and implements only approved resolutions.

## Trigger

Use this skill for whole-Wiki semantic lint, a bounded semantic review of one area, or when another workflow identifies a possible contradiction, stale claim, overclaim, authority problem or misleading relation.

Do not repeat completed structural lint. Reuse existing structural evidence and reopen a structural issue only when a semantic finding depends on it.

## What to look for


### Folder fitness

Treat root-folder design as part of semantic lint because folders exist for human navigation.

For each root folder, ask:

- Is its purpose clear to Syafiq without reconstructing hidden system logic?
- Do the notes inside broadly match that purpose?
- Does it overlap confusingly with another folder?
- Would renaming, splitting, merging or retiring it make the Wiki easier to browse?
- Is a new root folder justified by a genuinely distinct human-facing purpose?

The Wiki may have as many root folders as useful for human readability. The structural constraint is shallow depth: maintained notes live one folder below root, with no folders nested inside those root folders.

Folder fitness is about human meaning and navigation, not authority. Folder location still does not determine whether a claim is true or current.

Test for:

- contradictory claims;
- stale claims presented as current;
- materially divergent duplicate concepts;
- conclusions stronger than their evidence;
- proposals, history or agent interpretation presented as settled decisions;
- semantically misleading relations;
- current notes that conflict with newer decisions;
- source-facing synthesis that exceeds its source;
- unclear provenance;
- unclear boundary between historical, provisional and current knowledge.

A missing or unresolved wikilink is not a semantic defect by itself.

## Authority model

No note is authoritative merely because it calls itself active, canonical, a decision or a source of truth.

Assess authority from the evidence graph:

- direct user decisions;
- corroboration across independent notes;
- recurrence and downstream implementation;
- provenance;
- recency where relevant;
- contradictions;
- explicit supersession;
- current applicability.

A historical decision may remain a true record of what was decided then while no longer governing now. Preserve that distinction.

Folder location does not by itself determine authority. Raw material may contain genuine decisions, but source-facing or provisional placement lowers the presumption that surrounding interpretation is current policy.

## Procedure

### 1. Establish scope

Read the current Wiki contract and triage procedure. Recover any persisted lint Task and completed prior work.

State what is in scope, what has already been completed and what must not be repeated.

### 2. Retrieve minimum evidence

Read the affected claim or note directly.

Then retrieve only the evidence needed to test it: newer decisions, linked notes, project state, relations, source provenance or downstream implementation.

Prefer targeted observations, metadata and graph traversal before loading entire notes.

Do not rely on session memory as evidence.

### 3. Classify the finding

Separate findings into three classes:

- **deterministic**: current explicit evidence resolves the issue without new human judgement;
- **judgement-required**: meaning, policy, intent, applicability or authority depends on Syafiq;
- **verification-needed**: external or primary-source evidence is required before the claim can be promoted or relied on.

Deterministic does not mean autonomously editable. Record the proposed correction for review unless an existing workflow already authorises that exact semantic change.

### 4. Expose the issue

Every meaningful finding must be visible to Syafiq before semantic meaning is changed.

Use concise observation-style records where possible so individual findings can be retrieved without loading the full audit.

For a judgement-required issue capture:

- stable issue ID;
- affected note or claim;
- issue;
- strongest competing evidence;
- recommended interpretation or correction;
- one clear question;
- response;
- lifecycle state.

Prefer the shortest wording that preserves the decision-relevant distinction.

### 5. Centralise human review

For a lint run with multiple findings, use one review inbox Task or review note. Syafiq should not need to open multiple source notes to decide.

Do not scatter required questions across source notes.

Keep unresolved issues non-blocking. Continue the sweep unless a normal safety, tool or governance stop rule applies.

### 6. Review one decision at a time

When interacting synchronously, present one semantic element at a time.

Do not ask Syafiq to classify an entire complex note as current or obsolete when individual claims may differ.

Break compound notes into claims such as:

- current decision;
- proposal or option;
- historical provenance;
- superseded claim;
- unresolved question;
- current implementation;
- supporting rationale.

If Syafiq gives a nuanced answer, refine the classification rather than forcing a binary label.

Never ask Syafiq to repeat a decision already recorded in the Wiki or current review.

### 7. Preserve knowledge evolution

Do not delete knowledge merely because it is stale.

Where appropriate:

- mark it superseded;
- bound it historically;
- demote its current authority;
- preserve provenance;
- link the newer state.

Distinguish decision truth from decision applicability.

### 8. Handle relations conservatively

Use precise semantic predicates only when evidence justifies them.

If a meaningful connection exists but its exact nature has not been reviewed, prefer `relates_to` as the unclassified relation. Treat it as a future classification signal, not an evidentiary claim.

### 9. Apply approved resolutions

Only after approval:

1. re-read each affected note immediately before editing;
2. verify the recorded decision still matches the current evidence;
3. use checksum-guarded edits;
4. make the smallest change that resolves the semantic issue;
5. preserve useful historical context;
6. read back and verify;
7. update the issue as applied.

Batch approved fixes when efficient, but never merge distinct epistemic decisions into one assumed resolution.

### 10. Finish and hand off

Record:

- scope and coverage;
- deterministic findings;
- judgement-required findings;
- verification needs;
- approved but unapplied fixes;
- applied fixes;
- unresolved issues;
- exact next step.

A fresh agent must be able to resume from Wiki state without relying on chat history.

## Review states

Prefer informative lifecycle states such as:

- `todo`
- `doing`
- `answered`
- `approved`
- `applied`
- `done`
- `superseded`
- `dropped`
- `abandoned`

Avoid vague `active` where a more precise state is available.

## Operating principles

- Semantic lint surfaces issues for human judgement; it does not silently rewrite meaning.
- No one note has absolute authority.
- Authority is graph-derived and evidence-sensitive.
- Historical knowledge is normally superseded, not erased.
- One complex note may contain claims with different lifecycle and authority states.
- Human questions should be centralised, concise and presented one decision at a time.
- Observations should make findings retrievable without forcing future agents to reread whole audit notes.
- Completed lint work must not be repeated merely to reconstruct context.

