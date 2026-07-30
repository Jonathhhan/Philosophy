#!/usr/bin/env python3
"""Run the repository's complete deterministic validation suite."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERACTIVE = ROOT / "interaktiv"
EVENTS = ROOT / "knowledge" / "change-events"


def command_label(command: list[str]) -> str:
    return subprocess.list2cmdline(command)


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    print(f"\n==> {command_label(command)}", flush=True)
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(command, cwd=cwd, check=False, env=environment)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def npm_command() -> str:
    executable = shutil.which("npm")
    if executable is None:
        raise SystemExit("npm is required but was not found on PATH")
    return executable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run knowledge, recursive, MCP, hook, and Anschlusslabor checks."
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Reuse the existing interaktiv/node_modules instead of running npm ci.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    python = sys.executable
    npm = npm_command()

    run([python, "scripts/validate_knowledge.py"])

    event_files = sorted(EVENTS.glob("*.yaml"))
    if not event_files:
        raise SystemExit("knowledge/change-events contains no YAML event files")
    for event in event_files:
        run(
            [
                python,
                ".agents/skills/recursive-codex/scripts/validate_change_event.py",
                event.relative_to(ROOT).as_posix(),
            ]
        )

    run([python, ".agents/skills/recursive-codex/scripts/check_recursive_state.py"])
    run([python, "-m", "py_compile", "scripts/philosophie_automat.py"])
    run([python, "scripts/philosophie_automat.py", "--format", "json", "Kritik steht nicht außerhalb der Organisation."])
    run([python, "scripts/philosophie_automat.py", "--find-anchors", "--suggest", "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."])
    run([python, "scripts/philosophie_automat.py", "--format", "json", "--draft-for", "manuskript/08-algorithmus.md", "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."])
    run([python, "scripts/philosophie_automat.py", "--format", "json", "--draft-for", "manuskript/08-algorithmus.md", "--event-draft", "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."])
    run([python, "scripts/philosophie_automat.py", "--format", "json", "--draft-for", "manuskript/08-algorithmus.md", "--validate-event-draft", "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."])
    run([python, "-m", "py_compile", "scripts/unterscheidungsautomat.py"])
    run([python, "-m", "py_compile", "scripts/tractatus_automat.py"])
    run([python, "-m", "py_compile", "scripts/kunstwerk_automat.py"])
    run([python, "-m", "py_compile", "scripts/automatenverbund.py"])
    run([python, "scripts/unterscheidungsautomat.py", "Anschliessen", "Nicht-Anschluss", "--format", "json"])
    run([python, "scripts/tractatus_automat.py", "Jede Aktualisierung veraendert den Raum weiterer Anschlussmoeglichkeiten", "--format", "json"])
    run([python, "scripts/kunstwerk_automat.py", "Anschliessen", "Nicht-Anschluss", "--max-steps", "5", "--format", "json"])
    run([python, "scripts/automatenverbund.py", "Anschliessen", "Nicht-Anschluss", "--context", "Smoke-Test", "--max-steps", "5", "--format", "json"])
    run([python, "scripts/test_recursive_graph.py"])
    run([python, ".codex/hooks/recursive_stop.py", "--self-test"])

    if not args.skip_install:
        run([npm, "ci"], cwd=INTERACTIVE)
    run([npm, "run", "check"], cwd=INTERACTIVE)
    run([npm, "test"], cwd=INTERACTIVE)
    run([npm, "run", "build"], cwd=INTERACTIVE)

    print("\nALL REPOSITORY CHECKS PASSED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
