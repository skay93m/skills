---
name: sk-create-adapter
description: Retired legacy skill. Superseded by agent-ecosystem. Retained as a fail-closed tombstone through v0.3.0. Use when migrating legacy workflows to agent-ecosystem.
disable-model-invocation: true
user-invoked: true
metadata:
  origin: original
  agent_involvement: full
  category: tombstone
---

# SAFE TOMBSTONE: sk-create-adapter (RETIRED)

> **Status**: RETIRED / DEPRECATED  
> **Successor Module**: `agent-ecosystem`  
> **Tombstone Policy**: Retained through Extended Tombstone Period (at least v0.3.0).

## Fail-Closed Notice
This legacy skill has been retired and performs **zero mutations** and executes **zero scripts**.

## Migration
To install and use the successor deep module:
```bash
npx skills add skay93m/skills --skill agent-ecosystem
```

### Successor Mapping
- **Retired capability**: Scaffolding seam adapter wrappers for external CLI tools.
- **Successor deep module**: `agent-ecosystem`
