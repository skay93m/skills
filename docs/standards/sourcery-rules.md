# Sourcery AI Dashboard Rules

Sourcery's PR Reviewer requires custom rules to be added via the Sourcery Dashboard (up to 3,000 characters each). 

Copy and paste the following rules into your Sourcery Dashboard to enforce the repository's hard constraints:

## Rule 1: Security and Privacy Constraints
**Pattern/Scope:** `*`
**Rule Text:**
```
Check the pull request for any exposed secrets, private Wiki content, personal information, local paths, private prompts, or internal URLs. If any of these are found, or if there are unresolved material security issues, you MUST flag them as blocking issues and recommend requesting changes. You must not recommend approval if these risks are present. (Standard version: 2026-10-10)
```

## Rule 2: Design and Skill Duplication
**Pattern/Scope:** `skills/**/SKILL.md`, `scripts/**`
**Rule Text:**
```
Review the implementation against agreed design principles. Ensure there is no duplication with authorised upstream skills. If the implementation violates design principles in a material way, or if evidence is insufficient for a confident recommendation, you must flag these as blocking. Additionally, surface any optimisation concerns. (Standard version: 2026-10-10)
```

## Rule 3: Review Standard Currency
**Pattern/Scope:** `*`
**Rule Text:**
```
When reviewing this pull request, identify the principle versions and timestamps you are using for the review. If there is no applicable review standard or its currency cannot be established, you must flag this as a blocking issue and do not recommend approval. (Standard version: 2026-10-10)
```

## Rule 4: Actionable Handoff Prompt
**Pattern/Scope:** `*`
**Rule Text:**
```
At the end of your review, produce a concise handover prompt that an agent can use to diagnose and plan repairs based on your exact findings. Clearly distinguish blocking issues from non-blocking issues. (Standard version: 2026-10-10)
```
