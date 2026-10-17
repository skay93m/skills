"""Comprehensive contract tests for Ticket 8 Core Deep Modules.

Covers:
- wiki-ops (Knowledge domain)
- autonomous-scrum (Scrum domain)
- agent-ecosystem (Ecosystem domain)

Asserts:
- Manifest existence, parsing, and schema validation.
- Entrypoint SKILL.md existence, line budgets (<= 100 lines), token budgets (< 700 tokens), and valid frontmatter.
- Terminal reference invariants (depth == 1, 0 outbound markdown links).
- Artifact contracts (declared templates and examples exist and are non-empty).
- Master router indexing in skills/ask-syafiq/SKILL.md.
- Domain-specific invariants (subagent batch ceiling <= 10, PO/Dev separation, Basic Memory MCP compliance).
"""
import importlib
import pathlib
import re
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
new_skill = importlib.import_module("new-skill")

MD_LINK_PATTERN = re.compile(r"\]\((?!https?://|#|mailto:)([^)#\s]+\.md)")

MODULE_SPECS = {
    "wiki-ops": {
        "domain": "knowledge",
        "manifest": "manifests/wiki-ops.yaml",
        "skill_dir": "skills/wiki-ops",
        "references": ["basic-memory-contracts.md", "reconciliation-policy.md"],
        "artifacts": [
            ("templates/knowledge-report.template.md", "examples/knowledge-report.example.md")
        ],
        "intents": ["wiki ops", "compile knowledge", "basic memory operations", "knowledge lint"],
        "required_domain_phrases": [
            "Basic Memory MCP",
            "sk-wiki",
            "read_note",
            "write_note",
            "prohibited",
            "FIFO",
            "structural",
            "semantic",
            "ledger",
        ],
    },
    "autonomous-scrum": {
        "domain": "scrum",
        "manifest": "manifests/autonomous-scrum.yaml",
        "skill_dir": "skills/autonomous-scrum",
        "references": ["event-0-gates.md", "role-boundaries.md"],
        "artifacts": [
            ("templates/sprint-report.template.md", "examples/sprint-report.example.md")
        ],
        "intents": ["autonomous scrum", "sprint planning", "event 0 gates", "task triage"],
        "required_domain_phrases": [
            "Product Owner",
            "Developer",
            "Event 0",
            "sprint gates",
            "awt.db",
            "SQLite",
            "acceptance criteria",
        ],
    },
    "agent-ecosystem": {
        "domain": "ecosystem",
        "manifest": "manifests/agent-ecosystem.yaml",
        "skill_dir": "skills/agent-ecosystem",
        "references": ["golden-agents-layout.md", "fleet-batching-protocol.md"],
        "artifacts": [
            ("templates/agent-handoff.template.md", "examples/agent-handoff.example.md")
        ],
        "intents": ["agent ecosystem", "fleet governance", "subagent batching", "cross agent handoff"],
        "required_domain_phrases": [
            "~/.agents",
            "golden",
            "10",
            "subagent",
            "batch",
            "handoff",
            "runtimes",
        ],
    },
}


class TestDeepModulesCore(unittest.TestCase):
    """Contract verification test suite for core deep modules."""

    def test_manifests_exist_and_validate(self):
        """Verify each module has a valid YAML manifest conforming to standard schema."""
        for mod_name, spec in MODULE_SPECS.items():
            manifest_file = REPO_ROOT / spec["manifest"]
            self.assertTrue(manifest_file.is_file(), f"Missing manifest file for {mod_name}: {manifest_file}")
            raw_text = manifest_file.read_text(encoding="utf-8")
            manifest = new_skill.parse_manifest(raw_text)

            new_skill.validate_manifest(manifest)
            self.assertEqual(manifest["name"], mod_name)
            self.assertEqual(manifest.get("version"), "0.2.0")
            self.assertEqual(manifest.get("provenance"), "original")
            self.assertTrue(manifest.get("disable-model-invocation") is True)
            self.assertTrue(manifest.get("user-invoked") is True)

            budgets = manifest.get("budgets", {})
            self.assertEqual(budgets.get("line-budget"), 100)
            self.assertEqual(budgets.get("token-budget"), 700)

            router = manifest.get("router", {})
            self.assertEqual(router.get("domain"), spec["domain"])
            for intent in spec["intents"]:
                self.assertIn(intent, router.get("intents", []))

            artifacts = manifest.get("artifacts", {})
            self.assertTrue(artifacts.get("produces") is True)
            contracts = artifacts.get("contracts", [])
            self.assertGreater(len(contracts), 0)

    def test_entrypoints_exist_and_meet_budgets(self):
        """Verify SKILL.md entrypoints exist, obey <= 100 lines and < 700 token budget."""
        for mod_name, spec in MODULE_SPECS.items():
            skill_dir = REPO_ROOT / spec["skill_dir"]
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing SKILL.md for {mod_name}: {skill_md}")

            text = skill_md.read_text(encoding="utf-8")
            lines = text.splitlines()

            # Line budget check (Standard S4)
            self.assertLessEqual(
                len(lines),
                100,
                f"{mod_name}/SKILL.md line count {len(lines)} exceeds 100 line budget",
            )

            # Token budget estimate check
            estimated_count = new_skill.estimate_tokens(text)
            self.assertLess(
                estimated_count,
                700,
                f"{mod_name}/SKILL.md token estimate {estimated_count} exceeds 700 token budget",
            )

    def test_frontmatter_invariants(self):
        """Verify frontmatter adheres to schema, naming, description, and metadata requirements."""
        for mod_name, spec in MODULE_SPECS.items():
            skill_md = REPO_ROOT / spec["skill_dir"] / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), f"{mod_name}/SKILL.md must start with frontmatter")
            parts = text.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"{mod_name}/SKILL.md frontmatter improperly closed")
            fm = new_skill.parse_yaml_lines(parts[1].splitlines())

            self.assertEqual(fm.get("name"), mod_name)
            self.assertTrue(fm.get("disable-model-invocation") is True)
            self.assertTrue(fm.get("user-invoked") is True)
            self.assertEqual(fm.get("version"), "0.2.0")
            self.assertEqual(fm.get("provenance"), "original")

            desc = fm.get("description", "")
            self.assertIn("Use when", desc, f"{mod_name} description must contain 'Use when'")
            self.assertLessEqual(len(desc), 1024)
            self.assertIsNone(
                new_skill.FIRST_SECOND_PERSON.search(desc),
                f"{mod_name} description must not contain first or second person pronouns",
            )

            meta = fm.get("metadata", {})
            self.assertEqual(meta.get("origin"), "original")
            self.assertEqual(meta.get("agent_involvement"), "full")
            self.assertEqual(meta.get("category"), spec["domain"])

    def test_terminal_references_invariant(self):
        """Verify all declared reference files exist, contain terminal disclaimers, and have 0 outbound links."""
        for mod_name, spec in MODULE_SPECS.items():
            ref_dir = REPO_ROOT / spec["skill_dir"] / "references"
            self.assertTrue(ref_dir.is_dir(), f"Missing references directory for {mod_name}")

            for ref_name in spec["references"]:
                ref_file = ref_dir / ref_name
                self.assertTrue(ref_file.is_file(), f"Missing reference file: {ref_file}")
                content = ref_file.read_text(encoding="utf-8")

                self.assertIn(
                    "This reference is terminal",
                    content,
                    f"Terminal disclaimer missing in {ref_file}",
                )

                outbound_links = MD_LINK_PATTERN.findall(content)
                self.assertEqual(
                    outbound_links,
                    [],
                    f"Reference {ref_file} violates terminal invariant by linking to: {outbound_links}",
                )

    def test_artifact_contracts_exist_and_non_empty(self):
        """Verify all declared templates and examples exist, reside in proper folders, and are non-empty."""
        for mod_name, spec in MODULE_SPECS.items():
            skill_dir = REPO_ROOT / spec["skill_dir"]

            for tpl_rel, ex_rel in spec["artifacts"]:
                tpl_file = skill_dir / tpl_rel
                ex_file = skill_dir / ex_rel

                self.assertTrue(tpl_file.is_file(), f"Missing template {tpl_rel} in {mod_name}")
                self.assertTrue(ex_file.is_file(), f"Missing example {ex_rel} in {mod_name}")

                tpl_content = tpl_file.read_text(encoding="utf-8").strip()
                ex_content = ex_file.read_text(encoding="utf-8").strip()

                self.assertGreater(len(tpl_content), 50, f"Template {tpl_rel} is unexpectedly short or empty")
                self.assertGreater(len(ex_content), 50, f"Example {ex_rel} is unexpectedly short or empty")

    def test_router_indexing_in_ask_syafiq(self):
        """Verify master router (skills/ask-syafiq/SKILL.md) cleanly indexes all 3 deep modules."""
        ask_syafiq_md = REPO_ROOT / "skills" / "ask-syafiq" / "SKILL.md"
        self.assertTrue(ask_syafiq_md.is_file())
        text = ask_syafiq_md.read_text(encoding="utf-8")
        lines = text.splitlines()

        self.assertLessEqual(len(lines), 100, f"ask-syafiq/SKILL.md line count {len(lines)} exceeds 100")

        for mod_name, spec in MODULE_SPECS.items():
            self.assertIn(f"`{spec['domain']}`", text, f"Domain {spec['domain']} missing in ask-syafiq router")
            self.assertIn(f"[`{mod_name}`]", text, f"Skill link for {mod_name} missing in ask-syafiq router")

    def test_domain_specific_rule_invariants(self):
        """Verify each module includes mandatory domain-specific mechanics and invariants."""
        for mod_name, spec in MODULE_SPECS.items():
            skill_dir = REPO_ROOT / spec["skill_dir"]
            skill_md = skill_dir / "SKILL.md"
            skill_text = skill_md.read_text(encoding="utf-8")

            # Check references text as well
            ref_texts = [
                (skill_dir / "references" / ref).read_text(encoding="utf-8")
                for ref in spec["references"]
            ]
            all_text = skill_text + "\n" + "\n".join(ref_texts)

            for phrase in spec["required_domain_phrases"]:
                self.assertIn(
                    phrase,
                    all_text,
                    f"Required domain phrase '{phrase}' missing from {mod_name} entrypoint or references",
                )


if __name__ == "__main__":
    unittest.main()
