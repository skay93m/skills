---
status: proposed
---

# Guarded unattended mutation is expressed through an opt-in `--rc` check

The seam can now describe `knowledge.lint` and `knowledge.ingest` runs that mutate the knowledge store without a human present, but only through a separate, opt-in `--rc` conformance mode that accepts draft release-candidate profiles carrying an owner-issued approval. The default check stays strict. Status: Proposed; the owner accepts or rejects it.

## Context

Seam round 14 recorded `knowledge.ingest` as report-only and propose-only until its tests pass, and the default conformance check encodes that: no profile may open the `apply` mode or the `apply-change` and `delete` operation classes. Since then, the Wiki-side ADR 0002 and the owner's decision allow guarded unattended mutation for `knowledge.lint` and `knowledge.ingest` under guardrails (append-only compile, exclusive-create, guarded edit with read-back, a deletion allowlist, a snapshot precondition and a separate post-run audit). This repository has to record how the seam expresses that without weakening what the default check already promises.

## Decision

- The default `scripts/seam_conformance.py` check stays strict. It rejects `apply`, `apply-change` and `delete` in profiles, and rejects any `delete` grant, even when a profile carries approval fields.
- A separate, opt-in `--rc` mode checks DRAFT release-candidate profiles. It accepts `apply` or `apply-change` only when the profile carries `approval-state: approved` and a well-formed opaque `approval-reference` that the owner issued. It prints a banner that it does not verify the approval is genuine.
- `delete` exists only for `knowledge.lint`, and only within the deletion allowlist. `--rc` rejects `delete` for any other capability, in a profile or in a grant.
- Effective permission stays grant AND mode AND profile AND first-run scope. A profile grants nothing by itself.
- The allowlist, the approval reference and the ratified `seam-v0.1.0` release remain the owner's decisions. The draft rc.1 profiles (`docs/seam/profiles/*-rc.1.json`) carry no approval fields, so `--rc` rejects them until the owner issues an approval reference.

## Considered options

1. **Loosen the default checker** so it accepts mutation profiles. Rejected: it would silently remove the guarantee every existing consumer of the default check relies on, and a profile with `apply` would pass without anyone choosing to run a release-candidate check.
2. **Keep rc.1 as a failing draft until ratified.** Rejected: with no check that accepts a mutation profile, the draft rules for approval, delete scope and mode gating could not be tested, and drift between the draft and the checker would go unseen.
3. **A separate opt-in `--rc` mode (chosen).** The default stays strict, the relaxed rules are named and tested, and a person has to pass the flag on purpose.

## Consequences

- The `--rc` mode cannot verify that an approval is genuine. It checks only the presence and format of the fields.
- Residual risk: a profile author can claim an approval by writing the two fields. Mitigation: never run `--rc` on production profiles in CI, and keep the approval reference something only the owner issues. A profile that passes `--rc` is a draft that conforms in shape, not an authorised one.
- Two checks now exist, so documentation and tests must say which one a result came from. Tests cover both, including the committed rc.1 profiles under each.
- Moving from draft to a ratified release needs further owner decisions: the allowlist, the approval format, and the checker change that would let a ratified profile pass the default mode.
