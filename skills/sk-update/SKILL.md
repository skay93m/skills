---
name: sk-update
description: Runs the deterministic terminal script to update all agent skills and auto-heal any configuration drift.
---

# sk-update

This skill delegates the task of updating centralized repositories and verifying configuration integrity to the deterministic bash script located at `~/.local/bin/skills`. 

This is incredibly token-efficient, as the agent does not need to perform complex git operations or read multiple configuration files manually.

## Trigger

Run this skill when:
- The user requests to "update skills".
- The user invokes `/sk-update`.
- The user wants to repair configuration drift across their local agents.

## Instructions

When invoked, execute the following command in the terminal:

```bash
skills update --heal
```

### Reporting
After the command completes, output the exact terminal response to the user. That's it!
