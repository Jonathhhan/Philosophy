import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from automation import artifact_bundle
from automation import generative_runner as runner
from automation import generative_schemas


class StrictContractTests(unittest.TestCase):
    def test_unknown_theory_field_is_rejected(self):
        data = {
            "text": "x", "chosen_connection": "x", "alternatives_rejected": [],
            "new_concepts": [], "new_relations": [], "definition_refinements": [],
            "countermodels": [], "merged_nodes": [], "removed_categories": [],
            "productive_difference": "", "revisions": [], "tensions_preserved": [],
            "heuristic_effect": "", "continue": False, "preserved_definitions": [],
            "claims_in_tension": [], "departures_from_sources": [],
            "unresolved_source_conflicts": [], "open_objections": [],
            "binding_updates": [], "new_relation": [],
        }
        with self.assertRaisesRegex(generative_schemas.SchemaError, "unexpected fields"):
            generative_schemas.parse_and_validate(json.dumps(data), "theory")

    def test_review_result_is_structured(self):
        review = {
            "recommended_status": "proposal",
            "validated_relations": [{"from": "A", "relation": "öffnet", "to": "B", "reason": "trägt"}],
            "rejected_relations": [], "strong_objections": [],
            "countermodel_results": [], "method_assessment": "begrenzt tragfähig",
            "requires_author_decision": True,
        }
        self.assertEqual(generative_schemas.validate_review_result(review), review)


class EpistemicLevelTests(unittest.TestCase):
    def test_novelty_and_relevance_do_not_claim_philosophical_productivity(self):
        result = {
            "new_relations": [{"from": "Kritik", "relation": "öffnet", "to": "Anschluss"}],
            "definition_refinements": [], "countermodels": [], "merged_nodes": [],
            "removed_categories": [], "revisions": [], "productive_difference": "Behauptung",
        }
        check = runner.verify_productivity(result, [], {"kritik"})
        self.assertTrue(check["novelty_verified"])
        self.assertTrue(check["project_relevance_verified"])
        self.assertFalse(check["philosophical_productivity_verified"])

    def test_binding_can_be_resolved(self):
        old = {"open_objections": [{
            "id": "o1", "value": "Einwand", "status": "open",
            "introduced_in_cycle": 1, "resolved_in_cycle": None, "resolution": None,
        }], "preserved_definitions": [], "claims_in_tension": [],
            "departures_from_sources": [], "unresolved_source_conflicts": []}
        result = {key: [] for key in old}
        result["binding_updates"] = [{
            "kind": "open_objections", "id": "o1", "action": "resolve",
            "value": "Einwand", "resolution": "durch Gegenmodell geklärt",
        }]
        updated = runner.update_binding_matrix(old, result, 2)
        self.assertEqual(updated["open_objections"][0]["status"], "resolved")
        self.assertEqual(updated["open_objections"][0]["resolved_in_cycle"], 2)


class ArtifactBundleTests(unittest.TestCase):
    def test_generated_relative_path_is_accepted(self):
        self.assertEqual(
            artifact_bundle._safe_generated_path("generated/active/result.txt").as_posix(),
            "generated/active/result.txt",
        )

    def test_traversal_and_non_generated_paths_are_rejected(self):
        for path in ("generated/../secret.txt", "manuskript/01.md", "/generated/result.txt"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                artifact_bundle._safe_generated_path(path)


if __name__ == "__main__":
    unittest.main()
