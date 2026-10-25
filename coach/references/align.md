---
name: coach-align
description: Reference workflow for auditing existing Specialist Coach Vaults against the Shared Coaching Boundary (Revision 3) and Coach Adapter Interface, generating structured gap reports and proposed remediations.
---

# Coach Alignment Reference Workflow (`align.md`)

This workflow inspects an existing **Specialist Coach Vault** against Revision `3` of the **Shared Coaching Boundary** and the uniform **Coach Adapter Interface**.

## Step 0: Desktop Environment Gate (macOS / Windows Only)
Verify that the runtime has direct local filesystem and shell access to the Meta-Repository (`/Users/syafiq/basic-memory` on macOS, or Windows equivalent). If invoked from a mobile or cloud-only session (e.g. ChatGPT/Claude iOS/Android app), **immediately halt and refuse** with a polite notice stating that coach alignment audits require a local desktop environment, deferring the request to a desktop session.

## Audit Checks
1. **Adapter Interface & Revision 3**: Verify presence and compliance of `AGENTS.md` (with `architecture_revision: 3`), `index.md`, `log.md` (`bm_parse_semantics: false`), `standards.md`, `contract/`, and `record/`.
2. **Explicit Project Rule**: Verify that all records and notes adhere to explicit project scoping (`project="<coach>"`).
3. **Vault Boundaries**: Confirm local mount at `/Users/syafiq/basic-memory/coaches/<coach>` and non-duplication of wiki notes.
4. **Life Compass Registration**: Verify registration in `wiki:projects/life-compass/current-season` (`active_coaches`).

## Output
Produce a structured gap report (Aligned vs Drift/Missing) and offer to:
1. Raise GitHub issues (`skay93m/<coach>`) / Superfocus governance items.
2. Apply a user-ratified alignment spec.
- **Strict Invariant**: Never silently rewrite or delete existing coach notes.
