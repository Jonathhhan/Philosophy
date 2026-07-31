from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import automatenverbund
import philosophie_automat


class PhilosophieAutomatBoundaryTests(unittest.TestCase):
    def test_scoped_freedom_claim_is_recognized_without_boundary_warning(self) -> None:
        report = philosophie_automat.build_report(
            "Innerhalb dieses Begriffsrahmens beginnt Freiheit nicht dort, wo Organisation endet."
        )
        ids = {item["id"] for item in report["mentioned_concepts"]}
        warning_ids = {item["id"] for item in report["boundary_warnings"]}
        self.assertIn("freiheit", ids)
        self.assertNotIn("universal_freedom_claim", warning_ids)

    def test_unscoped_freedom_claim_warns(self) -> None:
        report = philosophie_automat.build_report(
            "Freiheit beginnt dort, wo Organisation endet."
        )
        warning_ids = {item["id"] for item in report["boundary_warnings"]}
        self.assertIn("universal_freedom_claim", warning_ids)

    def test_tragfaehigkeit_is_not_allowed_to_become_supreme_standard(self) -> None:
        report = philosophie_automat.build_report(
            "Tragfähigkeit ist der Maßstab, der jedes Urteil entscheidet."
        )
        ids = {item["id"] for item in report["mentioned_concepts"]}
        warning_ids = {item["id"] for item in report["boundary_warnings"]}
        self.assertIn("tragfaehigkeit", ids)
        self.assertIn("tragfaehigkeit_as_supreme_standard", warning_ids)

    def test_automation_provenance_is_flagged(self) -> None:
        report = philosophie_automat.build_report(
            "Die Automatenanalyse bestätigt diese Manuskriptthese."
        )
        warning_ids = {item["id"] for item in report["boundary_warnings"]}
        self.assertIn("automation_provenance_in_manuscript", warning_ids)


class AutomatenverbundProvenanceTests(unittest.TestCase):
    def test_iterative_output_preserves_initial_input(self) -> None:
        with mock.patch.object(automatenverbund, "save_state"):
            data = automatenverbund.run_until_new(
                "Freiheit",
                "allgemeine Freiheitstheorie",
                "Regressionstest",
                max_steps=3,
                max_runs=2,
                state_path=ROOT / "recovered" / "state" / "unused-test-state.json",
            )
        iterative = data["iterative_run"]
        self.assertEqual(iterative["initial_input"]["marked"], "Freiheit")
        self.assertEqual(
            iterative["initial_input"]["unmarked"],
            "allgemeine Freiheitstheorie",
        )
        rendered = automatenverbund.markdown(data)
        self.assertIn("- markiert: Freiheit", rendered)
        self.assertIn("- unmarkiert: allgemeine Freiheitstheorie", rendered)


if __name__ == "__main__":
    unittest.main()
