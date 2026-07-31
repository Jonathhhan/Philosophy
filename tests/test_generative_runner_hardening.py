import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation import generative_runner as runner
from automation import generative_schemas


def theory_result(**overrides):
    result = {
        "text": "Entwurf",
        "chosen_connection": "Anschluss",
        "alternatives_rejected": [],
        "new_concepts": [],
        "new_relations": [],
        "definition_refinements": [],
        "countermodels": [],
        "merged_nodes": [],
        "removed_categories": [],
        "productive_difference": "",
        "revisions": [],
        "tensions_preserved": [],
        "heuristic_effect": "keine nachgewiesene Wirkung",
        "continue": False,
        "preserved_definitions": ["Programm", "Algorithmus", "Montage"],
        "claims_in_tension": [],
        "departures_from_sources": [],
        "unresolved_source_conflicts": [],
        "open_objections": [],
    }
    result.update(overrides)
    return result


def meta_result(**overrides):
    result = {
        "assessment": "Kontinuität",
        "current_rule_limit": "keine",
        "proposed_heuristic": "Heuristik",
        "selected_style": "exploratory",
        "reason": "Kein Wechsel erforderlich.",
        "alternatives_rejected": [],
        "expected_gain": "Kontinuität",
        "expected_risk": "Wiederholung",
        "change_rule": False,
        "constitutional_compatibility": "compatible",
        "project_relations_preserved": ["Programm != Algorithmus", "Montage epistemisches Modell"],
        "project_relations_endangered": [],
        "requires_author_decision": False,
    }
    result.update(overrides)
    return result


def config(max_cycles=1):
    return {
        "seed": "Anfang",
        "title": "Test",
        "mode": "autonomous_theory_generation",
        "target": "theory",
        "orientation": "",
        "source_context": ["quelle.md"],
        "source_context_text": "QUELLENTEXT",
        "source_provenance": [{"path": "quelle.md", "sha256": "a" * 64}],
        "project_binding_text": "VERFASSUNG PROGRAMM ALGORITHMUS MONTAGE",
        "project_binding_provenance": [{"path": "CONSTITUTION.md", "sha256": "b" * 64}],
        "initial_binding_matrix": {
            "preserved_definitions": ["Programm", "Algorithmus", "Montage"],
            "claims_in_tension": [],
            "departures_from_sources": [],
            "unresolved_source_conflicts": [],
            "open_objections": [],
        },
        "allow_new_concepts": True,
        "allow_divergence": True,
        "initial_heuristic": "Heuristik",
        "epistemic_styles": ["exploratory", "dialectical"],
        "max_cycles": max_cycles,
        "meta_agent": False,
        "meta_interval": 1,
        "minimum_productive_decisions": 1,
        "start_review_after_generation": False,
    }


class RequestContractTests(unittest.TestCase):
    def test_rejects_unknown_epistemic_style(self):
        request = "seed: Anfang\nmax_cycles: 2\nminimum_productive_decisions: 1\nepistemic_styles: [unknown]\n"
        with patch.object(Path, "read_text", return_value=request):
            with self.assertRaises(SystemExit):
                runner.load_request(Path("request.yaml"))

    def test_rejects_string_boolean(self):
        request = "seed: Anfang\nmax_cycles: 2\nminimum_productive_decisions: 1\nmeta_agent: 'false'\n"
        with patch.object(Path, "read_text", return_value=request):
            with self.assertRaises(SystemExit):
                runner.load_request(Path("request.yaml"))

class StrictSchemaTests(unittest.TestCase):
    def test_rejects_wrong_boolean_type(self):
        raw = theory_result(continue_="false")
        raw["continue"] = "false"
        raw.pop("continue_", None)
        with self.assertRaises(generative_schemas.SchemaError):
            generative_schemas.parse_and_validate(json.dumps(raw), "theory")

    def test_non_greedy_extraction_rejects_multiple_objects(self):
        with self.assertRaises(generative_schemas.SchemaError):
            generative_schemas.extract_json_object('prefix {"text": "one"} middle {"text": "two"}')

    def test_repairs_one_invalid_response(self):
        invalid = json.dumps({"text": "unvollständig"})
        valid = json.dumps(theory_result())
        with patch.object(runner, "api_call", side_effect=[invalid, valid]) as api:
            result = runner.call_structured_agent(
                [{"role": "user", "content": "test"}],
                schema="theory",
                endpoint="endpoint",
                model="model",
                api_key="key",
                temperature=0,
            )
        self.assertEqual(result["text"], "Entwurf")
        self.assertEqual(api.call_count, 2)
        self.assertIn("Repariere", api.call_args.args[0][-1]["content"])


class ProductivityTests(unittest.TestCase):
    def test_model_claim_alone_is_not_productive(self):
        result = theory_result(productive_difference="Ich bin produktiv.")
        verification = runner.verify_productivity(result, [])
        self.assertFalse(verification["productive"])
        self.assertEqual(verification["model_claim"], "Ich bin produktiv.")

    def test_new_relation_is_independently_productive(self):
        result = theory_result(
            new_relations=[{"from": "A", "relation": "begrenzt", "to": "B"}]
        )
        verification = runner.verify_productivity(result, [])
        self.assertTrue(verification["productive"])
        self.assertEqual(verification["evidence"][0]["kind"], "new_relation")


class MetaAgentTests(unittest.TestCase):
    def test_meta_agent_receives_project_and_source_binding(self):
        cfg = config()
        cfg["meta_agent"] = True
        decision = {"binding_matrix": cfg["initial_binding_matrix"]}
        response = json.dumps(meta_result())
        with patch.object(runner, "api_call", return_value=response) as api:
            runner.run_meta_agent(
                cfg, "Heuristik", "exploratory", "Text", [decision],
                "endpoint", "model", "key",
            )
        messages = api.call_args.args[0]
        self.assertIn("VERFASSUNG PROGRAMM ALGORITHMUS MONTAGE", messages[0]["content"])
        self.assertIn("QUELLENTEXT", messages[1]["content"])
        self.assertIn("open_objections", messages[1]["content"])

    def test_endangered_relation_blocks_method_change(self):
        cfg = config()
        response = json.dumps(meta_result(
            proposed_heuristic="Neue Heuristik",
            selected_style="dialectical",
            change_rule=True,
            project_relations_endangered=["Programm != Algorithmus"],
        ))
        with patch.object(runner, "api_call", return_value=response):
            decision = runner.run_meta_agent(
                cfg, "Heuristik", "exploratory", "Text", [],
                "endpoint", "model", "key",
            )
        self.assertFalse(decision["change_rule"])
        self.assertIn("project_relations_endangered", decision["change_blocked_reasons"])


class MethodVersionAndStopTests(unittest.TestCase):
    def test_retained_method_does_not_increment_version(self):
        cfg = config(max_cycles=2)
        cfg["meta_agent"] = True
        first = theory_result(
            new_relations=[{"from": "A", "relation": "öffnet", "to": "B"}],
            **{"continue": True},
        )
        second = theory_result(
            countermodels=[{"claim": "A", "countermodel": "Nicht-A", "consequence": "Grenze"}]
        )
        responses = [json.dumps(first), json.dumps(meta_result()), json.dumps(second)]
        with patch.object(runner, "api_call", side_effect=responses):
            _, decisions, meta = runner.run_theory_cycles(cfg, "endpoint", "model", "key")
        self.assertEqual([item["heuristic_version"] for item in decisions], [1, 1])
        self.assertFalse(meta[0]["change_rule"])

    def test_changed_method_increments_version(self):
        cfg = config(max_cycles=2)
        cfg["meta_agent"] = True
        first = theory_result(
            new_relations=[{"from": "A", "relation": "öffnet", "to": "B"}],
            **{"continue": True},
        )
        changed = meta_result(
            proposed_heuristic="Neue Heuristik",
            selected_style="dialectical",
            change_rule=True,
        )
        second = theory_result(
            countermodels=[{"claim": "A", "countermodel": "Nicht-A", "consequence": "Grenze"}]
        )
        with patch.object(
            runner, "api_call",
            side_effect=[json.dumps(first), json.dumps(changed), json.dumps(second)],
        ):
            _, decisions, _ = runner.run_theory_cycles(cfg, "endpoint", "model", "key")
        self.assertEqual([item["heuristic_version"] for item in decisions], [1, 2])

    def test_unverified_model_stop_does_not_end_cycle_early(self):
        cfg = config(max_cycles=2)
        responses = [
            json.dumps(theory_result(productive_difference="behauptet")),
            json.dumps(theory_result(text="zweiter Zyklus")),
        ]
        with patch.object(runner, "api_call", side_effect=responses):
            _, decisions, _ = runner.run_theory_cycles(cfg, "endpoint", "model", "key")
        self.assertEqual(len(decisions), 2)
        self.assertFalse(decisions[0]["productivity_verification"]["productive"])

class CycleAndOutputTests(unittest.TestCase):
    def test_later_cycle_receives_binding_matrix_and_provenance(self):
        first = theory_result(
            new_relations=[{"from": "A", "relation": "öffnet", "to": "B"}],
            claims_in_tension=["A oder B"],
            **{"continue": True},
        )
        second = theory_result(
            text="Revision",
            countermodels=[{"claim": "A", "countermodel": "Nicht-A", "consequence": "Begrenzung"}],
        )
        with patch.object(
            runner, "api_call",
            side_effect=[json.dumps(first), json.dumps(second)],
        ) as api:
            _, decisions, _ = runner.run_theory_cycles(
                config(max_cycles=2), "endpoint", "model", "key"
            )
        self.assertEqual(len(decisions), 2)
        second_prompt = api.call_args_list[1].args[0][1]["content"]
        self.assertIn("A oder B", second_prompt)
        self.assertIn("quelle.md", second_prompt)
        self.assertTrue(decisions[1]["productivity_verification"]["productive"])

    def test_writes_all_four_schema_valid_outputs(self):
        cfg = config()
        decision = {
            "new_concepts": ["A"],
            "new_relations": [{"from": "A", "relation": "öffnet", "to": "B"}],
            "productivity_verification": {"productive": True, "evidence": []},
            "binding_matrix": cfg["initial_binding_matrix"],
        }
        with (
            patch.object(Path, "mkdir") as mkdir,
            patch.object(Path, "write_text") as write,
            patch.dict(os.environ, {"GENERATIVE_MODEL": "recorded-model"}),
        ):
            paths = runner.write_outputs(
                cfg, "Text", [decision], [], None, Path("request.yaml")
            )
        self.assertEqual(len(paths), 4)
        self.assertEqual(write.call_count, 4)
        self.assertEqual(mkdir.call_count, 1)
        self.assertIn(Path("generated") / "active", paths[0].parents)
class WorkflowSecurityTests(unittest.TestCase):
    def test_generation_and_publication_jobs_have_separate_permissions(self):
        import yaml

        workflow = yaml.safe_load(
            Path(".github/workflows/autonomous-generative.yml").read_text(encoding="utf-8")
        )
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertEqual(workflow["jobs"]["generate"]["permissions"], {"contents": "read"})
        self.assertEqual(
            workflow["jobs"]["publish"]["permissions"],
            {"contents": "write", "pull-requests": "write"},
        )
        self.assertEqual(workflow["jobs"]["publish"]["needs"], "generate")

class StyleComparisonTests(unittest.TestCase):
    def test_comparison_reports_metrics_without_selecting_winner(self):
        productive = {
            "new_relations": [{"from": "A", "relation": "öffnet", "to": "B"}],
            "definition_refinements": [],
            "countermodels": [],
            "productivity_verification": {"productive": True},
        }
        conservative = {
            "new_relations": [],
            "definition_refinements": [],
            "countermodels": [],
            "productivity_verification": {"productive": False},
        }
        summary = runner.style_comparison_summary([
            {"style": "exploratory", "decisions": [productive], "meta_decisions": []},
            {"style": "conservative", "decisions": [conservative], "meta_decisions": []},
        ])
        self.assertEqual(summary["status"], "generated_comparison")
        self.assertIn("none", summary["selection"])
        self.assertEqual(summary["runs"][0]["verified_productive_cycles"], 1)
        self.assertEqual(summary["runs"][1]["verified_productive_cycles"], 0)

if __name__ == "__main__":
    unittest.main()
