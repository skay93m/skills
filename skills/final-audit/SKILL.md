---
name: final-audit
description: Use when a student needs a complete essay or dissertation checked before submission for audit defects and a verdict.
disable-model-invocation: true
model: original
metadata:
  origin: original
  agent_involvement: full
  category: academic
---

# Final Audit

Audit a complete essay or dissertation manuscript before submission. Work through the steps in order. A Blocking defect stops the audit after its scan.

## Flag Format

Each flag gives the tier and rule label, the rule, `Line N` with the student's unchanged span, and a one or two sentence defect explanation. An omission reads `Line absent` without a quotation; a declaration flag reads `Line declaration`. Do not give replacement wording or code.

## Line Numbering

Number each prose sentence from 1 across paragraphs in order. Do not number headings, a title page or the bibliography. If the text is unnumbered, number it unchanged, state the total and wait for the student's confirmation before auditing. Every flag cites its line.

## Steps

### Read the Governing Documents

Read SOUL.md and ACADEMIC_STANDARDS.md from the working directory by bare name; if either is missing, name it and stop before the next step. Follow the shared authorship, flag-only, privacy, citation and style rules in SOUL.md and ACADEMIC_STANDARDS.md.

### Validate the Manuscript

Confirm that the complete manuscript is present, its module and word limit are stated in the module brief, and its prose lines follow Line Numbering. The module brief and KCL Academic Regulations take precedence where they conflict with ACADEMIC_STANDARDS.md.

### Scan for Blocking Defects

Check for AI-generated or AI-rewritten prose, plagiarism or unacknowledged third-party text, fabricated or unverified citations, and confidential clinical or privileged data under section 6.7. Evidence includes a tool artefact, text marked as machine-generated, prose the student cannot account for in the audit trail, or unattributed third-party material. A citation without recorded verification in the manuscript or audit trail is Blocking; identifiable clinical details and protected records are also Blocking. Style alone is not evidence. Any Blocking flag fails the audit and goes straight to Issue the Verdict without running later checks.

### Verify the Coursework Declaration

Check the declaration against section 7 of ACADEMIC_STANDARDS.md. It must be on the title page or immediately before the OSCOLA bibliography, use the prescribed heading, match the template with the tool named, and contain no unfilled placeholder. Each failed condition is a Major flag under Coursework Declaration fault.

### Check Major Defects

Check citations against the OSCOLA 4th edition rules in section 4, including neutral citations, report series, statutory section numbers, journal bracket style and jurisdiction. Under section 5, check contentious claims for pinpoints, empirical assertions for peer-reviewed or official support, and binding counter-precedent only when named in the manuscript or audit trail. Never supply authority from memory. A declaration fault is Major.

### Check Minor Defects

Check prose for nominalisations, passive voice where the actor is clear, needless filler, and spelling or punctuation divergences under sections 1 to 3. Include em dashes, double quotation marks outside nested quotations, and American spellings. Each flag cites its line.

### Issue the Verdict

Fail with `AUDIT_FAILED` if any Blocking or Major flag was raised. Pass with `AUDIT_PASSED` only when neither tier has a flag and the declaration is present and exact. Minor flags do not change the verdict. State `Verdict: AUDIT_PASSED` or `Verdict: AUDIT_FAILED` on its own line, then list flags in Blocking, Major, Minor order with each tier's count, recording what was done and what comes next. A pass certifies only these mechanical checks and does not replace citation verification or the viva voce.

## Coursework Declaration

Section 7 of ACADEMIC_STANDARDS.md holds the mandatory Generative Artificial Intelligence declaration. Check its location, heading, exact statement with the tool placeholder replaced, and absence of any remaining placeholder. Raise a separate flag for each failed condition; never fill in or reproduce the declaration.
