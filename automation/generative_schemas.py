"""Strict, dependency-free contracts for autonomous generation records."""

from __future__ import annotations

import json
import re
from typing import Any, Callable


class SchemaError(ValueError):
    """Raised when a model or generated record violates its contract."""


def extract_json_object(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        objects = []
        cursor = 0
        while cursor < len(cleaned):
            index = cleaned.find("{", cursor)
            if index < 0:
                break
            try:
                candidate, consumed = decoder.raw_decode(cleaned[index:])
            except json.JSONDecodeError:
                cursor = index + 1
                continue
            if isinstance(candidate, dict):
                objects.append(candidate)
            cursor = index + max(consumed, 1)
        if len(objects) != 1:
            raise SchemaError("response must contain exactly one JSON object")
        value = objects[0]
    if not isinstance(value, dict):
        raise SchemaError("response must be a JSON object")
    return value


def _require(data: dict[str, Any], fields: set[str], name: str) -> None:
    missing = sorted(fields - data.keys())
    if missing:
        raise SchemaError(f"{name} missing fields: {', '.join(missing)}")


def _string(data: dict[str, Any], key: str, nonempty: bool = False) -> str:
    value = data.get(key)
    if not isinstance(value, str) or (nonempty and not value.strip()):
        raise SchemaError(f"{key} must be a{' non-empty' if nonempty else ''} string")
    return value


def _bool(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if type(value) is not bool:
        raise SchemaError(f"{key} must be a boolean")
    return value


def _strings(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise SchemaError(f"{key} must be a list of strings")
    return value


def _objects(
    data: dict[str, Any],
    key: str,
    fields: set[str],
    string_fields: set[str] | None = None,
) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise SchemaError(f"{key} must be a list of objects")
    for index, item in enumerate(value):
        missing = fields - item.keys()
        if missing:
            raise SchemaError(f"{key}[{index}] missing fields: {', '.join(sorted(missing))}")
        for field in string_fields or set():
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise SchemaError(f"{key}[{index}].{field} must be a non-empty string")
    return value


THEORY_FIELDS = {
    "text", "chosen_connection", "alternatives_rejected", "new_concepts",
    "new_relations", "definition_refinements", "countermodels", "merged_nodes",
    "removed_categories", "productive_difference", "revisions",
    "tensions_preserved", "heuristic_effect", "continue",
    "preserved_definitions", "claims_in_tension", "departures_from_sources",
    "unresolved_source_conflicts", "open_objections",
}


def validate_theory_cycle(data: dict[str, Any]) -> dict[str, Any]:
    _require(data, THEORY_FIELDS, "TheoryCycleResult")
    _string(data, "text", True)
    _string(data, "chosen_connection", True)
    _string(data, "productive_difference")
    _string(data, "heuristic_effect")
    _bool(data, "continue")
    for key in (
        "alternatives_rejected", "new_concepts", "tensions_preserved",
        "preserved_definitions", "claims_in_tension", "departures_from_sources",
        "unresolved_source_conflicts", "open_objections",
    ):
        _strings(data, key)
    _objects(data, "new_relations", {"from", "relation", "to"}, {"from", "relation", "to"})
    _objects(
        data, "definition_refinements",
        {"concept", "previous", "refined", "distinction"},
        {"concept", "previous", "refined", "distinction"},
    )
    _objects(
        data, "countermodels", {"claim", "countermodel", "consequence"},
        {"claim", "countermodel", "consequence"},
    )
    _objects(data, "merged_nodes", {"nodes", "result", "reason"}, {"result", "reason"})
    for index, item in enumerate(data["merged_nodes"]):
        if not isinstance(item["nodes"], list) or len(item["nodes"]) < 2 or any(
            not isinstance(node, str) or not node.strip() for node in item["nodes"]
        ):
            raise SchemaError(f"merged_nodes[{index}].nodes must contain at least two strings")
    _objects(data, "removed_categories", {"category", "reason"}, {"category", "reason"})
    _objects(data, "revisions", {"target", "reason"}, {"target", "reason"})
    return data


META_FIELDS = {
    "assessment", "current_rule_limit", "proposed_heuristic",
    "selected_style", "reason", "alternatives_rejected", "expected_gain",
    "expected_risk", "change_rule", "constitutional_compatibility",
    "project_relations_preserved", "project_relations_endangered",
    "requires_author_decision",
}


def validate_meta_decision(data: dict[str, Any]) -> dict[str, Any]:
    _require(data, META_FIELDS, "MetaDecision")
    for key in (
        "assessment", "current_rule_limit", "proposed_heuristic",
        "selected_style", "reason", "expected_gain", "expected_risk",
        "constitutional_compatibility",
    ):
        _string(data, key, True)
    for key in (
        "alternatives_rejected", "project_relations_preserved",
        "project_relations_endangered",
    ):
        _strings(data, key)
    if data["constitutional_compatibility"] not in {"compatible", "incompatible", "uncertain"}:
        raise SchemaError("constitutional_compatibility must be compatible, incompatible or uncertain")
    _bool(data, "change_rule")
    _bool(data, "requires_author_decision")
    return data


def validate_theory_graph(data: dict[str, Any]) -> dict[str, Any]:
    _require(data, {"status", "seed", "concepts", "relations", "connection_decisions"}, "TheoryGraph")
    _string(data, "status", True)
    _string(data, "seed", True)
    _strings(data, "concepts")
    _objects(data, "relations", {"from", "relation", "to"}, {"from", "relation", "to"})
    if not isinstance(data["connection_decisions"], list):
        raise SchemaError("connection_decisions must be a list")
    return data


def validate_generation_record(data: dict[str, Any]) -> dict[str, Any]:
    required = {
        "mode", "status", "seed", "created_by", "model", "cycles",
        "method_revisions", "source_context", "source_provenance",
        "next_possible_steps", "request_file", "target", "max_cycles",
        "connection_decisions", "meta_decisions", "review_started",
        "review", "output_file", "graph_file", "method_file",
    }
    _require(data, required, "GenerationRecord")
    for key in ("mode", "status", "seed", "created_by", "model", "request_file", "target"):
        _string(data, key, True)
    for key in ("cycles", "method_revisions", "max_cycles"):
        if type(data[key]) is not int or data[key] < 0:
            raise SchemaError(f"{key} must be a non-negative integer")
    for key in ("source_context", "next_possible_steps"):
        _strings(data, key)
    if not isinstance(data["source_provenance"], list):
        raise SchemaError("source_provenance must be a list")
    if not isinstance(data["connection_decisions"], list) or not isinstance(data["meta_decisions"], list):
        raise SchemaError("decision fields must be lists")
    if type(data["review_started"]) is not bool:
        raise SchemaError("review_started must be a boolean")
    if data["review"] is not None and not isinstance(data["review"], str):
        raise SchemaError("review must be null or a string")
    for key in ("output_file", "graph_file", "method_file"):
        _string(data, key, True)
    return data


VALIDATORS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "theory": validate_theory_cycle,
    "meta": validate_meta_decision,
    "graph": validate_theory_graph,
    "record": validate_generation_record,
}


def parse_and_validate(raw: str, schema: str) -> dict[str, Any]:
    try:
        validator = VALIDATORS[schema]
    except KeyError as exc:
        raise SchemaError(f"unknown schema: {schema}") from exc
    return validator(extract_json_object(raw))
