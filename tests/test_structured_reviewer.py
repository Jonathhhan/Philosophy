import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from automation import structured_reviewer as reviewer


VALID_REVIEW = {
    "recommended_status": "generated",
    "novelty_assessment": "supported",
    "project_relevance_assessment": "plausible",
    "philosophical_productivity_assessment": "plausible",
    "validated_relations": [],
    "rejected_relations": [],
    "strong_objections": ["Normative basis remains open"],
    "countermodel_results": [],
    "method_assessment": "Method remains inspectable.",
    "required_revisions": ["Clarify the normative basis"],
    "resolved_binding_items": [],
    "new_binding_items": [{"kind": "objection", "claim": "Normative basis remains open", "status": "open"}],
    "requires_author_decision": False,
    "decision_reason": "Novel, but not yet sufficiently justified.",
}


class StructuredReviewTests(unittest.TestCase):
    def test_valid_review_passes(self):
        self.assertEqual(reviewer.parse_and_validate(json.dumps(VALID_REVIEW)), VALID_REVIEW)

    def test_unknown_field_is_rejected(self):
        data = dict(VALID_REVIEW)
        data["surprise"] = True
        with self.assertRaises(reviewer.ReviewError):
            reviewer.validate_review(data)

    def test_proposal_requires_supported_productivity(self):
        data = dict(VALID_REVIEW)
        data["recommended_status"] = "proposal"
        data["strong_objections"] = []
        with self.assertRaises(reviewer.ReviewError):
            reviewer.validate_review(data)

    def test_proposal_rejects_strong_objections(self):
        data = dict(VALID_REVIEW)
        data["recommended_status"] = "proposal"
        data["philosophical_productivity_assessment"] = "supported"
        with self.assertRaises(reviewer.ReviewError):
            reviewer.validate_review(data)

    def test_repair_retry(self):
        repaired = json.dumps(VALID_REVIEW)
        with patch.object(reviewer, "api_call", side_effect=["not json", repaired]) as api:
            result = reviewer.call_reviewer([], "endpoint", "model", "key")
        self.assertEqual(result, VALID_REVIEW)
        self.assertEqual(api.call_count, 2)

    def test_generated_boundary(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "generated").mkdir()
            record = root / "outside.yaml"
            record.write_text("output_file: outside.md\ngraph_file: outside.yaml\n", encoding="utf-8")
            with patch("pathlib.Path.cwd", return_value=root):
                with self.assertRaises(SystemExit):
                    reviewer.resolve_generated_paths(record, {"output_file": "outside.md", "graph_file": "outside.yaml"})


if __name__ == "__main__":
    unittest.main()
