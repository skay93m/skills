## Agent skills

### Issue tracker

Issues and specs are tracked on GitHub. See `docs/agents/issue-tracker.md`.

### Domain docs

Domain docs are single-context. See `docs/agents/domain.md`.

## Context & Memory

This project uses the Basic Memory persistent memory app. When gathering context, agents should query the `wiki` project in Basic Memory to retrieve relevant information.

## Session start
On session start, run `./scripts/trial.sh` before doing anything else.

## General advice
Write clean, maintainable code. Follow best practices. The repository has a skills folder, a docs folder and a scripts folder. Always be careful and write clean code.
