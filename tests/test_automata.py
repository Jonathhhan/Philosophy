from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import automatenverbund
import kollektiv_automat
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

class KollektivAutomatTests(unittest.TestCase):
    def test_boundary_warning_has_precedence_and_blocks(self) -> None:
        report = kollektiv_automat.build_collective_report(
            "Freiheit beginnt dort, wo Organisation endet."
        )
        self.assertEqual(report["collective_recommendation"]["outcome"], "BLOCKED")
        self.assertEqual(report["collective_recommendation"]["rule"], "boundary_precedence")

    def test_explicit_variants_are_forked_without_majority_vote(self) -> None:
        report = kollektiv_automat.build_collective_report(
            "Organisation verändert Anschlussmöglichkeiten.",
            variants=["lokale Präzisierung", "kapitelübergreifende Reorganisation"],
        )
        self.assertEqual(report["collective_recommendation"]["outcome"], "FORK")
        self.assertTrue(report["dissent"]["preserved"])
        self.assertIn("nicht gezählt", report["dissent"]["note"])

    def test_existing_statement_is_kept(self) -> None:
        report = kollektiv_automat.build_collective_report(
            "Kritik steht nicht außerhalb der Organisation"
        )
        self.assertEqual(report["collective_recommendation"]["outcome"], "KEEP")
        self.assertTrue(report["shared_evidence"]["exact_occurrences"])

    def test_bounded_target_produces_patch_proposal(self) -> None:
        report = kollektiv_automat.build_collective_report(
            "Organisation verändert die Bedingungen weiterer Anschlüsse.",
            target_file="manuskript/01-anschliessen.md",
        )
        self.assertEqual(report["collective_recommendation"]["outcome"], "PATCH")
        self.assertTrue(report["collective_recommendation"]["requires_author_decision"])

    def test_cross_file_evidence_can_require_reorganization(self) -> None:
        result = kollektiv_automat._recommendation(
            {"boundary_warnings": []},
            [],
            [],
            ["manuskript/01.md", "manuskript/02.md", "manuskript/03.md"],
            None,
        )
        self.assertEqual(result["outcome"], "REORGANIZE")

if __name__ == "__main__":
    unittest.main()
