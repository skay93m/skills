---
name: sk-writing-coach
---

# writing-coach skill

## Purpose

Review Syafiq's unreviewed journal notes for style fit against the writing-practice-plan, flag issues, suggest next readings, and select weekly pieces for promotion. The skill operates under the role separation: Claude scaffolds and reviews, Syafiq writes the draft and decides publication.

**When to run**: Trigger this skill when you want coaching feedback on your practice notes. It reviews all unreviewed notes at once.

## Scope

- Read all unreviewed journal notes (marked `reviewed: false`)
- Assess each against the writing-practice-plan style traits: plain short sentences, numbered paragraphs, direct argument, pointed questions
- Flag publication-policy issues without deciding for you
- Suggest a next reading for each piece (from the writing-practice-plan or your earlier review feedback)
- Identify the strongest candidate from this week's practice for promotion to the site
- Never write in the `Your writing` section
- Never publish or move anything to the site repository

## Key decisions (from writing-practice-plan)

- **Frequency**: Write every day; publish one piece per week on a fixed rhythm
- **Length**: 300–500 words, 8–12 numbered paragraphs per piece
- **Style**: Plain short sentences, numbered paragraphs, direct argument, pointed questions (copied from Che Det)
- **Publication gate**: Every piece passes the Publication Policy in syafiqkay.com's AGENTS.md before publication
- **Coach role**: Nudge, review drafts, suggest readings, pick weekly candidates—never write the actual draft or decide publication

## Step-by-step

### 0. Read the journal index and log

Before reading project guidance or individual notes, read these two journal control notes in order:

1. `journal/index` — conventions, privacy boundary and the route from practice to publication.
2. `journal/log` — which notes have been reviewed, the latest weekly pick, backlog state and whether the seeder's coaching-use gate has triggered.

Use both to decide your triage strategy and what to surface in your final message.

### 1. Read governance notes

Always read the latest from Basic Memory Cloud (never rely on memory):
- `projects/writing-practice-plan.md` — style, rhythm, and publication gate
- `projects/syafiqkay.com-writing-pipeline-coordination.md` — the full pipeline and role separation
- `syafiq-kay.com-website.md` (if available) — Publication Policy details

### 2. List all unreviewed journal notes

Search `journal/` for notes with `reviewed: false`. Sort by date, oldest first.

### 3. For each unreviewed note

**Read the note.** Check:
- Does the writing use plain, short sentences?
- Are paragraphs numbered?
- Is the argument direct and clear?
- Are there pointed questions where they belong?
- Is the piece roughly 300–500 words?
- Are there any identifiable patient, colleague, employer or confidential professional details? (Flag these; never assume they are fine.)

**Record feedback.** Add or update the `Coach review` section with:
- What worked well (one or two specific observations, not generic praise)
- Gaps or unclear passages (be specific: quote the line if needed)
- Style mismatches (for example, passive voice, vague phrasing, missing numbers on paragraphs)
- Any Publication Policy flags (patterns vs. named individuals, patterns vs. confidential clinical info, etc.)

**Suggest next reading.** Add to the review: "Next reading: [title/link and one-sentence bearing on this piece]". The reading can be a wiki note, an essay, an article, or something from the writing-practice-plan. Ground it in the piece's argument or question.

**Set `reviewed: true`.** Mark the note as reviewed so the scheduler knows not to nudge again.

### 4. Identify the strongest piece from this week

From all the notes you reviewed, pick one (or note if there isn't a clear candidate yet):
- Strongest central question or argument
- Best fit to publication-plan style
- Most likely to be useful to readers
- Readiest for publication gate

Add an observation to this note: `[coaching-pick] YYYY-MM-DD-slug: [central question or theme]. Ready for promotion step: [yes/no/needs X]`.

### 5. Record in coordination note and coaching log

Add one line to `projects/syafiqkay.com-writing-pipeline-coordination.md` under a `Coach review` section:
- Date and who was reviewed (e.g., "2026-10-05: reviewed 2026-10-04 and 2026-10-05 notes; pick is 2026-10-05-X for [reason]; flagged [N] publication issues")

Append one entry to `journal/log`:
- Format: `- YYYY-MM-DD [session date]: reviewed [note slugs]; pick: [note slug] ([central question or theme]); [status or note]`
- Example: `- 2026-10-05: reviewed 2026-10-04, 2026-10-05; pick: 2026-10-05-example-title (why this matters); 2 issues flagged`

This keeps both the pipeline record and the coaching working memory in sync.

### 6. Message

Report one message to Syafiq:
- How many notes reviewed, how many with issues
- The weekly pick (title, central question, ready status)
- Any blocking publication issues (be specific; don't list every feedback item)
- What's next (promotion to site step, or needs more drafting)

Keep it plain, direct British English, no therapy-speak. One message; let him decide what to do next.

## When coaching lags behind writing

If you find yourself reviewing 5+ notes at once or if unreviewed notes are stacking up:
- Triage oldest first
- If a piece is weak but Syafiq is on a roll (lots of writing happening), mark it reviewed with feedback but do not flag it as the weekly pick
- If the stack is large, note this in your message: "You've built up a backlog; [coaching-pick] is strongest but worth reviewing the rest before the next promotion step"

If Syafiq is running behind on writing (few notes, or notes not being written despite seeding):
- Check whether the coaching-use gate triggered in the scheduler (coaching nudge sent instead of new prompt)
- If so, flag this in your message: "The seeder detected incomplete coaching from [date]; focus there before adding new prompts"

