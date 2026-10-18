---
name: supervision-prep
description: Use when preparing a one-page Briefing Memo before a dissertation Supervision Gate.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: academic
---

# Supervision Prep

Prepare the student for one of the Supervision Gates authorised in MISSION.md. Work through the steps in order.

## Steps

### Validate the Gate

Accept exactly `gate-1`, `gate-2`, or `gate-3`. Any other argument, including none, stops the command before questions, a memo or any GitHub call. Reply in one line listing those three arguments with their months from MISSION.md. If MISSION.md is missing, name it and stop. Apply its three-gate, 30-minute limit; never propose an extra meeting, standing check-in or email substitute.

### Read the Governing Documents

Read MISSION.md, SOUL.md, GLOSSARY.md, ACADEMIC_STANDARDS.md, USER.md and RESOURCES.md from the working directory by bare file name. Apply the Socratic Academic Fellow mode and Ghostwriting Boundary in SOUL.md, citation verification in ACADEMIC_STANDARDS.md section 6.4 and confidentiality in section 6.5. Read the Supervision Briefing Memo, Supervision Gate and Epistemic Spine definitions in GLOSSARY.md. Take `<tracker repository>` from the 'Tracker repository' line in the GitHub Tracker section of RESOURCES.md for every GitHub call. If a document, section or repository value is missing, empty or malformed (not `owner/repo`), name the gap and stop before any GitHub call; never infer it from the current directory or a Git remote.

### Gather the Progress

Read dissertation progress with `gh issue list -R <tracker repository> --label module:dissertation --state all --limit 100 --json number,title,state,labels,milestone` and gate records with `gh issue list -R <tracker repository> --label type:supervision --label module:dissertation --state all --limit 100 --json number,title,body`. Identify the latest completed gate record and what has closed since it; if results may be truncated, retrieve the remaining records before claiming completeness. If a read fails, report the error and ask for the missing progress rather than inventing it.

Ask in one list for everything the tracker does not show: the student's current Core Thesis, Epistemic Spine claims in order, chapter or block status and the selected Gate Template's items. Record each answer as given.

### Draft the Memo

Assemble the Briefing Memo Shape using the selected Gate Template. Preserve the Core Thesis and spine claims verbatim. Progress Summary names closed Issue numbers since the last gate, or states that none closed. Decisions holds two or three high-leverage questions that change a decision the student cannot settle alone and can be answered within the meeting. Present named options without recommending one; leave source-answerable questions or matters that can wait out of the memo. Proposed Post-Meeting Actions holds at most five actions.

### Check the Memo

Count the Decisions questions: two or three. Count question marks outside double quotes across the whole memo: the total must equal the Decisions count. Each decision must name at least two options joined by "or" and end with a question mark. Count the words: at most 450 words in total. Fix failures by merging, cutting or rewording only the coach's questions; keep every required section and the student's claims intact. For citation gaps use `[student to supply]` under ACADEMIC_STANDARDS.md section 6.4.

### Hand Over the Memo

Show the checked memo in chat, including what was done in Progress Summary and what comes next in Proposed Post-Meeting Actions. The student decides what to send and when. Send no email and create or edit no Issue for the memo. Point to `/supervision-debrief <gate>` after the meeting.

## Briefing Memo Shape

Use the selected gate number and month in the title. The Decisions section is the only place for coach questions; words in double quotes are the student's and are exempt from the question-mark count.

```text
Briefing Memo: Gate N (<month from MISSION.md>)

### Progress Summary
What has closed since the last gate, by Issue number, or none.

### Epistemic Spine and Draft Status
The student's Core Thesis and ordered claims, with each block's status.

### Decisions for the Supervisor
1. Option A or option B?
2. Option A or option B?

### Proposed Post-Meeting Actions
- At most five actions.
```

## Gate Templates

### Gate 1: Topic, Research Question, Scope, and Methodology

In Progress Summary and Epistemic Spine and Draft Status: topic in the student's words; research question quoted in full in double quotes with its question mark intact; in-scope and out-of-scope lists; methodology (doctrinal, socio-legal or empirical) with one sentence explaining why it answers the question.

### Gate 2: Chapter Architecture, Core Controversy, and Empirical or Doctrinal Clash

In Epistemic Spine and Draft Status: chapter architecture with each chapter's function and spine-claim number; core controversy as the student phrases it; empirical or doctrinal clash where doctrine and evidence diverge, and which side the chapter must defend.

### Gate 3: Pre-Submission Audit, Structural Coherence, and Defensibility

In Progress Summary and Epistemic Spine and Draft Status: pre-submission audit of OSCOLA, outstanding `[student to supply]` markers and primary-source verification under ACADEMIC_STANDARDS.md section 6.4; structural coherence mapping every chapter to a spine claim; defensibility of the three most exposed claims, each with its supporting authority and counter-argument.
