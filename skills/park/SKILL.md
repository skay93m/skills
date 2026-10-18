---
name: park
description: Use when a tangent needs to be captured in the working vault so the student can return to the active task.
disable-model-invocation: true
model: original
metadata:
  origin: original
  agent_involvement: full
  category: study
---

# Park

## Steps

### Read the Governing Documents

Read SOUL.md, ACADEMIC_STANDARDS.md and PARKING_LOT.md from the working directory by bare name; stop before proceeding if any is missing. Shared rules in those documents govern this skill.

### Capture

Take the thought as all text after the invocation, including embedded line breaks. Replace each CRLF, CR, or LF with the two literal characters `\\n` without trimming or dropping content, so arbitrary invocation text remains safely representable in one physical entry line. Get local time from the shell with `date "+%Y-%m-%d %H:%M"`. Use a destination only if the student names one in the same message; otherwise record `unassigned`. Do not ask for a destination. If the timestamp command fails, show the thought and say it was not saved.

### Append

Append one entry to the Entries section of PARKING_LOT.md using its rules. Put it before the next level-two heading. Replace `No entries yet.` on the first entry. Change nothing else in the file. This step adds one line only and writes exactly one physical line.

### Validate and Redirect

Read the new entry back to confirm the write, then reply with exactly one gentle sentence that validates the capture, recording what was done and what comes next, for example "That is safely captured, so you can let it rest and return to <Atomic Target>." If none is active, name the current physical action. If the append fails, say so, show the entry in the reply, and keep the thought there so it is not lost.
