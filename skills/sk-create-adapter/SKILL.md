---
name: sk-create-adapter
description: >-
  Use this skill when the user asks to modify, adapt, or wrap an existing skill (such as a Matt Pocock skill) to change its output behavior (like forcing it to write to a Wiki) without hard-forking the upstream logic.
---

# Create Adapter Skill

When the user triggers this skill, you are acting as an Agent Architect. Your job is to create a new "Adapter Skill" that uses the **Agentic Proxy Pattern**.

This pattern delegates the core reasoning/logic to an existing upstream skill, but overrides the I/O (Input/Output) operations—for example, forcing the agent to use Basic Memory MCP tools instead of local file system commands.

### Step 1: Gather Requirements
Ask the user for three things (if they haven't provided them):
1. **Upstream Skill Path:** The absolute path to the `SKILL.md` they want to adapt (e.g., `~/.agents/mattpocock-skills/...`).
2. **Adapter Name:** The name of the new adapter skill (e.g., `sk-wiki-teach`).
3. **The Override Rules:** Exactly what behavior needs to change (e.g., "Save files to Basic Memory wiki instead of local disk").

### Step 2: Scaffold the Directory
Once requirements are gathered, create the skill folder inside the user's custom skills directory:
`mkdir -p ~/.agents/syafiq-kay-skills/skills/<adapter-name>`

### Step 3: Write the Adapter SKILL.md
Create the `SKILL.md` file using this template. **You must customize the instructions based on the user's override rules.**

```markdown
---
name: <adapter-name>
description: >-
  [Write a highly specific trigger description here, explaining when to use this adapter instead of the default skill]
---

# [Adapter Name] (Adapter)

### 1. Ingest Upstream Methodology
First, read the upstream instructions located here:
`[Upstream Skill Path]`

Adopt ALL of its core logic, philosophies, and workflows.

### 2. The I/O Override
You MUST IGNORE the upstream skill's instructions regarding [insert what is being overridden, e.g., file creation].
Instead, you must strictly follow these rules:
- [Insert specific user override rule 1]
- [Insert specific user override rule 2]

### 3. Execution
Proceed with the upstream workflow, strictly applying the overrides defined in Step 2.
```

### Step 4: Confirmation
Save the file, then ask the user to test their new adapter skill.
