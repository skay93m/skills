---
name: coach-setup
description: Use when initialising a new coaching workspace or reconfiguring the 8 governing documents.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: setup
---

# Coach Setup

This skill initialises or reconfigures a coaching workspace by interviewing the student in rounds and generating the eight runtime governing documents. Work through the steps in order.

## Steps

### Read Reference Templates

Read the template structures in `references/templates.md` within this skill. Verify that template structures for all eight governing documents (MISSION.md, USER.md, SOUL.md, RESOURCES.md, PARKING_LOT.md, ACADEMIC_STANDARDS.md, GLOSSARY.md, and AGENTS.md) are present.

### Interview the Student in Rounds

Interview the student in sequential rounds to configure workspace parameters. For reconfigurations, read the existing tracker repository from RESOURCES.md by bare name as the default. Present each question with a recommended default, and resolve each branch before proceeding:
- Round 1 (Academic Mission): Ask for the degree programme, institution, remaining modules, dissertation topic, and personal stakes for MISSION.md.
- Round 2 (Student Profile): Ask for cognitive patterns, activation hurdles, rabbit holes, shame spirals, and grounding preferences for USER.md.
- Round 3 (Coaching Posture): Confirm the dual-mode identity (Socratic Academic Fellow vs Empathetic Partner) and strict anti-ghostwriting boundary for SOUL.md.
- Round 4 (Workspace Resources): Ask for the GitHub tracker repository (owner/repo), research portals, and storage paths for RESOURCES.md.
- Round 5 (Focus & Vocabulary): Confirm tangent capture protocol for PARKING_LOT.md and domain definitions for GLOSSARY.md.
- Round 6 (Standards & Invariants): Present baseline repository versions of ACADEMIC_STANDARDS.md and AGENTS.md for student review and confirmation.

### Generate Governing Documents

Instantiate all eight governing documents in the working directory using the confirmed answers and the templates in `references/templates.md`:
1. MISSION.md: Populated with degree programme, modules, dissertation targets, and personal stakes.
2. USER.md: Populated with student executive function profile and Grounding Protocol.
3. SOUL.md: Populated with dual-mode coaching identity and ghostwriting boundary.
4. RESOURCES.md: Populated with resource paths and `- Tracker repository: <tracker repository>` substituting the configured repository under `## GitHub Tracker`.
5. PARKING_LOT.md: Initialised with `No entries yet.` under `## Entries`.
6. ACADEMIC_STANDARDS.md: Baseline academic writing, citation, and integrity standards from the repository version.
7. GLOSSARY.md: Domain terminology and operational harness vocabulary.
8. AGENTS.md: Issue tracking conventions, triage labels, and markdown file naming invariants from the repository version.

Never author student academic prose. Write only structural configuration and governing files.

### Record Output and Recommend Ask-Coach

Record a summary of what was done and what comes next, listing all eight files and the configured GitHub tracker repository. Conclude by directing the student to run `/ask-coach` to orient themselves and begin their first study session.
