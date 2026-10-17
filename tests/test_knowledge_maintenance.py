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
    base = {"approved_commit_sha": SHA, "loaded_commit_sha": SHA, "wiki_project": "sk-wiki",
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


class RevisionOk(unittest.TestCase):
    A, B = "a" * 40, "b" * 40

    def test_unattended_match_passes(self):
        self.assertTrue(km.revision_ok(self.A, self.A, False))

    def test_unattended_mismatch_fails(self):
        self.assertFalse(km.revision_ok(self.A, self.B, False))

    def test_unattended_requires_approved(self):
        for bad in (None, "", "none", "main", "a" * 39, "a" * 41, "A" * 40, "g" * 40, 5):
            self.assertFalse(km.revision_ok(self.A, bad, False), bad)

    def test_loaded_must_be_full_sha(self):
        for bad in (None, "", "none", "main", "a" * 39, "A" * 40, "a" * 40 + "\n"):
            self.assertFalse(km.revision_ok(bad, self.A, False), bad)
            self.assertFalse(km.revision_ok(bad, "none", True), bad)

    def test_supervised_may_record_none(self):
        self.assertTrue(km.revision_ok(self.A, "none", True))
        self.assertTrue(km.revision_ok(self.A, None, True))

    def test_supervised_with_approved_must_still_match(self):
        self.assertTrue(km.revision_ok(self.A, self.A, True))
        self.assertFalse(km.revision_ok(self.A, self.B, True))
        self.assertFalse(km.revision_ok(self.A, "main", True))

    def test_preflight_accepts_revision_names(self):
        r = request(approved_commit_sha=None, approved_revision=self.A,
                    loaded_commit_sha=None, loaded_revision=self.A)
        self.assertEqual(km.preflight(r, CAPS, STATE)["mode"], "full")
        r = request(approved_commit_sha=None, approved_revision=self.B,
                    loaded_commit_sha=None, loaded_revision=self.A)
        self.assertEqual(km.preflight(r, CAPS, STATE)["mode"], "blocked")


class Preflight(unittest.TestCase):
    def test_missing_revision_blocks(self):
        for bad in (None, "", "abc", "main"):
            self.assertEqual(km.preflight(request(approved_commit_sha=bad, loaded_commit_sha=bad),
                                          CAPS, STATE)["mode"], "blocked")

    def test_supervised_true_with_tracking_branch_and_loaded_sha_passes(self):
        r = km.preflight(request(approved_commit_sha=None, tracking_branch="main", supervised=True,
                                 loaded_commit_sha="a" * 40), CAPS, STATE)
        self.assertEqual(r["mode"], "full")

    def test_supervised_without_valid_loaded_sha_blocks(self):
        for bad in (None, "", "not-a-sha"):
            r = km.preflight(request(approved_commit_sha=None, tracking_branch="main", supervised=True,
                                     loaded_commit_sha=bad), CAPS, STATE)
            self.assertEqual(r["mode"], "blocked")

    def test_tracking_branch_without_supervised_is_unattended(self):
        # Absent supervised flag: a tracking branch does not relax the rules.
        r = km.preflight(request(approved_commit_sha=None, tracking_branch="main",
                                 loaded_commit_sha="a" * 40), CAPS, STATE)
        self.assertEqual(r["mode"], "blocked")
        r = km.preflight(request(approved_commit_sha=None, tracking_branch="main", supervised=False,
                                 loaded_commit_sha="a" * 40), CAPS, STATE)
        self.assertEqual(r["mode"], "blocked")

    def test_supervised_must_be_boolean_true(self):
        for bad in ("true", "True", 1, "yes", [True], None):
            r = km.preflight(request(approved_commit_sha=None, tracking_branch="main", supervised=bad,
                                     loaded_commit_sha="a" * 40), CAPS, STATE)
            self.assertEqual(r["mode"], "blocked", bad)

    def test_revision_ok_strict_supervised(self):
        for bad in ("true", 1, "yes"):
            self.assertFalse(km.revision_ok("a" * 40, "none", bad), bad)

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


class LoadedRevision(unittest.TestCase):
    """Tracking main with an optional owner-set override (#106), seen through run()."""

    SOURCES = [src("raw/a")]
    OTHER = "b" * 40

    def go(self, **kw):
        store = FakeStore()
        res = km.run(request(**kw), CAPS, dict(STATE), self.SOURCES,
                     lambda i: {"proposals": [{"op": "provenance_record", "path": "n", "content": "x"}]},
                     lambda n: {"findings": []}, store=store)
        return res, store

    def test_tracking_resolves_and_records_the_loaded_commit(self):
        # Adapted for the explicit supervised flag: tracking main with no approved SHA is supervised only.
        res, _ = self.go(approved_commit_sha=None, tracking_branch="main", supervised=True,
                         loaded_commit_sha=self.OTHER)
        self.assertNotEqual(res["mode"], "blocked")
        self.assertEqual(res["revision"], self.OTHER)
        res, _ = self.go(approved_commit_sha=None, tracking_branch="main", loaded_commit_sha=self.OTHER)
        self.assertEqual(res["mode"], "blocked")
        self.assertIn("Revision: " + self.OTHER, km.render_report(res))
        self.assertNotIn("Revision: None", km.render_report(res))

    def test_override_equal_to_loaded_is_honoured_and_recorded(self):
        res, _ = self.go(tracking_branch="main", approved_commit_sha=SHA, loaded_commit_sha=SHA)
        self.assertNotEqual(res["mode"], "blocked")
        self.assertEqual(res["revision"], SHA)

    def test_override_wins_over_tracking_when_loaded_differs(self):
        res, store = self.go(tracking_branch="main", approved_commit_sha=SHA, loaded_commit_sha=self.OTHER)
        self.assertEqual(res["mode"], "blocked")
        self.assertEqual((res["mutations"], store.writes), ([], 0))
        self.assertEqual(res["revision"], self.OTHER)

    def test_malformed_override_blocks_a_tracking_run(self):
        for bad in ("abc", "main", "A" * 40):
            res, store = self.go(tracking_branch="main", approved_commit_sha=bad, loaded_commit_sha=SHA)
            self.assertEqual(res["mode"], "blocked")
            self.assertTrue(any("approved_commit_sha" in r for r in res["reasons"]))
            self.assertEqual((res["mutations"], res["completed"], store.writes), ([], [], 0))

    def test_unresolved_or_malformed_loaded_revision_blocks_with_no_mutation(self):
        for bad in (None, "", "not-a-sha"):
            for override in (None, SHA):
                res, store = self.go(tracking_branch="main", approved_commit_sha=override, loaded_commit_sha=bad)
                self.assertEqual(res["mode"], "blocked")
                self.assertEqual((res["mutations"], store.writes), ([], 0))
                self.assertNotIn("Revision: " + SHA, km.render_report(res))

    def test_sha_with_trailing_newline_is_not_a_full_sha(self):
        nl = SHA + "\n"
        for kw in (dict(tracking_branch="main", approved_commit_sha=nl, loaded_commit_sha=SHA),
                   dict(tracking_branch="main", approved_commit_sha=None, loaded_commit_sha=nl)):
            res, store = self.go(**kw)
            self.assertEqual(res["mode"], "blocked")
            self.assertEqual((res["mutations"], store.writes), ([], 0))

    def test_blocked_report_does_not_present_an_unloaded_value_as_the_revision(self):
        for bad in ("not-a-sha", "main", SHA + "\n"):
            res, _ = self.go(tracking_branch="main", approved_commit_sha=None, loaded_commit_sha=bad)
            self.assertEqual(res["mode"], "blocked")
            self.assertIsNone(res["revision"])
            self.assertNotIn("Revision: " + bad, km.render_report(res))

    def test_recorded_revision_is_the_loaded_one_without_tracking(self):
        res, _ = self.go()
        self.assertEqual(res["revision"], SHA)

    def test_no_tracking_and_no_override_stays_blocked(self):
        res, _ = self.go(approved_commit_sha=None, loaded_commit_sha=SHA)
        self.assertEqual(res["mode"], "blocked")


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

    def test_deletion_is_never_applied(self):
        for op in ("delete", "move_delete", "overwrite_source"):
            self.assertEqual(km.classify({"op": op, "reversible": True}), "review")

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
        self.assertEqual(plan, {"a": "repair_allowed", "b": "check_only", "c": "check_only",
                                "d": "check_only", "e": "check_only"})
        full = km.index_drift_plan(["d", "c", "b", "a", "e"], pol, True)
        self.assertEqual(full["unpoliced"], ["c", "e"])  # logged, never inferred
        self.assertEqual(list(plan), ["a", "b", "c", "d", "e"])


def prop(path="n1", op="link_normalise", content="new", **kw):
    return dict({"path": path, "op": op, "content": content, "reversible": True}, **kw)


class WikiStore:
    """Dict-backed store with checksum compare-and-swap, for whole-run tests."""
    def __init__(self, notes):
        self.notes = {k: [v, 0] for k, v in notes.items()}
        self.log = []

    def read(self, path):
        return {"content": self.notes[path][0], "checksum": "v%d" % self.notes[path][1]}

    def write(self, path, content, expected_checksum):
        if expected_checksum != "v%d" % self.notes[path][1]:
            raise km.Conflict()
        self.notes[path] = [content, self.notes[path][1] + 1]
        self.log.append(path)


class Run(unittest.TestCase):
    sources = [src("a", "x"), src("b", "y")]

    @staticmethod
    def ok(i):
        return {"proposals": [prop(i)], "findings": []}

    @staticmethod
    def lint_ok(notes):
        return {"proposals": [], "findings": [{"kind": "k", "notes": notes, "check": "c"}]}

    def store(self):
        return WikiStore({"a": "old", "b": "old"})

    def test_blocked_run_touches_nothing(self):
        calls = []
        res = km.run(request(approved_commit_sha=None), CAPS, STATE, self.sources,
                     lambda i: calls.append(i), lambda n: calls.append(n))
        self.assertEqual((res["mode"], calls, res["mutations"]), ("blocked", [], []))

    def test_read_only_never_writes_and_lists_would_apply(self):
        st = self.store()
        res = km.run(request(), CAPS, dict(STATE, history_reconciled=False), self.sources,
                     self.ok, self.lint_ok, store=st)
        self.assertEqual((res["mode"], res["mutations"], res["ledger"], st.log), ("read_only", [], {}, []))
        self.assertEqual(sorted(w["path"] for w in res["would_apply"]), ["a", "b"])

    def test_full_run_writes_verifies_and_ledgers(self):
        st = self.store()
        res = km.run(request(), CAPS, STATE, self.sources, self.ok, self.lint_ok, store=st)
        self.assertEqual(sorted(st.log), ["a", "b"])
        self.assertEqual(res["ledger"], {"a": "x", "b": "y"})
        self.assertTrue(all(m["before"] != m["after"] for m in res["mutations"]))

    def test_semantic_proposal_becomes_review_not_write(self):
        st = self.store()
        res = km.run(request(), CAPS, STATE, self.sources,
                     lambda i: {"proposals": [prop(i, op="new_relation")], "findings": []},
                     self.lint_ok, store=st)
        self.assertEqual(st.log, [])
        self.assertTrue(any(f["kind"] == "proposal:new_relation" for f in res["findings"]))

    def test_conflict_blocks_only_that_item(self):
        st = self.store()
        st.notes["a"][1] = 5  # concurrent edit after the planner read? simulate stale expected
        orig = st.read
        st.read = lambda p: dict(orig(p), checksum="stale") if p == "a" else orig(p)
        res = km.run(request(), CAPS, STATE, self.sources, self.ok, self.lint_ok, store=st)
        self.assertEqual(res["blocked_items"], ["a"])
        self.assertEqual(res["completed"], ["b"])
        self.assertNotIn("a", res["ledger"])

    def test_ingest_failure_does_not_stop_lint(self):
        def process(i):
            if i == "a":
                raise RuntimeError("boom")
            return self.ok(i)
        res = km.run(request(), CAPS, STATE, self.sources, process, self.lint_ok, store=self.store())
        self.assertEqual([f["id"] for f in res["failed"]], ["a"])
        self.assertEqual(res["lint_scope"], ["b"])
        self.assertNotIn("a", res["ledger"])

    def test_repeat_run_is_idempotent(self):
        st = self.store()
        first = km.run(request(), CAPS, STATE, self.sources, self.ok, self.lint_ok, store=st)
        state2 = dict(STATE, ledger=first["ledger"], cursor=first["cursor"])
        second = km.run(request(run_id="run-2"), CAPS, state2, self.sources, self.ok, self.lint_ok, store=st)
        self.assertEqual(second["ledger"], first["ledger"])
        self.assertEqual(len(second["completed"]), 1)  # rotation slot only
        self.assertEqual(second["mutations"], [])      # content already applied
        self.assertEqual(sorted(st.log), ["a", "b"])
        self.assertEqual(first["review_ids"], km.run(request(), CAPS, STATE, self.sources, self.ok,
                                                      self.lint_ok, store=self.store())["review_ids"])

    def test_crash_resume_skips_done_items_in_same_run(self):
        saved = []
        st = self.store()

        class Crash(Exception):
            pass

        def cp(s):
            saved.append(s)
            if len(saved) == 1:
                raise Crash()
        with self.assertRaises(Crash):
            km.run(request(), CAPS, STATE, self.sources, self.ok, self.lint_ok, store=st, checkpoint=cp)
        resume = dict(STATE, **saved[0])
        seen = []
        res = km.run(request(), CAPS, resume, self.sources,
                     lambda i: (seen.append(i), self.ok(i))[1], self.lint_ok, store=st)
        self.assertNotIn(saved[0]["done"][0], seen)
        self.assertEqual(sorted(res["ledger"]), ["a", "b"])
        self.assertEqual(sorted(st.log), ["a", "b"])

    def test_budget_exhaustion_defers_and_mutation_cap(self):
        many = [src("s%d" % i, created="2026-01-%02d" % (i + 1)) for i in range(6)]
        st = WikiStore({"s%d" % i: "old" for i in range(6)})
        res = km.run(request(budgets={"sources": 4, "mutations": 2}), CAPS, STATE, many,
                     self.ok, self.lint_ok, store=st)
        self.assertEqual(len(st.log), 2)
        self.assertEqual(len(res["completed"]), 2)
        self.assertEqual(sorted(res["deferred"]), ["s2", "s3", "s4", "s5"])

    def test_lint_scope_is_capped_and_queue_drains(self):
        many = [src("s%d" % i, created="2026-01-%02d" % (i + 1)) for i in range(15)]
        st = WikiStore({"s%d" % i: "old" for i in range(15)})
        seen = []
        res = km.run(request(budgets={"sources": 15, "mutations": 99, "lint_notes": 12}), CAPS,
                     dict(STATE, lint_queue=["q1", "q2"]), many, self.ok,
                     lambda n: (seen.append(n), {"findings": []})[1], store=st)
        self.assertEqual(len(seen[0]), 12)
        self.assertEqual(len(set(seen[0])), 12)

    def test_missing_drive_is_reported_not_fatal(self):
        res = km.run(request(), CAPS, STATE, self.sources, self.ok, self.lint_ok, store=self.store())
        self.assertTrue(any("Drive" in x for x in res["limitations"]))
        self.assertEqual(res["mode"], "full")


class Persistence(unittest.TestCase):
    def test_state_round_trip_and_fail_closed(self):
        s = {"run_id": "r", "ledger": {"a": "x"}, "cursor": "a", "deferred": [], "lint_queue": [], "done": ["a"]}
        self.assertEqual(km.load_state(km.dump_state(s)), s)
        for bad in ("", "no block", "```km-state\n{}\n```", "```km-state\nnot json\n```"):
            with self.assertRaises((ValueError, KeyError)):
                km.load_state(bad)

    def test_report_is_plain_markdown_with_required_facts(self):
        res = km.run(request(), CAPS, STATE, [src("a", "x")], lambda i: {"proposals": [prop(i)]},
                     lambda n: {"findings": []}, store=WikiStore({"a": "old"}))
        text = km.render_report(res)
        for needle in ("run-1", SHA, "Mutation: a v0 -> v1", "Limitation: Drive", "Lint index drift"):
            self.assertIn(needle, text)
        self.assertNotIn("[[", text)


class DryRunFixture(unittest.TestCase):
    """The committed synthetic snapshot exercises the whole workflow read-only."""

    def test_fixture_dry_run(self):
        import json
        snap = json.load(open(_path.parent.parent / "tests" / "fixtures" / "dry_run_snapshot.json"))
        plans = snap["proposals"]
        res = km.run(snap["request"], snap["capabilities"], snap["state"], snap["sources"],
                     lambda i: {"proposals": plans.get(i, [])},
                     lambda n: {"findings": snap["lint_findings"]}, store=None,
                     index=(snap["folders"], snap["policies"], True))
        self.assertEqual(res["mode"], "read_only")
        self.assertEqual(res["mutations"], [])
        self.assertEqual(res["cursor"], snap["state"]["cursor"])
        self.assertEqual(res["completed"], ["raw/changed-note", "raw/new-note", "raw/old-b"])
        self.assertEqual([w["op"] for w in res["would_apply"]], ["provenance_record"])
        kinds = sorted(f["kind"] for f in res["findings"])
        self.assertEqual(kinds, ["missing_index_policy", "proposal:new_relation", "proposal:task_lifecycle", "stale_claim"])
        self.assertEqual(res["index_drift"]["folders"],
                         {"projects": "repair_allowed", "systems": "check_only", "tasks": "check_only"})
        self.assertIn("notes/stale-1", res["lint_scope"])
        self.assertIn("missing_index_policy", [f["kind"] for f in res["findings"]])


class GuardedUnattendedRules(unittest.TestCase):
    def test_legacy_wiki_project_blocks(self):
        r = km.preflight(request(wiki_project="wiki"), CAPS, STATE)
        self.assertEqual(r["mode"], "blocked")

    def test_snapshot_name_and_clock(self):
        self.assertEqual(km.derived_snapshot_name("2026-10-16"), "auto-daily-auto-20261016-000000")
        # BST runs (03:00 London is 02:00 UTC)
        self.assertTrue(km.clock_ok("02:15"))
        self.assertTrue(km.clock_ok("02:30"))
        # GMT runs (03:00 London is 03:00 UTC)
        self.assertTrue(km.clock_ok("03:15"))
        self.assertTrue(km.clock_ok("04:00"))
        # Rejections outside 02:00-06:00 UTC window
        self.assertFalse(km.clock_ok("01:59"))
        self.assertFalse(km.clock_ok("06:01"))
        self.assertFalse(km.clock_ok("14:00"))
        self.assertFalse(km.clock_ok("23:59"))

    def test_change_key(self):
        self.assertEqual(km.change_key("f1", 10, "t"), ["f1", 10, "t"])
        self.assertEqual(km.change_key("f1", 10, "t", "ab"), ["f1", 10, "t", "ab"])

    def test_clock_parses_time(self):
        for bad in ("3:00", "T03:00", "03:15 ", "25:00", "", None, "0315"):
            self.assertFalse(km.clock_ok(bad), bad)
        self.assertTrue(km.clock_ok("02:00:00"))
        self.assertTrue(km.clock_ok("03:15:00"))
        self.assertTrue(km.clock_ok("06:00:00"))
        self.assertFalse(km.clock_ok("01:59:59"))
        self.assertFalse(km.clock_ok("06:00:01"))
        self.assertFalse(km.clock_ok("23:59"))

    def dele(self, entry, **kw):
        kw.setdefault("first_run_limit", False)
        return km.deletion_allowed(entry, **kw)

    def test_deletion_allowlist(self):
        base = {"permalink": "scratch/x", "before_checksum": "c"}
        self.assertTrue(self.dele(dict(base, allowlist_rule="scratch"), run_created=["scratch/x"]))
        self.assertFalse(self.dele(dict(base, allowlist_rule="scratch")))
        dup = dict(base, permalink="knowledge/a", allowlist_rule="duplicate")
        self.assertTrue(self.dele(dict(dup, similarity_score=0.97)))
        self.assertFalse(self.dele(dict(dup, similarity_score=0.9)))
        self.assertFalse(self.dele(dup))
        self.assertFalse(self.dele(dict(base, allowlist_rule="other")))
        self.assertFalse(self.dele({"permalink": "scratch/x", "allowlist_rule": "scratch"}))

    def test_similarity_must_be_numeric(self):
        base = {"permalink": "knowledge/a", "before_checksum": "c", "allowlist_rule": "duplicate"}
        for bad in (None, True, "0.99", 1.5):
            self.assertFalse(self.dele(dict(base, similarity_score=bad)), bad)
        self.assertFalse(self.dele(dict(base, allowlist_rule="scratch", permalink="scratch/x",
                                        similarity_score=0.99), run_created=["scratch/x"]))

    def test_scratch_needs_prefix_and_run_origin(self):
        e = {"permalink": "knowledge/real-note", "before_checksum": "c", "allowlist_rule": "scratch"}
        self.assertFalse(self.dele(e, run_created=["knowledge/real-note"]))
        e = dict(e, permalink="scratch/tmp")
        self.assertFalse(self.dele(e))
        self.assertFalse(self.dele(e, run_created=["scratch/other"]))
        self.assertTrue(self.dele(e, run_created=["scratch/tmp"]))
        e = dict(e, permalink="ws/sk-wiki/scratch/tmp")
        self.assertTrue(self.dele(e, run_created=["scratch/tmp"]))

    FIXTURE = {"allowlist_rule": "fixture", "before_checksum": "c", "body_chars": 0, "size": 0}

    def test_fixture_rule_is_encoded(self):
        f = dict(self.FIXTURE, permalink="knowledge/empty")
        self.assertTrue(self.dele(f))
        self.assertTrue(self.dele(dict(f, size=40, frontmatter_parses=False)))
        self.assertFalse(self.dele(dict(f, body_chars=12)))
        self.assertFalse(self.dele(dict(f, body_chars=12, size=40, frontmatter_parses=False)))
        self.assertFalse(self.dele(dict(f, size=40, frontmatter_parses=True)))
        self.assertFalse(self.dele(dict(f, size=40)))
        self.assertFalse(self.dele({k: v for k, v in f.items() if k != "body_chars"}))
        self.assertFalse(self.dele(dict(f, body_chars=True)))

    def test_deletion_path_scope(self):
        for p in ("operations/r0-start", "operations/r0", "operations/issues/schema-drift",
                  "schemas/concept", "index", "log", "knowledge/index/../../log",
                  "ws/wiki/knowledge/a", "wiki/knowledge/a", "other/a"):
            self.assertFalse(self.dele(dict(self.FIXTURE, permalink=p)), p)
            self.assertFalse(self.dele({"permalink": p, "before_checksum": "c",
                                        "allowlist_rule": "duplicate", "similarity_score": 0.99}), p)
        for p in ("knowledge/a", "source-notes/a", "ws/sk-wiki/knowledge/a"):
            self.assertTrue(self.dele(dict(self.FIXTURE, permalink=p)), p)

    def test_no_deletion_under_first_run_limit(self):
        e = {"permalink": "scratch/x", "before_checksum": "c", "allowlist_rule": "scratch"}
        for flag in (True, None):
            self.assertFalse(km.deletion_allowed(e, run_created=["scratch/x"], first_run_limit=flag))
        self.assertFalse(km.deletion_allowed(e, run_created=["scratch/x"]))
        self.assertTrue(km.deletion_allowed(e, run_created=["scratch/x"], first_run_limit=False))

    def test_first_run_scope(self):
        self.assertTrue(km.write_allowed("operations/r1-start", True, "r1"))
        self.assertTrue(km.write_allowed("operations/r1", True, "r1"))
        self.assertFalse(km.write_allowed("knowledge/a", True, "r1"))
        self.assertTrue(km.write_allowed("knowledge/a", False, "r1"))

    def test_write_scope_allowlist(self):
        ok = ["knowledge/a", "source-notes/a", "scratch/a", "operations/issues/schema-drift",
              "operations/r1", "operations/r1-start", "log", "index", "knowledge/index",
              "source-notes/index", "operations/issues/index", "ws/sk-wiki/knowledge/a"]
        for p in ok:
            self.assertTrue(km.write_allowed(p, False, "r1"), p)
        for p in ("schemas/concept", "schemas/index", "ws/sk-wiki/schemas/concept", "other/a",
                  "knowledge/../schemas/x", "operations/a/b", "operations/r1-audit",
                  "operations/r2", "operations/r2-start", "operations/index", "scratch/index/../../x",
                  "projects/index", "operations/log"):
            self.assertFalse(km.write_allowed(p, False, "r1"), p)

    def test_first_run_scope_defaults_to_limited_and_strips_prefix(self):
        self.assertTrue(km.write_allowed("ws/sk-wiki/operations/r1-start", None, "r1"))
        self.assertFalse(km.write_allowed("knowledge/a", None, "r1"))
        self.assertFalse(km.write_allowed("log", True, "r1"))
        self.assertFalse(km.write_allowed("operations/r1-audit", True, "r1"))

    def test_start_without_run_is_failed_run(self):
        self.assertEqual(km.failed_runs(["r1-start", "r1", "r2-start", "r2-audit"]), ["r2"])


class EmbeddedCopies(unittest.TestCase):
    ROOT = pathlib.Path(__file__).resolve().parents[1] / "skills"

    def test_duplicated_references_are_identical(self):
        for name in ("mutation-rules.md", "schemas.md"):
            a = (self.ROOT / "knowledge-ingest" / "references" / name).read_bytes()
            b = (self.ROOT / "knowledge-lint" / "references" / name).read_bytes()
            self.assertEqual(a, b, name)

    def test_checksum_tables_agree(self):
        import re
        pat = re.compile(r"`(schemas/[a-z-]+)` \| `([0-9a-f]{64})`")
        tables = [dict(pat.findall((self.ROOT / d / "references" / f).read_text()))
                  for d, f in (("knowledge-ingest", "schemas.md"), ("knowledge-lint", "schemas.md"),
                               ("daily-knowledge-maintenance", "schema-checksums.md"))]
        self.assertEqual(len(tables[0]), 4)
        self.assertEqual(tables[0], tables[1])
        self.assertEqual(tables[0], tables[2])


if __name__ == "__main__":
    unittest.main()
