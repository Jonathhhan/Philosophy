import json
import tempfile
import unittest
from pathlib import Path

from automation.research_program import (
    DiscoveryManager,
    ExperimentManager,
    ResearchBoundaryError,
    ResearchDirector,
    validate_experiment,
    validate_research_program,
)


def scored(identifier, value, **extra):
    return {
        "id": identifier,
        "uncertainty": value,
        "connectivity": value,
        "theoretical_scope": value,
        "experimentability": value,
        **extra,
    }


class SchemaTests(unittest.TestCase):
    def test_machine_readable_schemas_are_json(self):
        for name in ("research-program.schema.json", "experiment.schema.json"):
            data = json.loads((Path("automation/schemas") / name).read_text(encoding="utf-8"))
            self.assertEqual(data["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_program_requires_constitutional_boundary(self):
        program = {
            "schema_version": 1, "id": "rp", "title": "Program",
            "questions": ["Q"], "methods": [{"id": "m"}], "open_problems": [],
            "authority": {
                "constitution_mutable": False, "protected_concepts_mutable": False,
                "authority_rules_mutable": False, "automatic_confirmation": True,
            },
        }
        with self.assertRaises(ResearchBoundaryError):
            validate_research_program(program)

    def test_experiment_requires_multiple_unique_variants(self):
        experiment = {
            "schema_version": 1, "id": "e", "research_program": "rp", "seed": "S",
            "status": "planned", "variants": [{"id": "a"}, {"id": "a"}],
        }
        with self.assertRaises(ValueError):
            validate_experiment(experiment)


class ResearchDirectorTests(unittest.TestCase):
    def test_prioritizes_four_criteria_and_returns_proposals(self):
        ranked = ResearchDirector().prioritize([scored("low", 0.2), scored("high", 0.9)])
        self.assertEqual([item["id"] for item in ranked], ["high", "low"])
        self.assertEqual(ranked[0]["priority_score"], 0.9)
        self.assertTrue(all(item["decision_status"] == "proposal" for item in ranked))


class DiscoveryManagerTests(unittest.TestCase):
    def test_selects_only_expected_gain_and_does_not_execute_structure(self):
        result = DiscoveryManager().select([
            scored("productive", 0.9, cost=0.1, structural_action="fusion", target="agents-a-b"),
            scored("weak", 0.05, cost=0.9),
        ], minimum_gain=0.3)
        self.assertEqual([item["id"] for item in result["selected"]], ["productive"])
        self.assertEqual([item["id"] for item in result["deferred"]], ["weak"])
        proposal = result["structural_proposals"][0]
        self.assertEqual(proposal["status"], "proposal")
        self.assertFalse(proposal["executed"])
        self.assertTrue(proposal["requires_author_decision"])


class ExperimentManagerTests(unittest.TestCase):
    def setUp(self):
        self.experiment = {
            "schema_version": 1, "id": "e", "research_program": "rp", "seed": "S",
            "status": "planned",
            "variants": [{"id": "a", "method": "m1"}, {"id": "b", "method": "m2"}],
        }

    def test_runs_variants_and_compares_without_selection_or_confirmation(self):
        record = ExperimentManager().run(self.experiment, lambda seed, variant: {
            "status": "generated", "text": seed + variant["id"],
            "new_relations": [variant["id"]], "invariants": [], "countermodels": [],
            "open_tensions": [], "simplifications": [], "explanatory_power": 0.5,
        })
        self.assertEqual(len(record["results"]), 2)
        self.assertEqual(record["comparison"]["selection"], "none")
        self.assertFalse(record["automatic_confirmation"])
        self.assertEqual(record["next_step"], "author_review")

    def test_rejects_executor_confirmation(self):
        with self.assertRaises(ResearchBoundaryError):
            ExperimentManager().run(self.experiment, lambda seed, variant: {"status": "confirmed"})

    def test_write_is_restricted_to_generated_experiments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manager = ExperimentManager()
            record = {"status": "generated_comparison"}
            path = manager.write(record, Path("generated/experiments/result.yaml"), root)
            self.assertTrue(path.exists())
            with self.assertRaises(ResearchBoundaryError):
                manager.write(record, Path("manuskript/01-anschliessen.md"), root)
            with self.assertRaises(ResearchBoundaryError):
                manager.write(record, Path("CONSTITUTION.md"), root)


if __name__ == "__main__":
    unittest.main()
