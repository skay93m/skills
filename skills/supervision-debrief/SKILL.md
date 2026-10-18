---
name: supervision-debrief
description: Use when recording dissertation Supervision Gate decisions and turning confirmed directives into tracker slices after the meeting.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: academic
---

# Supervision Debrief

Capture a completed Supervision Gate and its follow-up work. Work through the steps in order.

## Steps

### Validate the Gate

Accept exactly `gate-1`, `gate-2`, or `gate-3`. Any other argument, including none, stops the command before questions or any GitHub call. Reply in one line listing those three arguments with their months from MISSION.md. If MISSION.md is missing, name it and stop. Apply its three-gate, 30-minute limit; never propose an extra meeting, standing check-in or email substitute.

### Read the Governing Documents

Read MISSION.md, SOUL.md, GLOSSARY.md, ACADEMIC_STANDARDS.md, USER.md and RESOURCES.md from the working directory by bare file name. Apply the Socratic Academic Fellow mode and Ghostwriting Boundary in SOUL.md, citation verification in ACADEMIC_STANDARDS.md section 6.4, confidentiality in section 6.5 and 15-Minute Micro-scaffolding in USER.md. Take `<tracker repository>` from the 'Tracker repository' line in the GitHub Tracker section of RESOURCES.md for every GitHub call. If a document, section or repository value is missing, empty or malformed (not `owner/repo`), name the gap and stop before any GitHub call; never infer it from the current directory or a Git remote.

### Capture the Feedback

Obtain the selected gate's Briefing Memo from the student if it is absent. Ask one question per turn about the supervisor's decision on each memo question, then each directive. Record the student's own paraphrase under ACADEMIC_STANDARDS.md section 6.5; if verbatim feedback is pasted, ask for a paraphrase before recording anything. Record unanswered questions as open.

### Record the Decisions

Write exactly one line per memo question in memo order: question number, decision as the student states it, and the supervisor's reason in one sentence, or `open`. Never turn an open question into a decision.

### Slice the Directives

Every directive yields at least one slice and each slice traces to exactly one directive. Record open questions without slicing them. Split work too large for one block. Apply USER.md's Micro-scaffolding rule, with each first action starting Open, Print, Copy, Highlight, Move, Tick, Set or Save, taking under a minute to start and at most 15 minutes to complete.

Use `[Dissertation/Gate N] Slice N: <functional objective>` for each title, `module:dissertation` and exactly one of `type:drafting` (prose), `type:audit` (citation and OSCOLA checks), `type:reading`, `type:spec` (planning) or `type:spike` (exploratory probe). Each body holds these labelled lines in order:

- `Part of #<record>`
- `Directive:` the student's paraphrase.
- `First action:` the physical action.
- `Output:` the object that exists at the end.
- `Done when:` the closing condition.

### Confirm the Plan

Find the dissertation milestone by title with `gh api repos/<tracker repository>/milestones --paginate --jq '.[] | select(.title | test("Dissertation")) | .title'`. If zero or multiple titles match, ask the student to name the milestone and wait. If the call fails, report the error and stop before writes. Show a table of the proposed record and slices, including title, type label, milestone, first action and minutes. The student may choose a different milestone. Ask for an explicit yes to this complete plan; approval of anything else does not count. Create, edit or link no Issue until that confirmation. A declined or changed plan returns to confirmation before any write.

### Create the Records

Create the gate record first, using the confirmed milestone title:

```bash
gh issue create -R <tracker repository> --title "Supervision Gate N Record" --label type:supervision --label module:dissertation --milestone "<dissertation milestone>" --body-file - <<'MSC_BODY'
<decision lines and directives in the student's paraphrase>
Completed: <what was recorded>
Next: <first confirmed slice and when to start>
MSC_BODY
```

Record its issue number from the returned URL. Then create each slice in order, replacing its `Part of` placeholder with that real number. Pass student text as literal data in quoted heredocs or safely quoted arguments; never expand it as shell code.

```bash
gh issue create -R <tracker repository> --title "<slice title>" --label module:dissertation --label "<type label>" --milestone "<dissertation milestone>" --body-file - <<'MSC_BODY'
<the five labelled lines above, with the actual record number>
MSC_BODY
```

Where supported, link with `gh issue edit <record> -R <tracker repository> --add-sub-issue <slice>`. Otherwise keep `Part of` and report the fallback. If any write fails, stop, report the error and links already created, and reconcile before retrying to avoid duplicate records or slices. Never claim an unsuccessful write completed.

### Report

List the record and each slice with its link, what was done and what comes next. Name the first slice and the Session in which to start it. Include that same completion and next-action record in the gate Issue. List open questions for the next authorised gate; after gate-3, record unresolved matters for independent follow-up within the existing plan, never a fourth gate.
