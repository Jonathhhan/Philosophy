#!/usr/bin/env python3
"""Check recursive-codex event schemas and repository knowledge integrity."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from validate_change_event import validate_event


ROOT = Path(__file__).resolve().parents[4]
EVENT_DIR = ROOT / "knowledge" / "change-events"
KNOWLEDGE_VALIDATOR = ROOT / "scripts" / "validate_knowledge.py"


def validate_events() -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    files = sorted(EVENT_DIR.glob("*.yaml"))
    if not files:
        errors.append("knowledge/change-events contains no YAML event files")
        return {"count": 0, "valid": 0}, errors, warnings

    valid_count = 0
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: unreadable YAML: {exc}")
            continue

        event_errors = validate_event(data)
        if event_errors:
            errors.extend(f"{relative}: {message}" for message in event_errors)
            continue

        valid_count += 1
        if isinstance(data, dict) and data.get("status") == "proposed":
            warnings.append(f"{relative}: status is still proposed")

    return {"count": len(files), "valid": valid_count}, errors, warnings


def parse_knowledge_output(returncode: int, stdout: str, stderr: str) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    combined = "\n".join(part.strip() for part in (stdout, stderr) if part.strip())
    lines = [line.strip() for line in combined.splitlines() if line.strip()]

    if returncode != 0:
        detail = " | ".join(lines[-8:]) if lines else f"exit code {returncode}"
        errors.append(f"knowledge validation failed: {detail}")
    else:
        warning_lines = [line[2:] for line in lines if line.startswith("- ")]
        warnings.extend(f"knowledge: {line}" for line in warning_lines)

    return {
        "passed": returncode == 0,
        "warning_count": len([line for line in lines if line.startswith("- ")]),
    }, errors, warnings


def validate_knowledge() -> tuple[dict[str, Any], list[str], list[str]]:
    if not KNOWLEDGE_VALIDATOR.is_file():
        return {"passed": False, "warning_count": 0}, ["scripts/validate_knowledge.py is missing"], []

    try:
        completed = subprocess.run(
            [sys.executable, str(KNOWLEDGE_VALIDATOR)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"passed": False, "warning_count": 0}, [f"knowledge validation could not run: {exc}"], []

    return parse_knowledge_output(completed.returncode, completed.stdout, completed.stderr)


def run_checks() -> dict[str, Any]:
    event_check, event_errors, event_warnings = validate_events()
    knowledge_check, knowledge_errors, knowledge_warnings = validate_knowledge()
    errors = event_errors + knowledge_errors
    warnings = event_warnings + knowledge_warnings
    return {
        "ok": not errors,
        "checks": {
            "change_events": event_check,
            "knowledge": knowledge_check,
        },
        "errors": errors,
        "warnings": warnings,
        "scope": "schema and declared knowledge integrity; not philosophical completeness",
    }


def run_self_test() -> int:
    passed, errors, warnings = parse_knowledge_output(
        0,
        "Knowledge validation warnings:\n- existing warning\nKnowledge validation passed with warnings.",
        "",
    )
    if not passed["passed"] or passed["warning_count"] != 1 or errors or len(warnings) != 1:
        print("SELF-TEST FAILED: warning policy", file=sys.stderr)
        return 1

    failed, errors, warnings = parse_knowledge_output(1, "Knowledge validation failed", "")
    if failed["passed"] or not errors or warnings:
        print("SELF-TEST FAILED: failure policy", file=sys.stderr)
        return 1

    print("SELF-TEST PASSED")
    return 0


def print_human(report: dict[str, Any]) -> None:
    state = "VALID" if report["ok"] else "INVALID"
    print(f"RECURSIVE STATE {state}")
    events = report["checks"]["change_events"]
    knowledge = report["checks"]["knowledge"]
    print(f"- change events: {events['valid']}/{events['count']} valid")
    print(f"- knowledge validation: {'passed' if knowledge['passed'] else 'failed'}")
    print(f"- knowledge warnings: {knowledge['warning_count']}")
    for error in report["errors"]:
        print(f"ERROR: {error}")
    for warning in report["warnings"]:
        print(f"WARNING: {warning}")


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return run_self_test()
    if argv not in ([], ["--json"]):
        print("usage: check_recursive_state.py [--json | --self-test]", file=sys.stderr)
        return 2

    report = run_checks()
    if argv == ["--json"]:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    else:
        print_human(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
