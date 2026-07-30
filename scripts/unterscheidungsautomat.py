#!/usr/bin/env python3
"""Codex-Automat der Unterscheidung.

Inspiriert von George Spencer Browns Formkalkül, aber für dieses Projekt
vorsichtig als Prüfwerkzeug gefasst: Eine Unterscheidung markiert eine Seite,
lässt eine unmarkierte Seite mitlaufen und verändert dadurch mögliche Anschlüsse.
Das Werkzeug schreibt nur bei explizitem --output und verändert keine
Manuskriptdateien.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Missing dependency: PyYAML", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parents[1]
CONCEPT_DIR = ROOT / "knowledge" / "concepts"
MANUSCRIPT_DIR = ROOT / "manuskript"

BOUNDARY_WARNINGS = {
    "macht": "Macht nur als abgeleiteten Diagnosebegriff organisierter Asymmetrie behandeln, nicht als Grundachse.",
    "herrschaft": "Herrschaft nur als abgeleiteten Diagnosebegriff organisierter Asymmetrie behandeln, nicht als Grundachse.",
    "gesellschaft": "Keine allgemeine Gesellschaftstheorie einführen.",
    "codex entscheidet": "Codex darf keine Autorentscheidung ersetzen.",
    "ki entscheidet": "KI darf keine Autorentscheidung ersetzen.",
    "wahrheit": "Das Werkzeug prüft Anschlussbedingungen, nicht philosophische Wahrheit.",
}

SPECIAL_ALIASES = {
    "anschliessen": {"anschließen", "anschluss", "anschlüsse", "anschlussmöglichkeit", "anschlussmöglichkeiten"},
    "aktualisieren": {"aktualisierung", "aktualisiert"},
    "algorithmus": {"algorithmisch", "algorithmische", "algorithmen", "algorithmusidentität"},
    "asymmetrie": {"asymmetrisch", "asymmetrische"},
    "form": {"formen", "unterscheidung", "markierung", "markierte", "unmarkierte"},
    "improvisieren": {"improvisation", "improvisatorisch"},
    "kritisieren": {"kritik", "kritisch"},
    "moeglichkeitsraum": {"möglichkeitsraum", "möglichkeit", "möglichkeiten", "anschlussmöglichkeiten"},
    "organisieren": {"organisation", "organisiert", "organisierte"},
    "program": {"programm", "programme", "programmatisch"},
    "reorganisieren": {"reorganisation", "reorganisiert"},
    "revidieren": {"revision", "revidiert"},
    "unterbrechen": {"unterbrechung", "bruch"},
    "verteilen": {"verteilung", "verteilt"},
}


@dataclass(frozen=True)
class Concept:
    id: str
    label: str
    status: str
    file: str
    chapter: Any | None
    definition: str | None
    depends_on: list[str]
    required_for: list[str]
    related: list[str]
    constraints: list[str]
    source_files: list[str]


def normalize(text: str) -> str:
    lowered = text.casefold().replace("ß", "ss")
    return lowered.translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue"}))


def slug(text: str) -> str:
    value = normalize(text)
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "unterscheidung"


def load_concepts() -> list[Concept]:
    concepts: list[Concept] = []
    for path in sorted(CONCEPT_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        concepts.append(Concept(
            id=str(data.get("id", path.stem)),
            label=str(data.get("label", data.get("id", path.stem))),
            status=str(data.get("status", "unknown")),
            file=str(path.relative_to(ROOT)),
            chapter=data.get("chapter"),
            definition=data.get("definition") or data.get("working_definition"),
            depends_on=list(data.get("depends_on", []) or []),
            required_for=list(data.get("required_for", []) or []),
            related=list(data.get("related", []) or []),
            constraints=list(data.get("constraints", []) or []),
            source_files=list(data.get("source_files", []) or []),
        ))
    return concepts


def aliases(concept: Concept) -> set[str]:
    values = {concept.id, concept.label, concept.id.replace("ae", "ä").replace("oe", "ö").replace("ue", "ü")}
    values.update(SPECIAL_ALIASES.get(concept.id, set()))
    return {normalize(value) for value in values if value}


def relevant_concepts(text: str, concepts: list[Concept], limit: int = 10) -> list[dict[str, Any]]:
    haystack = normalize(text)
    scored: list[tuple[int, Concept, set[str]]] = []
    for concept in concepts:
        hits = {alias for alias in aliases(concept) if len(alias) > 2 and re.search(rf"(?<![a-z0-9_]){re.escape(alias)}(?![a-z0-9_])", haystack)}
        concept_text = normalize(" ".join([concept.label, concept.definition or "", " ".join(concept.constraints)]))
        loose = {normalize(word) for word in re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", text) if normalize(word) in concept_text}
        score = 4 * len(hits) + len(loose)
        if score:
            scored.append((score, concept, hits | loose))
    scored.sort(key=lambda item: (-item[0], item[1].id))
    return [concept_dict(concept, score=score, hits=sorted(hits)) for score, concept, hits in scored[:limit]]


def concept_dict(concept: Concept, score: int | None = None, hits: list[str] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": concept.id,
        "label": concept.label,
        "status": concept.status,
        "file": concept.file,
        "chapter": concept.chapter,
        "definition": concept.definition,
        "depends_on": concept.depends_on,
        "required_for": concept.required_for,
        "related": concept.related,
        "constraints": concept.constraints,
    }
    if score is not None:
        data["score"] = score
    if hits is not None:
        data["hits"] = hits
    return data


def boundary_warnings(text: str) -> list[str]:
    haystack = normalize(text)
    return [warning for term, warning in BOUNDARY_WARNINGS.items() if normalize(term) in haystack]


def find_anchors(text: str, concepts: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    terms = {normalize(word) for word in re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", text)}
    by_id = {concept.id: concept for concept in load_concepts()}
    for item in concepts:
        concept = by_id.get(item["id"])
        if concept:
            terms.update(alias for alias in aliases(concept) if len(alias) > 3)
    anchors: list[dict[str, Any]] = []
    for path in sorted(MANUSCRIPT_DIR.glob("*.md")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip() or line.startswith("#"):
                continue
            haystack = normalize(line)
            hits = sorted({term for term in terms if len(term) > 3 and term in haystack})
            if hits:
                anchors.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": line_number,
                    "score": len(hits),
                    "hits": hits[:10],
                    "excerpt": line.strip()[:220],
                })
    anchors.sort(key=lambda item: (-item["score"], item["file"], item["line"]))
    return anchors[:limit]


def analyze(marked: str, unmarked: str, context: str, anchor_limit: int) -> dict[str, Any]:
    concepts = load_concepts()
    full = " ".join([marked, unmarked, context])
    marked_concepts = relevant_concepts(marked + " " + context, concepts)
    unmarked_concepts = relevant_concepts(unmarked + " " + context, concepts)
    all_concepts = {item["id"]: item for item in marked_concepts + unmarked_concepts}
    warnings = boundary_warnings(full)
    if not unmarked.strip():
        warnings.append("Die unmarkierte Seite fehlt; dadurch droht die Unterscheidung als vollständige Beschreibung zu erscheinen.")
    return {
        "status": "Unterscheidungsanalyse; keine Theorieentscheidung",
        "marked_side": marked,
        "unmarked_side": unmarked,
        "context": context,
        "distinction": f"{marked} / {unmarked or 'TODO: unmarkierte Seite bestimmen'}",
        "operation": {
            "mark": "Eine Seite wird als bearbeitbare Seite gesetzt.",
            "cross": "Ein Wiedereintritt oder Seitenwechsel fragt, was die markierte Seite von ihrer unmarkierten Bedingung abhängig macht.",
            "observe": "Beobachtet wird nicht nur der Inhalt, sondern die Unterscheidung, durch die Inhalt sichtbar wird.",
            "reenter": "Die Unterscheidung kann selbst wieder in den markierten Zusammenhang eintreten und dort revidierbar werden.",
        },
        "marked_concepts": marked_concepts,
        "unmarked_concepts": unmarked_concepts,
        "shared_or_adjacent_concepts": sorted(all_concepts),
        "anchors": find_anchors(full, list(all_concepts.values()), anchor_limit),
        "warnings": warnings,
        "recommended_next_steps": [
            "Prüfen, ob die Unterscheidung eine bestehende Definition verändert oder nur eine Beobachtungsform bereitstellt.",
            "Unmarkierte Seite ausdrücklich benennen, wenn aus der Analyse ein Manuskriptvorschlag werden soll.",
            "Anschlussfolgen für Form, Aktualisierung, Organisation und Kritik prüfen.",
            "Bei Manuskriptintegration TODO oder Change Event mit Status der Entscheidung anlegen.",
        ],
        "limits": [
            "Spencer Brown wird hier als operative Beobachtungsfigur verwendet, nicht als neue Grundachse des Buches stabilisiert.",
            "Das Werkzeug erzeugt keine philosophische Geltung, sondern prüfbare Anschlussbedingungen.",
            "Textuelle Manuskriptanker sind Lesehinweise, keine Quellenbelege.",
        ],
    }


def mermaid(data: dict[str, Any]) -> str:
    marked_id = "marked_" + slug(data["marked_side"])
    unmarked_id = "unmarked_" + slug(data["unmarked_side"] or "unmarkiert")
    distinction_id = "distinction"
    lines = ["```mermaid", "flowchart TD"]
    lines.append(f'  {distinction_id}["Unterscheidung: {data["distinction"]}"]')
    lines.append(f'  {distinction_id} -->|markiert| {marked_id}["{data["marked_side"]}"]')
    lines.append(f'  {distinction_id} -.->|unmarkiert| {unmarked_id}["{data["unmarked_side"] or "TODO"}"]')
    lines.append(f'  {marked_id} -->|crossing / Wiedereintritt prüfen| {unmarked_id}')
    lines.append(f'  {unmarked_id} -.->|Bedingung der Markierung| {marked_id}')
    for concept in data["marked_concepts"][:5]:
        cid = "c_" + slug(concept["id"])
        lines.append(f'  {marked_id} -->|berührt| {cid}["{concept["label"]}"]')
    for concept in data["unmarked_concepts"][:5]:
        cid = "u_" + slug(concept["id"])
        lines.append(f'  {unmarked_id} -.->|mitlaufend| {cid}["{concept["label"]}"]')
    lines.append("```")
    return "\n".join(lines)


def markdown(data: dict[str, Any]) -> str:
    lines = [f"# Automat der Unterscheidung: {data['distinction']}", "", f"Status: {data['status']}", "", mermaid(data), "", "## Operation", ""]
    for key, value in data["operation"].items():
        lines.append(f"- **{key}**: {value}")
    lines.extend(["", "## Markierte Seite", ""])
    if data["marked_concepts"]:
        for concept in data["marked_concepts"]:
            lines.append(f"- **{concept['label']}** (`{concept['id']}`): {concept.get('definition') or 'TODO: keine Definition gefunden.'}")
    else:
        lines.append("- TODO: Keine passende Begriffsadresse erkannt.")
    lines.extend(["", "## Unmarkierte Seite", ""])
    if data["unmarked_concepts"]:
        for concept in data["unmarked_concepts"]:
            lines.append(f"- **{concept['label']}** (`{concept['id']}`): {concept.get('definition') or 'TODO: keine Definition gefunden.'}")
    else:
        lines.append("- TODO: Unmarkierte Seite begrifflich bestimmen.")
    lines.extend(["", "## Manuskriptanker", ""])
    if data["anchors"]:
        for anchor in data["anchors"]:
            lines.append(f"- `{anchor['file']}:{anchor['line']}` — {anchor['excerpt']}")
    else:
        lines.append("- Keine Manuskriptanker gefunden.")
    if data["warnings"]:
        lines.extend(["", "## Warnungen", ""])
        lines.extend(f"- {warning}" for warning in data["warnings"])
    lines.extend(["", "## Nächste Prüfschritte", ""])
    lines.extend(f"- {step}" for step in data["recommended_next_steps"])
    lines.extend(["", "## Grenzen", ""])
    lines.extend(f"- {limit}" for limit in data["limits"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analysiert eine Unterscheidung als markierte/unmarkierte Form.")
    parser.add_argument("marked", help="markierte Seite der Unterscheidung")
    parser.add_argument("unmarked", nargs="?", default="", help="unmarkierte Seite der Unterscheidung")
    parser.add_argument("--context", default="", help="zusätzlicher Kontext oder Frage")
    parser.add_argument("--anchor-limit", type=int, default=8, help="maximale Zahl der Manuskriptanker")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path, help="optionale Ausgabedatei")
    args = parser.parse_args()

    data = analyze(args.marked, args.unmarked, args.context, args.anchor_limit)
    output = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else markdown(data)
    if args.output:
        target = args.output if args.output.is_absolute() else ROOT / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())