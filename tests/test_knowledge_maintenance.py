import importlib.util
import pathlib
import unittest

_path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "knowledge_maintenance.py"
_spec = importlib.util.spec_from_file_location("knowledge_maintenance", _path)
km = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(km)

SHA = "a" * 40
CAPS = {c: True for c in km.REQUIRED_CAPABILITIES}
STATE = {"report_note": "r", "review_register": "q", "ledger_note": "l",
         "history_reconciled": True, "ledger": {}, "cursor": None}


def request(**kw):
    base = {"approved_commit_sha": SHA, "loaded_commit_sha": SHA, "wiki_project": "wiki",
            "run_id": "run-1", "budgets": {"sources": 3}}
    base.update(kw)
    return base


def src(i, checksum="c", created="2026-01-01"):
    return {"id": i, "checksum": checksum, "created": created}


class FakeStore:
    def __init__(self, content="old", conflict=False, lose_response=False):
        self.content, self.n, self.conflict, self.lose = content, 0, conflict, lose_response
        self.writes = 0

    def read(self, path):
        return {"content": self.content, "checksum": "v%d" % self.n}

    def write(self, path, content, expected_checksum):
        if self.conflict or expected_checksum != "v%d" % self.n:
            raise km.Conflict()
        self.content, self.n, self.writes = content, self.n + 1, self.writes + 1
        if self.lose:
            raise TimeoutError("response lost")


class Preflight(unittest.TestCase):
    def test_missing_pin_blocks(self):
        for bad in (None, "", "abc", "main"):
            self.assertEqual(km.preflight(request(approved_commit_sha=bad, loaded_commit_sha=bad),
                                          CAPS, STATE)["mode"], "blocked")

    def test_loaded_revision_mismatch_blocks(self):
        self.assertEqual(km.preflight(request(loaded_commit_sha="b" * 40), CAPS, STATE)["mode"], "blocked")

    def test_all_gates_pass_is_full(self):
        self.assertEqual(km.preflight(request(), CAPS, STATE)["mode"], "full")

    def test_unreconciled_history_is_read_only(self):
        r = km.preflight(request(), CAPS, dict(STATE, history_reconciled=False))
        self.assertEqual(r["mode"], "read_only")

    def test_undesignated_storage_is_read_only(self):
        for key in ("report_note", "review_register", "ledger_note"):
            self.assertEqual(km.preflight(request(), CAPS, dict(STATE, **{key: None}))["mode"], "read_only")

    def test_missing_write_guard_is_read_only(self):
        r = km.preflight(request(), dict(CAPS, guarded_overwrite=False), STATE)
        self.assertEqual(r["mode"], "read_only")


class Pagination(unittest.TestCase):
    def test_complete_read(self):
        pages = {1: {"items": [1, 2], "total": 3, "has_more": True},
                 2: {"items": [3], "total": 3, "has_more": False}}
        self.assertEqual(km.read_all(pages.__getitem__), [1, 2, 3])

    def test_total_mismatch_is_incomplete(self):
        with self.assertRaises(km.Incomplete):
            km.read_all(lambda n: {"items": [1], "total": 2, "has_more": False})

    def test_empty_page_with_more_is_incomplete(self):
        with self.assertRaises(km.Incomplete):
            km.read_all(lambda n: {"items": [], "has_more": True})


class Selection(unittest.TestCase):
    def test_unchanged_is_skipped_but_rotates(self):
        sources = [src("a"), src("b"), src("c")]
        ledger = {s["id"]: "c" for s in sources}
        sel, _, cur = km.select_sources(sources, ledger, None, 3)
        self.assertEqual(sel, [{"id": "a", "reason": "historical_rotation"}])
        sel2, _, cur2 = km.select_sources(sources, ledger, cur, 3)
        self.assertEqual((sel2[0]["id"], cur2), ("b", "b"))
        sel3, _, _ = km.select_sources(sources, ledger, "c", 3)
        self.assertEqual(sel3[0]["id"], "a")  # wraps

    def test_new_and_changed_first_with_reasons(self):
        sources = [src("a", "new-sum"), src("b"), src("c"), src("d")]
        ledger = {"a": "old-sum", "b": "c", "c": "c"}
        sel, deferred, _ = km.select_sources(sources, ledger, None, 3)
        self.assertEqual([(s["id"], s["reason"]) for s in sel],
                         [("a", "changed"), ("d", "new"), ("b", "historical_rotation")])
        self.assertEqual(deferred, [])

    def test_budget_exhaustion_defers_with_cursor_kept(self):
        sources = [src("n%d" % i, created="2026-01-%02d" % (i + 1)) for i in range(5)] + [src("z")]
        ledger = {"z": "c"}
        sel, deferred, cur = km.select_sources(sources, ledger, None, 3)
        self.assertEqual([s["id"] for s in sel], ["n0", "n1", "z"])
        self.assertEqual(deferred, ["n2", "n3", "n4"])
        self.assertEqual(cur, "z")


class Dispositions(unittest.TestCase):
    def test_settled_reversible_applies(self):
        self.assertEqual(km.classify({"op": "provenance_record", "reversible": True}), "apply")

    def test_human_gated_and_unknown_go_to_review(self):
        for op in sorted(km.HUMAN_GATED_OPS) + ["something_new"]:
            self.assertEqual(km.classify({"op": op, "reversible": True}), "review", op)

    def test_semantic_or_irreversible_settled_op_goes_to_review(self):
        self.assertEqual(km.classify({"op": "link_normalise", "reversible": False}), "review")
        self.assertEqual(km.classify({"op": "link_normalise", "reversible": True, "semantic": True}), "review")

    def test_task_lifecycle_proposal_is_never_applied(self):
        self.assertEqual(km.classify({"op": "task_lifecycle", "reversible": True}), "review")


class Findings(unittest.TestCase):
    F = {"kind": "novel_relation", "notes": ["b", "a"], "check": "rel-1"}

    def test_stable_id_ignores_note_order(self):
        self.assertEqual(km.finding_id("k", ["a", "b"], "c"), km.finding_id("k", ["b", "a"], "c"))

    def test_repeat_is_deduplicated_and_response_preserved(self):
        reg, added = km.merge_findings([], [self.F])
        self.assertEqual(len(added), 1)
        reg[0]["status"], reg[0]["response"] = "answered", "yes"
        reg2, added2 = km.merge_findings(reg, [self.F, self.F])
        self.assertEqual((added2, len(reg2)), ([], 1))
        self.assertEqual((reg2[0]["status"], reg2[0]["response"]), ("answered", "yes"))


class Writes(unittest.TestCase):
    def test_write_and_verify(self):
        s = FakeStore()
        out = km.guarded_write(s, "p", "new")
        self.assertEqual((out["outcome"], out["before"], out["after"]), ("written", "v0", "v1"))

    def test_second_identical_write_is_noop(self):
        s = FakeStore()
        km.guarded_write(s, "p", "new")
        self.assertEqual(km.guarded_write(s, "p", "new")["outcome"], "already_applied")
        self.assertEqual(s.writes, 1)

    def test_conflict_blocks_item_without_write(self):
        s = FakeStore(conflict=True)
        self.assertEqual(km.guarded_write(s, "p", "new")["outcome"], "conflict")
        self.assertEqual(s.writes, 0)

    def test_uncertain_response_rereads_and_does_not_duplicate(self):
        s = FakeStore(lose_response=True)
        out = km.guarded_write(s, "p", "new")
        self.assertEqual(out["outcome"], "written")
        self.assertEqual(s.writes, 1)


class IndexDrift(unittest.TestCase):
    def test_not_due_is_skipped(self):
        self.assertEqual(km.index_drift_plan(["a"], {}, False)["status"], "skipped")

    def test_policy_aware_modes(self):
        pol = {"a": {"index_scope": "exhaustive", "scheduled_repair": "allowed"},
               "b": {"index_scope": "curated", "scheduled_repair": "report-only"},
               "c": {"index_scope": "exhaustive"},
               "d": {"index_scope": "exhaustive", "scheduled_repair": "report-only"}}
        plan = km.index_drift_plan(["d", "c", "b", "a", "e"], pol, True)["folders"]
        self.assertEqual(plan, {"a": "repair_allowed", "b": "check_only", "c": "inspect_only",
                                "d": "check_only", "e": "inspect_only"})
        self.assertEqual(list(plan), ["a", "b", "c", "d", "e"])


class Run(unittest.TestCase):
    sources = [src("a", "x"), src("b", "y")]

    @staticmethod
    def ok(i):
        return {"mutations": [{"target": i}], "findings": []}

    @staticmethod
    def lint_ok(notes):
        return {"mutations": [], "findings": [{"kind": "k", "notes": notes, "check": "c"}]}

    def test_blocked_run_touches_nothing(self):
        calls = []
        res = km.run(request(approved_commit_sha=None), CAPS, STATE, self.sources,
                     lambda i: calls.append(i), lambda n: calls.append(n))
        self.assertEqual((res["mode"], calls, res["mutations"]), ("blocked", [], []))

    def test_read_only_discards_mutations_and_keeps_ledger(self):
        res = km.run(request(), CAPS, dict(STATE, history_reconciled=False), self.sources,
                     self.ok, self.lint_ok)
        self.assertEqual(res["mode"], "read_only")
        self.assertEqual((res["mutations"], res["ledger"]), ([], {}))
        self.assertEqual(res["discarded_mutations"], 2)
        self.assertEqual(len(res["findings"]), 1)

    def test_ingest_failure_does_not_stop_lint(self):
        def process(i):
            if i == "a":
                raise RuntimeError("boom")
            return self.ok(i)
        res = km.run(request(), CAPS, STATE, self.sources, process, self.lint_ok)
        self.assertEqual([f["id"] for f in res["failed"]], ["a"])
        self.assertEqual(res["completed"], ["b"])
        self.assertEqual(res["findings"][0]["notes"], ["b"])
        self.assertNotIn("a", res["ledger"])

    def test_repeat_run_is_idempotent(self):
        first = km.run(request(), CAPS, STATE, self.sources, self.ok, self.lint_ok)
        state2 = dict(STATE, ledger=first["ledger"], cursor=first["cursor"])
        second = km.run(request(), CAPS, state2, self.sources, self.ok, self.lint_ok)
        self.assertEqual(sorted(first["ledger"]), ["a", "b"])
        self.assertEqual(second["ledger"], first["ledger"])
        self.assertEqual([s for s in second["completed"] if s in ("a", "b")],
                         second["completed"])
        self.assertEqual(len(second["completed"]), 1)  # only the rotation slot
        reg, _ = km.merge_findings([], first["findings"])
        reg2, added = km.merge_findings(reg, first["findings"])
        self.assertEqual((reg2, added), (reg, []))

    def test_budget_exhaustion_reports_deferred(self):
        many = [src("s%d" % i, created="2026-01-%02d" % (i + 1)) for i in range(6)]
        res = km.run(request(budgets={"sources": 2}), CAPS, STATE, many, self.ok, self.lint_ok)
        self.assertEqual(len(res["completed"]), 2)
        self.assertEqual(len(res["deferred"]), 4)


if __name__ == "__main__":
    unittest.main()
