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


if __name__ == "__main__":
    unittest.main()
