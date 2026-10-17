"""Contract tests for safe tombstones of legacy skills (Ticket 10).

Validates that all 26 legacy skills are replaced with fail-closed safe tombstones,
auxiliary files are removed, frontmatter flags prevent autonomous model invocation,
line and token budgets are strictly respected, migration paths to successor deep modules
are documented, no destructive commands exist, and all active skills remain intact.
"""
import importlib
import os
import pathlib
import re
import sys
import unittest

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
new_skill = importlib.import_module("new-skill")

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# 26 Legacy Skills categorized by domain and mapped to their successor deep module
LEGACY_SKILLS = {
    # Knowledge / Wiki skills -> Successor: wiki-ops (9)
    "sk-wiki-maintenance": (
        "wiki-ops",
        "Routine automated maintenance, index verification, and health checks for personal wiki notes.",
    ),
    "sk-semantic-lint": (
        "wiki-ops",
        "Semantic linting and structural consistency verification across wiki entities.",
    ),
    "sk-index-governance": (
        "wiki-ops",
        "Index file formatting, link integrity checks, and folder governance across the wiki.",
    ),
    "sk-local-cloud-reconciliation": (
        "wiki-ops",
        "Reconciliation between local note files and remote or cloud sync targets.",
    ),
    "sk-supervised-ingest": (
        "wiki-ops",
        "Supervised ingestion of external notes and articles into the wiki knowledge base.",
    ),
    "sk-unsupervised-ingest": (
        "wiki-ops",
        "Automated background ingestion of raw notes into the wiki knowledge base.",
    ),
    "sk-wiki-stop": (
        "wiki-ops",
        "Emergency halt and fail-safe shutdown for wiki automated ingestion pipelines.",
    ),
    "sk-wiki-teach": (
        "wiki-ops",
        "Interactive teaching and ontology ingestion for wiki concept definitions.",
    ),
    "sk-email-ingest": (
        "wiki-ops",
        "Parsing and archiving incoming email digests into wiki notes.",
    ),
    # Task / Agile skills -> Successor: autonomous-scrum (3)
    "task-assistant": (
        "autonomous-scrum",
        "Daily standup preparation, sprint backlog updates, and task management.",
    ),
    "sk-triage": (
        "autonomous-scrum",
        "Issue triage, label assignment, and ticket prioritization workflows.",
    ),
    "sk-claude-weekly-task-consolidation": (
        "autonomous-scrum",
        "Weekly consolidation of completed tasks, backlogs, and status summaries.",
    ),
    # Agent tooling / Onboarding skills -> Successor: agent-ecosystem (4)
    "sk-onboarding": (
        "agent-ecosystem",
        "Environment setup and agent skill directory verification (all destructive commands neutralized).",
    ),
    "sk-cli-agent-onboarding": (
        "agent-ecosystem",
        "Command-line agent environment provisioning and workspace onboarding.",
    ),
    "sk-create-adapter": (
        "agent-ecosystem",
        "Scaffolding seam adapter wrappers for external CLI tools.",
    ),
    "sk-update": (
        "agent-ecosystem",
        "Centralized skill updating and synchronization from golden repository manifests.",
    ),
    # Academic / Writing skills -> Successor: academic-scholar (2)
    "sk-writing-coach": (
        "academic-scholar",
        "Academic and essay writing feedback, style guidance, and argument critique.",
    ),
    "sk-claude-daily-writing-journal-seed": (
        "academic-scholar",
        "Daily journal prompt seeding and academic writing scratchpad generation.",
    ),
    # Cadence / Techo / Hermes / Energy skills -> Successor: personal-cadence (8)
    "sk-claude-techo-evening-pull": (
        "personal-cadence",
        "Evening journal extraction, reflection capture, and daily shutdown routine.",
    ),
    "sk-codex-weekday-morning-brief": (
        "personal-cadence",
        "Morning agenda compilation, calendar review, and weekday priority briefing.",
    ),
    "sk-hermes-daily-audit": (
        "personal-cadence",
        "Daily audit of communications, scheduled alerts, and message activity.",
    ),
    "sk-hermes-energy-inventory-14-days": (
        "personal-cadence",
        "Multi-week personal energy level tracking and inventory analysis.",
    ),
    "sk-claude-draft-energy-map": (
        "personal-cadence",
        "Visual mapping and retrospective analysis of personal energy expenditure.",
    ),
    "sk-claude-daily-inbox-triage": (
        "personal-cadence",
        "Daily inbox sweep, notification sorting, and action-item triage.",
    ),
    "sk-claude-inbox-triage-nudge": (
        "personal-cadence",
        "Automated nudge reminders for unreviewed notifications and inbox items.",
    ),
    "sk-claude-weekly-review-prep": (
        "personal-cadence",
        "End-of-week review preparation, metric aggregation, and reflection synthesis.",
    ),
}

# 6 Active Skills that must be preserved untouched and functional
ACTIVE_SKILLS = {
    "daily-knowledge-maintenance",
    "knowledge-ingest",
    "knowledge-lint",
    "knowledge-run-audit",
    "seam-adapter",
    "ask-syafiq",
}


class TestSafeTombstones(unittest.TestCase):
    """Test suite validating fail-closed safe tombstones for all 26 legacy skills."""

    def test_legacy_skills_inventory_count(self):
        """Must have exactly 26 legacy skills mapped to successors."""
        self.assertEqual(len(LEGACY_SKILLS), 26)

    def test_all_26_legacy_skills_exist_and_contain_skill_md(self):
        """All 26 legacy skills must exist with a valid SKILL.md and no auxiliary files."""
        for skill_name in LEGACY_SKILLS:
            skill_dir = SKILLS_DIR / skill_name
            self.assertTrue(
                skill_dir.is_dir(),
                f"Legacy skill directory missing: {skill_dir}",
            )
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(
                skill_md.is_file(),
                f"Missing SKILL.md in legacy skill: {skill_dir}",
            )

            # Assert auxiliary files were purged (only SKILL.md should remain in legacy skill directory)
            all_files = [p for p in skill_dir.rglob("*") if p.is_file()]
            self.assertEqual(
                [skill_md],
                all_files,
                f"Legacy skill {skill_name} contains unexpected auxiliary files: {all_files}",
            )

    def test_frontmatter_flags_and_metadata(self):
        """Frontmatter must have disable-model-invocation: true, user-invoked: true, and valid metadata."""
        for skill_name, (successor, _) in LEGACY_SKILLS.items():
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            self.assertTrue(
                text.startswith("---\n"),
                f"Frontmatter missing opening delimiter in {skill_name}",
            )
            parts = text.split("---", 2)
            self.assertGreaterEqual(
                len(parts),
                3,
                f"Frontmatter missing closing delimiter in {skill_name}",
            )

            fm = new_skill.parse_yaml_lines(parts[1].splitlines())
            self.assertEqual(
                fm.get("name"),
                skill_name,
                f"Frontmatter name mismatch in {skill_name}",
            )
            self.assertTrue(
                fm.get("disable-model-invocation") is True,
                f"disable-model-invocation must be True in {skill_name}",
            )
            self.assertTrue(
                fm.get("user-invoked") is True,
                f"user-invoked must be True in {skill_name}",
            )

            desc = fm.get("description", "")
            self.assertIn(
                "Retired legacy skill.",
                desc,
                f"Description should declare retired status in {skill_name}",
            )
            self.assertIn(
                f"Superseded by {successor}.",
                desc,
                f"Description should mention successor in {skill_name}",
            )
            self.assertIn(
                f"Use when migrating legacy workflows to {successor}.",
                desc,
                f"Description should have 'Use when' migration clause in {skill_name}",
            )
            self.assertLessEqual(
                len(desc),
                1024,
                f"Description exceeds 1024 chars in {skill_name}",
            )
            self.assertIsNone(
                new_skill.FIRST_SECOND_PERSON.search(desc),
                f"Description must not use first/second person in {skill_name}",
            )

            metadata = fm.get("metadata", {})
            self.assertEqual(
                metadata.get("origin"),
                "original",
                f"metadata.origin must be 'original' in {skill_name}",
            )
            self.assertEqual(
                metadata.get("category"),
                "tombstone",
                f"metadata.category must be 'tombstone' in {skill_name}",
            )
            self.assertEqual(
                metadata.get("agent_involvement"),
                "full",
                f"metadata.agent_involvement must be 'full' in {skill_name}",
            )

    def test_line_and_token_budget_limits(self):
        """SKILL.md must be strictly <= 100 lines and < 700 tokens for each legacy skill."""
        for skill_name in LEGACY_SKILLS:
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            lines = text.splitlines()

            self.assertLessEqual(
                len(lines),
                100,
                f"{skill_name} exceeds 100 line limit (has {len(lines)} lines)",
            )

            est_count = new_skill.estimate_tokens(text)
            self.assertLess(
                est_count,
                700,
                f"{skill_name} exceeds 700 token limit (has {est_count} tokens)",
            )

    def test_successor_and_migration_instructions(self):
        """Tombstone body must state fail-closed notice, migration command, and successor mapping."""
        for skill_name, (successor, capability) in LEGACY_SKILLS.items():
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")

            self.assertIn(
                f"# SAFE TOMBSTONE: {skill_name} (RETIRED)",
                text,
                f"Header missing in {skill_name}",
            )
            self.assertIn(
                f"> **Successor Module**: `{successor}`",
                text,
                f"Successor blockquote missing in {skill_name}",
            )
            self.assertIn(
                "## Fail-Closed Notice",
                text,
                f"Fail-closed section missing in {skill_name}",
            )
            self.assertIn(
                "zero mutations",
                text,
                f"Zero mutations guarantee missing in {skill_name}",
            )
            self.assertIn(
                "zero scripts",
                text,
                f"Zero scripts guarantee missing in {skill_name}",
            )
            self.assertIn(
                f"npx skills add skay93m/skills --skill {successor}",
                text,
                f"Migration install command missing in {skill_name}",
            )
            self.assertIn(
                f"- **Retired capability**: {capability}",
                text,
                f"Capability explanation missing in {skill_name}",
            )
            self.assertIn(
                f"- **Successor deep module**: `{successor}`",
                text,
                f"Successor mapping missing in {skill_name}",
            )

    def test_no_destructive_commands_or_scripts(self):
        """Assert no legacy skill contains destructive commands or unsafe shell operations."""
        destructive_patterns = [
            r"\brm\s+-[rf]{1,2}\b",
            r"\bdelete\s+directory\b",
            r"\bdelete\s+folders?\b",
            r"\bclean\s+the\s+agent-specific\b",
            r"\bpurge\b",
            r"\bshutil\.rmtree\b",
            r"\|\s*(sudo\s+)?(ba|z)?sh\b",
            r"docker\.sock",
        ]
        compiled = [re.compile(p, re.IGNORECASE) for p in destructive_patterns]

        for skill_name in LEGACY_SKILLS:
            skill_dir = SKILLS_DIR / skill_name
            for p in skill_dir.rglob("*"):
                if p.is_file():
                    content = p.read_text(encoding="utf-8")
                    for pat in compiled:
                        match = pat.search(content)
                        self.assertIsNone(
                            match,
                            f"Destructive pattern '{pat.pattern}' found in {p}: '{match.group(0) if match else ''}'",
                        )

    def test_active_skills_untouched_and_functional(self):
        """All 6 active skills must remain intact, functional, and NOT tombstoned."""
        for skill_name in ACTIVE_SKILLS:
            skill_dir = SKILLS_DIR / skill_name
            self.assertTrue(
                skill_dir.is_dir(),
                f"Active skill directory missing: {skill_dir}",
            )
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(
                skill_md.is_file(),
                f"Active skill missing SKILL.md: {skill_md}",
            )
            text = skill_md.read_text(encoding="utf-8")

            self.assertNotIn(
                "SAFE TOMBSTONE",
                text,
                f"Active skill {skill_name} must NOT be tombstoned!",
            )
            self.assertNotIn(
                "category: tombstone",
                text,
                f"Active skill {skill_name} must NOT have tombstone category!",
            )
            self.assertIn(
                f"name: {skill_name}",
                text,
                f"Active skill {skill_name} name mismatch in SKILL.md",
            )


if __name__ == "__main__":
    unittest.main()
