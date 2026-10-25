---
name: coach-create
description: Reference workflow for creating new specialist coach workspaces or extending existing coaches with new programmes/exams, enforcing Revision 3 architecture, desktop environment gates, and registering active coaches in current-season.md.
---

# Coach Creation & Extension Reference Workflow (`create.md`)

This workflow governs creating new specialist coach workspaces and extending existing coaches (such as `study-coach`) with new programmes, certifications, or contracts under Revision `3` of the Shared Coaching Boundary.

## Step 0: Desktop Environment Gate (macOS / Windows Only)
Verify that the runtime has direct local filesystem and shell access to the Meta-Repository (`/Users/syafiq/basic-memory` on macOS, or Windows equivalent). If invoked from a mobile or cloud-only session (e.g. ChatGPT/Claude iOS/Android app), **immediately halt and refuse** with a polite notice stating that coach creation and extension require a local desktop environment, deferring the request to a desktop session.

## Step 1: Official Exam / Qualification Identity Gate
For any ambiguous or code-named exam/qualification request (e.g. `CS1`), verify and confirm with the user before routing or scaffolding:
1. Official full title.
2. Awarding body (e.g. IFoA vs university module).
3. Exact syllabus version or examination session.

## Step 2: Human Ratification Gate
Present the proposed boundary, adapter files (`AGENTS.md` with `architecture_revision: 3`, `index.md`, `log.md`, `standards.md`, `contract/`, `record/`), and Superfocus link.
- **Wait for explicit approval** before creating any Basic Memory project, Git repository, or notes.

## Step 3: Scaffold & Implementation
Upon ratification:
1. Initialize the coach vault structure under `/Users/syafiq/basic-memory/coaches/<domain>-coach` (or extend the existing vault).
2. Ensure explicit `project="<domain>-coach"` usage for all memory operations.
3. Link relevant Superfocus items (read-only reference).
4. **Register in Life Compass**: Append `<domain>-coach` to the `active_coaches` list in `wiki:projects/life-compass/current-season` (`project="wiki"`) so `life-coach` automatically includes it in weekly alignment and session oversight.

## Step 4: Independent Standards + Spec Review Pass
Execute an independent review of the created/extended workspace against the Coach Adapter Interface and Shared Coaching Boundary standards before handoff.
