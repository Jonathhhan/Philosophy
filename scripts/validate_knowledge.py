#!/usr/bin/env python3
"""Validate YAML syntax, schemas, IDs, and repository references."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Knowledge validation failed:\n- Missing dependency: PyYAML")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
CONCEPT_DIR = ROOT / "knowledge" / "concepts"
DECISION_DIR = ROOT / "knowledge" / "decisions"
REQUIRED_CONCEPT_KEYS = {"id", "label", "status"}
REQUIRED_DECISION_KEYS = {"id", "date", "title", "status", "decision", "reason"}
REFERENCE_KEYS = ("depends_on", "required_for", "related")


def load_yaml(path: Path, errors: list[str]) -> object | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{path.relative_to(ROOT)} is not valid YAML: {exc}")
        return None


def validate_group(
    directory: Path, required: set[str], errors: list[str]
) -> tuple[dict[str, Path], list[tuple[Path, dict[str, object]]]]:
    ids: dict[str, Path] = {}
    records: list[tuple[Path, dict[str, object]]] = []
    if not directory.exists():
        errors.append(f"Missing directory: {directory.relative_to(ROOT)}")
        return ids, records
    files = sorted(directory.glob("*.yaml"))
    if not files:
        errors.append(f"No YAML files in {directory.relative_to(ROOT)}")
        return ids, records

    for path in files:
        data = load_yaml(path, errors)
        if data is None:
            continue
        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(ROOT)} must contain a mapping")
            continue
        records.append((path, data))
        missing = required - data.keys()
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)} missing keys: {', '.join(sorted(missing))}"
            )
        item_id = data.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{path.relative_to(ROOT)} has no readable id")
        elif item_id in ids:
            errors.append(f"Duplicate id {item_id}: {ids[item_id]} and {path}")
        else:
            ids[item_id] = path
    return ids, records


def validate_all_yaml(errors: list[str]) -> None:
    managed = set(CONCEPT_DIR.glob("*.yaml")) | set(DECISION_DIR.glob("*.yaml"))
    for path in sorted(ROOT.rglob("*.yaml")):
        if path not in managed:
            load_yaml(path, errors)


def validate_references(
    concept_ids: set[str], records: list[tuple[Path, dict[str, object]]], warnings: list[str]
) -> None:
    for path, data in records:
        for key in REFERENCE_KEYS:
            values = data.get(key, [])
            if not isinstance(values, list):
                warnings.append(f"{path.relative_to(ROOT)} {key} should be a list")
                continue
            for value in values:
                if value not in concept_ids:
                    warnings.append(
                        f"{path.relative_to(ROOT)} {key} references undeclared concept: {value}"
                    )


def validate_paths(records: list[tuple[Path, dict[str, object]]], warnings: list[str]) -> None:
    for path, data in records:
        for key in ("source_files", "affected"):
            values = data.get(key, [])
            if not isinstance(values, list):
                warnings.append(f"{path.relative_to(ROOT)} {key} should be a list")
                continue
            for value in values:
                if not isinstance(value, str) or not (ROOT / value).exists():
                    warnings.append(
                        f"{path.relative_to(ROOT)} {key} path does not exist: {value}"
                    )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    concept_ids, concept_records = validate_group(
        CONCEPT_DIR, REQUIRED_CONCEPT_KEYS, errors
    )
    _, decision_records = validate_group(
        DECISION_DIR, REQUIRED_DECISION_KEYS, errors
    )
    validate_all_yaml(errors)
    validate_references(set(concept_ids), concept_records, warnings)
    validate_paths(concept_records + decision_records, warnings)

    if not (ROOT / "CONSTITUTION.md").exists():
        errors.append("Missing CONSTITUTION.md")

    if warnings:
        print("Knowledge validation warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("Knowledge validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    message = "Knowledge validation passed"
    if warnings:
        message += " with warnings"
    print(message + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
