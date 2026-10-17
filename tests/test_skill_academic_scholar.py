import os
import pathlib
import re
import unittest

SKILL_NAME = "academic-scholar"


class TestSkillAcademicScholar(unittest.TestCase):
    def setUp(self):
        env_skills = os.environ.get("SKILLS_DIR")
        if env_skills:
            self.skill_dir = pathlib.Path(env_skills) / SKILL_NAME
        else:
            rel = pathlib.Path("../skills/academic-scholar")
            candidate = (pathlib.Path(__file__).resolve().parent / rel).resolve()
            if candidate.exists():
                self.skill_dir = candidate
            else:
                self.skill_dir = pathlib.Path(__file__).resolve().parent.parent / "skills" / SKILL_NAME

    def test_skill_md_exists_and_line_budget(self):
        skill_md = self.skill_dir / "SKILL.md"
        self.assertTrue(skill_md.exists(), f"SKILL.md missing for {SKILL_NAME}")
        lines = skill_md.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), 100, f"SKILL.md line count {len(lines)} exceeds 100")

    def test_terminal_references_invariant(self):
        ref_dir = self.skill_dir / "references"
        if not ref_dir.exists():
            return
        link_re = re.compile(r"\]\((?!https?://|#|mailto:)([^)]*\.md[^)]*)\)")
        for ref_file in ref_dir.glob("*.md"):
            content = ref_file.read_text(encoding="utf-8")
            matches = link_re.findall(content)
            self.assertEqual(matches, [], f"Reference file {ref_file.name} links to other markdown files: {matches}")

    def test_artifact_contracts_exist(self):
        for rel_path in ['templates/supervisory-feedback.template.md', 'examples/supervisory-feedback.example.md']:
            target = self.skill_dir / rel_path
            self.assertTrue(target.exists(), f"Contract artifact {rel_path} does not exist")


if __name__ == "__main__":
    unittest.main()
