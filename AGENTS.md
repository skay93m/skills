## Agent skills

### Issue tracker

Issues and specs are tracked on GitHub. See `docs/agents/issue-tracker.md`.

### Triage labels

Default triage label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Domain docs are single-context. The glossary is `GLOSSARY.md`; `CONTEXT.md` only redirects to it. See `docs/agents/domain.md`.

### Coordinator & subagent protocol

All feature work, refactoring, and multi-step tasks follow the Coordinator & Subagent Protocol (pure delegation, cheaper flash subagents, two-axis adversarial review loop: Spec + Standards, zero approval on latent defects). See `docs/agents/coordinator-protocol.md`.

## Context & Memory

This project uses the Basic Memory persistent memory app. When gathering context, agents should query the `sk-wiki` project in Basic Memory to retrieve relevant information.
