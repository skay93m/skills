"""Comprehensive contract tests for Ticket 9 Deep Modules.

Covers:
- academic-scholar (Scholarship domain)
- personal-cadence (Cadence domain)
- thinking-partner (Cognition domain)

Asserts:
- Manifest existence, parsing, and schema validation.
- Entrypoint SKILL.md existence, line budgets (<= 100 lines), token budgets (< 700 tokens), and valid frontmatter.
- Terminal reference invariants (depth == 1, 0 outbound markdown links).
- Artifact contracts (declared templates and examples exist, placeholders exist in templates, 0 unreplaced {{ or }} in examples).
- Master router indexing in skills/ask-syafiq/SKILL.md.
- Domain-specific invariants:
  - academic-scholar: strict student-authored prose invariant, zero ghostwriting, primary UK statutory authorities (MHA 1983, MCA 2005), Strasbourg/ECHR jurisprudence (Articles 5, 8), OSCOLA citations.
  - personal-cadence: ADHD momentum scaffolding, low-activation energy onramps, Jibun Techo 3-phase projections, Hermes daily standups, Neko companion integration.
  - thinking-partner: Oxford tutorial Socratic sparring, assumption unmasking, failure mode pre-mortems, Architecture Decision Record (ADR) formulation.
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

TESTS_DIR = str(pathlib.Path(__file__).resolve().parent)
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)
# Ticket #164 deletes this shared map.
from legacy_domains import LEGACY_TO_V1_DOMAIN  # noqa: E402

MD_LINK_PATTERN = re.compile(r"\]\((?!https?://|#|mailto:)([^)#\s]+\.md)")

MODULE_SPECS = {
    "academic-scholar": {
        "domain": "scholarship",
        "manifest": "manifests/academic-scholar.yaml",
        "skill_dir": "skills/academic-scholar",
        "references": ["student-authored-invariant.md", "legal-citation-standards.md"],
        "artifacts": [
            ("templates/supervisory-feedback.template.md", "examples/supervisory-feedback.example.md")
        ],
        "intents": ["academic scholar", "msc supervisory coaching", "legal citation check", "student authored invariant"],
        "required_domain_phrases": [
            "student-authored",
            "Zero Ghostwriting",
            "Mental Health Act 1983",
            "Mental Capacity Act 2005",
            "OSCOLA",
            "ECHR",
            "Article 5",
            "Article 8",
            "supervisory-feedback",
        ],
    },
    "personal-cadence": {
        "domain": "cadence",
        "manifest": "manifests/personal-cadence.yaml",
        "skill_dir": "skills/personal-cadence",
        "references": ["techo-projection-framework.md", "energy-momentum-protocol.md"],
        "artifacts": [
            ("templates/daily-cadence.template.md", "examples/daily-cadence.example.md")
        ],
        "intents": ["personal cadence", "adhd momentum", "jibun techo planning", "energy check in"],
        "required_domain_phrases": [
            "ADHD",
            "momentum",
            "executive",
            "onramp",
            "Jibun Techo",
            "Hermes",
            "Neko",
            "daily-cadence",
        ],
    },
    "thinking-partner": {
        "domain": "cognition",
        "manifest": "manifests/thinking-partner.yaml",
        "skill_dir": "skills/thinking-partner",
        "references": ["socratic-sparring-method.md", "adr-formulation-guide.md"],
        "artifacts": [
            ("templates/concept-adr.template.md", "examples/concept-adr.example.md")
        ],
        "intents": ["thinking partner", "socratic sparring", "stress test assumptions", "formulate adr"],
        "required_domain_phrases": [
            "Oxford tutorial",
            "Socratic",
            "assumptions",
            "failure mode",
            "Pre-Mortem",
            "Architecture Decision Record",
            "ADR",
            "concept-adr",
        ],
    },
}




class TestDeepModulesScholarshipCadenceCognition(unittest.TestCase):
    """Contract verification test suite for scholarship, cadence, and cognition deep modules."""

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
            # Manifests use the v1 domain enum; spec["domain"] is the legacy category.
            self.assertEqual(router.get("domain"), LEGACY_TO_V1_DOMAIN[spec["domain"]])
            for intent in spec["intents"]:
                self.assertIn(intent, router.get("intents", []))

            artifacts = manifest.get("artifacts", {})
            self.assertTrue(artifacts.get("produces") is True)
            contracts = artifacts.get("contracts", [])
            self.assertGreater(len(contracts), 0)

            # Assert manifest references strictly match references on disk
            declared_refs = manifest.get("references", [])
            ref_dir = REPO_ROOT / spec["skill_dir"] / "references"
            disk_refs = [f.name for f in ref_dir.glob("*.md")]
            self.assertEqual(
                sorted(declared_refs),
                sorted(disk_refs),
                f"Manifest references for {mod_name} do not match references on disk",
            )
            self.assertEqual(
                sorted(declared_refs),
                sorted(spec["references"]),
                f"Manifest references for {mod_name} do not match test spec references",
            )

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

    def test_artifact_placeholders_and_example_hygiene(self):
        """Verify all artifact templates declare valid {{...}} placeholders and examples contain 0 unreplaced tokens."""
        placeholder_pattern = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")
        for mod_name, spec in MODULE_SPECS.items():
            skill_dir = REPO_ROOT / spec["skill_dir"]
            for tpl_rel, ex_rel in spec["artifacts"]:
                tpl_file = skill_dir / tpl_rel
                ex_file = skill_dir / ex_rel

                tpl_content = tpl_file.read_text(encoding="utf-8")
                ex_content = ex_file.read_text(encoding="utf-8")

                placeholders = placeholder_pattern.findall(tpl_content)
                self.assertGreater(
                    len(placeholders),
                    0,
                    f"Template {tpl_rel} in {mod_name} must declare valid {{{{...}}}} placeholders",
                )
                self.assertNotIn(
                    "{{",
                    ex_content,
                    f"Example {ex_rel} in {mod_name} contains unreplaced '{{{{' token",
                )
                self.assertNotIn(
                    "}}",
                    ex_content,
                    f"Example {ex_rel} in {mod_name} contains unreplaced '}}}}' token",
                )

    def test_router_indexing_in_ask_syafiq(self):
        """Verify master router (skills/ask-syafiq/SKILL.md) cleanly indexes all 3 deep modules."""
        ask_syafiq_md = REPO_ROOT / "skills" / "ask-syafiq" / "SKILL.md"
        self.assertTrue(ask_syafiq_md.is_file())
        text = ask_syafiq_md.read_text(encoding="utf-8")
        lines = text.splitlines()

        self.assertLessEqual(len(lines), 100, f"ask-syafiq/SKILL.md line count {len(lines)} exceeds 100")

        for mod_name, spec in MODULE_SPECS.items():
            self.assertIn(f"`{spec['domain']}`", text, f"Domain {spec['domain']} missing in ask-syafiq router")
            self.assertIn(f"`{mod_name}`", text, f"Skill {mod_name} missing in ask-syafiq router")

    def test_domain_specific_rule_invariants(self):
        """Verify each module includes mandatory domain-specific mechanics and invariants."""
        for mod_name, spec in MODULE_SPECS.items():
            skill_dir = REPO_ROOT / spec["skill_dir"]
            skill_md = skill_dir / "SKILL.md"
            skill_text = skill_md.read_text(encoding="utf-8")

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

    def test_academic_scholar_prose_invariant_and_oscola(self):
        """Verify strict student-authored prose invariant and OSCOLA standards in academic-scholar."""
        skill_dir = REPO_ROOT / "skills" / "academic-scholar"
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        student_invariant = (skill_dir / "references" / "student-authored-invariant.md").read_text(encoding="utf-8")
        legal_citations = (skill_dir / "references" / "legal-citation-standards.md").read_text(encoding="utf-8")

        self.assertIn("Zero Ghostwriting Policy", skill_text)
        self.assertIn("Zero Ghostwriting Policy", student_invariant)
        self.assertIn("Never write, draft, or dictate essay paragraphs", student_invariant)
        self.assertIn("Mental Health Act 1983", legal_citations)
        self.assertIn("Mental Capacity Act 2005", legal_citations)
        self.assertIn("Article 5", legal_citations)
        self.assertIn("Article 8", legal_citations)
        self.assertIn("Winterwerp v Netherlands", legal_citations)
        self.assertIn("HL v United Kingdom", legal_citations)

    def test_personal_cadence_techo_and_momentum_protocols(self):
        """Verify ADHD momentum scaffolding, Jibun Techo projections, and Hermes/Neko integration."""
        skill_dir = REPO_ROOT / "skills" / "personal-cadence"
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        techo_text = (skill_dir / "references" / "techo-projection-framework.md").read_text(encoding="utf-8")
        energy_text = (skill_dir / "references" / "energy-momentum-protocol.md").read_text(encoding="utf-8")

        self.assertIn("ADHD Momentum Scaffolding", skill_text)
        self.assertIn("Jibun Techo 3-Phase Projections", skill_text)
        self.assertIn("Hermes Daily Standups", skill_text)
        self.assertIn("Neko Companion Integration", skill_text)

        self.assertIn("Phase 1: Morning Intention", techo_text)
        self.assertIn("Phase 2: Daytime Focus Blocks", techo_text)
        self.assertIn("Phase 3: Evening Debrief", techo_text)

        self.assertIn("Peak Mental Energy (PME) Window", energy_text)
        self.assertIn("Two-Minute Micro-Step Technique", energy_text)
        self.assertIn("Hyperfocus & Cognitive Fatigue Detection", energy_text)

    def test_thinking_partner_socratic_sparring_and_adr(self):
        """Verify Oxford tutorial Socratic sparring method and ADR formulation guide."""
        skill_dir = REPO_ROOT / "skills" / "thinking-partner"
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        socratic_text = (skill_dir / "references" / "socratic-sparring-method.md").read_text(encoding="utf-8")
        adr_text = (skill_dir / "references" / "adr-formulation-guide.md").read_text(encoding="utf-8")

        self.assertIn("Oxford Tutorial Socratic Sparring", skill_text)
        self.assertIn("Failure Mode & Tradeoff Analysis", skill_text)
        self.assertIn("Architecture Decision Record (ADR) Formulation", skill_text)

        self.assertIn("Socratic Question Taxonomy", socratic_text)
        self.assertIn("Probing Unstated Assumptions", socratic_text)
        self.assertIn("Cognitive Blind Spot Detection", socratic_text)

        self.assertIn("Type 1 Decisions (One-Way Doors)", adr_text)
        self.assertIn("Type 2 Decisions (Two-Way Doors)", adr_text)
        self.assertIn("Pre-Mortem & Tradeoff Quantification", adr_text)


if __name__ == "__main__":
    unittest.main()
