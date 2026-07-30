#!/usr/bin/env python3
"""Tractatus-philosophicus-Automat.

Erzeugt eine nummerierte, propositionale Prüfstruktur zu einem Thema. Das
Werkzeug imitiert keinen Autorstil und behauptet keine Theorieentscheidung. Es
ordnet mögliche Sätze, Unterfragen, Grenzen und Anschlussstellen im Rahmen des
Buchprojekts.
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

SPECIAL_ALIASES = {
    "anschliessen": {"anschließen", "anschluss", "anschlüsse", "anschlussmöglichkeit", "anschlussmöglichkeiten"},
    "aktualisieren": {"aktualisierung", "aktualisiert"},
    "algorithmus": {"algorithmisch", "algorithmische", "algorithmen", "algorithmusidentität"},
    "asymmetrie": {"asymmetrisch", "asymmetrische"},
    "form": {"formen", "unterscheidung", "markierung"},
    "improvisieren": {"improvisation", "improvisatorisch"},
    "kritisieren": {"kritik", "kritisch"},
    "moeglichkeitsraum": {"möglichkeitsraum", "möglichkeit", "möglichkeiten", "anschlussmöglichkeiten"},
    "organisieren": {"organisation", "organisiert", "organisierte"},
    "program": {"programm", "programme", "programmatisch"},
    "reorganisieren": {"reorganisation", "reorganisiert"},
    "revidieren": {"revision", "revidiert"},
    "stabilisieren": {"stabilisierung", "stabilisiert"},
    "unterbrechen": {"unterbrechung", "bruch"},
    "verteilen": {"verteilung", "verteilt"},
}

BOUNDARY_TERMS = {
    "macht": "Macht nicht als Grundtheorie, sondern allenfalls als abgeleitete Diagnose organisierter Asymmetrie behandeln.",
    "herrschaft": "Herrschaft nicht als Grundtheorie, sondern allenfalls als abgeleitete Diagnose organisierter Asymmetrie behandeln.",
    "gesellschaft": "Keine allgemeine Gesellschaftstheorie einführen.",
    "ki entscheidet": "KI ersetzt keine Autorenentscheidung.",
    "codex entscheidet": "Codex ersetzt keine Autorenentscheidung.",
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


def score_concepts(topic: str, concepts: list[Concept], limit: int) -> list[dict[str, Any]]:
    haystack = normalize(topic)
    scored: list[tuple[int, Concept, set[str]]] = []
    for concept in concepts:
        hits = {alias for alias in aliases(concept) if len(alias) > 2 and re.search(rf"(?<![a-z0-9_]){re.escape(alias)}(?![a-z0-9_])", haystack)}
        concept_text = normalize(" ".join([concept.label, concept.definition or "", " ".join(concept.constraints)]))
        loose = {normalize(word) for word in re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", topic) if normalize(word) in concept_text}
        score = 4 * len(hits) + len(loose)
        if score:
            scored.append((score, concept, hits | loose))
    scored.sort(key=lambda item: (-item[0], item[1].id))
    return [{
        "id": concept.id,
        "label": concept.label,
        "status": concept.status,
        "chapter": concept.chapter,
        "file": concept.file,
        "definition": concept.definition,
        "depends_on": concept.depends_on,
        "required_for": concept.required_for,
        "related": concept.related,
        "constraints": concept.constraints,
        "hits": sorted(hits),
        "score": score,
    } for score, concept, hits in scored[:limit]]


def find_anchors(topic: str, selected: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    concepts = {concept.id: concept for concept in load_concepts()}
    terms = {normalize(word) for word in re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", topic)}
    for item in selected:
        concept = concepts.get(item["id"])
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
                anchors.append({"file": str(path.relative_to(ROOT)), "line": line_number, "score": len(hits), "hits": hits[:8], "excerpt": line.strip()[:220]})
    anchors.sort(key=lambda item: (-item["score"], item["file"], item["line"]))
    return anchors[:limit]


def warnings(topic: str) -> list[str]:
    haystack = normalize(topic)
    return [warning for term, warning in BOUNDARY_TERMS.items() if normalize(term) in haystack]


def proposition_text(topic: str, concepts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    subject = topic.strip().rstrip(".")
    primary = concepts[0] if concepts else None
    props: list[dict[str, Any]] = []
    props.append({"number": "1", "kind": "Leitsatz", "text": f"{subject} ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung."})
    props.append({"number": "1.1", "kind": "Bestimmung", "text": "Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen."})
    props.append({"number": "1.11", "kind": "Grenze", "text": "Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung."})
    if primary:
        props.append({"number": "2", "kind": "Begriffsadresse", "text": f"Die erste erkannte Begriffsadresse ist {primary['label']}: {primary.get('definition') or 'TODO: Definition prüfen'}."})
        for index, concept in enumerate(concepts[1:5], start=1):
            props.append({"number": f"2.{index}", "kind": "Nachbarbegriff", "text": f"{concept['label']} bildet eine mögliche Anschlussadresse für die weitere Prüfung."})
    else:
        props.append({"number": "2", "kind": "TODO", "text": "Es wurde keine eindeutige Begriffsadresse erkannt; die thematische Markierung muss manuell bestimmt werden."})
    props.append({"number": "3", "kind": "Operation", "text": "Eine propositionale Ordnung macht sichtbar, welche Sätze voneinander abhängen und welche Anschlüsse sie eröffnen."})
    props.append({"number": "3.1", "kind": "Prüfung", "text": "Jeder Unterpunkt muss als Definition, Anwendung, Einwand, Beispiel oder TODO klassifizierbar bleiben."})
    props.append({"number": "4", "kind": "Anschluss", "text": "Wenn ein Satz ins Manuskript übernommen werden soll, sind Herkunft, Status und Folgeanschlüsse auszuweisen."})
    return props


def analyze(topic: str, concept_limit: int, anchor_limit: int) -> dict[str, Any]:
    concepts = score_concepts(topic, load_concepts(), concept_limit)
    return {
        "topic": topic,
        "status": "propositionale Prüfstruktur; keine Theorieentscheidung",
        "concepts": concepts,
        "propositions": proposition_text(topic, concepts),
        "anchors": find_anchors(topic, concepts, anchor_limit),
        "warnings": warnings(topic),
        "limits": [
            "Der Automat imitiert keinen Autorstil und ersetzt keine Lektüre.",
            "Die Nummerierung ist ein Ordnungsinstrument, keine Gewissheitsform.",
            "Manuskriptanker sind Prüfhinweise, keine Belege.",
        ],
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [f"# Tractatus-philosophicus-Automat: {data['topic']}", "", f"Status: {data['status']}", "", "## Propositionen", ""]
    for proposition in data["propositions"]:
        lines.append(f"{proposition['number']}. **{proposition['kind']}** — {proposition['text']}")
    lines.extend(["", "## Begriffsadressen", ""])
    if data["concepts"]:
        for concept in data["concepts"]:
            chapter = f", Kapitel {concept['chapter']}" if concept.get("chapter") is not None else ""
            lines.append(f"- **{concept['label']}** (`{concept['id']}`{chapter}): {concept.get('definition') or 'TODO: Definition prüfen.'}")
    else:
        lines.append("- TODO: Keine Begriffsadresse erkannt.")
    lines.extend(["", "## Manuskriptanker", ""])
    if data["anchors"]:
        for anchor in data["anchors"]:
            lines.append(f"- `{anchor['file']}:{anchor['line']}` — {anchor['excerpt']}")
    else:
        lines.append("- Keine Manuskriptanker gefunden.")
    if data["warnings"]:
        lines.extend(["", "## Warnungen", ""])
        lines.extend(f"- {warning}" for warning in data["warnings"])
    lines.extend(["", "## Grenzen", ""])
    lines.extend(f"- {limit}" for limit in data["limits"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Erzeugt eine nummerierte propositionale Prüfstruktur zu einem Thema.")
    parser.add_argument("topic", help="Thema oder Satz")
    parser.add_argument("--concept-limit", type=int, default=8)
    parser.add_argument("--anchor-limit", type=int, default=8)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = analyze(args.topic, args.concept_limit, args.anchor_limit)
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