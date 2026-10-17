import pathlib
import unittest


ROOT = pathlib.Path(__file__).parents[1]
SETUP = ROOT / "scripts" / "setup-chatgpt-ingest-lint.sh"


class ScheduledIngestLintSetupContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SETUP.read_text(encoding="utf-8")

    def test_setup_does_not_depend_on_broken_raw_contract_url(self):
        self.assertNotIn("raw.githubusercontent.com", self.text)

    def test_setup_carries_rolling_control_plane_contract(self):
        for expected in (
            "knowledge-maintenance",
            "knowledge-maintenance-ledger",
            "A dated report alone is never proof",
            "relation gaps and inconsistent links as report-only",
            "blocked or failed stage reports",
            "historical reconciliation",
            "Tracking branch: main",
            "preserve dated historical reports",
            "prior ledger evidence",
            "current control-plane gate",
            "skip both ingest and lint",
            "This gate takes precedence over all historical-reconciliation rules",
            "Still paginate the raw inventory",
            "select bounded ingest candidates",
            "run bounded lint over the current scope",
            "Apply zero meaning-changing repairs",
            "A previous blocked or unreconciled report is audit context, not a gate",
            "unreconciled report gap, ledger state, or review state",
        ):
            self.assertIn(expected, self.text)

    def test_setup_tracks_main_without_a_release_stage(self):
        for gone in ("v0.1.0", "RELEASE_SHA", "releases/new", "pinned", "pin the"):
            self.assertNotIn(gone, self.text)

    def test_stage_count_matches_declared_total(self):
        stages = [l for l in self.text.splitlines() if l.startswith("stage ")]
        self.assertIn("TOTAL_STAGES=%d\n" % len(stages), self.text)

    def test_prompt_honours_override_and_records_loaded_commit(self):
        self.assertIn("it takes precedence over tracking", self.text)
        self.assertIn("Record the loaded commit SHA in all reports", self.text)

    def test_prompt_does_not_block_an_override_for_not_matching_main(self):
        # A rollback override loads an old SHA that by definition is not main.
        self.assertNotIn("does not match main", self.text)
        self.assertIn("the loaded revision must equal that override exactly", self.text)
        self.assertIn("otherwise it must equal the resolved latest commit of main", self.text)

    # Proposed (best guess, #109): first runs are report-only and speak the seam.
    def test_prompt_makes_first_runs_report_only_with_mutation_ceiling_for_later(self):
        self.assertIn("report-only with zero substantive Wiki mutations until Syafiq approves writes", self.text)
        self.assertIn("contract limit for a later approved full mode, not an authorisation for these runs", self.text)

    def test_prompt_loads_seam_adapter_from_same_revision_and_ends_with_envelope(self):
        self.assertIn("skills/seam-adapter/SKILL.md from the same loaded commit", self.text)
        self.assertIn("end the run result with one seam envelope that conforms to docs/seam/envelope.md", self.text)

    def test_prompt_states_where_the_owner_override_is_set(self):
        self.assertIn("Owner commit SHA override: none", self.text)
        self.assertIn("Syafiq sets an override by replacing", self.text)


if __name__ == "__main__":
    unittest.main()
