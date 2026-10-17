"""Tests for the committed draft rc.1 profiles. Run: python3 -m unittest discover -s tests

The rc.1 profiles intentionally carry no approval fields: only the owner can
issue an approval. As committed they fail the default check by design and fail
`--rc` at rc-approval-state. The synthetic approval below exists only in memory,
is labelled as a placeholder, and is never written to disk or committed. It
proves the approval is the profiles' only remaining gap; it is not an approval.
"""
import copy
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import seam_conformance as sc  # noqa: E402

FIX = os.path.join(ROOT, "tests", "fixtures", "seam")
PROFILES = os.path.join(ROOT, "docs", "seam", "profiles")
FILES = {
    "knowledge.ingest": "knowledge-ingest-0.1.0-rc.1.json",
    "knowledge.lint": "knowledge-lint-0.1.0-rc.1.json",
}
# TEST PLACEHOLDER, NOT AN OWNER APPROVAL. Well-formed only so the checker's format rule is met.
PLACEHOLDER_APPROVAL_REFERENCE = "approval-syntheticplaceholderonlyzz"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def profile(capability):
    return load(os.path.join(PROFILES, FILES[capability]))


def inputs(capability):
    """Report-only envelope and grants (the existing fixtures) retargeted at one capability."""
    env = load(os.path.join(FIX, "envelope-report-only.json"))
    grants = load(os.path.join(FIX, "grants-report-only.json"))
    env["capability"] = capability
    for entry in grants["grants"]:
        entry["capability"] = capability
    return env, grants


def with_placeholder_approval(prof):
    """In-memory copy only. Never serialise the result."""
    synthetic = copy.deepcopy(prof)
    synthetic["approval-state"] = "approved"
    synthetic["approval-reference"] = PLACEHOLDER_APPROVAL_REFERENCE
    return synthetic


class Rc1Profiles(unittest.TestCase):
    def test_both_files_load_with_expected_shape(self):
        for capability in FILES:
            with self.subTest(capability=capability):
                prof = profile(capability)
                self.assertEqual(prof["capability"], capability)
                self.assertIn("apply", prof["execution-modes"])
                self.assertIn("apply-change", prof["allowed-operation-classes"])
                self.assertEqual("delete" in prof["allowed-operation-classes"], capability == "knowledge.lint")

    def test_committed_files_carry_no_approval_fields(self):
        for capability in FILES:
            with self.subTest(capability=capability):
                prof = profile(capability)
                self.assertNotIn("approval-state", prof)
                self.assertNotIn("approval-reference", prof)

    def test_default_mode_rejects_both_by_design(self):
        for capability in FILES:
            with self.subTest(capability=capability):
                env, grants = inputs(capability)
                result = sc.check(env, profile(capability), grants)
                self.assertEqual(result["result"], "fail", result)
                self.assertEqual(result["error-category"], "not-permitted")
                self.assertIn(result["rule"], ("profile-mode", "profile-operation-class"))

    def test_rc_mode_rejects_both_as_committed_at_approval_state(self):
        for capability in FILES:
            with self.subTest(capability=capability):
                env, grants = inputs(capability)
                result = sc.check(env, profile(capability), grants, rc=True)
                self.assertEqual(result["result"], "fail", result)
                self.assertEqual(result["rule"], "rc-approval-state")
                self.assertEqual(result["error-category"], "not-permitted")

    def test_placeholder_is_well_formed_and_not_on_disk(self):
        self.assertRegex(PLACEHOLDER_APPROVAL_REFERENCE, sc.REF_APPROVAL)
        for name in os.listdir(PROFILES):
            with open(os.path.join(PROFILES, name), encoding="utf-8") as f:
                self.assertNotIn(PLACEHOLDER_APPROVAL_REFERENCE, f.read())

    def test_in_memory_placeholder_approval_passes_rc_only(self):
        # Only the owner's approval is missing: with a placeholder the rest of each profile conforms.
        for capability in FILES:
            with self.subTest(capability=capability):
                env, grants = inputs(capability)
                synthetic = with_placeholder_approval(profile(capability))
                self.assertEqual(sc.check(env, synthetic, grants, rc=True)["result"], "pass")
                # The default check still rejects it: an approval never opens apply or delete there.
                self.assertEqual(sc.check(env, synthetic, grants)["result"], "fail")

    def test_placeholder_does_not_modify_the_loaded_profile(self):
        prof = profile("knowledge.lint")
        with_placeholder_approval(prof)
        self.assertNotIn("approval-state", prof)

    def test_delete_stays_with_knowledge_lint_even_with_placeholder(self):
        env, grants = inputs("knowledge.ingest")
        synthetic = with_placeholder_approval(profile("knowledge.ingest"))
        synthetic["allowed-operation-classes"].append("delete")
        self.assertEqual(sc.check(env, synthetic, grants, rc=True)["rule"], "profile-operation-class")


if __name__ == "__main__":
    unittest.main()
