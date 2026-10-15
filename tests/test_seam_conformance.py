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


class ExtensionsAndCrossingRule(Verdict):
    def test_unknown_extension_is_ignored(self):
        result = run(lambda e: e["extensions"].update({"org.example.demo.batch-size": 4}))
        self.assertEqual(result["result"], "pass", result)

    def test_extension_key_must_be_namespaced(self):
        self.assertFails(run(lambda e: e["extensions"].update({"batch-size": 4})), "invalid-request")

    def test_extension_may_not_add_values_or_permission(self):
        for name in ("org.example.demo.extra-status", "org.example.demo.grant-delete",
                     "org.example.demo.allow-apply", "org.example.demo.vocabulary"):
            with self.subTest(name=name):
                self.assertFails(run(lambda e, n=name: e["extensions"].update({n: 1})), "not-permitted")

    def test_extension_value_cannot_be_text_or_structure(self):
        self.assertFails(run(lambda e: e["extensions"].update({"org.example.demo.note": "free text"})), "invalid-request")
        self.assertFails(run(lambda e: e["extensions"].update({"org.example.demo.rows": [1]})), "invalid-request")

    def test_extension_may_carry_an_opaque_reference(self):
        ref = "run-" + "b" * 26
        self.assertEqual(run(lambda e: e["extensions"].update({"org.example.demo.parent": ref}))["result"], "pass")

    def test_nothing_private_crosses(self):
        for key in ("checksum", "permalink", "note-id", "drive-id", "content", "source", "query",
                    "approval-record", "target", "before", "after", "diagnostic"):
            with self.subTest(key=key):
                self.assertFails(run(lambda e, k=key: e.update({k: "x"})), "invalid-request")
                self.assertFails(run(lambda e, k=key: e["extensions"].update({"org.example.demo." + k: 1})),
                                 "invalid-request")
                self.assertFails(run(lambda e, k=key: e["mutation-summary"]["read"].update({k: 1})), "invalid-request")


def refuse(op):
    """Mutate an envelope into the correct fail-closed report for one class."""
    def apply(e):
        row = e["mutation-summary"][op]
        row.update({"requested": 1, "granted": 0, "applied": 0, "refused": 1})
        e.update({"status": "refused", "error-category": "not-permitted", "disposition": "skipped"})
    return apply


def drop_grant(op):
    return lambda g: g.update({"grants": [x for x in g["grants"] if x["operation-class"] != op]})


class GrantsAndModes(Verdict):
    def test_request_outside_a_grant_must_be_refused_not_permitted(self):
        # write-report was requested but is no longer granted; the envelope still says granted.
        self.assertFails(run(grants_mutate=drop_grant("write-report")), "not-permitted")

    def test_correct_refusal_passes(self):
        def both(e):
            refuse("write-report")(e)
            e["mutation-summary"]["read"].update({"requested": 3, "granted": 3, "applied": 3})
        self.assertEqual(run(both, grants_mutate=drop_grant("write-report"))["result"], "pass")

    def test_refusal_reported_as_succeeded_fails(self):
        def lie(e):
            e["mutation-summary"]["write-report"].update({"granted": 0, "applied": 0, "refused": 1})
        self.assertFails(run(lie, grants_mutate=drop_grant("write-report")), "not-permitted")

    def test_refused_status_requires_not_permitted(self):
        self.assertFails(run(lambda e: e.update({"status": "refused", "error-category": "internal"})), "invalid-request")

    def test_grant_for_another_capability_grants_nothing(self):
        def other(g):
            for x in g["grants"]:
                x["capability"] = "knowledge.lint"
        self.assertFails(run(grants_mutate=other), "not-permitted")

    def test_grant_reference_must_match_the_grant_set(self):
        self.assertFails(run(lambda e: e.update({"grant-reference": "grant-" + "c" * 26})), "not-permitted")
        self.assertFails(run(lambda e: e.update({"grant-reference": ""})), "not-permitted")

    def test_empty_grant_reference_when_nothing_granted(self):
        def none(e):
            for op in ("read", "write-report"):
                refuse(op)(e)
            e["grant-reference"] = ""
            e["counts"].update({"seen": 0, "reported": 0})
        self.assertEqual(run(none, grants_mutate=lambda g: g.update({"grants": [], "grant-reference": ""}))["result"], "pass")

    def test_delete_is_never_granted(self):
        self.assertFails(run(grants_mutate=lambda g: g["grants"].append(
            {"capability": "knowledge.ingest", "operation-class": "delete"})), "not-permitted")
        self.assertFails(run(lambda e: e["mutation-summary"]["delete"].update(
            {"requested": 1, "granted": 1, "applied": 0})), "not-permitted")
        self.assertEqual(run(refuse("delete"))["result"], "pass")

    def test_apply_change_is_never_applied(self):
        self.assertFails(run(lambda e: e["mutation-summary"]["apply-change"].update(
            {"requested": 1, "granted": 1, "applied": 1})), "not-permitted")
        self.assertFails(run(lambda e: e.update({"disposition": "applied"})), "not-permitted")
        self.assertFails(run(lambda e: e["counts"].update({"applied": 1})), "not-permitted")

    def test_mode_grants_nothing_and_restricts(self):
        propose = lambda e: e["mutation-summary"]["propose-change"].update(  # noqa: E731
            {"requested": 1, "granted": 1, "applied": 1})
        # Report-only mode with a propose-change grant in the set: mode still bars it.
        add = lambda g: g["grants"].append({"capability": "knowledge.ingest", "operation-class": "propose-change"})  # noqa: E731
        self.assertFails(run(propose, grants_mutate=add), "not-permitted")
        # Propose-only mode plus the grant allows it.
        def both(g):
            add(g)
            g["mode"] = "propose-only"
        ok = run(lambda e: (propose(e), e.update({"disposition": "proposed"})), grants_mutate=both)
        self.assertEqual(ok["result"], "pass", ok)
        # Propose-only mode without the grant allows nothing extra.
        self.assertFails(run(propose, grants_mutate=lambda g: g.update({"mode": "propose-only"})), "not-permitted")

    def test_knowledge_ingest_accepts_only_report_only_and_propose_only(self):
        self.assertFails(run(grants_mutate=lambda g: g.update({"mode": "apply"})), "not-permitted")
        self.assertFails(run(grants_mutate=lambda g: g.update({"mode": "delete"})), "invalid-request")
        self.assertFails(run(profile_mutate=lambda p: p["execution-modes"].append("apply")), "not-permitted")


class ProfileChecks(Verdict):
    def test_profile_may_not_allow_apply_or_delete_in_0_1_0(self):
        for op in ("apply-change", "delete"):
            with self.subTest(op=op):
                self.assertFails(run(profile_mutate=lambda p, o=op: p["allowed-operation-classes"].append(o)), "not-permitted")

    def test_profile_must_match_the_envelope(self):
        self.assertFails(run(profile_mutate=lambda p: p.update({"capability": "knowledge.lint"})), "invalid-request")
        self.assertFails(run(profile_mutate=lambda p: p.update({"capability-version": "0.2.0"})), "invalid-request")
        self.assertFails(run(profile_mutate=lambda p: p.update({"seam-versions": ["0.2.0"]})), "invalid-request")

    def test_profile_conformance_status_is_closed(self):
        self.assertFails(run(profile_mutate=lambda p: p.update({"conformance-status": "green"})), "invalid-request")

    def test_profile_declares_every_field(self):
        _, prof, _ = base()
        for field in prof:
            with self.subTest(field=field):
                self.assertFails(run(profile_mutate=lambda p, f=field: p.pop(f)), "invalid-request")

    def test_capability_version_moves_independently_of_seam_version(self):
        def bump(p):
            p["capability-version"] = "0.3.0"
        self.assertEqual(run(lambda e: e.update({"capability-version": "0.3.0"}), profile_mutate=bump)["result"], "pass")


class CommandLine(unittest.TestCase):
    def test_exit_status_and_output(self):
        import subprocess
        script = os.path.join(ROOT, "scripts", "seam_conformance.py")
        args = ["--envelope", os.path.join(FIX, "envelope-report-only.json"), "--profile", PROFILE,
                "--grants", os.path.join(FIX, "grants-report-only.json")]
        done = subprocess.run([sys.executable, script, *args], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0)
        self.assertEqual(json.loads(done.stdout)["result"], "pass")
        bad = subprocess.run([sys.executable, script, "--envelope", "missing.json", *args[2:]], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(json.loads(bad.stdout)["error-category"], "invalid-request")


if __name__ == "__main__":
    unittest.main()
