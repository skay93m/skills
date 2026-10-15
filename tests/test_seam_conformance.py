"""Tests for scripts/seam_conformance.py. Run: python3 -m unittest discover -s tests

All data is synthetic. Tests go through check(), the public entry point, and
through the command line; they never touch a real backend.
"""
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import seam_conformance as sc  # noqa: E402

FIX = os.path.join(ROOT, "tests", "fixtures", "seam")
PROFILE = os.path.join(ROOT, "docs", "seam", "profiles", "knowledge-ingest-0.1.0.json")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def base():
    return (load(os.path.join(FIX, "envelope-report-only.json")),
            load(PROFILE),
            load(os.path.join(FIX, "grants-report-only.json")))


def run(mutate=None, profile_mutate=None, grants_mutate=None):
    env, prof, grants = base()
    if mutate:
        mutate(env)
    if profile_mutate:
        profile_mutate(prof)
    if grants_mutate:
        grants_mutate(grants)
    return sc.check(env, prof, grants)


class Verdict(unittest.TestCase):
    def assertFails(self, result, category):
        self.assertEqual(result["result"], "fail", result)
        self.assertEqual(result["error-category"], category, result)
        self.assertEqual(result["conformance-status"], "failed")

    def test_valid_report_only_envelope_passes(self):
        result = run()
        self.assertEqual(result["result"], "pass")
        self.assertEqual(result["error-category"], "")
        self.assertEqual(result["conformance-status"], "passed")


class RequiredFieldsAndVocabularies(Verdict):
    def test_every_required_field_is_needed(self):
        env, _, _ = base()
        for field in env:
            with self.subTest(field=field):
                self.assertFails(run(lambda e, f=field: e.pop(f)), "invalid-request")

    def test_version_fields_are_separate_and_not_combined(self):
        self.assertFails(run(lambda e: e.update({"capability": "knowledge.ingest@0.1.0"})), "invalid-request")
        self.assertFails(run(lambda e: e.update({"seam-version": "1"})), "invalid-request")
        self.assertFails(run(lambda e: e.update({"capability-version": ""})), "invalid-request")

    def test_only_closed_vocabulary_values(self):
        for field, bad in (("status", "done"), ("disposition", "deleted"),
                           ("approval-state", "maybe"), ("error-category", "oops")):
            with self.subTest(field=field):
                self.assertFails(run(lambda e, f=field, b=bad: e.update({f: b})), "invalid-request")

    def test_succeeded_needs_empty_error_category(self):
        self.assertFails(run(lambda e: e.update({"error-category": "internal"})), "invalid-request")

    def test_failed_needs_an_error_category(self):
        self.assertFails(run(lambda e: e.update({"status": "failed"})), "invalid-request")

    def test_counts_use_closed_integer_keys(self):
        self.assertFails(run(lambda e: e["counts"].update({"items": 1})), "invalid-request")
        self.assertFails(run(lambda e: e["counts"].update({"seen": "3"})), "invalid-request")
        self.assertFails(run(lambda e: e["counts"].update({"seen": -1})), "invalid-request")
        self.assertFails(run(lambda e: e["counts"].pop("failed")), "invalid-request")

    def test_mutation_summary_covers_every_class_with_four_counts(self):
        self.assertFails(run(lambda e: e["mutation-summary"].pop("delete")), "invalid-request")
        self.assertFails(run(lambda e: e["mutation-summary"].update({"remove": {}})), "invalid-request")
        self.assertFails(run(lambda e: e["mutation-summary"]["read"].pop("refused")), "invalid-request")

    def test_reference_formats(self):
        self.assertFails(run(lambda e: e.update({"run-reference": "note-123"})), "invalid-request")
        self.assertFails(run(lambda e: e.update({"grant-reference": "grant-short"})), "invalid-request")


if __name__ == "__main__":
    unittest.main()
