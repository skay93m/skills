---
name: blueprint
description: Use when the student has a research synthesis and a Stance Anchor and needs a one-page argument blueprint, with its Technical Artefact or waiver, before drafting.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: planning
---

# Blueprint

This skill lays out one essay or chapter argument as a one-page blueprint, a GitHub Issue that the slice-tickets skill reads. Work through the steps in order. Run in the Socratic Academic Fellow mode of SOUL.md, asking one question at a time.

## Steps

### Read the Governing Documents

Read SOUL.md, ACADEMIC_STANDARDS.md, GLOSSARY.md and RESOURCES.md from the working directory, by bare file name. Apply the Ghostwriting Boundary in SOUL.md and the citation rules in ACADEMIC_STANDARDS.md. Take the tracker repository from the GitHub Tracker section of RESOURCES.md and use it as `<tracker repository>` in every GitHub call. If one of these files is missing, name it to the student and stop before any GitHub call. If RESOURCES.md has no GitHub Tracker section or no 'Tracker repository' line, name what is missing to the student and stop before any GitHub call.

### Gather the Prompt and the Stance Anchor

Ask for the essay prompt or chapter question, the module label (one of the `module:*` labels) and the word limit, which defaults to 3,000 words. Ask the student to paste their Stance Anchor from /preview, in their own words. If none exists, return to /preview. Do not draft one.

### Elicit the Core Thesis

Ask the student to state the Core Thesis Statement in one sentence, in their own words, and record it verbatim. If the sentence is vague, ask what the student is trying to claim, and stop there. Never offer a sentence, a rewording or an opening.

### Build the Epistemic Spine

Ask for four to six claims that lead from the question to the thesis. Ask the student to number them in order and say which claim depends on which. Each claim is the step the next one needs. Record each as the student phrased it.

### Set the Paragraph Functional Budget

Ask the student to divide the essay into eight to twelve functional blocks, each budgeted 250 to 300 words. Report the sum against the word limit and let the student adjust until it fits; never refuse on the sum. For each block record a function as a role of at most eight words, such as "Set out the deference standard", the spine claim by number, the citations with OSCOLA pinpoints supplied by the student, and the counter-argument the block must meet. Body blocks need a citation and a counter-argument; the first and last may record `none`. A block count outside eight to twelve goes back to the student with the number alone.

### Map the Citation Budget

Ask for the primary authorities and the secondary literature, and assign each entry to its block numbers. Flag any body block with no citation. Add no entry the student has not read, and no case, statute or pinpoint from memory (section 6.4 of ACADEMIC_STANDARDS.md); a missing citation is recorded as `[student to supply]`.

### Test the Spine with One Model

Apply one mental model, Inversion: ask what the spine would reliably produce if applied without limit, and put that question once, to the student's own spine. If the spine breaks, the student revises the affected claim in their own words. Offer no second model in the same turn.

### Translate the Argument

Ask the student for their Technical Artefact: one small, real piece of technical work that turns part of the spine into an AI safety mechanism, with one "done looks like" line saying when it is finished. Record both in the student's words. If the essay has no natural translation, ask for the waiver reason instead. The coach never proposes a mechanism, project or done line, and never builds the artefact. If the wording is vague, ask what the mechanism would do, and stop there. The graded essay takes priority: a missing or waived artefact is flagged, never enforced.

### Approve and Publish the Blueprint

Show the assembled blueprint in the shape set out in Blueprint Shape, and ask whether it is ready. Only an explicit yes counts as approval. Then state the publish plan in one line, recording what was done and what comes next: the title, the `type:spec` and `module:*` labels, and the milestone, listed with `gh api repos/<tracker repository>/milestones --jq '.[] | .title'`. Create no Issue until the student confirms that plan. Then create the blueprint, with its sections as the body. The title is held in a quoted heredoc, so `$`, backticks and double quotes in the student's words are never expanded:

```bash
TITLE=$(cat <<'MSC_TITLE'
<title>
MSC_TITLE
)
gh issue create -R <tracker repository> --title "$TITLE" --label type:spec --label "<module label>" --milestone "<milestone>" --body-file - <<'MSC_BODY'
<the six labelled sections, in order, in the student's wording>
MSC_BODY
```

The label and milestone are copied from the listed names; rephrase a milestone that carries `$`, a backtick or a double quote before using it. Record the issue number from the URL that gh prints. That number is the input to slice-tickets.

## Blueprint Shape

The blueprint has six labelled sections, in this order. Each entry is a phrase or a short line, so the whole blueprint fits on one page. A function is a role of at most eight words, never a sentence of the essay.

- **Status**: `pending approval` until the student approves it, then `approved by student`.
- **Core Thesis Statement**: the student's sentence, verbatim.
- **Epistemic Spine**: the numbered claims, in order, each as the student phrased it.
- **Paragraph Functional Budget**: one line per block: `- Block N | 250-300 words | Function: <role> | Spine claim: <number> | Citations: <list or [student to supply]> | Counter-argument: <phrase or none>`.
- **Citation Budget**: the primary authorities and the secondary literature, each with its block numbers.
- **Technical Artefact**: exactly one of these two lines, in the student's words: `Artefact: <name>. Done looks like: <one concrete line>.` or `Waived: <reason the essay has no technical translation>.`
