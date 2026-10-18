---
name: slice-tickets
description: Use when the student has an approved blueprint and needs it sliced into drafting and technical GitHub Issues, each with a 15-minute first action.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: planning
---

# Slice Tickets

This skill slices an approved blueprint into GitHub Issues. Work through the steps in order. Run in the Socratic Academic Fellow mode of SOUL.md, asking one question at a time. It creates no Issue until the student confirms the plan.

## Steps

### Read the Governing Documents

Read SOUL.md, USER.md and RESOURCES.md from the working directory, by bare file name. Apply the Ghostwriting Boundary in SOUL.md and the 15-Minute Micro-scaffolding rule in USER.md. Take the tracker repository from the GitHub Tracker section of RESOURCES.md and use it as `<tracker repository>` in every GitHub call. If one of these files is missing, name it to the student and stop before any GitHub call. If RESOURCES.md has no GitHub Tracker section or no 'Tracker repository' line, name what is missing to the student and stop before any GitHub call.

### Load and Check the Approval

Ask for the blueprint's issue number if none is given, then read it with `gh issue view <number> -R <tracker repository> --json title,body,labels,milestone`. Refuse to slice unless the Status line reads `approved by student`, the labelled sections are present (Status, Core Thesis Statement, Epistemic Spine, Paragraph Functional Budget and Citation Budget), and the budget lines parse to eight to twelve blocks of 250 to 300 words each. Budget lines take this form: `- Block N | 250-300 words | Function: <role> | Spine claim: <number> | Citations: <list or [student to supply]> | Counter-argument: <phrase or none>`. A refusal returns the student to the blueprint skill and names the missing item in one line. Never slice an unapproved blueprint.

The Technical Artefact section takes one of two lines: `Artefact: <name>. Done looks like: <one concrete line>.` or `Waived: <reason the essay has no technical translation>.` A blueprint with neither line is not refused. Flag the gap in the plan table, make no technical slice, and continue.

### Slice the Blueprint

Drafting slices: group the blocks into four to six slices of two or three consecutive blocks. The slices partition the blocks in order, with no gap and no overlap. Each objective is the block functions in order, joined with semicolons, copied from the blueprint and never reworded.

Technical slice: an Artefact line yields exactly one technical slice, named by the artefact name and carrying its done line. A Waived line yields no technical slice. A blueprint with neither line yields none either. The technical slice neither blocks nor is blocked by the drafting slices.

### Write the Ticket Bodies

Each drafting slice has these sections, in order: **Parent**: `Part of #<blueprint number>`. **Blocks**: the block numbers, their combined budget and the spine claims they serve. **Functions and citations**: copied from the blueprint, with `[student to supply]` kept. **Counter-arguments to meet**: copied. **First action (15-minute block)**: one physical action that takes under one minute to start, such as "Open the citation list and highlight the three pinpoints for Block 3". It opens with Open, Print, Copy, Highlight, Move, Tick, Set or Save and runs to 20 words at most. **Blocked by** and **Blocks**: placeholders until the Link the Blockers step.

The technical slice has **Parent**, **Done looks like** (copied from the blueprint), a **First action** under the same rules, and **Blocked by: none** and **Blocks: none**.

The body tells the student what to write, and the student writes it. The ticket never contains sentences for the essay.

Titles: a drafting slice is `[<Module>/<Chapter>] Slice N: <Functional Objective>`; the technical slice is `[<Module>/<Chapter>] Technical Slice: <artefact name>`. Drafting slices carry the module's `module:*` label and `type:drafting`; the technical slice carries `module:*` and `type:technical`. The milestone is the sprint the student names, listed with `gh api repos/<tracker repository>/milestones --jq '.[] | .title'`. Do not add `sprint-active`, because the student sets that label.

### Confirm the Plan

Show the student a table of every Issue: type, number, title, blocks, word budget and first action. If the blueprint has neither Technical Artefact line, add a row that flags the missing artefact and says that no technical slice is made. Ask for explicit confirmation before any Issue is created. Only an explicit yes counts; a yes to anything else does not.

### Create the Issues in Order

Create the drafting slices in order, then the technical slice, one Issue each, with its title, labels, milestone and body. For a drafting slice, use:

```bash
TITLE=$(cat <<'MSC_TITLE'
<ticket title>
MSC_TITLE
)
gh issue create -R <tracker repository> --title "$TITLE" --label "<module label>" --label type:drafting --milestone "<milestone>" --body-file - <<'MSC_BODY'
<ticket body>
MSC_BODY
```

For the technical slice, use:

```bash
TITLE=$(cat <<'MSC_TITLE'
<technical ticket title>
MSC_TITLE
)
gh issue create -R <tracker repository> --title "$TITLE" --label "<module label>" --label type:technical --milestone "<milestone>" --body-file - <<'MSC_BODY'
<technical ticket body>
MSC_BODY
```

The quoted title and body heredocs mean `$`, backticks and double quotes in the student's words are never expanded.

The label and milestone are copied from the listed names; rephrase a milestone that carries `$`, a backtick or a double quote before using it. Record each issue number from the URL that gh prints. Creation order matters, because the second pass needs the numbers of the Issues that already exist.

### Link the Blockers

Blocking among drafting slices is linear: slice N is blocked by slice N minus 1. Link in two passes. First, edit each drafting body with `gh issue edit <number> -R <tracker repository> --body-file - <<'MSC_BODY'`, so that every Blocked by line has a matching Blocks line. Slice 1 has no blocker. Second, add the native dependency for each edge: read the blocker's database id with `gh api repos/<tracker repository>/issues/<blocker> --jq .id`, then run `gh api --method POST repos/<tracker repository>/issues/<blocked>/dependencies/blocked_by -F issue_id=<blocker database id>`. If the dependencies endpoint is unavailable, keep the body lines and say so. The technical slice gets no links. Finish by listing the created Issues with their links, recording what was done and what comes next, naming the slice to start first.
