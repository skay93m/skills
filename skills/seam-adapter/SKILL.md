---
name: seam-adapter
description: Tells a scheduled agent task what to put in its run result so the result is a valid seam envelope. Use when a scheduled task runs a seam capability such as knowledge.ingest in report-only or propose-only mode and must return a machine-checkable result.
metadata:
  origin: original
  agent_involvement: full
  category: knowledge
---

# Seam adapter

Draft. Speaks only the public seam: one envelope per run. It knows nothing about any storage backend, and it grants no permission. Full field rules and a worked example are in [references/envelope-reference.md](references/envelope-reference.md).

## When to use

The task prompt names a capability, a mode and a grant set. If any of the three is missing, return a `refused` envelope with `error-category: not-permitted` and do nothing else.

## What to return

End the run result with one JSON object, the envelope, in a fenced `json` block. Put nothing private in it. The object has exactly these keys:

- `seam-version`, `capability`, `capability-version`: three separate fields, copied from the task prompt.
- `run-reference`: the opaque reference the task prompt supplies. Never invent or derive one.
- `status`, `disposition`, `approval-state`, `error-category`: closed values only (see the reference).
- `grant-reference`: the opaque reference the task prompt supplies for the grant set, or `""` when no grant applies.
- `counts`: the six integer keys `seen`, `reported`, `proposed`, `applied`, `skipped`, `failed`.
- `mutation-summary`: for each of the five operation classes, the integers `requested`, `granted`, `applied`, `refused`.
- `extensions`: `{}` unless the task prompt names an extension.

## Rules

1. Allowed modes are `report-only` and `propose-only`. Never claim `apply`, `applied` or a delete. `counts.applied` is `0` and `apply-change` and `delete` stay all zeros except `requested` and `refused`.
2. A mode grants nothing. Use an operation class only if the grant set lists it for the capability and the mode permits it.
3. Anything requested outside the grant set gives `status: refused` and `error-category: not-permitted`. Count it as `requested` and `refused`, never `granted`.
4. `succeeded` has `error-category` set to `""`. `failed` means the run ran and broke; `refused` means it was not allowed to run.
5. Counts only. Never include names, titles, paths, links, checksums, identifiers, source text, query text, diagnostics or before and after content, in the envelope or in its extensions.
6. Unknown extension keys in the task prompt are ignored. Never add an extension that adds a value, grants permission or changes a core field.
7. Report what was observed. If the run could not complete, say `failed` with `backend-unavailable` or `internal`; do not guess counts.

## Check

The repository's conformance check validates the envelope against the capability profile and the grant set on synthetic data. Treat a failing envelope as a failed run; do not repair it by editing values to pass.

## Out of scope

Release, ratification, activation, tags, any apply mode, any delete grant, and any backend binding. Those belong to the owner and to the backend project.
