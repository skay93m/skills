---
title: Scope-Drift Check for Tickets (Design Note)
type: proposal
status: draft
date: 2026-10-18
tags:
  - governance
  - standards
  - work-orders
  - follow-up
---

# Scope-Drift Check for Tickets (Design Note)

Status: design note only. Nothing in this note is implemented.

## Idea

Compare the files a ticket changes with the files the ticket names in its scope. A ticket that touches files outside its named scope may indicate scope drift, and the reviewer should see that before merge.

## Proposed Behaviour

- Non-blocking: the check reports a `NON-BLOCKING` finding with an advisory ID and never changes the exit code.
- Input: the changed files from the diff, and the paths or directories the ticket names. Tickets that name no paths produce no finding.
- Output: one advisory line listing the unnamed files, for the reviewer to accept or reject.

## Status

- Not implemented. No check ID is reserved and no code exists.
- Non-blocking by design, so it cannot stop a merge or a Work Order ledger entry.
- Revisit after the first Work Order closes, and only if drift is seen in practice.
