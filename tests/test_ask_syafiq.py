"""Tests for the master router skill (skills/ask-syafiq/SKILL.md).

Validates entrypoint existence, strict line and token budgets, frontmatter properties,
terminal reference invariants (Standard S5), coverage of all 8 active workspaces,
6 deep modules, upstream engineering pipeline, and execution phase boundaries.
"""
import importlib
import os
import pathlib
import re
import sys
import unittest

# Import new-skill module from scripts directory
SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
new_skill = importlib.import_module("new-skill")

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "ask-syafiq"
SKILL_MD = SKILL_DIR / "SKILL.md"
WORKSPACE_MATRIX_MD = SKILL_DIR / "references" / "workspace-matrix.md"
ROUTING_TABLE_MD = SKILL_DIR / "references" / "routing-table.md"
MANIFEST_YAML = REPO_ROOT / "manifests" / "ask-syafiq.yaml"

WORKSPACES = [
    "skills",
    "sk-wiki",
    "awt",
    "kos",
    "syafiq-kay.github.io",
    "neko",
    "hermes",
    "archive",
]

DEEP_MODULES = [
    "wiki-ops",
    "autonomous-scrum",
    "agent-ecosystem",
    "academic-scholar",
    "personal-cadence",
    "thinking-partner",
]

PIPELINE_STEPS = [
    "/grill-me",
    "/to-spec",
    "/to-tickets",
    "/tdd",
    "/code-review",
    "/pr",
]

PHASE_BOUNDARIES = [
    "Continue",
    "/clear",
    "/handoff",
    "Subagent",
    "/compact",
]


class TestAskSyafiqMasterRouter(unittest.TestCase):
    """Test suite for ask-syafiq master router skill."""

    def setUp(self):
        self.assertTrue(SKILL_MD.exists(), f"Missing required file: {SKILL_MD}")
        self.skill_text = SKILL_MD.read_text(encoding="utf-8")
        self.skill_lines = self.skill_text.splitlines()

    def test_skill_file_exists_and_non_empty(self):
        """SKILL.md must exist and contain non-empty content."""
        self.assertTrue(SKILL_MD.is_file())
        self.assertGreater(len(self.skill_text.strip()), 0)

    def test_skill_line_budget_strictly_le_100(self):
        """SKILL.md line count must be strictly <= 100 lines (Standard S4)."""
        line_count = len(self.skill_lines)
        self.assertLessEqual(
            line_count,
            100,
            f"skills/ask-syafiq/SKILL.md has {line_count} lines, exceeding the 100 line budget.",
        )

    def test_skill_token_budget_strictly_lt_700(self):
        """SKILL.md token count estimate must be strictly < 700 tokens."""
        est_count = new_skill.estimate_tokens(self.skill_text)
        self.assertLess(
            est_count,
            700,
            f"Estimated tokens ({est_count}) exceeds the 700 token budget.",
        )

    def test_frontmatter_properties(self):
        """Verify frontmatter properties adhere to specifications and standards."""
        # Extract frontmatter block
        self.assertTrue(self.skill_text.startswith("---\n"))
        parts = self.skill_text.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Frontmatter not properly delimited by '---'")
        fm_text = parts[1]

        # Use new_skill YAML parser
        fm = new_skill.parse_yaml_lines(fm_text.splitlines())
        self.assertEqual(fm.get("name"), "ask-syafiq")
        self.assertTrue(fm.get("disable-model-invocation") is True)
        self.assertTrue(fm.get("user-invoked") is True)
        self.assertEqual(fm.get("version"), "0.2.0")
        self.assertEqual(fm.get("provenance"), "original")

        desc = fm.get("description", "")
        self.assertIn("Use when", desc)
        self.assertLessEqual(len(desc), 1024)
        self.assertIsNone(
            new_skill.FIRST_SECOND_PERSON.search(desc),
            "Description must not use first or second person pronouns.",
        )

        metadata = fm.get("metadata", {})
        self.assertIsInstance(metadata, dict)
        self.assertEqual(metadata.get("origin"), "original")
        self.assertEqual(metadata.get("agent_involvement"), "full")
        self.assertEqual(metadata.get("category"), "router")

    def test_manifest_exists_and_validates(self):
        """Verify manifests/ask-syafiq.yaml exists and passes manifest schema validation."""
        self.assertTrue(MANIFEST_YAML.exists(), f"Missing manifest file: {MANIFEST_YAML}")
        manifest_text = MANIFEST_YAML.read_text(encoding="utf-8")
        manifest = new_skill.parse_manifest(manifest_text)

        # Validate against standard schema
        new_skill.validate_manifest(manifest)

        self.assertEqual(manifest.get("name"), "ask-syafiq")
        self.assertTrue(manifest.get("disable-model-invocation") is True)
        self.assertTrue(manifest.get("user-invoked") is True)
        self.assertEqual(manifest.get("version"), "0.2.0")
        self.assertEqual(manifest.get("provenance"), "original")

        budgets = manifest.get("budgets", {})
        self.assertEqual(budgets.get("line-budget"), 100)
        self.assertEqual(budgets.get("token-budget"), 700)

        refs = manifest.get("references", [])
        self.assertIn("references/workspace-matrix.md", refs)
        self.assertIn("references/routing-table.md", refs)

        router = manifest.get("router", {})
        self.assertEqual(router.get("domain"), "general")
        self.assertIn("ask syafiq", router.get("intents", []))
        self.assertIn("workspace detection", router.get("intents", []))

    def test_terminal_reference_files_exist_and_are_terminal(self):
        """Verify terminal references exist, are terminal, and contain NO outbound markdown links (Standard S5)."""
        link_pattern = re.compile(r"\]\((?!https?://|#|mailto:)([^)#\s]+\.md)")

        for ref_path in [WORKSPACE_MATRIX_MD, ROUTING_TABLE_MD]:
            self.assertTrue(ref_path.exists(), f"Terminal reference missing: {ref_path}")
            text = ref_path.read_text(encoding="utf-8")
            self.assertIn(
                "This reference is terminal",
                text,
                f"Terminal disclaimer missing in {ref_path}",
            )
            matches = link_pattern.findall(text)
            self.assertEqual(
                matches,
                [],
                f"Reference file {ref_path} violates terminal invariant by linking to markdown files: {matches}",
            )

    def test_all_8_workspaces_documented(self):
        """Verify all 8 active repositories are documented in both SKILL.md and workspace-matrix.md."""
        matrix_text = WORKSPACE_MATRIX_MD.read_text(encoding="utf-8")

        for ws in WORKSPACES:
            self.assertIn(
                ws,
                self.skill_text,
                f"Workspace '{ws}' missing from skills/ask-syafiq/SKILL.md",
            )
            self.assertIn(
                ws,
                matrix_text,
                f"Workspace '{ws}' missing from references/workspace-matrix.md",
            )

    def test_all_6_deep_modules_documented(self):
        """Verify all 6 deep modules are documented in both SKILL.md and routing-table.md."""
        routing_text = ROUTING_TABLE_MD.read_text(encoding="utf-8")

        for dm in DEEP_MODULES:
            self.assertIn(
                dm,
                self.skill_text,
                f"Deep module '{dm}' missing from skills/ask-syafiq/SKILL.md",
            )
            self.assertIn(
                dm,
                routing_text,
                f"Deep module '{dm}' missing from references/routing-table.md",
            )

    def test_upstream_engineering_pipeline_documented(self):
        """Verify the upstream engineering pipeline is documented in SKILL.md and routing-table.md."""
        routing_text = ROUTING_TABLE_MD.read_text(encoding="utf-8")

        for step in PIPELINE_STEPS:
            self.assertIn(
                step,
                self.skill_text,
                f"Pipeline step '{step}' missing from skills/ask-syafiq/SKILL.md",
            )
            self.assertIn(
                step,
                routing_text,
                f"Pipeline step '{step}' missing from references/routing-table.md",
            )

    def test_execution_phase_boundaries_documented(self):
        """Verify execution phase boundary directives are documented in SKILL.md and routing-table.md."""
        routing_text = ROUTING_TABLE_MD.read_text(encoding="utf-8")

        for phase in PHASE_BOUNDARIES:
            self.assertIn(
                phase,
                self.skill_text,
                f"Phase boundary '{phase}' missing from skills/ask-syafiq/SKILL.md",
            )
            self.assertIn(
                phase,
                routing_text,
                f"Phase boundary '{phase}' missing from references/routing-table.md",
            )

        # Ensure subagent batch limit (<=10) is documented
        self.assertIn("10", self.skill_text)
        self.assertIn("10", routing_text)

    def test_ask_coach_routing_documented(self):
        """Coaching intents route to /ask-coach, which exists and is not counted as a deep module."""
        routing_text = ROUTING_TABLE_MD.read_text(encoding="utf-8")
        self.assertTrue((REPO_ROOT / "skills" / "ask-coach" / "SKILL.md").is_file())
        for text in (self.skill_text, routing_text):
            self.assertIn("/ask-coach", text)
            self.assertIn("skills/ask-coach/SKILL.md", text)
            self.assertIn("academic-scholar", text)
        self.assertIn("Not a seventh deep module", self.skill_text)
        self.assertIn("unchanged", routing_text)
        self.assertNotIn("mhel-coaching", self.skill_text + routing_text)
        self.assertIn("across 8 repositories", self.skill_text)
        self.assertIn("6 deep modules", self.skill_text)


if __name__ == "__main__":
    unittest.main()
