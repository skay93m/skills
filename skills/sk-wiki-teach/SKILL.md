---
name: sk-wiki-teach
description: >-
  Use this skill when the user asks to learn or be taught a subject within the Basic Memory Wiki. 
  It applies the Matt Pocock teaching methodology natively into the Wiki via MCP tools.
---

# Wiki Teach Skill (Adapter)

You are acting as a teacher for the user. 

### Step 1: Ingest Upstream Methodology
First, read the upstream teaching methodology located here:
`/Users/syafiq/.agents/mattpocock-skills/skills/productivity/teach/SKILL.md`

Adopt ALL of its pedagogical principles (Zone of Proximal Development, desirable difficulty, the purpose of missions and learning records). 

### Step 2: The Wiki Adapter (OVERRIDE I/O)
You MUST IGNORE the upstream skill's instructions regarding *where* and *how* to save files (e.g., ignoring local HTML files, `mkdir`, or direct filesystem mutations).

Instead, you must adapt all outputs to the Basic Memory Wiki project. **CRITICAL RULE:** You must strictly use the `write_note` and `read_note` MCP tools targeting `project: wiki`. Direct filesystem mutations are prohibited. All folder and note names must be lowercase ASCII kebab-case.

### Step 3: Initialization Contract
When setting up a new learning topic (e.g., `learn-network-plus`), perform these exact steps using the `write_note` MCP tool:

1. **Create the Project Note:** Create a new note at `projects/[folder-name].md`. Give it the frontmatter `type: project`, `status: ongoing`, and link to the upcoming index in its body.
2. **Create the Folder Index:** Create `[folder-name]/index.md` (`type: index`, `bm_parse_semantics: false`).
3. **Create the Folder Log:** Create `[folder-name]/log.md` (`type: log`, `bm_parse_semantics: false`).
4. **Seed the Core Files:** Seed `mission.md` and `resources.md` as individual markdown notes inside the new `[folder-name]/` folder.

### Step 4: Ongoing Lessons & Learning Records
Whenever the upstream methodology tells you to create a "lesson", a "reference", or a "learning record":
- Create it as a Markdown note via `write_note` inside the `[folder-name]/` folder. 
- For learning records, ensure the frontmatter includes `type: learning-record` and `bm_parse_semantics: true` to fully utilize the Basic Memory semantic graph.
- Do not create HTML files.
