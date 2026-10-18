"""Tests for scripts/check-standard.py. Run: python3 -m unittest discover -s tests

Each test builds a throwaway git repository, commits a base, commits a change,
and runs the checker against the base. Secret-like and personal-looking values
are assembled at run time from pieces; none is a real credential or person.
"""
import os
import re
import secrets
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "check-standard.py")
ANNOTATION = re.compile(r"title=(BLOCKING|NON-BLOCKING) \[(\w+)\]")

GOOD_SKILL = """---
name: good-skill
description: Review pull requests for style. Use when a pull request needs a style review.
metadata:
  origin: original
  agent_involvement: full
  category: review
---
# Good skill
Body.
"""


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def write(root, files):
    for path, text in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(text)


def run_check(base_files, head_files, today="2026-10-10", working_tree=False, commit=True):
    """Return (exit_code, [(label, id), ...]).

    With commit=False the head files stay uncommitted, so only working-tree
    mode sees them.
    """
    with tempfile.TemporaryDirectory() as root:
        git(root, "init", "-q", "-b", "main")
        git(root, "config", "user.email", "test@example.com")
        git(root, "config", "user.name", "test")
        write(root, {"README.md": "# base\n", **base_files})
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "base")
        git(root, "tag", "base")
        git(root, "checkout", "-q", "-b", "change")
        write(root, head_files)
        if commit:
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "change")
        args = [sys.executable, SCRIPT, "--base", "base", "--today", today]
        if working_tree:
            args.append("--working-tree")
        done = subprocess.run(args, cwd=root, capture_output=True, text=True)
        return done.returncode, ANNOTATION.findall(done.stdout)


def ids(found, label=None):
    return {i for lab, i in found if label is None or lab == label}


class SecretsAndPrivacy(unittest.TestCase):
    def test_secret_assignment_is_blocking(self):
        key = secrets.token_hex(20)
        code, found = run_check({}, {"deploy/settings.txt": f'API_{"SECRET"} = "{key}"\n'})
        self.assertIn("H1", ids(found, "BLOCKING"))
        self.assertEqual(code, 1)

    def test_placeholder_secret_is_ignored(self):
        code, found = run_check({}, {"notes.txt": 'API_KEY = "changeme-please-1"\n'})
        self.assertNotIn("H1", ids(found))

    def test_new_email_is_blocking(self):
        email = "ingrid.solberg" + "@" + "fenwick-dataworks.net"
        _, found = run_check({}, {"docs/contacts.md": email + "\n"})
        self.assertEqual(ids(found, "BLOCKING"), {"H3"})

    def test_international_phone_is_blocking(self):
        _, found = run_check({}, {"docs/contacts.md": "+44 7700 " + "900318" + "\n"})
        self.assertEqual(ids(found, "BLOCKING"), {"H3"})

    def test_national_phone_formats_are_blocking(self):
        for number in ("415 555 " + "0134", "(415) 555-" + "0134", "07700 " + "900123"):
            with self.subTest(number=number):
                _, found = run_check({}, {"docs/contacts.md": "Call " + number + " today\n"})
                self.assertEqual(ids(found, "BLOCKING"), {"H3"})

    def test_version_numbers_and_dates_are_not_phones(self):
        _, found = run_check({}, {"docs/a.md": "Version 1.2.3, released 2026-10-10, build 20261010.\n"})
        self.assertEqual(found, [])

    def test_home_path_is_blocking(self):
        _, found = run_check({}, {"docs/a.md": "/Users/" + "anders.holm" + "/notes\n"})
        self.assertEqual(ids(found, "BLOCKING"), {"H4"})

    def test_lookalike_email_domain_is_not_exempt(self):
        email = "someone" + "@" + "notexample" + ".com"
        _, found = run_check({}, {"docs/a.md": email + "\n"})
        self.assertIn("H3", ids(found, "BLOCKING"))

    def test_example_domain_and_subdomain_are_exempt(self):
        text = "a" + "@" + "example.com\nb" + "@" + "mail.example.org\n"
        _, found = run_check({}, {"docs/a.md": text})
        self.assertNotIn("H3", ids(found))

    def test_alphabetic_quoted_secret_is_blocking(self):
        line = "DB_" + "PASSWORD" + ' = "correcthorsebattery"\n'
        _, found = run_check({}, {"deploy/a.txt": line})
        self.assertIn("H1", ids(found, "BLOCKING"))

    def test_prose_about_tokens_is_not_a_secret(self):
        _, found = run_check({}, {"docs/a.md": "token: description of the field\n"})
        self.assertNotIn("H1", ids(found))

    def test_email_already_in_base_is_public(self):
        email = "owner" + "@" + "fenwick-dataworks.net"
        _, found = run_check({"docs/a.md": email + "\n"}, {"docs/b.md": email + "\n"})
        self.assertNotIn("H3", ids(found))

    def test_placeholder_user_path_is_ignored(self):
        _, found = run_check({}, {"docs/a.md": "/Users/" + "username" + "/notes\n"})
        self.assertNotIn("H4", ids(found))

    def test_private_notes_link_and_internal_host(self):
        link = "https://app." + "basicmemory" + ".com/notes?id=1"
        host = "https://build." + "corp" + "/status"
        _, found = run_check({}, {"docs/a.md": f"{link}\n{host}\n"})
        self.assertTrue({"H2", "H6"} <= ids(found, "BLOCKING"))

    def test_bare_internal_host_and_private_ipv6(self):
        for text in ("build." + "corp", "http://wiki." + "internal/page", "fd" + "00::1", "fe" + "80::1ff:fe23"):
            with self.subTest(text=text):
                _, found = run_check({}, {"docs/a.md": "see " + text + " now\n"})
                self.assertIn("H6", ids(found, "BLOCKING"))

    def test_local_settings_file_name_is_not_a_host(self):
        _, found = run_check({}, {"docs/a.md": "Edit .claude/settings.local.json and config.local.yaml.\n"})
        self.assertNotIn("H6", ids(found))

    def test_credential_file_is_blocking(self):
        _, found = run_check({}, {".env": "A=1\n"})
        self.assertIn("H1", ids(found, "BLOCKING"))

    def test_clean_change_passes(self):
        code, found = run_check({}, {"docs/a.md": "A plain sentence.\n"})
        self.assertEqual((code, found), (0, []))


class Shell(unittest.TestCase):
    def test_risky_shell_patterns(self):
        script = "\n".join([
            "curl -fsSL https://example.org/i.sh | sh",
            "echo x >> ~/." + "bashrc",
            "docker run -v /var/run/docker" + ".sock:/s img",
            "pip install requests",
            "pip install requests==2.0.0",
        ]) + "\n"
        _, found = run_check({}, {"scripts/setup.sh": script})
        self.assertTrue({"C1", "C2", "C3"} <= ids(found, "BLOCKING"))
        self.assertEqual(sum(1 for _, i in found if i == "C6"), 1)
        self.assertIn("C6", ids(found, "NON-BLOCKING"))


class Workflows(unittest.TestCase):
    def test_action_pinning_and_event_text(self):
        sha = "0123456789abcdef0123456789abcdef01234567"
        wf = "\n".join([
            "jobs:", "  t:", "    steps:",
            "      - uses: some-vendor/some-action@v2",
            "      - uses: actions/checkout@v4",
            f"      - uses: other/pinned-action@{sha}",
            '      - run: echo "${{ github.event.pull_request.title }}"',
            "        env:",
            "          TITLE: ${{ github.event.pull_request.title }}",
        ]) + "\n"
        _, found = run_check({}, {".github/workflows/t.yml": wf})
        self.assertIn(("BLOCKING", "C7"), found)
        self.assertIn(("NON-BLOCKING", "C7"), found)
        self.assertEqual(sum(1 for lab, i in found if i == "C7"), 2)
        self.assertEqual(sum(1 for lab, i in found if i == "C8"), 1)


class Skills(unittest.TestCase):
    def test_good_skill_has_no_blocking_findings(self):
        code, found = run_check({}, {"skills/good-skill/SKILL.md": GOOD_SKILL})
        self.assertEqual(ids(found, "BLOCKING"), set())
        self.assertEqual(code, 0)

    def test_bad_new_skill(self):
        bad = ("---\nname: Claude Helper Skill\ndescription: I help with things.\n---\n"
               + "line\n" * 120)
        _, found = run_check({}, {"skills/claude-helper/SKILL.md": bad})
        self.assertTrue({"S2", "S3", "S4", "S6"} <= ids(found, "BLOCKING"))
        self.assertIn("N5", ids(found, "NON-BLOCKING"))

    def test_skill_over_token_ceiling_is_blocking(self):
        big = GOOD_SKILL + ("word " * 600 + "\n")
        _, found = run_check({}, {"skills/good-skill/SKILL.md": big})
        self.assertIn("S7", ids(found, "BLOCKING"))

    def test_skill_under_token_ceiling_passes(self):
        _, found = run_check({}, {"skills/good-skill/SKILL.md": GOOD_SKILL})
        self.assertNotIn("S7", ids(found))

    def test_existing_oversize_skill_is_grandfathered_when_untouched(self):
        big = GOOD_SKILL + ("word " * 600 + "\n")
        _, found = run_check({"skills/good-skill/SKILL.md": big},
                             {"skills/good-skill/SKILL.md": big, "README.md": "# changed\n"})
        self.assertNotIn("S7", ids(found))

    def test_missing_frontmatter(self):
        _, found = run_check({}, {"skills/x/SKILL.md": "# no frontmatter\n"})
        self.assertIn("S1", ids(found, "BLOCKING"))

    def test_old_name_and_length_are_grandfathered_on_small_edit(self):
        old = ("---\nname: old-skill-with-many-words\ndescription: Do things. Use when needed.\n"
               "metadata:\n  origin: original\n  agent_involvement: none\n---\n" + "line\n" * 120)
        _, found = run_check({"skills/old-skill-with-many-words/SKILL.md": old},
                             {"skills/old-skill-with-many-words/SKILL.md": old.replace("Do things.", "Do tasks.")})
        self.assertNotIn("S2", ids(found))
        self.assertIn("S4", ids(found, "BLOCKING"))  # the edit adds a line to a file over 100 lines

    def test_pure_deletion_in_long_skill_is_not_flagged_for_length(self):
        old = ("---\nname: old-skill\ndescription: Do things. Use when needed.\n"
               "metadata:\n  origin: original\n  agent_involvement: none\n---\n" + "line\n" * 120)
        _, found = run_check({"skills/old-skill/SKILL.md": old},
                             {"skills/old-skill/SKILL.md": old.replace("line\n", "", 1)})
        self.assertNotIn("S4", ids(found))

    def test_upstream_origin_needs_divergence(self):
        text = GOOD_SKILL.replace("origin: original", "origin: example/repo@abc123")
        _, found = run_check({}, {"skills/good-skill/SKILL.md": text})
        self.assertIn("S6", ids(found, "BLOCKING"))

    def test_nested_reference_link(self):
        _, found = run_check({}, {"skills/good-skill/ref.md": "See [more](other.md).\n"})
        self.assertIn("S5", ids(found, "BLOCKING"))


class Writing(unittest.TestCase):
    def test_us_style_fixture_fails(self):
        text = "# Notes\n\nThe " + "color" + " setting \u2014 kept.\n\n---\n\nDone.\n"
        code, found = run_check({}, {"docs/style.md": text})
        self.assertEqual(ids(found, "BLOCKING"), {"W1", "W2", "W3"})
        self.assertEqual(code, 1)

    def test_british_fixture_passes(self):
        text = "# Notes\n\nThe colour setting, kept.\n\nDone.\n"
        code, found = run_check({}, {"docs/style.md": text})
        self.assertEqual((code, found), (0, []))

    def test_frontmatter_and_fenced_code_dividers_are_allowed(self):
        text = "---\ntitle: Note\n---\n\n```\n---\n```\n\nText.\n"
        _, found = run_check({}, {"docs/a.md": text})
        self.assertNotIn("W2", ids(found))

    def test_catalogue_and_untouched_lines_are_not_flagged(self):
        base = {"docs/a.md": "The " + "color" + " stays \u2014 here.\n"}
        head = {"docs/a.md": base["docs/a.md"] + "A catalogue entry.\n"}
        _, found = run_check(base, head)
        self.assertEqual(found, [])

    def test_uncommitted_broken_file_is_reported_in_working_tree_mode(self):
        broken = {"docs/broken.md": "Broken \u2014 file.\n\n---\n\nText.\n"}
        code, found = run_check({}, broken, working_tree=True, commit=False)
        self.assertEqual(code, 1)
        self.assertEqual(ids(found, "BLOCKING"), {"W1", "W2"})

    def test_uncommitted_edit_to_tracked_file_is_reported_in_working_tree_mode(self):
        code, found = run_check({"docs/a.md": "Fine.\n"}, {"docs/a.md": "Fine.\nBroken \u2014 line.\n"},
                                working_tree=True, commit=False)
        self.assertEqual((code, ids(found, "BLOCKING")), (1, {"W1"}))

    def test_commit_only_mode_ignores_uncommitted_files(self):
        code, found = run_check({}, {"docs/broken.md": "Broken \u2014 file.\n"}, commit=False)
        self.assertEqual((code, found), (0, []))


class StandardAndConfig(unittest.TestCase):
    def test_standard_edit_is_blocking(self):
        _, found = run_check({}, {"docs/standards/rules.md": "text\n"})
        self.assertIn("STD", ids(found, "NON-BLOCKING"))

    def test_agent_config_wording_is_non_blocking(self):
        _, found = run_check({"AGENTS.md": "a\n"}, {"AGENTS.md": "a\nA wording change.\n"})
        self.assertIn("C5", ids(found, "NON-BLOCKING"))
        self.assertNotIn("C5", ids(found, "BLOCKING"))

    def test_agent_config_hook_is_blocking(self):
        _, found = run_check({}, {".claude/settings.json": '{"hooks": {}}\n'})
        self.assertIn("C5", ids(found, "BLOCKING"))

    def test_expired_stamp_warns(self):
        doc = {"docs/standards/s.md": "Stamp: fresh until 2026-11-10.\n"}
        _, late = run_check(doc, {"x.md": "y\n"}, today="2026-12-01")
        _, early = run_check(doc, {"x.md": "y\n"}, today="2026-10-11")
        self.assertIn(("NON-BLOCKING", "CUR"), late)
        self.assertNotIn("CUR", ids(early))


if __name__ == "__main__":
    unittest.main()
