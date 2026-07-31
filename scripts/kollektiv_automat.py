#!/usr/bin/env python3
"""Kollektiv-Automat für rollengetrennte, nicht-majoritäre Projektprüfung.

Das Werkzeug bündelt vorhandene lokale Evidenz, bewahrt abweichende Befunde
und erzeugt ausschließlich eine operative Redaktionsempfehlung. Es verändert
keine Manuskriptdatei und ersetzt keine Autorenentscheidung.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import philosophie_automat


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "manuskript"
OUTCOMES = ("PATCH", "KEEP", "BLOCKED", "REORGANIZE", "FORK")


def _exact_occurrences(thought: str) -> list[dict[str, Any]]:
    needle = philosophie_automat.normalize(thought.strip().rstrip("."))
    if not needle:
        return []
    occurrences = []
    for path in sorted(MANUSCRIPT_DIR.glob("*.md")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if needle in philosophie_automat.normalize(line):
                occurrences.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": line_number,
                    "excerpt": line.strip()[:240],
                })
    return occurrences


def _affected_manuscript_files(report: dict[str, Any]) -> list[str]:
    files: set[str] = set()
    for concept in report["mentioned_concepts"]:
        for source in concept.get("source_files", []):
            normalized = str(source).replace("\\", "/")
            if normalized.startswith("manuskript/"):
                files.add(normalized)
    for anchor in report["anchors"]:
        files.add(anchor["file"].replace("\\", "/"))
    return sorted(files)


def _role_findings(
    report: dict[str, Any],
    exact: list[dict[str, Any]],
    affected_files: list[str],
    target_file: str | None,
) -> list[dict[str, Any]]:
    concepts = report["mentioned_concepts"]
    warnings = report["boundary_warnings"]
    source_files = sorted({
        source
        for concept in concepts
        for source in concept.get("source_files", [])
    })
    material_terms = {
        "montage", "material", "programm", "algorithmus", "implementierung",
        "ausführung", "ausfuehrung", "komposition", "technik",
    }
    normalized = philosophie_automat.normalize(report["thought"])
    material_hits = sorted(term for term in material_terms if philosophie_automat.normalize(term) in normalized)

    return [
        {
            "role": "genealogist",
            "stance": "supported" if source_files or exact else "insufficient",
            "finding": (
                "Deklarierte Quellen oder eine vorhandene Manuskriptstelle tragen die Prüfung."
                if source_files or exact
                else "Keine deklarierte Quelle oder exakte Manuskriptstelle trägt den Gedanken."
            ),
            "evidence": source_files[:12] + [
                f"{item['file']}:{item['line']}" for item in exact[:4]
            ],
        },
        {
            "role": "consistency_checker",
            "stance": "blocked" if warnings else ("relational" if len(affected_files) > 1 else "compatible"),
            "finding": (
                "Eine Projektgrenze ist berührt."
                if warnings
                else (
                    "Der Gedanke betrifft mehrere Manuskriptbeziehungen."
                    if len(affected_files) > 1
                    else "Keine automatische Begriffsverschiebung wurde erkannt."
                )
            ),
            "evidence": [item["warning"] for item in warnings] or affected_files,
        },
        {
            "role": "critic",
            "stance": "caution",
            "finding": (
                "Die Empfehlung muss als Vorschlag reversibel bleiben; Evidenz ersetzt keine Begründung."
            ),
            "evidence": [
                "Keine Mehrheitsentscheidung.",
                "Keine automatische Theorie- oder Autorenentscheidung.",
            ],
        },
        {
            "role": "material_technical",
            "stance": "relevant" if material_hits else "not_triggered",
            "finding": (
                "Materielle oder technische Begriffe müssen in ihrer Eigenständigkeit geprüft werden."
                if material_hits
                else "Keine explizite material-technische Prüfadresse wurde ausgelöst."
            ),
            "evidence": material_hits,
        },
        {
            "role": "boundary_checker",
            "stance": "blocked" if warnings else "safe",
            "finding": (
                "Mindestens eine deklarierte Projektgrenze blockiert die Integration."
                if warnings
                else "Keine automatische Grenzwarnung wurde ausgelöst."
            ),
            "evidence": [item["id"] for item in warnings],
        },
        {
            "role": "editorial_locator",
            "stance": "located" if target_file or exact else "unlocated",
            "finding": (
                "Eine konkrete redaktionelle Adresse liegt vor."
                if target_file or exact
                else "Ein konkretes Manuskriptziel fehlt."
            ),
            "evidence": ([target_file] if target_file else []) + [
                f"{item['file']}:{item['line']}" for item in exact[:4]
            ],
        },
    ]


def _recommendation(
    report: dict[str, Any],
    variants: list[str],
    exact: list[dict[str, Any]],
    affected_files: list[str],
    target_file: str | None,
) -> dict[str, Any]:
    if report["boundary_warnings"]:
        outcome = "BLOCKED"
        rule = "boundary_precedence"
        reason = "Eine deklarierte Projektgrenze hat Vorrang vor positiven Rollenbefunden."
    elif len(variants) >= 2:
        outcome = "FORK"
        rule = "explicit_non_equivalent_variants"
        reason = "Mehrere ausdrücklich übergebene Varianten bleiben getrennt prüfbar."
    elif exact:
        outcome = "KEEP"
        rule = "explicit_manuscript_presence"
        reason = "Der Gedanke ist bereits ausdrücklich im Manuskript vorhanden."
    elif target_file:
        outcome = "PATCH"
        rule = "bounded_editorial_target"
        reason = "Ein konkretes Ziel liegt vor; ein Eingriff kann als markierter Vorschlag vorbereitet werden."
    elif len(affected_files) >= 3:
        outcome = "REORGANIZE"
        rule = "cross_file_relations"
        reason = "Der Gedanke berührt mindestens drei Manuskriptdateien und verlangt eine Relationsprüfung."
    else:
        outcome = "BLOCKED"
        rule = "missing_editorial_address"
        reason = "Für einen Eingriff fehlt eine hinreichend bestimmte redaktionelle Adresse."
    return {
        "outcome": outcome,
        "status": "collective_proposal",
        "rule": rule,
        "reason": reason,
        "requires_author_decision": outcome in {"PATCH", "REORGANIZE", "FORK"},
    }


def _dissent(
    report: dict[str, Any],
    variants: list[str],
    exact: list[dict[str, Any]],
    affected_files: list[str],
    target_file: str | None,
    roles: list[dict[str, Any]],
) -> dict[str, Any]:
    tensions = []
    if len(variants) >= 2:
        tensions.append({
            "id": "non_equivalent_variants",
            "between": ["variants"],
            "description": "Mehrere ausdrücklich übergebene Varianten beanspruchen getrennte Weiterarbeit.",
        })
    if report["boundary_warnings"] and (exact or target_file or report["mentioned_concepts"]):
        tensions.append({
            "id": "evidence_vs_boundary",
            "between": ["genealogist", "boundary_checker"],
            "description": "Vorhandene Evidenz oder eine redaktionelle Adresse hebt die Grenzwarnung nicht auf.",
        })
    if exact and len(affected_files) >= 3:
        tensions.append({
            "id": "presence_vs_relational_scope",
            "between": ["editorial_locator", "consistency_checker"],
            "description": "Explizite Präsenz und dateiübergreifende Folgen begründen verschiedene Weiterarbeitsrichtungen.",
        })
    if target_file and len(affected_files) >= 3:
        tensions.append({
            "id": "local_target_vs_cross_file_scope",
            "between": ["editorial_locator", "consistency_checker"],
            "description": "Das lokale Ziel steht einer weiter reichenden Relationsprüfung gegenüber.",
        })
    return {
        "preserved": True,
        "active": bool(tensions),
        "role_plurality": sorted({item["stance"] for item in roles}),
        "tensions": tensions,
        "note": (
            "Benannte Spannungen bleiben unaufgelöst; sie werden nicht gezählt oder gemittelt."
            if tensions
            else "Rollenpluralität ist erhalten, ohne daraus automatisch inhaltlichen Dissens abzuleiten."
        ),
    }

def build_collective_report(
    thought: str,
    *,
    variants: list[str] | None = None,
    target_file: str | None = None,
) -> dict[str, Any]:
    variants = [item.strip() for item in (variants or []) if item.strip()]
    normalized_target = None
    if target_file:
        path = philosophie_automat.safe_existing_path(
            target_file,
            MANUSCRIPT_DIR,
            "--target-file muss auf eine vorhandene Datei unter manuskript/ zeigen.",
        )
        normalized_target = str(path.relative_to(ROOT))

    base = philosophie_automat.build_report(thought, include_anchors=True)
    exact = _exact_occurrences(thought)
    affected_files = _affected_manuscript_files(base)
    roles = _role_findings(base, exact, affected_files, normalized_target)
    recommendation = _recommendation(base, variants, exact, affected_files, normalized_target)

    return {
        "protocol": "collective-difference-protocol/v1",
        "thought": thought,
        "variants": variants,
        "target_file": normalized_target,
        "shared_evidence": {
            "mentioned_concepts": base["mentioned_concepts"],
            "adjacent_concepts": base["adjacent_concepts"],
            "anchors": base["anchors"],
            "exact_occurrences": exact,
            "affected_manuscript_files": affected_files,
            "boundary_warnings": base["boundary_warnings"],
        },
        "role_findings": roles,
        "dissent": _dissent(base, variants, exact, affected_files, normalized_target, roles),
        "collective_recommendation": recommendation,
        "limits": [
            "Die Empfehlung folgt transparenten Vorrangregeln, nicht einer Mehrheitsentscheidung.",
            "Das Kollektiv verändert keine Manuskriptdatei.",
            "PATCH, REORGANIZE und FORK benötigen eine Autorenentscheidung.",
            "Mechanische Evidenz ist weder philosophische Wahrheit noch theoretische Bestätigung.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    recommendation = report["collective_recommendation"]
    lines = [
        "# Kollektive Prüfung",
        "",
        f"**Gedanke:** {report['thought']}",
        f"**Empfehlung:** `{recommendation['outcome']}`",
        f"**Regel:** `{recommendation['rule']}`",
        f"**Begründung:** {recommendation['reason']}",
        "",
        "## Rollenbefunde",
    ]
    for finding in report["role_findings"]:
        lines.append(f"- **{finding['role']}** — `{finding['stance']}`: {finding['finding']}")
        for evidence in finding["evidence"]:
            lines.append(f"  - {evidence}")
    lines.extend(["", "## Erhaltener Dissens"])
    lines.append(f"- Aktiv: {'ja' if report['dissent']['active'] else 'nein'}")
    lines.append(f"- Rollenstände: {', '.join(report['dissent']['role_plurality'])}")
    for tension in report["dissent"]["tensions"]:
        lines.append(f"- `{tension['id']}`: {tension['description']}")
    lines.append(f"- {report['dissent']['note']}")
    lines.extend(["", "## Betroffene Manuskriptdateien"])
    affected = report["shared_evidence"]["affected_manuscript_files"]
    lines.extend(f"- `{item}`" for item in affected)
    if not affected:
        lines.append("- Keine hinreichend bestimmte Datei.")
    lines.extend(["", "## Grenzen"])
    lines.extend(f"- {item}" for item in report["limits"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prüft einen Gedanken durch ein nicht-majoritäres lokales Automatenkollektiv."
    )
    parser.add_argument("thought", nargs="*", help="Zu prüfender Gedanke.")
    parser.add_argument("--variant", action="append", default=[], help="Alternative Fassung; mehrfach verwendbar.")
    parser.add_argument("--target-file", help="Konkretes Ziel unter manuskript/ für eine PATCH-Prüfung.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", help="Ausgabe in eine Datei schreiben.")
    args = parser.parse_args(argv)
    thought = " ".join(args.thought).strip() or sys.stdin.read().strip()
    if not thought:
        parser.error("Bitte einen Gedanken als Argument oder über stdin übergeben.")

    report = build_collective_report(thought, variants=args.variant, target_file=args.target_file)
    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else render_markdown(report)
    )
    if args.output:
        output = (ROOT / args.output).resolve()
        if ROOT.resolve() not in output.parents:
            raise SystemExit("--output muss innerhalb des Projekts liegen.")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
