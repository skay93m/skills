"""Multi-Agent npx skills Packaging & Verification Contract Test Suite (Ticket 11).

Verifies that all 38 skills in the repository comply with:
- Entrypoint existence and frontmatter validity (name matching directory, description with 'Use when').
- Strict line budgets (<= 100 lines) and token budgets (< 700 tokens).
- Declarative skill manifests in manifests/ schema-validity and artifact contract compliance.
- Single-module installation resolution (--skill <name>) for all 38 skills.
- Multi-runtime packaging simulation across Claude Code, Codex, Antigravity, and Hermes,
  verifying self-contained asset resolution (references, templates, examples, scripts).
"""
import importlib
import os
import pathlib
import re
import shutil
import tempfile
import unittest

import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MANIFESTS_DIR = REPO_ROOT / "manifests"
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

new_skill = importlib.import_module("new-skill")
check_std = importlib.import_module("check-standard")

DEEP_MODULES = {
    "wiki-ops",
    "autonomous-scrum",
    "agent-ecosystem",
    "academic-scholar",
    "personal-cadence",
    "thinking-partner",
}

ROUTER_SKILLS = {
    "ask-syafiq",
}

KNOWLEDGE_AND_SEAM_SKILLS = {
    "daily-knowledge-maintenance",
    "knowledge-ingest",
    "knowledge-lint",
    "knowledge-run-audit",
    "seam-adapter",
}

TOMBSTONE_SKILLS = {
    "sk-claude-daily-inbox-triage",
    "sk-claude-daily-writing-journal-seed",
    "sk-claude-draft-energy-map",
    "sk-claude-inbox-triage-nudge",
    "sk-claude-techo-evening-pull",
    "sk-claude-weekly-review-prep",
    "sk-claude-weekly-task-consolidation",
    "sk-cli-agent-onboarding",
    "sk-codex-weekday-morning-brief",
    "sk-create-adapter",
    "sk-email-ingest",
    "sk-hermes-daily-audit",
    "sk-hermes-energy-inventory-14-days",
    "sk-index-governance",
    "sk-local-cloud-reconciliation",
    "sk-onboarding",
    "sk-semantic-lint",
    "sk-supervised-ingest",
    "sk-triage",
    "sk-unsupervised-ingest",
    "sk-update",
    "sk-wiki-maintenance",
    "sk-wiki-stop",
    "sk-wiki-teach",
    "sk-writing-coach",
    "task-assistant",
}

ALL_38_SKILLS = DEEP_MODULES | ROUTER_SKILLS | KNOWLEDGE_AND_SEAM_SKILLS | TOMBSTONE_SKILLS


def resolve_skill_source(repo_root: pathlib.Path, skill_name: str) -> pathlib.Path:
    """Simulate npx skills add skay93m/skills --skill <name> resolution."""
    skill_dir = repo_root / "skills" / skill_name
    if not skill_dir.is_dir():
        raise KeyError(f"Skill '{skill_name}' not found in {repo_root / 'skills'}")
    entrypoint = skill_dir / "SKILL.md"
    if not entrypoint.is_file():
        raise FileNotFoundError(f"SKILL.md missing in {skill_dir}")
    return skill_dir


def install_skill_to_runtime(source_dir: pathlib.Path, target_skills_dir: pathlib.Path, skill_name: str) -> pathlib.Path:
    """Simulate copying/installing a single skill into a runtime skill directory."""
    dest_dir = target_skills_dir / skill_name
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(source_dir, dest_dir)
    return dest_dir


class TestNpxSkillsPackagingContract(unittest.TestCase):
    """Packaging contract and multi-agent runtime verification test suite."""

    def test_exact_inventory_of_38_skills(self):
        """Repository must contain exactly 38 skills across the four defined categories."""
        actual_dirs = sorted([p.name for p in SKILLS_DIR.iterdir() if p.is_dir()])
        self.assertEqual(len(actual_dirs), 38, f"Expected 38 skill directories, found {len(actual_dirs)}")
        self.assertEqual(set(actual_dirs), ALL_38_SKILLS)
        self.assertEqual(len(DEEP_MODULES), 6)
        self.assertEqual(len(ROUTER_SKILLS), 1)
        self.assertEqual(len(KNOWLEDGE_AND_SEAM_SKILLS), 5)
        self.assertEqual(len(TOMBSTONE_SKILLS), 26)

    def test_all_38_skills_frontmatter_invariants(self):
        """Every skill must contain a valid SKILL.md with valid name and description."""
        for skill_name in ALL_38_SKILLS:
            skill_dir = SKILLS_DIR / skill_name
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing SKILL.md in {skill_name}")

            content = skill_md.read_text(encoding="utf-8")
            data, where = check_std.parse_frontmatter(content)
            self.assertIsNotNone(data, f"Frontmatter missing or invalid in {skill_name}/SKILL.md")

            name = data.get("name")
            self.assertEqual(name, skill_name, f"Name in frontmatter ('{name}') must match directory '{skill_name}'")
            self.assertTrue(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name), f"Name '{name}' must be kebab-case")

            # Active deep modules and router adhere to strict <= 3 word and vendor label bans
            if skill_name in (DEEP_MODULES | ROUTER_SKILLS | KNOWLEDGE_AND_SEAM_SKILLS):
                self.assertLessEqual(len(name.split("-")), 3, f"Name '{name}' must have at most 3 words")
                self.assertNotIn("anthropic", name.lower())
                self.assertNotIn("claude", name.lower())

            desc = data.get("description", "")
            self.assertTrue(isinstance(desc, str) and desc.strip(), f"Missing description in {skill_name}")
            self.assertLessEqual(len(desc), 1024, f"Description in {skill_name} exceeds 1024 characters")
            self.assertIn("use when", desc.lower(), f"Description in {skill_name} missing 'Use when' clause")
            self.assertIsNone(
                new_skill.FIRST_SECOND_PERSON.search(desc),
                f"Description in {skill_name} contains 1st/2nd person pronouns",
            )

    def test_all_38_skills_strictly_obey_line_and_token_budgets(self):
        """Every SKILL.md must strictly obey line budget (<= 100 lines) and token budget (< 700 tokens)."""
        for skill_name in ALL_38_SKILLS:
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8")
            lines = content.splitlines()
            tok_estimate = new_skill.estimate_tokens(content)

            self.assertLessEqual(
                len(lines),
                100,
                f"Skill {skill_name}/SKILL.md has {len(lines)} lines, exceeding 100-line budget",
            )
            self.assertLess(
                tok_estimate,
                700,
                f"Skill {skill_name}/SKILL.md has ~{tok_estimate} tokens, exceeding 700-token budget",
            )

    def test_all_manifests_are_schema_valid(self):
        """All declarative manifests in manifests/ must pass schema validation."""
        manifest_files = sorted(list(MANIFESTS_DIR.glob("*.yaml")) + list(MANIFESTS_DIR.glob("*.yml")))
        self.assertGreaterEqual(len(manifest_files), 7, "Expected at least 7 skill manifests in manifests/")

        expected_manifest_names = {
            "academic-scholar",
            "agent-ecosystem",
            "ask-syafiq",
            "autonomous-scrum",
            "personal-cadence",
            "thinking-partner",
            "wiki-ops",
        }
        manifest_stems = {mf.stem for mf in manifest_files}
        self.assertTrue(expected_manifest_names.issubset(manifest_stems))

        for mf in manifest_files:
            content = mf.read_text(encoding="utf-8")
            data = new_skill.parse_manifest(content)
            # Must validate with new_skill.validate_manifest without raising ValueError
            new_skill.validate_manifest(data)

            self.assertEqual(data["name"], mf.stem)
            budgets = data.get("budgets", {})
            self.assertLessEqual(budgets.get("line-budget", 100), 100)
            self.assertLessEqual(budgets.get("token-budget", 700), 700)

            # If artifacts are declared, verify template and example files exist
            artifacts = data.get("artifacts", {})
            if artifacts.get("produces"):
                contracts = artifacts.get("contracts", [])
                self.assertGreater(len(contracts), 0, f"Manifest {mf.name} produces artifacts but has no contracts")
                skill_dir = SKILLS_DIR / data["name"]
                for contract in contracts:
                    tpl_path = skill_dir / contract["template"]
                    ex_path = skill_dir / contract["example"]
                    self.assertTrue(tpl_path.is_file(), f"Template missing: {tpl_path}")
                    self.assertTrue(ex_path.is_file(), f"Example missing: {ex_path}")
                    tpl_content = tpl_path.read_text(encoding="utf-8")
                    ex_content = ex_path.read_text(encoding="utf-8")
                    self.assertIn("{{", tpl_content)
                    self.assertNotIn("{{", ex_content)

    def test_module_installation_resolution_all_38_skills(self):
        """Simulate npx skills add skay93m/skills --skill <name> resolution for all 38 skills."""
        for skill_name in ALL_38_SKILLS:
            resolved_dir = resolve_skill_source(REPO_ROOT, skill_name)
            self.assertTrue(resolved_dir.is_dir())
            self.assertEqual(resolved_dir.name, skill_name)
            self.assertTrue((resolved_dir / "SKILL.md").is_file())

        # Assert invalid skill names raise KeyError
        for bad_name in ("non-existent-skill", "unknown-module", "foo-bar"):
            with self.assertRaises(KeyError):
                resolve_skill_source(REPO_ROOT, bad_name)

    def test_simulated_runtime_packaging_claude_codex_antigravity_hermes(self):
        """Simulate packaging and installing skills across diverse agent runtimes."""
        runtime_paths = {
            "claude": pathlib.Path(".claude") / "skills",
            "codex": pathlib.Path(".codex") / "skills",
            "antigravity": pathlib.Path(".gemini") / "antigravity-cli" / "skills",
            "hermes": pathlib.Path(".hermes") / "skills",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)

            for runtime_name, rel_path in runtime_paths.items():
                target_skills_dir = temp_root / rel_path
                target_skills_dir.mkdir(parents=True, exist_ok=True)

                # 1. Test full suite installation: install all 38 skills
                for skill_name in ALL_38_SKILLS:
                    src_dir = resolve_skill_source(REPO_ROOT, skill_name)
                    dest_dir = install_skill_to_runtime(src_dir, target_skills_dir, skill_name)
                    self.assertTrue((dest_dir / "SKILL.md").is_file())

                # Verify deep module self-contained assets in the runtime target
                for mod_name in DEEP_MODULES:
                    mod_dest = target_skills_dir / mod_name
                    # References directory and contents
                    ref_dir = mod_dest / "references"
                    if ref_dir.is_dir():
                        for ref_file in ref_dir.glob("*.md"):
                            self.assertTrue(ref_file.is_file())
                            # Terminal reference check: no reference file links to another reference file
                            content = ref_file.read_text(encoding="utf-8")
                            for line in content.splitlines():
                                self.assertIsNone(
                                    check_std.SHELL_STEP_LINK.search(line),
                                    f"Terminal reference violated in {runtime_name} installation: {ref_file}",
                                )

                    # Templates directory and contents
                    tpl_dir = mod_dest / "templates"
                    if tpl_dir.is_dir():
                        for tpl_file in tpl_dir.glob("*.md"):
                            self.assertTrue(tpl_file.is_file())

                    # Examples directory and contents
                    ex_dir = mod_dest / "examples"
                    if ex_dir.is_dir():
                        for ex_file in ex_dir.glob("*.md"):
                            self.assertTrue(ex_file.is_file())

                # Verify tombstones in runtime target are fail-closed and clean
                for tomb_name in TOMBSTONE_SKILLS:
                    tomb_dest = target_skills_dir / tomb_name
                    dest_files = [p.name for p in tomb_dest.iterdir()]
                    self.assertEqual(
                        dest_files,
                        ["SKILL.md"],
                        f"Tombstone {tomb_name} in {runtime_name} has extra files: {dest_files}",
                    )
                    content = (tomb_dest / "SKILL.md").read_text(encoding="utf-8")
                    self.assertIn("disable-model-invocation: true", content)
                    self.assertIn("zero mutations", content)


if __name__ == "__main__":
    unittest.main()
