import json
import unittest
from pathlib import Path
from unittest.mock import patch

from automation import generative_runner as runner


class SourceContextTests(unittest.TestCase):
    def test_loads_context_and_records_provenance(self):
        text, provenance = runner.load_source_context(["automation/requests/example.yaml"], Path.cwd())

        self.assertIn("autonomous_theory_generation", text)
        self.assertEqual(provenance[0]["path"], "automation/requests/example.yaml")
        self.assertGreater(provenance[0]["included_characters"], 0)
        self.assertFalse(provenance[0]["truncated"])
        self.assertEqual(len(provenance[0]["sha256"]), 64)

    def test_rejects_context_outside_repository(self):
        with self.assertRaises(SystemExit):
            runner.load_source_context(["../outside.md"], Path.cwd())

    def test_first_cycle_receives_loaded_context(self):
        config = {
            "seed": "Anfang",
            "orientation": "Orientierung",
            "source_context_text": "VERBINDLICHER KONTEXT",
            "source_provenance": [],
            "project_binding_text": "VERFASSUNG UND GLOSSAR",
            "project_binding_provenance": [],
            "initial_binding_matrix": {
                "preserved_definitions": [{"id": "definition-programm", "value": "Programm", "status": "active", "introduced_in_cycle": 0, "resolved_in_cycle": None, "resolution": None}],
                "claims_in_tension": [],
                "departures_from_sources": [],
                "unresolved_source_conflicts": [],
                "open_objections": [],
        "binding_updates": [],
            },
            "allow_new_concepts": True,
            "allow_divergence": True,
            "initial_heuristic": "Heuristik",
            "epistemic_styles": ["exploratory"],
            "max_cycles": 1,
            "meta_agent": False,
            "meta_interval": 2,
            "minimum_productive_decisions": 1,
            "temperature": 0.9,
            "sampling_seed": 7,
            "project_binding": {"protected_concepts": {"anschluss": {}}},
        }
        response = json.dumps({
            "text": "Entwurf",
            "chosen_connection": "Anschluss",
            "alternatives_rejected": [],
            "new_concepts": [],
            "new_relations": [],
            "definition_refinements": [],
            "countermodels": [],
            "merged_nodes": [],
            "removed_categories": [],
            "productive_difference": "Differenz",
            "revisions": [],
            "tensions_preserved": [],
            "heuristic_effect": "Wirkung",
            "preserved_definitions": ["Programm", "Algorithmus", "Montage"],
            "claims_in_tension": [],
            "departures_from_sources": [],
            "unresolved_source_conflicts": [],
            "open_objections": [],
        "binding_updates": [],
            "continue": False,
        })

        with patch.object(runner, "api_call", return_value=response) as api:
            runner.run_theory_cycles(config, "endpoint", "model", "key")

        messages = api.call_args.args[0]
        self.assertIn("VERBINDLICHER KONTEXT", messages[1]["content"])
        self.assertIn("Status generated", messages[0]["content"])


if __name__ == "__main__":
    unittest.main()