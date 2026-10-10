## Agent skills

### Issue tracker

Issues and specs are tracked on GitHub. See `docs/agents/issue-tracker.md`.

### Triage labels

Default triage label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Domain docs are single-context. The glossary is `GLOSSARY.md`; `CONTEXT.md` only redirects to it. See `docs/agents/domain.md`.

## Context & Memory

This project uses the Basic Memory persistent memory app. When gathering context, agents should query the `wiki` project in Basic Memory to retrieve relevant information.
