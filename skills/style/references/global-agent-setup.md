# Global Agent Setup

Make every agent session, in any repository, load the style standard. Sessions inside this repository already load it through `AGENTS.md`, so this setup covers sessions elsewhere.

## Steps

1. Note the absolute path of the local clone of this repository. Call it `$REPO` in the steps below. Agents do not expand variables, so replace `$REPO` with the real path before you save the file.
2. Add the instruction block below to the global instruction file of each agent you use:
   - Claude Code: `~/.claude/CLAUDE.md`.
   - Codex: `~/.codex/AGENTS.md`.
   - Other agents: their global rules or system prompt file.
3. Verify the file exists at that path: `test -f "$REPO/skills/style/SKILL.md" && echo ok`.

## Instruction Block

Paste this block, with `$REPO` replaced:

```text
Mandatory ambient standard: before writing any document, comment, code artefact, or reply for Syafiq, read and follow the style standard at $REPO/skills/style/SKILL.md. It requires British English, zero em dashes, zero horizontal dividers, and clean markdown tables.
```

## Claude Code Alternative

In `~/.claude/CLAUDE.md`, add an import line that loads the skill at session start:

```text
@$REPO/skills/style/SKILL.md
```

Replace `$REPO` with the absolute path, as in step 1.

## Keeping It Current

- Change the standard itself through a pull request to `main`. The global files only hold the path, so they need no edits when the standard changes.
- Update the global files only if the clone moves.
- Test the setup by starting a new session and asking the agent to state the four mandatory style rules. A correct answer names British spelling, zero em dashes, zero horizontal dividers, and clean tables.
