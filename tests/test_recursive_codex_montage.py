from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    ROOT
    / ".agents"
    / "skills"
    / "recursive-codex"
    / "scripts"
    / "validate_change_event.py"
)
SPEC = importlib.util.spec_from_file_location("change_event_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def montage_fixture() -> dict:
    return {
        "materials": [
            {
                "id": "baseline",
                "reference": "projekt/codex-prinzip-montage.md",
                "kind": "proposal",
                "status": "working material",
                "identity": "git:574a598",
            }
        ],
        "variants": [
            {
                "id": "documented",
                "derived_from": ["baseline"],
                "artifact_or_diff": "git diff -- projekt/codex-prinzip-montage.md",
                "status": "selected",
            },
            {
                "id": "undocumented",
                "derived_from": ["baseline"],
                "artifact_or_diff": "documentation-only alternative",
                "status": "rejected",
            },
        ],
        "selection": {
            "selected": [{"variant": "documented", "reason": "Executable and reviewable"}],
            "rejected": [{"variant": "undocumented", "reason": "Not mechanically verifiable"}],
            "deferred": [],
        },
        "arrangement": [
            {
                "position": 1,
                "variant": "documented",
                "target": "recursive-codex",
                "function": "Bind montage evidence to the existing workflow",
            }
        ],
        "feedback": [
            {
                "subject": "validator",
                "finding": "Legacy events remain valid",
                "consequence": "preserve",
            }
        ],
        "stabilization": {"state": "stabilized", "evidence": ["unit tests passed"]},
        "recovery": {
            "baseline": "git:574a598",
            "strategy": "Revert the dedicated commit",
            "verification": "git diff --check passed",
        },
    }


class MontageChangeEventTests(unittest.TestCase):
    def event(self) -> dict:
        event = validator.valid_self_test_event()
        event["montage"] = montage_fixture()
        return event

    def test_valid_montage_and_legacy_event(self) -> None:
        self.assertEqual(validator.validate_event(validator.valid_self_test_event()), [])
        self.assertEqual(validator.validate_event(self.event()), [])

    def test_unknown_field_and_duplicate_ids_are_rejected(self) -> None:
        event = self.event()
        event["montage"]["unknown"] = []
        event["montage"]["materials"].append(copy.deepcopy(event["montage"]["materials"][0]))
        errors = validator.validate_event(event)
        self.assertTrue(any("not allowed" in error for error in errors))
        self.assertTrue(any("unique non-empty" in error for error in errors))

    def test_cycles_and_selection_overlap_are_rejected(self) -> None:
        event = self.event()
        event["montage"]["variants"][0]["derived_from"] = ["undocumented"]
        event["montage"]["variants"][1]["derived_from"] = ["documented"]
        event["montage"]["selection"]["deferred"].append(
            {"variant": "documented", "reason": "conflicting category"}
        )
        errors = validator.validate_event(event)
        self.assertTrue(any("cycle" in error for error in errors))
        self.assertTrue(any("disjoint" in error for error in errors))

    def test_arrangement_and_stabilization_require_evidence(self) -> None:
        event = self.event()
        event["montage"]["arrangement"][0]["position"] = 2
        event["montage"]["feedback"] = []
        event["montage"]["stabilization"]["evidence"] = []
        errors = validator.validate_event(event)
        self.assertTrue(any("contiguous" in error for error in errors))
        self.assertTrue(any("requires feedback" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
