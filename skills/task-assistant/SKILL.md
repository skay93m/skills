---
name: task-assistant
description: Retired legacy skill. Superseded by autonomous-scrum. Retained as a fail-closed tombstone through v0.3.0. Use when migrating legacy workflows to autonomous-scrum.
disable-model-invocation: true
user-invoked: true
metadata:
  origin: original
  agent_involvement: full
  category: tombstone
---

# SAFE TOMBSTONE: task-assistant (RETIRED)

> **Status**: RETIRED / DEPRECATED  
> **Successor Module**: `autonomous-scrum`  
> **Tombstone Policy**: Retained through Extended Tombstone Period (at least v0.3.0).

## Fail-Closed Notice
This legacy skill has been retired and performs **zero mutations** and executes **zero scripts**.

## Migration
To install and use the successor deep module:
```bash
npx skills add skay93m/skills --skill autonomous-scrum
```

### Successor Mapping
- **Retired capability**: Daily standup preparation, sprint backlog updates, and task management.
- **Successor deep module**: `autonomous-scrum`
