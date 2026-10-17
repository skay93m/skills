---
name: sk-hermes-energy-inventory-14-days
description: Retired legacy skill. Superseded by personal-cadence. Retained as a fail-closed tombstone through v0.3.0. Use when migrating legacy workflows to personal-cadence.
disable-model-invocation: true
user-invoked: true
metadata:
  origin: original
  agent_involvement: full
  category: tombstone
---

# SAFE TOMBSTONE: sk-hermes-energy-inventory-14-days (RETIRED)

> **Status**: RETIRED / DEPRECATED  
> **Successor Module**: `personal-cadence`  
> **Tombstone Policy**: Retained through Extended Tombstone Period (at least v0.3.0).

## Fail-Closed Notice
This legacy skill has been retired and performs **zero mutations** and executes **zero scripts**.

## Migration
To install and use the successor deep module:
```bash
npx skills add skay93m/skills --skill personal-cadence
```

### Successor Mapping
- **Retired capability**: Multi-week personal energy level tracking and inventory analysis.
- **Successor deep module**: `personal-cadence`
