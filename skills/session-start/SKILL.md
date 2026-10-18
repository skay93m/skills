---
name: session-start
description: Use when the student opens a study Session, to set one Atomic Target, check in and bind the Session to the sprint issue.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: session
---

# Session Start

This skill opens a study block. Work through the steps in order.

## Steps

### Read the Governing Documents

Read SOUL.md, USER.md and RESOURCES.md from the working directory, by bare file name. Apply the mode rules in SOUL.md and the Grounding Protocol in USER.md. Take the tracker repository from the GitHub Tracker section of RESOURCES.md and use it as `<tracker repository>` in every GitHub call. If one of these files is missing, name it to the student and stop before any GitHub call. If RESOURCES.md has no GitHub Tracker section or no 'Tracker repository' line, name what is missing to the student and stop before any GitHub call.

### Surface the Sprint

Run the following to list the open issues marked as the current sprint focus:

```bash
gh issue list -R <tracker repository> --label sprint-active --state open --json number,title
```

Propose the first listed issue as the bound issue for this Session, and ask the student to confirm it or name another. If the command fails or returns no issues, ask the student for the issue number and say that the sprint list was not available.

### Somatic Check-in

Ask one body-level question, for example "tense, restless, flat, or steady?", and record the one-word answer. Apply the Somatic Check-in rule in USER.md.

If SOUL.md requires a mode switch, announce it under that document. On a switch, skip the Atomic Target and Micro-scaffolding steps for now. Run the Zero-Friction Kickoff under USER.md, then return to the Atomic Target once the action has started. Follow SOUL.md for the return to the Socratic Academic Fellow.

### Atomic Target

Ask for one Atomic Target for this study block: a single deliverable with a stated output, for example "read the abstract of one source and note its question on a card". If the student names more than one, ask which can finish first and keep only that one.

### Micro-scaffolding

Apply the 15-Minute Micro-scaffolding rule in USER.md to the Atomic Target. If the target feels overwhelming, or the student cannot name an action, shrink it under the same rule.

### Zero-Friction Kickoff

Apply the Zero-Friction Kickoff rule in USER.md. Ask the student to say when it has started.

### Bind to the Issue

Post the Session start comment to the bound issue, recording what was done and what comes next. Record the start time in local time as `YYYY-MM-DD HH:MM`, so the closing review can find the Parking Lot entries added during this Session:

```bash
gh issue comment <number> -R <tracker repository> --body-file - <<'MSC_BODY'
Session started at <YYYY-MM-DD HH:MM>. Atomic target: <target>. Kickoff: <action>.
MSC_BODY
```

If the command fails, show the error and say the comment was not posted.
