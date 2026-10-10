---
name: sk-onboarding
description: Enforces the centralized ~/.agents configuration by checking for and removing legacy skill installations from agent-specific directories, ensuring skills.json points to the canonical repositories.
---

# sk-onboarding

This skill is designed to ensure that the AI agent strictly uses the centralized `~/.agents` configuration architecture for managing custom skills, rather than relying on agent-specific configuration directories (like `~/.gemini`, `~/.claude`, or `~/.codex`).

## Trigger

Run this skill when:
- Setting up a new machine or environment.
- An agent seems to be using an outdated version of a skill.
- You suspect configuration drift or duplicate skill definitions clashing with one another.
- The user explicitly asks to run the onboarding or verify skill configuration.

## Instructions

When invoked, you MUST strictly follow these steps:

### 1. Verify the Golden Configuration
Check the configuration files:
- `~/.gemini/config/skills.json`
- `~/.claude/skills.json`
- `~/.codex/skills.json`

Ensure that they exist and their contents identically specify the centralized paths. The golden layout MUST include pointers to:
- `~/.agents/mattpocock-skills/skills/engineering`
- `~/.agents/mattpocock-skills/skills/productivity`
- `~/.agents/basic-memory-skills`
- `~/.agents/syafiq-kay-skills/skills`
- `~/.agents/agy-builtin-skills/skills`

If the files deviate from this, rewrite them to enforce this exact configuration. Ensure no other entries exist.

### 2. Purge Legacy/Duplicate Installations
To prevent naming collisions with the canonical repositories loaded via `skills.json`, aggressively clean the agent-specific auto-discovery directories.

Run commands to remove any manually copied skills or symlinks inside:
- `~/.gemini/config/skills/`
- `~/.claude/skills/`
- `~/.codex/skills/`
- `~/.agents/skills/`

Delete folders and symlinks matching `memory-*`, `kensho-*`, or any skill that is already provided by the centralized repositories.

### 3. Verify the Update Script
Ensure the `skills update` script exists at `~/.local/bin/skills` and is executable. Ensure it is configured to pull updates for `mattpocock-skills`, `basic-memory-skills`, and gracefully handle `syafiq-kay-skills` (if initialized as a git repository).

### 4. Report Status
After completing the onboarding checks, output a brief summary to the user confirming that all configurations are perfectly aligned with the `~/.agents` golden standard and all duplicate skills have been purged.
