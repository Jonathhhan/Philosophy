#!/usr/bin/env python3
"""Codex Stop-hook adapter for the recursive project closure check."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def find_root(cwd: str | None) -> Path:
    start = Path(cwd).resolve() if cwd else Path.cwd().resolve()
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=10,
        )
        return Path(completed.stdout.strip()).resolve()
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return Path(__file__).resolve().parents[2]


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def load_input() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid Stop-hook input: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Stop-hook input must be a JSON object")
    return value


def failure_payload(errors: list[str], already_active: bool) -> dict[str, Any]:
    summary = "\n".join(f"- {item}" for item in errors[:8])
    command = "python .agents\\skills\\recursive-codex\\scripts\\check_recursive_state.py"
    message = (
        "Recursive closure check failed.\n"
        f"{summary}\n"
        f"Run `{command}`, correct the reported project state, and validate again."
    )
    if already_active:
        return {
            "continue": True,
            "suppressOutput": False,
            "systemMessage": (
                message
                + " The hook already requested one continuation, so it will not request another. "
                "Do not claim that the closure check passed; disclose the remaining blocker."
            ),
        }
    return {"decision": "block", "reason": message}


def run_self_test() -> int:
    first = failure_payload(["fixture failure"], False)
    second = failure_payload(["fixture failure"], True)
    if first.get("decision") != "block" or "continue" in first:
        print("SELF-TEST FAILED: first failure must request one continuation", file=sys.stderr)
        return 1
    if second.get("continue") is not True or "decision" in second:
        print("SELF-TEST FAILED: repeated failure must not block again", file=sys.stderr)
        return 1
    print("SELF-TEST PASSED")
    return 0


def main() -> int:
    already_active = False
    try:
        hook_input = load_input()
        already_active = bool(hook_input.get("stop_hook_active", False))
        root = find_root(hook_input.get("cwd") if isinstance(hook_input.get("cwd"), str) else None)
        scripts = root / ".agents" / "skills" / "recursive-codex" / "scripts"
        sys.path.insert(0, str(scripts))
        from check_recursive_state import run_checks

        report = run_checks()
        if report["ok"]:
            emit({"continue": True, "suppressOutput": True})
        else:
            emit(failure_payload(list(report["errors"]), already_active))
        return 0
    except Exception as exc:  # Hook failures are closure failures, not silent passes.
        emit(failure_payload([f"closure hook error: {exc}"], already_active))
        return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        raise SystemExit(run_self_test())
    raise SystemExit(main())
