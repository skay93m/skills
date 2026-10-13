---
name: sk-index-governance
---

# Index Governance

This contract defines how agents interpret and maintain folder `index.md` notes. It separates what an index represents from whether an unsupervised agent may repair it.

## Two independent policies

Every maintained folder index has two policies:

- `index_scope`: what the index is intended to represent
- `scheduled_repair`: what an unsupervised scheduled agent may change

The policies are independent. An exhaustive index may still be report-only if it is part of the control plane.

## Index scope

Allowed values are:

- `exhaustive`: every eligible content note in the folder should be listed
- `curated`: the index intentionally lists selected important notes, themes or starting points
- `pointer`: the index primarily points to a dashboard, convention, workflow or another navigation surface

An agent must not infer `exhaustive` merely because an index currently lists every note. The index's wording, headings and established purpose are evidence of scope.

## Scheduled repair

Allowed values are:

- `allowed`: bounded, deterministic, reversible navigation repairs may be applied
- `report-only`: findings are reported for human review and no scheduled mutation is made

When policy is absent or ambiguous, use `report-only` and raise one grouped question rather than guessing.

## Deterministic checks

For an exhaustive index, the scheduled lint may compare the folder inventory with index entries and identify:

- content notes absent from the index;
- index links whose targets are missing or moved;
- duplicate entries;
- malformed or ambiguous links;
- missing folder `log.md`.

For a curated index, the agent may check dead links and malformed links but must not treat unlisted notes as defects.

For a pointer index, the agent checks only that declared pointers resolve and that the documented purpose remains structurally intact.

The `tasks/` index is not an exhaustive inventory merely because Task notes exist in the folder.

## Safe repairs

A scheduled agent may append a missing entry only when all of the following hold:

- the index scope is explicitly `exhaustive`;
- scheduled repair is explicitly `allowed`;
- the destination section is clearly intended for such entries;
- the note's title and description provide a sufficient one-line entry;
- the repair does not reorder, delete or rewrite existing entries.

A unique, evidence-supported replacement of an ambiguous or stale link may be proposed, but it is report-only unless the folder's scheduled repair policy explicitly permits link repair.

Scheduled agents never delete dead entries, reorder curated material or replace a curated or pointer index with an inventory.

## Production repair override

None. The retired `sk-scheduled-ingest-lint` and `sk-scheduled-lint` once allowed path-normalising moves and curated-index appends. The current `daily-knowledge-maintenance` contract, run through `knowledge-lint`, does not, so those repairs are report-only.

## Protected control plane

The following are control-plane notes and remain report-only for scheduled agents unless a later explicit contract says otherwise:

- `AGENTS.md`
- the root `index.md` and `log.md`
- `skills/` indexes, logs and skill notes
- `schema/` indexes, logs and schema notes
- `reports/` indexes, logs and report notes
- this contract

Changes to these notes require separate explicit approval.

## Human decisions

Syafiq sets or confirms index scope and scheduled repair policy. The agent supplies evidence, identifies ambiguity and recommends a policy. Syafiq does not need to decide individual missing entries once the folder policy is settled.

Questions requiring judgement are grouped in the relevant report and deferred to the governance review queue.

## Cadence and reporting

Daily lint checks the indexes directly affected by that day's work. A weekly structural slice may check stable folder indexes and the presence of folder logs.

Every finding records the folder, index, target note or link, evidence, proposed disposition and whether the finding is blocking. Any mutation records before and after checksums and a reversal method.

No folder policy is assigned by this contract. Those assignments are a separate reviewed step.