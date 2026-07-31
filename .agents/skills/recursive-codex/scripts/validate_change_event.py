#!/usr/bin/env python3
"""Validate recursive-codex change-event YAML files."""

from __future__ import annotations

import copy
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment failure
    raise SystemExit("PyYAML is required: pip install -r requirements-dev.txt") from exc


OPERATIONS = {"local_update", "composition", "revision", "reorganization", "audit"}
RELATIONS = {
    "defines",
    "depends_on",
    "cross_references",
    "sourced_from",
    "documents",
    "renders",
    "tests",
    "constrains",
    "supersedes",
    "other",
}
EFFECTS = {"preserved", "changed", "added", "removed", "uncertain"}
DECISION_STATUSES = {"not_required", "pending", "accepted", "delegated", "rejected"}
VALIDATION_RESULTS = {"passed", "warning", "failed", "not_run"}
STATUSES = {"proposed", "tested", "confirmed", "stabilized", "revised"}
OPTIONAL_TOP = {"montage"}
MATERIAL_KINDS = {"source", "manuscript", "decision", "proposal", "generated", "diff"}
VARIANT_STATUSES = {"candidate", "selected", "rejected", "deferred"}
MONTAGE_STATES = {"open", "tested", "stabilized"}
FEEDBACK_CONSEQUENCES = {"preserve", "revise", "reorder", "defer"}

REQUIRED_TOP = {
    "schema_version",
    "id",
    "created_at",
    "goal",
    "operation",
    "scope",
    "basis",
    "changes",
    "affected_relations",
    "possibilities",
    "uncertainties",
    "agent_findings",
    "authority",
    "validation",
    "status",
}


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_string_list(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    for index, item in enumerate(value):
        if not is_nonempty_string(item):
            errors.append(f"{path}[{index}] must be a non-empty string")

def check_enum(value: Any, path: str, allowed: set[str], errors: list[str]) -> None:
    if not isinstance(value, str) or value not in allowed:
        errors.append(f"{path} must be one of {sorted(allowed)}")



def check_exact_keys(value: Any, path: str, keys: set[str], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{path} must be a mapping")
        return False
    missing = keys - set(value)
    unknown = set(value) - keys
    for key in sorted(missing, key=str):
        errors.append(f"{path}.{key} is required")
    for key in sorted(unknown, key=str):
        errors.append(f"{path}.{key} is not allowed")
    return not missing


def check_date(value: Any, errors: list[str]) -> None:
    if isinstance(value, (date, datetime)):
        return
    if isinstance(value, str):
        try:
            date.fromisoformat(value)
            return
        except ValueError:
            pass
    errors.append("created_at must be an ISO date")


def validate_montage(value: Any, event: dict[str, Any], errors: list[str]) -> None:
    keys = {"materials", "variants", "selection", "arrangement", "feedback", "stabilization", "recovery"}
    if not check_exact_keys(value, "montage", keys, errors):
        return

    material_ids: set[str] = set()
    materials = value["materials"]
    if not isinstance(materials, list) or not materials:
        errors.append("montage.materials must be a non-empty list")
    else:
        for index, item in enumerate(materials):
            item_path = f"montage.materials[{index}]"
            if check_exact_keys(item, item_path, {"id", "reference", "kind", "status", "identity"}, errors):
                material_id = item["id"]
                if not is_nonempty_string(material_id) or material_id in material_ids:
                    errors.append(f"{item_path}.id must be a unique non-empty string")
                else:
                    material_ids.add(material_id)
                for key in ("reference", "status", "identity"):
                    if not is_nonempty_string(item[key]):
                        errors.append(f"{item_path}.{key} must be a non-empty string")
                check_enum(item["kind"], f"{item_path}.kind", MATERIAL_KINDS, errors)

    variant_ids: set[str] = set()
    variant_items: dict[str, dict[str, Any]] = {}
    variants = value["variants"]
    if not isinstance(variants, list) or not variants:
        errors.append("montage.variants must be a non-empty list")
    else:
        for index, item in enumerate(variants):
            item_path = f"montage.variants[{index}]"
            if check_exact_keys(item, item_path, {"id", "derived_from", "artifact_or_diff", "status"}, errors):
                variant_id = item["id"]
                if not is_nonempty_string(variant_id) or variant_id in variant_ids:
                    errors.append(f"{item_path}.id must be a unique non-empty string")
                else:
                    variant_ids.add(variant_id)
                    variant_items[variant_id] = item
                check_string_list(item["derived_from"], f"{item_path}.derived_from", errors)
                if not is_nonempty_string(item["artifact_or_diff"]):
                    errors.append(f"{item_path}.artifact_or_diff must be a non-empty string")
                check_enum(item["status"], f"{item_path}.status", VARIANT_STATUSES, errors)

    for variant_id, item in variant_items.items():
        for source in item.get("derived_from", []):
            if source == variant_id:
                errors.append(f"montage variant {variant_id} cannot derive from itself")
            elif source not in material_ids and source not in variant_ids:
                errors.append(f"montage variant {variant_id} has unknown derived_from reference {source}")

    graph = {key: [item for item in value.get("derived_from", []) if item in variant_ids] for key, value in variant_items.items()}
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            errors.append(f"montage variants contain a derived_from cycle at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for parent in graph.get(node, []):
            visit(parent)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)

    categories: dict[str, set[str]] = {}
    selection = value["selection"]
    if check_exact_keys(selection, "montage.selection", {"selected", "rejected", "deferred"}, errors):
        for category in ("selected", "rejected", "deferred"):
            categories[category] = set()
            entries = selection[category]
            if not isinstance(entries, list):
                errors.append(f"montage.selection.{category} must be a list")
                continue
            for index, item in enumerate(entries):
                item_path = f"montage.selection.{category}[{index}]"
                if check_exact_keys(item, item_path, {"variant", "reason"}, errors):
                    variant_id = item["variant"]
                    if variant_id not in variant_ids or variant_id in categories[category]:
                        errors.append(f"{item_path}.variant must reference a unique declared variant")
                    else:
                        categories[category].add(variant_id)
                    if not is_nonempty_string(item["reason"]):
                        errors.append(f"{item_path}.reason must be a non-empty string")
        overlap = (
            categories["selected"] & categories["rejected"]
            | categories["selected"] & categories["deferred"]
            | categories["rejected"] & categories["deferred"]
        )
        if overlap:
            errors.append(f"montage selection categories must be disjoint: {sorted(overlap)}")

    positions: list[int] = []
    arrangement = value["arrangement"]
    if not isinstance(arrangement, list):
        errors.append("montage.arrangement must be a list")
    else:
        for index, item in enumerate(arrangement):
            item_path = f"montage.arrangement[{index}]"
            if check_exact_keys(item, item_path, {"position", "variant", "target", "function"}, errors):
                position = item["position"]
                if not isinstance(position, int) or isinstance(position, bool) or position < 1:
                    errors.append(f"{item_path}.position must be a positive integer")
                else:
                    positions.append(position)
                if item["variant"] not in categories.get("selected", set()):
                    errors.append(f"{item_path}.variant must reference a selected variant")
                for key in ("target", "function"):
                    if not is_nonempty_string(item[key]):
                        errors.append(f"{item_path}.{key} must be a non-empty string")
        if positions and sorted(positions) != list(range(1, len(positions) + 1)):
            errors.append("montage.arrangement positions must be unique and contiguous from 1")

    feedback = value["feedback"]
    if not isinstance(feedback, list):
        errors.append("montage.feedback must be a list")
    else:
        for index, item in enumerate(feedback):
            item_path = f"montage.feedback[{index}]"
            if check_exact_keys(item, item_path, {"subject", "finding", "consequence"}, errors):
                for key in ("subject", "finding"):
                    if not is_nonempty_string(item[key]):
                        errors.append(f"{item_path}.{key} must be a non-empty string")
                check_enum(item["consequence"], f"{item_path}.consequence", FEEDBACK_CONSEQUENCES, errors)

    stabilization = value["stabilization"]
    if check_exact_keys(stabilization, "montage.stabilization", {"state", "evidence"}, errors):
        check_enum(stabilization["state"], "montage.stabilization.state", MONTAGE_STATES, errors)
        check_string_list(stabilization["evidence"], "montage.stabilization.evidence", errors)

    recovery = value["recovery"]
    if check_exact_keys(recovery, "montage.recovery", {"baseline", "strategy", "verification"}, errors):
        for key in ("baseline", "strategy", "verification"):
            if not is_nonempty_string(recovery[key]):
                errors.append(f"montage.recovery.{key} must be a non-empty string")

    if event.get("status") in {"confirmed", "stabilized", "revised"}:
        if stabilization.get("state") != "stabilized":
            errors.append("stable event status requires montage.stabilization.state stabilized")
        if not feedback or not stabilization.get("evidence"):
            errors.append("stable event status with montage requires feedback and stabilization evidence")


def validate_event(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["document root must be a mapping"]

    missing = REQUIRED_TOP - set(data)
    unknown = set(data) - REQUIRED_TOP - OPTIONAL_TOP
    for key in sorted(missing, key=str):
        errors.append(f"{key} is required")
    for key in sorted(unknown, key=str):
        errors.append(f"{key} is not allowed")
    if missing:
        return errors

    if data["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not is_nonempty_string(data["id"]) or not re.fullmatch(r"change-[a-z0-9][a-z0-9-]*", data["id"]):
        errors.append("id must match change-[a-z0-9][a-z0-9-]*")
    if data["id"] == "change-bezeichner-ersetzen":
        errors.append("id placeholder must be replaced")
    check_date(data["created_at"], errors)
    if not is_nonempty_string(data["goal"]):
        errors.append("goal must be a non-empty string")
    if data["goal"] == "Ziel der Änderung eintragen":
        errors.append("goal placeholder must be replaced")
    check_enum(data["operation"], "operation", OPERATIONS, errors)
    check_enum(data["status"], "status", STATUSES, errors)

    if check_exact_keys(data["scope"], "scope", {"allowed_files", "protected_files"}, errors):
        check_string_list(data["scope"]["allowed_files"], "scope.allowed_files", errors)
        check_string_list(data["scope"]["protected_files"], "scope.protected_files", errors)

    if check_exact_keys(data["basis"], "basis", {"project_files", "decisions", "sources"}, errors):
        for key in ("project_files", "decisions", "sources"):
            check_string_list(data["basis"][key], f"basis.{key}", errors)

    if not isinstance(data["changes"], list):
        errors.append("changes must be a list")
    else:
        for index, item in enumerate(data["changes"]):
            path = f"changes[{index}]"
            if check_exact_keys(item, path, {"file", "summary"}, errors):
                if not is_nonempty_string(item["file"]):
                    errors.append(f"{path}.file must be a non-empty string")
                if not is_nonempty_string(item["summary"]):
                    errors.append(f"{path}.summary must be a non-empty string")

    if not isinstance(data["affected_relations"], list):
        errors.append("affected_relations must be a list")
    else:
        for index, item in enumerate(data["affected_relations"]):
            path = f"affected_relations[{index}]"
            keys = {"from", "relation", "to", "effect", "note"}
            if check_exact_keys(item, path, keys, errors):
                for key in ("from", "to", "note"):
                    if not is_nonempty_string(item[key]):
                        errors.append(f"{path}.{key} must be a non-empty string")
                check_enum(item["relation"], f"{path}.relation", RELATIONS, errors)
                check_enum(item["effect"], f"{path}.effect", EFFECTS, errors)

    if check_exact_keys(data["possibilities"], "possibilities", {"opened", "restricted", "deferred"}, errors):
        for key in ("opened", "restricted", "deferred"):
            check_string_list(data["possibilities"][key], f"possibilities.{key}", errors)

    check_string_list(data["uncertainties"], "uncertainties", errors)

    role_keys = {"genealogist", "consistency_checker", "critic", "material_technical"}
    if check_exact_keys(data["agent_findings"], "agent_findings", role_keys, errors):
        for key in sorted(role_keys):
            check_string_list(data["agent_findings"][key], f"agent_findings.{key}", errors)

    authority_keys = {"requires_author_decision", "decision_status", "decision_reference"}
    authority_ok = check_exact_keys(data["authority"], "authority", authority_keys, errors)
    if authority_ok:
        authority = data["authority"]
        if not isinstance(authority["requires_author_decision"], bool):
            errors.append("authority.requires_author_decision must be boolean")
        check_enum(authority["decision_status"], "authority.decision_status", DECISION_STATUSES, errors)
        reference = authority["decision_reference"]
        if reference is not None and not is_nonempty_string(reference):
            errors.append("authority.decision_reference must be null or a non-empty string")

    if not isinstance(data["validation"], list):
        errors.append("validation must be a list")
    else:
        for index, item in enumerate(data["validation"]):
            path = f"validation[{index}]"
            if check_exact_keys(item, path, {"check", "result", "evidence"}, errors):
                if not is_nonempty_string(item["check"]):
                    errors.append(f"{path}.check must be a non-empty string")
                check_enum(item["result"], f"{path}.result", VALIDATION_RESULTS, errors)
                if not is_nonempty_string(item["evidence"]):
                    errors.append(f"{path}.evidence must be a non-empty string")

    operation = data["operation"] if isinstance(data["operation"], str) else ""
    status = data["status"] if isinstance(data["status"], str) else ""
    relations = data["affected_relations"] if isinstance(data["affected_relations"], list) else []
    validations = data["validation"] if isinstance(data["validation"], list) else []
    changes = data["changes"] if isinstance(data["changes"], list) else []

    if operation in {"revision", "reorganization"} and not relations:
        errors.append(f"{operation} requires at least one affected relation")
    if operation == "reorganization" and relations:
        effects = {item.get("effect") for item in relations if isinstance(item, dict)}
        if not effects.intersection({"changed", "added", "removed"}):
            errors.append("reorganization requires a changed, added, or removed relation")
    if status != "proposed" and not validations:
        errors.append(f"status {status} requires at least one validation")
    if status in {"confirmed", "stabilized", "revised"}:
        if any(isinstance(item, dict) and item.get("result") == "failed" for item in validations):
            errors.append(f"status {status} cannot contain failed validation")
    if status == "stabilized" and operation != "audit" and not changes:
        errors.append("stabilized non-audit events require at least one change")

    if "montage" in data:
        validate_montage(data["montage"], data, errors)

    if authority_ok and isinstance(data["authority"].get("requires_author_decision"), bool):
        authority = data["authority"]
        if authority["requires_author_decision"]:
            if status in {"confirmed", "stabilized", "revised"} and authority["decision_status"] not in {"accepted", "delegated"}:
                errors.append(f"status {status} requires an accepted or delegated author decision")
        elif authority["decision_status"] != "not_required":
            errors.append("decision_status must be not_required when no author decision is required")

    return errors


def valid_self_test_event() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "id": "change-self-test",
        "created_at": "2026-07-29",
        "goal": "Validate the change-event validator",
        "operation": "reorganization",
        "scope": {"allowed_files": ["WORKFLOW.md"], "protected_files": ["manuskript/"]},
        "basis": {"project_files": ["AGENTS.md"], "decisions": ["decision-0021"], "sources": []},
        "changes": [{"file": "WORKFLOW.md", "summary": "Add recursive workflow"}],
        "affected_relations": [
            {
                "from": "AGENTS.md",
                "relation": "documents",
                "to": "WORKFLOW.md",
                "effect": "changed",
                "note": "Durable rules and executable workflow now correspond",
            }
        ],
        "possibilities": {"opened": ["Reusable recursive work"], "restricted": [], "deferred": []},
        "uncertainties": [],
        "agent_findings": {
            "genealogist": [],
            "consistency_checker": [],
            "critic": [],
            "material_technical": [],
        },
        "authority": {
            "requires_author_decision": True,
            "decision_status": "accepted",
            "decision_reference": "decision-0021",
        },
        "validation": [{"check": "self-test", "result": "passed", "evidence": "in-memory fixture"}],
        "status": "stabilized",
    }


def run_self_test() -> int:
    valid = valid_self_test_event()
    if validate_event(valid):
        print("SELF-TEST FAILED: valid fixture was rejected", file=sys.stderr)
        return 1
    invalid = copy.deepcopy(valid)
    invalid["authority"]["decision_status"] = "pending"
    if not validate_event(invalid):
        print("SELF-TEST FAILED: invalid fixture was accepted", file=sys.stderr)
        return 1
    invalid_type = copy.deepcopy(valid)
    invalid_type["operation"] = []
    if not validate_event(invalid_type):
        print("SELF-TEST FAILED: non-string enum was accepted", file=sys.stderr)
        return 1
    invalid_key = copy.deepcopy(valid)
    invalid_key[1] = "unexpected"
    if not validate_event(invalid_key):
        print("SELF-TEST FAILED: non-string unknown key was accepted", file=sys.stderr)
        return 1
    placeholder = copy.deepcopy(valid)
    placeholder["id"] = "change-bezeichner-ersetzen"
    if not validate_event(placeholder):
        print("SELF-TEST FAILED: placeholder fixture was accepted", file=sys.stderr)
        return 1
    print("SELF-TEST PASSED")
    return 0


def validate_path(path: Path) -> bool:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"INVALID {path}: {exc}", file=sys.stderr)
        return False
    errors = validate_event(data)
    if errors:
        print(f"INVALID {path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return False
    print(f"VALID {path}")
    return True


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return run_self_test()
    if not argv:
        print("usage: validate_change_event.py <event.yaml> [...] | --self-test", file=sys.stderr)
        return 2
    return 0 if all(validate_path(Path(item)) for item in argv) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
