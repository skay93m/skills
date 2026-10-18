---
title: Authorised Skill Repositories
tags: [governance, skills, allowlist]
type: authority
---

# Authorised Skill Repositories

> **Note:** Only Syafiq may add or remove repositories from this list. Automation must never silently expand this allowlist.

| Source | Upstream repository | Local canonical path |
|---|---|---|
| Matt Pocock skills | [mattpocock/skills](https://github.com/mattpocock/skills) | `~/.agents/mattpocock-skills/skills` |
| Basic Memory skills | [basicmachines-co/basic-memory-skills](https://github.com/basicmachines-co/basic-memory-skills) | `~/.agents/basic-memory-skills` |
| Syafiq Kay skills | [skay93m/skills](https://github.com/skay93m/skills) | `~/Documents/skills` (workspace) and `~/.agents/skills` (installed) |
| Thinking partner | [mattnowdev/thinking-partner](https://github.com/mattnowdev/thinking-partner) | `~/.agents/skills/thinking-partner` |

## Observations
- [authority] Only Syafiq may modify the authorised repositories list #governance
- [convention] Skills installed via the agent skills standard resolve to local canonical directories #paths

## Relations
- defined_by [[GLOSSARY]]
- relates_to [[coordinator-protocol]]
