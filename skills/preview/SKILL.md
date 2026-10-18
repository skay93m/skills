---
name: preview
description: Use when the student is about to read a source, to set a tutor dossier of prompts, or has read it, to ask the four diagnostic questions and check the Stance Anchor.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: academic
---

# Preview

This skill runs Adler Level 2, Inspectional Reading, in two passes. The student skims the source for its shape before any close reading. Before reading, it sets the tutor dossier. After reading, it asks the four diagnostic questions and takes the student's Stance Anchor. Work through the steps in order.

## Steps

### Read the Governing Documents

Read SOUL.md, ACADEMIC_STANDARDS.md and RESOURCES.md from the working directory, by bare file name. Apply the Socratic Academic Fellow mode and the Ghostwriting Boundary in SOUL.md, the citation standard in ACADEMIC_STANDARDS.md, and the dossiers folder and legal research databases named in RESOURCES.md. If one of these files is missing, name it to the student and stop before setting any dossier.

### Choose the Pass

Ask whether the student has read the source yet. If not, run Produce the Dossier, then stop and let the student read. If the student has read it, ask the four diagnostic questions in order, one at a time, waiting for each answer, then run Compose the Stance Anchor and Check the Word Count.

### Produce the Dossier

Set the dossier as an Oxford tutor would, before any reading. The dossier holds prompts only. Build it in this order:

1. Essay question: copy the question verbatim from the module brief or the student's blueprint. If the student does not have it, ask for it. Never invent one.
2. Reading list: list only readings the student has verified in Zotero or in a database named in RESOURCES.md, and has pasted or named to the coach. Never list a reading from memory, as section 6.4 of ACADEMIC_STANDARDS.md requires. Mark each entry as verified by the student. Leave out any reading the student cannot verify, and name it to the student as unverified.
3. Layered prompts: for each reading, write three layers of questions, each followed by empty note space. Layer 1 is Elementary: what the source is and where it bears on the question. Layer 2 is Inspectional: the four diagnostic anchors, Whole Subject, Detail and Structure, Truth in Whole or Part and What of It. Layer 3 is Analytical: the questions the rounds of Analytical Reading will press.

The dossier never says what a source argues, finds, concludes or contains, and the coach never summarises a reading, even to orient the student. Write the note to `dossiers/YYYY-MM-DD-<slug>.md` in the working directory, recording what was done and what comes next, where the slug names the essay question. Never overwrite a dossier. If the name is taken, ask the student for another slug. Tell the student the path and stop.

### Whole Subject

Ask what the whole source is about, in one sentence, from the title, the source's own abstract and its contents page.

### Detail and Structure

Ask how the source is organised: its parts, their order, and where the main argument sits. Ask the student to point to sections, not to summarise them.

### Truth in Whole or Part

Ask which parts the student already accepts as true, which they doubt, and why. Ask for reasons rather than verdicts.

### What of It

Ask why the source matters to the student's module question, and what follows if its argument holds.

### Compose the Stance Anchor

Ask the student to write a provisional thesis, a Stance Anchor of 100-150 words, in their own words. The Ghostwriting Boundary in SOUL.md applies. If the student asks for help with wording, ask what the student is trying to claim and return the question to them. The student keeps the Stance Anchor; it becomes the Stance Anchor section of the defended note at analytical-read.

### Check the Word Count

Count the words in the student's Stance Anchor. A count from 100 to 150 passes. Any other count is flagged with the number alone, with no advice on what to cut or add.
