#!/usr/bin/env python3
"""Deterministic local orchestration for research-program experiments.

The module orders workshop material.  It cannot confirm theory, edit manuscript
files, or change the project's constitutional bindings.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Callable

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROTECTED_PREFIXES = ("manuskript/",)
PROTECTED_FILES = {"CONSTITUTION.md", "PROJECT.md", "GLOSSAR.md", "knowledge/project_binding.yaml"}
PROTECTED_STATUSES = {"confirmed", "stabilized"}
CRITERIA = ("uncertainty", "connectivity", "theoretical_scope", "experimentability")


class ResearchBoundaryError(ValueError):
    """Raised when an operation crosses the project's authority boundary."""


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping")
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    return _require_mapping(yaml.safe_load(path.read_text(encoding="utf-8")), str(path))


def assert_workshop_status(record: dict[str, Any]) -> None:
    status = str(record.get("status", "proposal"))
    if status in PROTECTED_STATUSES:
        raise ResearchBoundaryError(f"automatic status transition to {status!r} is forbidden")


def assert_writable_output(path: Path, root: Path = ROOT) -> Path:
    resolved_root = root.resolve()
    resolved = (path if path.is_absolute() else root / path).resolve()
    try:
        relative = resolved.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise ResearchBoundaryError("output must remain inside the repository") from exc
    if relative in PROTECTED_FILES or any(relative.startswith(prefix) for prefix in PROTECTED_PREFIXES):
        raise ResearchBoundaryError(f"protected project file cannot be written: {relative}")
    if not relative.startswith("generated/experiments/"):
        raise ResearchBoundaryError("experiment output is restricted to generated/experiments/")
    return resolved


def validate_research_program(program: dict[str, Any]) -> None:
    required = {"schema_version", "id", "title", "questions", "methods", "open_problems", "authority"}
    missing = sorted(required - program.keys())
    if missing:
        raise ValueError(f"research program missing fields: {', '.join(missing)}")
    if program["schema_version"] != 1 or not program["questions"] or not program["methods"]:
        raise ValueError("research program requires schema_version 1, questions, and methods")
    authority = _require_mapping(program["authority"], "authority")
    required_authority = {
        "constitution_mutable": False,
        "protected_concepts_mutable": False,
        "authority_rules_mutable": False,
        "automatic_confirmation": False,
    }
    for key, expected in required_authority.items():
        if authority.get(key) is not expected:
            raise ResearchBoundaryError(f"authority.{key} must be false")
    for problem in program["open_problems"]:
        _validate_scored_item(problem, "open problem")


def validate_experiment(experiment: dict[str, Any]) -> None:
    required = {"schema_version", "id", "research_program", "seed", "variants", "status"}
    missing = sorted(required - experiment.keys())
    if missing:
        raise ValueError(f"experiment missing fields: {', '.join(missing)}")
    if experiment["schema_version"] != 1 or len(experiment["variants"]) < 2:
        raise ValueError("experiment requires schema_version 1 and at least two variants")
    assert_workshop_status(experiment)
    ids = [item.get("id") for item in experiment["variants"]]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("variant ids must be present and unique")


def _validate_scored_item(item: dict[str, Any], label: str) -> None:
    _require_mapping(item, label)
    if not item.get("id"):
        raise ValueError(f"{label} requires id")
    for criterion in CRITERIA:
        score = item.get(criterion)
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 1:
            raise ValueError(f"{label}.{criterion} must be between 0 and 1")


class ResearchDirector:
    """Prioritize open problems by declared epistemic criteria."""

    def __init__(self, weights: dict[str, float] | None = None):
        self.weights = weights or {criterion: 0.25 for criterion in CRITERIA}
        if set(self.weights) != set(CRITERIA) or sum(self.weights.values()) <= 0:
            raise ValueError("weights must cover all four research criteria")

    def prioritize(self, problems: list[dict[str, Any]]) -> list[dict[str, Any]]:
        total = sum(self.weights.values())
        ranked = []
        for problem in problems:
            _validate_scored_item(problem, "open problem")
            item = copy.deepcopy(problem)
            item["priority_score"] = round(
                sum(float(item[key]) * self.weights[key] for key in CRITERIA) / total, 6
            )
            item["decision_status"] = "proposal"
            ranked.append(item)
        return sorted(ranked, key=lambda item: (-item["priority_score"], str(item["id"])))


class DiscoveryManager:
    """Select useful methods and propose, but never execute, fusion or split."""

    def select(self, candidates: list[dict[str, Any]], minimum_gain: float = 0.25) -> dict[str, Any]:
        selected, deferred, structural = [], [], []
        for candidate in candidates:
            _validate_scored_item(candidate, "candidate")
            cost = float(candidate.get("cost", 0.0))
            if not 0 <= cost <= 1:
                raise ValueError("candidate.cost must be between 0 and 1")
            gain = (
                float(candidate["uncertainty"])
                * float(candidate["connectivity"])
                * float(candidate["theoretical_scope"])
                * float(candidate["experimentability"])
                * (1 - cost)
            ) ** (1 / 4)
            item = copy.deepcopy(candidate)
            item["expected_knowledge_gain"] = round(gain, 6)
            item["selection_status"] = "selected" if gain >= minimum_gain else "deferred"
            (selected if gain >= minimum_gain else deferred).append(item)
            if candidate.get("structural_action") in {"fusion", "split"}:
                structural.append({
                    "action": candidate["structural_action"],
                    "target": candidate.get("target", candidate["id"]),
                    "status": "proposal",
                    "executed": False,
                    "requires_author_decision": True,
                })
        return {"selected": selected, "deferred": deferred, "structural_proposals": structural}


class ExperimentManager:
    """Run seed variants through an injected method and compare their records."""

    def run(
        self,
        experiment: dict[str, Any],
        executor: Callable[[str, dict[str, Any]], dict[str, Any]],
    ) -> dict[str, Any]:
        validate_experiment(experiment)
        results = []
        for variant in experiment["variants"]:
            result = _require_mapping(executor(experiment["seed"], copy.deepcopy(variant)), "variant result")
            assert_workshop_status(result)
            results.append({
                "variant_id": variant["id"],
                "method": variant.get("method"),
                "status": "generated",
                "result": result,
            })
        return {
            "schema_version": 1,
            "experiment_id": experiment["id"],
            "research_program": experiment["research_program"],
            "status": "generated_comparison",
            "automatic_confirmation": False,
            "results": results,
            "comparison": compare_results(results),
            "next_step": "author_review",
        }

    def write(self, record: dict[str, Any], output: Path, root: Path = ROOT) -> Path:
        assert_workshop_status(record)
        destination = assert_writable_output(output, root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return destination


def compare_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    dimensions = ("new_relations", "invariants", "countermodels", "open_tensions", "simplifications")
    variants = []
    for entry in results:
        payload = entry["result"]
        variants.append({
            "variant_id": entry["variant_id"],
            **{dimension: len(payload.get(dimension, [])) for dimension in dimensions},
            "explanatory_power": payload.get("explanatory_power"),
        })
    return {
        "dimensions": list(dimensions) + ["explanatory_power"],
        "variants": variants,
        "selection": "none",
        "reason": "metrics support comparison but do not authorize theoretical judgment",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and prioritize V3 research programs")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("kind", choices=("program", "experiment"))
    validate.add_argument("file", type=Path)
    prioritize = sub.add_parser("prioritize")
    prioritize.add_argument("program", type=Path)
    args = parser.parse_args()
    data = load_yaml(args.file if args.command == "validate" else args.program)
    if args.command == "validate":
        (validate_research_program if args.kind == "program" else validate_experiment)(data)
        print("VALID")
    else:
        validate_research_program(data)
        print(json.dumps(ResearchDirector().prioritize(data["open_problems"]), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
