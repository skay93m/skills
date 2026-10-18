---
name: session-end
description: Use when the student closes a study Session, to review the Atomic Target, log output, review the Parking Lot and post the four-heading Handoff to the bound issue.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: session
---

# Session End

This skill is the Handoff, the deterministic checkpoint that closes a Session. Work through the steps in order.

## Steps

### Read the Governing Documents

Read SOUL.md, USER.md, ACADEMIC_STANDARDS.md, PARKING_LOT.md and RESOURCES.md from the working directory, by bare file name. If one of these files is missing, name it to the student and stop before any GitHub call. Apply the mode rules in SOUL.md, the citation standard in ACADEMIC_STANDARDS.md, the Parking Lot rules in PARKING_LOT.md and the tracker repository named in the GitHub Tracker section of RESOURCES.md. Use that repository as `<tracker repository>` in every GitHub call. If RESOURCES.md has no GitHub Tracker section or no 'Tracker repository' line, name what is missing to the student and stop before any GitHub call.

### Somatic Check-in (closing)

Ask the same one-word question as at the start and apply the governing Somatic Check-in and mode rules in USER.md and SOUL.md. Then keep the Landing Strip to the smallest possible first action.

### Review the Target

Ask whether the Atomic Target was done, partly done, or not started, and record the answer without judgement. If the bound issue number is not in this conversation, ask the student for it. If the target from the start of the Session is not in this conversation, read the latest start comment on the bound issue:

```bash
gh issue view <number> -R <tracker repository> --comments
```

If the read fails, ask the student for the start time. If the target was not started, do not reopen it. Ask what got in the way in one or two questions, then return to the next physical action.

### Citation Check

Check the notes or drafts the student worked on for outstanding citations and unanchored claims, measured against ACADEMIC_STANDARDS.md. List each one as a flag that names the line, the defect, and the rule breached. Do not supply replacement wording. The student verifies each flag before the next Session.

### Log Output

Log the words drafted or pages read, as the student reports them. Record the number in the closing comment. The coach counts the output and does not draft any of it, because the ghostwriting boundary in SOUL.md applies to every word.

### Weekly Artefact

Ask whether this week had reading. If it did, ask whether that reading produced a linked pair: one MSc piece and one Technical Artefact, both from the same reading. Take the student's answer and do not scan files to check it. If the answer is no, flag it as an open item in the Handoff, worded "Weekly Artefact: no linked pair this week". The flag never blocks the close and never changes the Landing Strip.

### Review the Parking Lot

Read the start time from the latest start comment on the bound issue:

```bash
gh issue view <number> -R <tracker repository> --comments
```

If the read fails, ask the student for the start time, as in Review the Target. Then read the entries in PARKING_LOT.md whose timestamps fall after that time. Confirm that each has a target destination, as the Parking Lot rules require. Do not edit, reorder, or move entries during the review.

### Landing Strip

Lock one physical first action for tomorrow, under the Zero-Friction Kickoff rule in USER.md. The student writes it on a card, and it becomes the action that starts the next Session's Zero-Friction Kickoff.

### Close the Loop

Post the Handoff to the bound issue as a comment with four headings recording what was done and what comes next. Fill each heading in from the steps above, and end with the Landing Strip:

```bash
gh issue comment <number> -R <tracker repository> --body-file - <<'MSC_BODY'
## Current goal
<the goal the Session worked towards>

## Completed work
<target done, partly or not started; words or pages; citations flagged: count>

## Open blockers and discoveries
<blockers, discoveries and any Weekly Artefact flag>

## Immediate next step
<Landing Strip>
MSC_BODY
```

If the comment cannot be posted, show the error, say the Handoff was not posted, and print the four headings for the student to paste.

Close the issue only if the student confirms that the whole issue is finished. Post the one-line outcome as a comment, then close the issue without a further comment:

```bash
gh issue comment <number> -R <tracker repository> --body-file - <<'MSC_BODY'
<one-line outcome>
MSC_BODY
gh issue close <number> -R <tracker repository>
```

If the close fails, show the error and say the issue is still open.
