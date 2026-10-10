# 2026-10-10-commission-context-sourcery-pr-reviewer-standard

## What this is

The commissioning agent's written answers, pasted by Syafiq on 2026-10-10, about the purpose of the standards-bootstrap research. They are kept here faithfully paraphrased so that later synthesis does not depend on chat history. This is a source-facing capture of an instruction to the research, not a canonical statement and not a standard.

## Purpose of the standard

Sourcery acts as a pull request reviewer, not as the final authority. It should produce a balanced recommendation (approve, request changes or comment) against the canonical design, security and optimisation standard, explain its reasoning and name exact findings. It must not merge or approve on Syafiq's behalf, and Syafiq has final authority over approval and merging from develop into main. Whether Sourcery should enforce a blocking GitHub status check is not decided. The preferred initial mode is advisory or dry-run review. Blocking should be limited to having no usable standard to review against, being unable to establish the standard's currency, or finding severe public-surface or security violations.

## Scope

The first implementation covers the syafiq-kay-skills repository. Extension to other repositories later is intended, but that broader scope is not decided. "Audit the codebase" means reviewing the pull request diff together with its relevant repository context: affected skills, supporting scripts, references, configuration and public-surface implications. A full unrelated audit on every pull request is not required.

## Authors

Pull requests may be written by agents, by Syafiq or by both. The quality bar is the same for all. A pull request should disclose agent involvement and preserve provenance where relevant, but authorship must not lower the review standard.

## Form of the standard

Use both a canonical human-readable standard extracted into the repository's docs/ folder for each pull request, and Sourcery's native configuration or instruction mechanism if one exists. Do not invent a parallel rules system if Sourcery already provides one. Research should report exactly how Sourcery discovers and applies instructions.

## Hard constraints

Sourcery must never recommend approval when: there is no applicable review standard or its currency cannot be established; the pull request exposes secrets, private Wiki content, personal information, local paths, private prompts or internal URLs; material security issues remain unresolved; the implementation violates the agreed design principles in a material way; or the evidence is insufficient for a confident recommendation. It must surface optimisation concerns, duplication with authorised upstream skills, and security and public-repository risks.

## Definition of done

The standard is usable when it can review a real pull request on develop, identify the principle versions and timestamps it used, produce a balanced recommendation with exact findings, distinguish blocking from non-blocking issues, and generate a concise handover prompt for an agent to diagnose and plan repairs. Syafiq must be able to review the evidence and make the final decision.

## Observations

- [purpose] Sourcery reviews and recommends; Syafiq decides and merges (as relayed by the commissioning agent).
- [scope] First implementation covers syafiq-kay-skills only; review covers the diff plus relevant repository context.
- [constraint] Same quality bar for agent-authored and human-authored pull requests; agent involvement and provenance are disclosed.
- [constraint] Never recommend approval without an applicable standard whose currency can be established, or with exposed secrets, private Wiki content, personal information, local paths, private prompts or internal URLs, or unresolved security issues.
- [decision_open] Whether Sourcery runs a blocking status check is not decided; advisory or dry-run is preferred first.
- [decision_open] Extension beyond syafiq-kay-skills is not decided.
- [requirement] Output must name the principle versions and timestamps used, give exact findings, separate blocking from non-blocking and produce a concise handover prompt for repair planning.
- [gap] How Sourcery discovers and applies instructions was requested as research and was not answered by the first-batch sources.
