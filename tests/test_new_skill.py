import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import importlib.util

ROOT = pathlib.Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("new_skill", ROOT / "scripts" / "new-skill.py")
new_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(new_skill)


class TestManifestParsing(unittest.TestCase):
    def test_parse_valid_yaml(self):
        content = """
name: demo-skill
description: Use when testing skill manifest parsing.
version: 0.1.0
disable-model-invocation: true
triggers:
  - "first trigger"
  - "second trigger"
budgets:
  line-budget: 100
  token-budget: 700
references:
  - guide.md
scripts:
  - run.sh
artifacts:
  produces: true
  contracts:
    - name: report
      template: templates/report.template.md
      example: examples/report.example.md
router:
  domain: knowledge
  intents:
    - "Test intent"
"""
        manifest = new_skill.parse_manifest(content)
        self.assertEqual(manifest["name"], "demo-skill")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertTrue(manifest["disable-model-invocation"])
        self.assertEqual(manifest["triggers"], ["first trigger", "second trigger"])
        self.assertEqual(manifest["budgets"]["line-budget"], 100)
        self.assertEqual(manifest["references"], ["guide.md"])
        self.assertEqual(manifest["artifacts"]["contracts"][0]["name"], "report")
        self.assertEqual(manifest["router"]["domain"], "knowledge")

    def test_parse_yaml_block_scalars(self):
        content = """
name: block-skill
description: >
  Use when testing
  multi-line block folded scalar
  parsing in YAML manifests.
literal_spec: |
  # Header in literal block
  Line 1
  Line 2
"""
        manifest = new_skill.parse_manifest(content)
        self.assertEqual(
            manifest["description"],
            "Use when testing multi-line block folded scalar parsing in YAML manifests.",
        )
        self.assertEqual(
            manifest["literal_spec"],
            "# Header in literal block\nLine 1\nLine 2",
        )

    def test_parse_compact_yaml_lists(self):
        content = """
name: compact-skill
description: Use when verifying compact yaml list parsing.
triggers:
- "trigger 1"
- "trigger 2"
references:
- guide.md
- runbook.md
artifacts:
  produces: true
  contracts:
  - name: summary-report
    template: templates/summary-report.template.md
    example: examples/summary-report.example.md
"""
        manifest = new_skill.parse_manifest(content)
        self.assertEqual(manifest["triggers"], ["trigger 1", "trigger 2"])
        self.assertEqual(manifest["references"], ["guide.md", "runbook.md"])
        self.assertEqual(len(manifest["artifacts"]["contracts"]), 1)
        self.assertEqual(manifest["artifacts"]["contracts"][0]["name"], "summary-report")

    def test_strip_comment_with_escaped_quotes(self):
        line1 = r'name: "quoted # not a comment \" still inside" # actual comment'
        cleaned1 = new_skill.strip_comment(line1)
        self.assertEqual(cleaned1, r'name: "quoted # not a comment \" still inside"')

        line2 = r"description: 'single # not comment \' inside' # real comment"
        cleaned2 = new_skill.strip_comment(line2)
        self.assertEqual(cleaned2, r"description: 'single # not comment \' inside'")

    def test_parse_valid_json(self):
        content = '{"name": "json-skill", "description": "Use when testing json manifest."}'
        manifest = new_skill.parse_manifest(content)
        self.assertEqual(manifest["name"], "json-skill")

    def test_parse_invalid_json(self):
        with self.assertRaises(ValueError):
            new_skill.parse_manifest("{\ninvalid json")

    def test_parse_empty_content(self):
        with self.assertRaises(ValueError):
            new_skill.parse_manifest("   \n\n  ")


class TestManifestValidation(unittest.TestCase):
    def valid_manifest(self):
        return {
            "name": "valid-skill",
            "description": "Use when performing verified operations.",
            "budgets": {"line-budget": 100, "token-budget": 700},
            "references": ["guide.md"],
            "scripts": ["run.sh"],
            "artifacts": {
                "produces": True,
                "contracts": [{"name": "audit-report"}],
            },
            "router": {"domain": "knowledge", "intents": ["Audit operations"]},
        }

    def test_valid_manifest_passes(self):
        new_skill.validate_manifest(self.valid_manifest())

    def test_missing_name_fails(self):
        m = self.valid_manifest()
        del m["name"]
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("missing required field 'name'", str(ctx.exception))

    def test_invalid_name_casing_fails(self):
        for bad_name in ("ValidSkill", "valid_skill", "-bad-start", "bad-end-", "bad--name", "has spaces"):
            m = dict(self.valid_manifest(), name=bad_name)
            with self.assertRaises(ValueError):
                new_skill.validate_manifest(m)

    def test_name_word_count_exceeded_fails(self):
        m = dict(self.valid_manifest(), name="one-two-three-four")
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("at most three words", str(ctx.exception))

    def test_name_with_vendor_strings_fails(self):
        for bad in ("claude-helper", "anthropic-ops"):
            m = dict(self.valid_manifest(), name=bad)
            with self.assertRaises(ValueError) as ctx:
                new_skill.validate_manifest(m)
            self.assertIn("must not contain", str(ctx.exception))

    def test_missing_description_fails(self):
        m = self.valid_manifest()
        del m["description"]
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("missing required field 'description'", str(ctx.exception))

    def test_description_without_use_when_fails(self):
        m = dict(self.valid_manifest(), description="Performs verified operations.")
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("Use when", str(ctx.exception))

    def test_description_with_first_second_person_fails(self):
        for pronoun in ("I help users", "Manage your tasks", "We maintain notes"):
            m = dict(self.valid_manifest(), description=f"Use when: {pronoun}.")
            with self.assertRaises(ValueError) as ctx:
                new_skill.validate_manifest(m)
            self.assertIn("first or second person", str(ctx.exception))

    def test_description_too_long_fails(self):
        long_desc = "Use when " + ("a" * 1020)
        m = dict(self.valid_manifest(), description=long_desc)
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("exceeds maximum 1,024", str(ctx.exception))

    def test_line_budget_over_100_fails(self):
        m = dict(self.valid_manifest(), budgets={"line-budget": 105})
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("line-budget", str(ctx.exception))

    def test_token_budget_over_700_fails(self):
        m = dict(self.valid_manifest(), budgets={"token-budget": 750})
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("token-budget", str(ctx.exception))

    def test_falsy_bypass_rejections(self):
        # budgets must not accept list or non-dict
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), budgets=[]))

        # booleans must not pass integer check
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), budgets={"line-budget": True}))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), budgets={"line-budget": False}))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), budgets={"token-budget": True}))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), budgets={"line-budget": 0}))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), budgets={"line-budget": -10}))

        # references must not accept non-list
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), references={}))

        # scripts must not accept non-list
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), scripts={}))

        # artifacts must not accept non-dict
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), artifacts=[]))

        # router must not accept non-dict
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), router=[]))

    def test_invalid_triggers_fails(self):
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), triggers="single-trigger"))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), triggers=[""]))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), triggers=[123]))

    def test_invalid_router_domain_and_intents_fails(self):
        # Invalid domain
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(dict(self.valid_manifest(), router={"domain": "unsupported-domain"}))
        self.assertIn("router.domain", str(ctx.exception))

        # Non-string domain
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), router={"domain": 42}))

        # Invalid intents
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), router={"domain": "knowledge", "intents": "not-a-list"}))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), router={"domain": "knowledge", "intents": [""]}))
        with self.assertRaises(ValueError):
            new_skill.validate_manifest(dict(self.valid_manifest(), router={"domain": "knowledge", "intents": [123]}))

    def test_non_terminal_reference_fails(self):
        for bad_ref in ("sub/nested.md", "../outside.md", "/root.md", "guide.txt"):
            m = dict(self.valid_manifest(), references=[bad_ref])
            with self.assertRaises(ValueError) as ctx:
                new_skill.validate_manifest(m)
            self.assertIn("Reference", str(ctx.exception))

    def test_script_with_traversal_or_subdirectories_fails(self):
        for bad_scr in ("../evil.sh", "/bin/sh", "nested/sub.sh", "\\bad.sh"):
            m = dict(self.valid_manifest(), scripts=[bad_scr])
            with self.assertRaises(ValueError) as ctx:
                new_skill.validate_manifest(m)
            self.assertIn("Script", str(ctx.exception))

    def test_produces_artifacts_without_contracts_fails(self):
        m = dict(self.valid_manifest(), artifacts={"produces": True, "contracts": []})
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("requires a non-empty 'contracts' list", str(ctx.exception))

    def test_contract_with_bad_name_fails(self):
        m = dict(self.valid_manifest(), artifacts={"produces": True, "contracts": [{"name": "Bad_Name"}]})
        with self.assertRaises(ValueError) as ctx:
            new_skill.validate_manifest(m)
        self.assertIn("must be lowercase kebab-case", str(ctx.exception))

    def test_path_traversal_in_contract_templates_and_examples_fails(self):
        for bad_tpl in ("../../bad.md", "/etc/bad.md", "\\root.md", "other/bad.template.md", "bad.txt"):
            contract = {"name": "report", "template": bad_tpl}
            m = dict(self.valid_manifest(), artifacts={"produces": True, "contracts": [contract]})
            with self.assertRaises(ValueError) as ctx:
                new_skill.validate_manifest(m)
            self.assertIn("template", str(ctx.exception))

        for bad_ex in ("../../bad.md", "/etc/bad.md", "\\root.md", "other/bad.example.md", "bad.txt"):
            contract = {"name": "report", "example": bad_ex}
            m = dict(self.valid_manifest(), artifacts={"produces": True, "contracts": [contract]})
            with self.assertRaises(ValueError) as ctx:
                new_skill.validate_manifest(m)
            self.assertIn("example", str(ctx.exception))


class TestScaffoldingExecution(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp_dir.name)
        self.skills_dir = self.root / "skills"
        self.tests_dir = self.root / "tests"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scaffold_creates_expected_files(self):
        manifest = {
            "name": "sample-worker",
            "description": "Use when executing sample background tasks.",
            "version": "0.1.0",
            "provenance": "original",
            "references": ["workflow.md"],
            "scripts": ["worker.sh"],
            "artifacts": {
                "produces": True,
                "contracts": [{"name": "worker-log"}],
            },
            "router": {
                "domain": "cadence",
                "intents": ["Execute background work"],
            },
        }

        result = new_skill.scaffold_skill(manifest, self.skills_dir, self.tests_dir)
        skill_dir = pathlib.Path(result["skill_dir"])

        # SKILL.md assertions
        skill_md = skill_dir / "SKILL.md"
        self.assertTrue(skill_md.exists())
        lines = skill_md.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), 100)
        content = "\n".join(lines)
        self.assertIn("name: sample-worker", content)
        self.assertIn("category: cadence", content)
        self.assertIn("[Workflow](references/workflow.md)", content)
        self.assertIn("scripts/worker.sh", content)
        self.assertIn("templates/worker-log.template.md", content)

        # Reference assertions (terminal depth 1)
        ref_file = skill_dir / "references" / "workflow.md"
        self.assertTrue(ref_file.exists())
        ref_text = ref_file.read_text(encoding="utf-8")
        self.assertIn("This reference is terminal", ref_text)
        link_re = re.compile(r"\]\((?!https?://|#|mailto:)([^)]*\.md[^)]*)\)")
        self.assertEqual(link_re.findall(ref_text), [])

        # Script assertions (executable permissions chmod +x)
        script_file = skill_dir / "scripts" / "worker.sh"
        self.assertTrue(script_file.exists())
        self.assertTrue(os.access(script_file, os.X_OK))

        # Artifact templates & examples
        template_file = skill_dir / "templates" / "worker-log.template.md"
        example_file = skill_dir / "examples" / "worker-log.example.md"
        self.assertTrue(template_file.exists())
        self.assertTrue(example_file.exists())

        # Router ask-syafiq update
        ask_syafiq = self.skills_dir / "ask-syafiq" / "SKILL.md"
        self.assertTrue(ask_syafiq.exists())
        ask_text = ask_syafiq.read_text(encoding="utf-8")
        self.assertIn("| cadence | `sample-worker` | Execute background work |", ask_text)
        self.assertLessEqual(len(ask_text.splitlines()), 100)

        # Scaffolding test execution
        test_file = pathlib.Path(result["test_file"])
        self.assertTrue(test_file.exists())
        res = subprocess.run([sys.executable, str(test_file)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Generated test failed: {res.stderr}")

    def test_scaffold_non_artifact_skill(self):
        manifest = {
            "name": "thinking-partner",
            "description": "Use when stress-testing architectural decisions.",
            "version": "0.1.0",
            "provenance": "original",
            "references": ["heuristics.md"],
            "scripts": [],
            "artifacts": {
                "produces": False,
            },
            "router": {
                "domain": "cognition",
                "intents": ["Stress-test proposals"],
            },
        }

        result = new_skill.scaffold_skill(manifest, self.skills_dir, self.tests_dir)
        skill_dir = pathlib.Path(result["skill_dir"])

        self.assertFalse((skill_dir / "templates").exists())
        self.assertFalse((skill_dir / "examples").exists())
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("Artifact Contracts", skill_text)

        test_file = pathlib.Path(result["test_file"])
        res = subprocess.run([sys.executable, str(test_file)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Generated test failed: {res.stderr}")

    def test_scaffold_scripts_generation_both_python_and_bash(self):
        manifest = {
            "name": "scripted-worker",
            "description": "Use when running automated helper scripts.",
            "scripts": ["runner.py", "setup.sh"],
        }
        result = new_skill.scaffold_skill(manifest, self.skills_dir, self.tests_dir)
        skill_dir = pathlib.Path(result["skill_dir"])

        py_script = skill_dir / "scripts" / "runner.py"
        sh_script = skill_dir / "scripts" / "setup.sh"

        self.assertTrue(py_script.exists())
        self.assertTrue(os.access(py_script, os.X_OK))
        self.assertTrue(sh_script.exists())
        self.assertTrue(os.access(sh_script, os.X_OK))

    def test_scaffold_custom_line_budget_enforced(self):
        manifest = {
            "name": "bounded-skill",
            "description": "Use when testing strict custom line budgets.",
            "budgets": {"line-budget": 40},
        }
        result = new_skill.scaffold_skill(manifest, self.skills_dir, self.tests_dir)
        test_file = pathlib.Path(result["test_file"])
        test_code = test_file.read_text(encoding="utf-8")
        self.assertIn("exceeds 40", test_code)

    def test_scaffold_provenance_and_divergence_standard_s6(self):
        manifest = {
            "name": "derived-skill",
            "description": "Use when testing derived provenance handling.",
            "provenance": "https://github.com/upstream/skill@1a2b3c4d",
            "divergence": "Customized for personal repository standards.",
        }
        result = new_skill.scaffold_skill(manifest, self.skills_dir, self.tests_dir)
        skill_md = pathlib.Path(result["skill_md"])
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("origin: https://github.com/upstream/skill@1a2b3c4d", content)
        self.assertIn("divergence: Customized for personal repository standards.", content)

    def test_rollback_on_scaffolding_failure(self):
        # We craft a situation where scaffolding will fail mid-execution
        # E.g., preflight router line budget exhaustion
        ask_syafiq = self.skills_dir / "ask-syafiq" / "SKILL.md"
        ask_syafiq.parent.mkdir(parents=True, exist_ok=True)
        # Fill ask-syafiq to 100 lines
        lines = [f"# line {i}" for i in range(100)]
        ask_syafiq.write_text("\n".join(lines) + "\n", encoding="utf-8")

        manifest = {
            "name": "rollback-skill",
            "description": "Use when verifying atomic rollback on failure.",
            "router": {"domain": "cognition", "intents": ["Intent"]},
        }

        with self.assertRaises(ValueError) as ctx:
            new_skill.scaffold_skill(manifest, self.skills_dir, self.tests_dir)
        self.assertIn("line budget", str(ctx.exception))

        # Ensure skill directory was never created or left dirty
        skill_dir = self.skills_dir / "rollback-skill"
        self.assertFalse(skill_dir.exists(), "Skill directory should not exist after rollback")

    def test_scaffold_fail_closed_if_directory_exists(self):
        manifest = {
            "name": "existing-skill",
            "description": "Use when testing pre-existing skill collisions.",
        }
        (self.skills_dir / "existing-skill").mkdir(parents=True, exist_ok=True)
        with self.assertRaises(ValueError) as ctx:
            new_skill.scaffold_skill(manifest, self.skills_dir, self.tests_dir)
        self.assertIn("already exists", str(ctx.exception))

    def test_router_idempotency_and_pipe_escaping(self):
        ask_syafiq = self.skills_dir / "ask-syafiq" / "SKILL.md"

        # Call once with pipes in intent
        new_skill.update_master_router(
            ask_syafiq,
            name="pipe-skill",
            domain="knowledge",
            intents=["First intent | Second intent with pipes"],
        )
        content_1 = ask_syafiq.read_text(encoding="utf-8")
        self.assertIn(r"First intent \| Second intent with pipes", content_1)

        # Call again (idempotent - should not add duplicate row)
        new_skill.update_master_router(
            ask_syafiq,
            name="pipe-skill",
            domain="knowledge",
            intents=["First intent | Second intent with pipes"],
        )
        content_2 = ask_syafiq.read_text(encoding="utf-8")
        self.assertEqual(content_1, content_2)
        # Ensure count of `pipe-skill` is exactly 1
        self.assertEqual(content_2.count("`pipe-skill`"), 1)

    def test_terminal_reference_chaining_detection(self):
        # Verify the regex detects links with anchors and titles
        link_re = re.compile(r"\]\((?!https?://|#|mailto:)([^)]*\.md[^)]*)\)")

        # Normal markdown link
        m1 = link_re.findall("[Next](other.md)")
        self.assertEqual(m1, ["other.md"])

        # Link with anchor
        m2 = link_re.findall("[Section](other.md#section-name)")
        self.assertEqual(m2, ["other.md#section-name"])

        # Link with title
        m3 = link_re.findall('[Doc](other.md "Helpful Title")')
        self.assertEqual(m3, ['other.md "Helpful Title"'])

        # Permitted non-chaining links should not match
        self.assertEqual(link_re.findall("[External](https://example.com/doc.md)"), [])
        self.assertEqual(link_re.findall("[Local Anchor](#heading)"), [])
        self.assertEqual(link_re.findall("[Contact](mailto:test@example.com)"), [])


class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp_dir.name)
        self.manifest_file = self.root / "manifest.yaml"
        self.skills_dir = self.root / "skills"
        self.tests_dir = self.root / "tests"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cli_success(self):
        self.manifest_file.write_text("""
name: cli-test-skill
description: Use when verifying CLI invocation behavior.
router:
  domain: cognition
  intents:
    - "Test intent"
""")
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "new-skill.py"),
            "--manifest",
            str(self.manifest_file),
            "--skills-dir",
            str(self.skills_dir),
            "--tests-dir",
            str(self.tests_dir),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"CLI failed: {res.stderr}")
        self.assertIn("Successfully scaffolded skill 'cli-test-skill'", res.stdout)
        self.assertTrue((self.skills_dir / "cli-test-skill" / "SKILL.md").exists())

    def test_cli_missing_manifest_file_fails(self):
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "new-skill.py"),
            "--manifest",
            str(self.root / "missing.yaml"),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)
        self.assertIn("Manifest file not found", res.stderr)

    def test_cli_validation_failure_exits_code_1(self):
        self.manifest_file.write_text("""
name: BadSkillName
description: Missing use when clause.
""")
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "new-skill.py"),
            "--manifest",
            str(self.manifest_file),
            "--skills-dir",
            str(self.skills_dir),
            "--tests-dir",
            str(self.tests_dir),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error:", res.stderr)


if __name__ == "__main__":
    unittest.main()
