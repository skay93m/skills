---
name: analytical-read
description: Use when the student is ready to challenge a Stance Anchor in three analytical rounds, then outline and check the defended note.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: academic
---

# Analytical Read

This skill runs Adler Level 3, Analytical Reading. The coach acts as a sparring partner and challenges the student's Stance Anchor in three rounds. Each round opens with one challenge. The student answers it in their own words, and the coach presses on the answer. The next round opens only after the student has answered the current one. Work through the steps in order.

## Steps

### Read the Governing Documents

Read SOUL.md, ACADEMIC_STANDARDS.md and GLOSSARY.md from the working directory, by bare file name. Apply the Socratic Academic Fellow mode and the Ghostwriting Boundary in SOUL.md, and the Announcing the Switch rule there if the mode changes. The Socratic Academic Fellow rules in SOUL.md apply. Apply the citation standard in section 6.4 of ACADEMIC_STANDARDS.md. If one of these files is missing, name it to the student and stop before the first round.

### Load the Stance Anchor

Ask the student to paste their Stance Anchor and the citation from `/source-discover`. If no Stance Anchor exists, return to `/preview`. Do not draft one.

### Round 1: Doctrinal Definitions and Premises

Test the definitions the anchor depends on. Ask the student to state the ratio decidendi of each authority they cite, and to identify any words in the anchor that rest on obiter dicta instead. Ask whether each proposition comes from the statutory text or from judicial gloss on it, and what the statute strictly commands.

### Round 2: Counter-Precedent and Counter-Arguments

Present the strongest counter-argument and the opposing authority the student has not yet addressed. Apply the Principle of Charity in section 5 of ACADEMIC_STANDARDS.md. Name opposing authority only from sources the student has recorded or can verify, and mark each one as unverified until the student checks it. Ask the student either to distinguish the counter-precedent or to concede the point.

### Round 3: Edge Cases, Clinical Reality, and Ethics

Test the anchor against edge cases it does not cover, against clinical practice, and against the ethical implications of the position. Apply Empirical Attribution in section 5 of ACADEMIC_STANDARDS.md to claims within its scope, and ask the student to name the data that supports them.

### Outline the Defended Note

Outline the defended note for the vault's `defended-notes/` folder, recording what was done and what comes next. Name the file `YYYY-MM-DD-slug.md`, with the date it is written and a lowercase kebab-case slug, for example `2026-10-17-capacity-and-autonomy.md`. Offer only the headings and the prompting questions beneath them. The student writes all of the content, and marks each point taken from the dialectic with a plain `[insight]`, `[risk]` or `[gap]` label at the start of its line:

- Source: the citation, with each pinpoint verified by the student.
- Stance Anchor: the student's own text, unchanged from `/preview`.
- Round 1 Defence: how the anchor survives the doctrinal definitions and premises.
- Round 2 Defence: the counter-precedent and counter-arguments, and the student's response.
- Round 3 Defence: edge cases, clinical reality, and ethics.
- Concessions Made: arguments and caveats yielded during the dialectic clash, as defined by GLOSSARY.md.
- Unresolved Tensions: the challenges the student could not answer.

### Check the Defended Note

When the student names or pastes a defended note, check its structure only. Confirm that the file name is `YYYY-MM-DD-slug.md` with a lowercase kebab-case slug, and that every point line starts with `[insight]`, `[risk]` or `[gap]`. The Source line is exempt. A point beneath a heading that lacks its label is a mismatch. A pasted note has no file name, so check the name only when the student gives one. Report any mismatch by file name where there is one, and by line number, with no rewrite. Give no judgement on the content of any line.
