---
name: academic-review
description: Use when a student needs a ticket-level draft or Technical Artefact reviewed against its objective and academic standards.
disable-model-invocation: true
model: original
metadata:
  origin: original
  agent_involvement: full
  category: academic
---

# Academic Review

Review a ticket-level slice, paragraph draft or Technical Artefact. Return flags only and make no GitHub writes. Work through the steps in order.

## Steps

### Read the Governing Documents

Read SOUL.md and ACADEMIC_STANDARDS.md from the working directory by bare name; if either is missing, name it and stop before the next step. Follow the shared authorship, flag-only, privacy, citation and style rules in SOUL.md and ACADEMIC_STANDARDS.md.

### Validate the Scope

Confirm the slice objective or prompt, the thesis the draft should advance, and the text to review. The student may state the objective or provide its Issue number. If an Issue number is given, read RESOURCES.md by bare name and take the tracker repository from its GitHub Tracker section, then run `gh issue view <number> -R <tracker repository> --json title,body`. If RESOURCES.md has no tracker repository, or the Issue cannot be read, ask the student to paste the Issue text; do not infer its contents. If the objective is still missing, ask one question and stop.

### Number the Lines

Number each prose sentence from 1 across the paragraphs in order. Do not number headings, a title page, or a bibliography. If the text is unnumbered, return the numbered text unchanged and state its total line count; wait for the student's confirmation before reviewing. Cite every flag by line number. For code, preserve the supplied line numbers or number each code line from 1.

### Run the Two Axes in Parallel

Make separate passes over the same numbered material. Neither pass reads the other's flags.

- **Axis One: Spec Compliance.** Check whether prose answers the objective, advances the stated thesis and addresses every required counter-argument. Use the labels Objective not answered, Thesis not advanced and Counter-argument unaddressed. The last is an omission at `Line absent`.
- **Axis Two: Standards Compliance.** Check each prose line against sections 1 to 6 and the tier scheme in section 6.7 of ACADEMIC_STANDARDS.md. For a Technical Artefact, compare its behaviour with the student's objective and any stated done line; check correctness, safety, attribution, dependencies and exposed data. For code, use Blocking for AI-authored, plagiarised or confidentiality defects, Major for objective, correctness or safety defects, and Minor for style. Do not write or repair code.

### Merge and Report the Flags

List Spec Compliance flags first, then Standards Compliance flags in line order. Each flag gives its tier and rule label, the rule or objective, `Line N` with an unchanged quoted span (or `Line absent` for an omission), and a one or two sentence defect explanation. Return flags and counts only, with the count for each axis, recording what was done and what comes next. Never issue `AUDIT_PASSED`, `AUDIT_FAILED`, or any verdict, and never rewrite or repair the supplied text or code. Do not mention lines without defects or propose wording.
