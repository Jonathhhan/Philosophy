#!/usr/bin/env python3
"""Validate the machine-readable knowledge base without external packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONCEPT_DIR = ROOT / "knowledge" / "concepts"
DECISION_DIR = ROOT / "knowledge" / "decisions"
REQUIRED_CONCEPT_KEYS = {"id", "label", "status"}
REQUIRED_DECISION_KEYS = {"id", "date", "title", "status", "decision", "reason"}
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s|$)")


def top_level_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith((" ", "\t", "-")) or not line.strip() or line.lstrip().startswith("#"):
            continue
        match = KEY_RE.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def validate_group(directory: Path, required: set[str]) -> list[str]:
    errors: list[str] = []
    if not directory.exists():
        return [f"Missing directory: {directory.relative_to(ROOT)}"]
    files = sorted(directory.glob("*.yaml"))
    if not files:
        return [f"No YAML files in {directory.relative_to(ROOT)}"]
    ids: dict[str, Path] = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        keys = top_level_keys(path)
        missing = required - keys
        if missing:
            errors.append(f"{path.relative_to(ROOT)} missing keys: {', '.join(sorted(missing))}")
        match = re.search(r"^id:\s*([^\n#]+)", text, re.MULTILINE)
        if match:
            item_id = match.group(1).strip()
            if item_id in ids:
                errors.append(f"Duplicate id {item_id}: {ids[item_id]} and {path}")
            ids[item_id] = path
        else:
            errors.append(f"{path.relative_to(ROOT)} has no readable id")
    return errors


def main() -> int:
    errors = []
    errors.extend(validate_group(CONCEPT_DIR, REQUIRED_CONCEPT_KEYS))
    errors.extend(validate_group(DECISION_DIR, REQUIRED_DECISION_KEYS))

    constitution = ROOT / "CONSTITUTION.md"
    if not constitution.exists():
        errors.append("Missing CONSTITUTION.md")

    if errors:
        print("Knowledge validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Knowledge validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
