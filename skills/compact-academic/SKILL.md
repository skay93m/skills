---
name: compact-academic
description: Use when an academic Session needs a lossless state snapshot before context compaction.
disable-model-invocation: true
metadata:
  origin: original
  agent_involvement: full
  category: academic
---

# Compact Academic

Read SOUL.md, USER.md, RESOURCES.md, PARKING_LOT.md and GLOSSARY.md by bare name. Apply their shared rules. Capture state verbatim, never draft or rewrite student prose, and use the tracker repository from RESOURCES.md for any GitHub call.

## Invariants

The snapshot is lossless and self-contained: preserve the six fields exactly, count output rather than authoring it, and never substitute prose for the student's Stance Anchor. The wake-up agent must rehydrate state, verify disk state, confirm the bound issue, restore the Stance Anchor verbatim and present the Landing Strip.

## Steps

### Inspect Session Deliverables

Capture the bound issue, Atomic Target and uncommitted output such as words drafted or pages read. Verify the files named by the student.

### Extract Stance Anchor

Capture the provisional thesis as a verbatim 100 to 150 word Stance Anchor. If it is absent or outside that range, flag it without repairing it.

### Harvest Session Parking Lot

Read PARKING_LOT.md and harvest entries added since the Session start. Preserve tangents verbatim and retain their destinations.

### Lock Tomorrow Landing Strip

Record one physical action that takes 15 minutes and creates zero activation friction. Keep it as the single Landing Strip.

### Generate Re-hydration Snapshot

Write a lossless snapshot for the wake-up agent containing all six fields and the Wake-Up Protocol, recording what was done and what comes next: rehydrate state, verify disk state, confirm the bound issue, restore the Stance Anchor verbatim and present the Landing Strip.

## Wake-Up Protocol for Post-Compaction Agent

1. Re-hydrate state immediately from this snapshot; do not prompt the student for orientation.
2. Verify local disk state against the uncommitted output and target files.
3. Confirm the bound issue via `gh issue view <number> -R <tracker repository>`.
4. Restore the Active Stance Anchor verbatim as the active analytical thesis without semantic alteration.
5. Present the Landing Strip to the student as the immediate kickoff action and await confirmation before taking further action.
