#!/usr/bin/env python3
"""Synchronisiert Theoriearchitektur und Codex-Arbeitsweise.

Der Synchronisierer prüft keine philosophische Wahrheit. Er kontrolliert, ob die
operative Codex-Arbeit dieselben bestätigten Relationen, Statusgrenzen und
Revisionsbedingungen verwendet, die das Projekt für seine Theorie festgelegt hat.
Er schreibt niemals selbst ins Manuskript.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_MOVEMENT = [
    "Anschließen",
    "Organisieren",
    "Aktualisieren",
    "Reorganisieren",
    "Kritisieren",
]

REQUIRED_FILES = {
    "constitution": ROOT / "CONSTITUTION.md",
    "agents": ROOT / "AGENTS.md",
    "workflow": ROOT / "WORKFLOW.md",
    "glossary": ROOT / "GLOSSAR.md",
    "pipeline": ROOT / "projekt" / "editor-pipeline.md",
    "recursive_skill": ROOT / ".agents" / "skills" / "recursive-codex" / "SKILL.md",
}

THEORY_MARKERS = {
    "recursive_thesis": "Jede Aktualisierung verändert den Raum weiterer Anschlussmöglichkeiten.",
    "program_distinction": "Programm",
    "algorithm_distinction": "Algorithmus",
    "organization": "Organisieren",
    "distribution": "Verteilen",
    "asymmetry": "Asymmetrie",
    "critique": "Kritisieren",
}

STATUS_MARKERS = {
    "proposal": ("Vorschlag", "proposal"),
    "confirmed": ("bestätigt", "confirmed"),
    "delegated": ("delegierte Codex-Entscheidung", "decision_status: delegated"),
    "blocked": ("BLOCKED", "blocked"),
}


@dataclass
class Finding:
    level: str
    code: str
    message: str
    files: list[str]


@dataclass
class SyncResult:
    status: str
    operation: str
    findings: list[Finding]
    next_step: str
    checked_files: list[str]


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def contains_ordered(text: str, terms: Iterable[str]) -> bool:
    position = 0
    folded = text.casefold()
    for term in terms:
        match = folded.find(term.casefold(), position)
        if match < 0:
            return False
        position = match + len(term)
    return True


def classify_operation(changed_files: list[str]) -> str:
    manuscript = [path for path in changed_files if path.startswith("manuskript/")]
    governance = [
        path
        for path in changed_files
        if path in {"AGENTS.md", "WORKFLOW.md", "CONSTITUTION.md", "GLOSSAR.md"}
        or path.startswith(".agents/")
        or path.startswith("projekt/")
    ]
    if manuscript and governance:
        return "reorganization"
    if len(manuscript) > 1:
        return "composition"
    if manuscript:
        return "local_update"
    if governance:
        return "reorganization"
    return "audit"


def synchronize(changed_files: list[str]) -> SyncResult:
    texts = {name: read(path) for name, path in REQUIRED_FILES.items()}
    findings: list[Finding] = []

    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES.values() if not path.exists()]
    if missing:
        findings.append(Finding("error", "missing_required_file", "Verbindliche Projektdateien fehlen.", missing))

    agents = texts["agents"]
    skill = texts["recursive_skill"]
    pipeline = texts["pipeline"]
    combined_workflow = "\n".join([agents, skill, pipeline, texts["workflow"]])

    if THEORY_MARKERS["recursive_thesis"] not in agents:
        findings.append(
            Finding(
                "error",
                "missing_recursive_thesis",
                "Die bestätigte rekursive These fehlt in AGENTS.md.",
                ["AGENTS.md"],
            )
        )

    if not contains_ordered(combined_workflow, CANONICAL_MOVEMENT):
        findings.append(
            Finding(
                "error",
                "workflow_sequence_drift",
                "Die Codex-Arbeitsweise bildet die bestätigte rekursive Bewegung nicht vollständig und geordnet ab.",
                ["AGENTS.md", ".agents/skills/recursive-codex/SKILL.md", "projekt/editor-pipeline.md"],
            )
        )

    for marker_name in ("program_distinction", "algorithm_distinction"):
        marker = THEORY_MARKERS[marker_name]
        if marker not in agents or marker not in texts["glossary"]:
            findings.append(
                Finding(
                    "warning",
                    f"unsynchronized_{marker_name}",
                    f"Der Begriff {marker} ist nicht zugleich in Arbeitsregeln und Glossar verankert.",
                    ["AGENTS.md", "GLOSSAR.md"],
                )
            )

    if "PATCH" not in pipeline or "KEEP" not in pipeline or "BLOCKED" not in pipeline:
        findings.append(
            Finding(
                "error",
                "missing_editor_decision_gate",
                "Die Pipeline besitzt kein vollständiges editorisches Entscheidungstor.",
                ["projekt/editor-pipeline.md"],
            )
        )

    if "produktive Differenz" not in pipeline:
        findings.append(
            Finding(
                "warning",
                "missing_productive_difference_gate",
                "Der Automatenlauf ist nicht ausdrücklich an eine produktive Differenz gebunden.",
                ["projekt/editor-pipeline.md"],
            )
        )

    if not all(any(marker in combined_workflow for marker in variants) for variants in STATUS_MARKERS.values()):
        findings.append(
            Finding(
                "warning",
                "status_boundary_drift",
                "Vorschlag, bestätigter Status, Delegation und Blockierung sind nicht vollständig synchronisiert.",
                ["AGENTS.md", ".agents/skills/recursive-codex/SKILL.md", "projekt/editor-pipeline.md"],
            )
        )

    operation = classify_operation(changed_files)
    errors = [finding for finding in findings if finding.level == "error"]
    warnings = [finding for finding in findings if finding.level == "warning"]

    if errors:
        status = "blocked"
        next_step = "Projektregeln vor jeder weiteren Manuskriptintegration synchronisieren."
    elif warnings:
        status = "review"
        next_step = "Warnungen prüfen; nur bei bestätigtem Statusgefälle reorganisieren."
    else:
        status = "synchronized"
        next_step = {
            "local_update": "Kleinste hinreichende Manuskriptänderung ausführen und Folgebeziehungen prüfen.",
            "composition": "Abschnitte integrieren und Begriffsrelationen erneut kontrollieren.",
            "reorganization": "Change Event führen und Theorie- sowie Arbeitsrelationen gemeinsam validieren.",
            "audit": "Nächste noch ungeprüfte Anschlussstelle bestimmen.",
        }[operation]

    return SyncResult(
        status=status,
        operation=operation,
        findings=findings,
        next_step=next_step,
        checked_files=[str(path.relative_to(ROOT)) for path in REQUIRED_FILES.values()],
    )


def markdown(result: SyncResult) -> str:
    lines = [
        "# Theorie-Codex-Synchronisierung",
        "",
        f"- Status: **{result.status}**",
        f"- Eingriff: **{result.operation}**",
        f"- Nächster Schritt: {result.next_step}",
        "",
        "## Befunde",
        "",
    ]
    if not result.findings:
        lines.append("- Keine Abweichung zwischen Theoriearchitektur und Codex-Arbeitsweise gefunden.")
    else:
        for finding in result.findings:
            files = ", ".join(f"`{path}`" for path in finding.files)
            lines.append(f"- **{finding.level.upper()} · {finding.code}:** {finding.message} ({files})")
    lines.extend(["", "## Geprüfte Dateien", ""])
    lines.extend(f"- `{path}`" for path in result.checked_files)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronisiert Theoriearchitektur und Codex-Arbeitsweise.")
    parser.add_argument("changed_files", nargs="*", help="Relativpfade der aktuell geänderten Dateien")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = synchronize(args.changed_files)
    output = (
        json.dumps(asdict(result), ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else markdown(result)
    )
    if args.output:
        target = args.output if args.output.is_absolute() else ROOT / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 1 if result.status == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
