---
name: sk-local-cloud-reconciliation
description: Retired legacy skill. Superseded by wiki-ops. Retained as a fail-closed tombstone through v0.3.0. Use when migrating legacy workflows to wiki-ops.
disable-model-invocation: true
user-invoked: true
metadata:
  origin: original
  agent_involvement: full
  category: tombstone
---

# SAFE TOMBSTONE: sk-local-cloud-reconciliation (RETIRED)

> **Status**: RETIRED / DEPRECATED  
> **Successor Module**: `wiki-ops`  
> **Tombstone Policy**: Retained through Extended Tombstone Period (at least v0.3.0).

## Fail-Closed Notice
This legacy skill has been retired and performs **zero mutations** and executes **zero scripts**.

## Migration
To install and use the successor deep module:
```bash
npx skills add skay93m/skills --skill wiki-ops
```

### Successor Mapping
- **Retired capability**: Reconciliation between local note files and remote or cloud sync targets.
- **Successor deep module**: `wiki-ops`
