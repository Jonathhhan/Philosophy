#!/usr/bin/env python3
"""Begriffsnetz: erzeugt ein lesendes Begriffsnetz zu einem Thema.

Das Werkzeug liest die lokale Wissensbasis und Manuskriptanker. Es schreibt nur
bei explizitem --output und verändert keine Manuskriptdateien. Das Netz ist eine
Orientierungskarte, keine Theorieentscheidung.
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

RELATION_LABELS = {
    "depends_on": "setzt voraus",
    "required_for": "erforderlich für",
    "related": "verwandt mit",
    "theme": "thematisiert",
    "anchor": "Anker in",
}

SPECIAL_ALIASES = {
    "anschliessen": {"anschließen", "anschluss", "anschlüsse", "anschlussmöglichkeit", "anschlussmöglichkeiten"},
    "aktualisieren": {"aktualisierung", "aktualisiert", "aktuelle"},
    "algorithmus": {"algorithmen", "algorithmisch", "algorithmische", "algorithmischer", "algorithmusidentität"},
    "asymmetrie": {"asymmetrisch", "asymmetrische", "asymmetrischer"},
    "beurteilen": {"urteil", "beurteilung", "beurteilt"},
    "form": {"formen", "förmig"},
    "improvisieren": {"improvisation", "improvisiert", "improvisatorisch"},
    "kritisieren": {"kritik", "kritisch", "kritische", "kritischer"},
    "moeglichkeitsraum": {"möglichkeitsraum", "möglichkeit", "möglichkeiten", "anschlussmöglichkeiten"},
    "organisieren": {"organisation", "organisiert", "organisierte", "organisierter"},
    "program": {"programm", "programme", "programms", "programmatisch"},
    "reorganisieren": {"reorganisation", "reorganisiert"},
    "revidieren": {"revision", "revidiert", "revidierbar"},
    "stabilisieren": {"stabilisierung", "stabilisiert", "stabilität"},
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
    return value or "thema"


def mermaid_id(prefix: str, value: str) -> str:
    return prefix + "_" + slug(value)[:60]


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
    values = {concept.id, concept.label, concept.id.replace("moeg", "mög"), concept.id.replace("ae", "ä").replace("oe", "ö").replace("ue", "ü")}
    values.update(SPECIAL_ALIASES.get(concept.id, set()))
    return {normalize(item) for item in values if item}


def score_concepts(theme: str, concepts: list[Concept]) -> list[tuple[int, Concept, set[str]]]:
    haystack = normalize(theme)
    scored: list[tuple[int, Concept, set[str]]] = []
    for concept in concepts:
        hits = {alias for alias in aliases(concept) if len(alias) > 2 and re.search(rf"(?<![a-z0-9_]){re.escape(alias)}(?![a-z0-9_])", haystack)}
        text = " ".join([concept.label, concept.definition or "", " ".join(concept.constraints)])
        loose_hits = {word for word in re.findall(r"[a-zA-ZäöüÄÖÜß]{5,}", theme) if normalize(word) in normalize(text)}
        score = 4 * len(hits) + len(loose_hits)
        if score:
            scored.append((score, concept, hits | {normalize(item) for item in loose_hits}))
    scored.sort(key=lambda item: (-item[0], item[1].id))
    return scored


def expand_neighborhood(seed_ids: set[str], concepts: list[Concept], depth: int) -> list[Concept]:
    by_id = {concept.id: concept for concept in concepts}
    selected = set(seed_ids)
    frontier = set(seed_ids)
    for _ in range(depth):
        next_frontier: set[str] = set()
        for concept_id in frontier:
            concept = by_id.get(concept_id)
            if not concept:
                continue
            next_frontier.update(concept.depends_on)
            next_frontier.update(concept.required_for)
            next_frontier.update(concept.related)
            for other in concepts:
                if concept_id in other.depends_on or concept_id in other.required_for or concept_id in other.related:
                    next_frontier.add(other.id)
        next_frontier -= selected
        selected.update(next_frontier)
        frontier = next_frontier
    return [by_id[item] for item in sorted(selected) if item in by_id]


def relation_edges(selected: list[Concept]) -> list[dict[str, str]]:
    ids = {concept.id for concept in selected}
    edges: list[dict[str, str]] = []
    for concept in selected:
        for relation in ("depends_on", "required_for", "related"):
            for target in getattr(concept, relation):
                if target in ids:
                    edges.append({"from": concept.id, "to": target, "relation": relation, "label": RELATION_LABELS[relation]})
    seen: set[tuple[str, str, str]] = set()
    unique = []
    for edge in edges:
        key = (edge["from"], edge["to"], edge["relation"])
        if key not in seen:
            unique.append(edge)
            seen.add(key)
    return unique


def find_anchors(selected: list[Concept], limit: int) -> list[dict[str, Any]]:
    terms: dict[str, set[str]] = {concept.id: aliases(concept) for concept in selected}
    anchors: list[dict[str, Any]] = []
    for path in sorted(MANUSCRIPT_DIR.glob("*.md")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip() or line.startswith("#"):
                continue
            haystack = normalize(line)
            hit_ids = [concept_id for concept_id, concept_terms in terms.items() if any(term and len(term) > 3 and term in haystack for term in concept_terms)]
            if hit_ids:
                anchors.append({"file": str(path.relative_to(ROOT)), "line": number, "concepts": sorted(hit_ids), "score": len(hit_ids), "excerpt": line.strip()[:220]})
    anchors.sort(key=lambda item: (-item["score"], item["file"], item["line"]))
    return anchors[:limit]


def build_json(theme: str, depth: int, anchor_limit: int) -> dict[str, Any]:
    concepts = load_concepts()
    scored = score_concepts(theme, concepts)
    seeds = {concept.id for _, concept, _ in scored} or {concept.id for concept in concepts if normalize(concept.label) in normalize(theme)}
    selected = expand_neighborhood(seeds, concepts, depth) if seeds else []
    return {
        "theme": theme,
        "status": "lesendes Begriffsnetz; keine Theorieentscheidung",
        "seed_concepts": [{"id": concept.id, "label": concept.label, "score": score, "hits": sorted(hits)} for score, concept, hits in scored],
        "concepts": [concept.__dict__ for concept in selected],
        "relations": relation_edges(selected),
        "anchors": find_anchors(selected, anchor_limit) if selected else [],
        "limits": [
            "Das Netz zeigt deklarierte und textuell gefundene Anschlüsse.",
            "Es bestätigt keine neuen Definitionen.",
            "Nicht gefundene Begriffe können dennoch philosophisch relevant sein.",
        ],
    }


def markdown(data: dict[str, Any]) -> str:
    by_id = {concept["id"]: concept for concept in data["concepts"]}
    lines = [f"# Begriffsnetz: {data['theme']}", "", f"Status: {data['status']}", "", "```mermaid", "graph TD"]
    theme_id = "theme"
    lines.append(f'  {theme_id}["Thema: {data["theme"]}"]')
    for seed in data["seed_concepts"]:
        cid = mermaid_id("c", seed["id"])
        label = by_id.get(seed["id"], {}).get("label", seed["label"])
        lines.append(f'  {theme_id} -->|{RELATION_LABELS["theme"]}| {cid}["{label}"]')
    for concept in data["concepts"]:
        cid = mermaid_id("c", concept["id"])
        meta = f"Kap. {concept['chapter']}" if concept.get("chapter") is not None else concept.get("status", "")
        lines.append(f'  {cid}["{concept["label"]} ({meta})"]')
    for edge in data["relations"]:
        lines.append(f'  {mermaid_id("c", edge["from"])} -->|{edge["label"]}| {mermaid_id("c", edge["to"])}')
    lines.append("```")
    lines.extend(["", "## Begriffe", ""])
    for concept in data["concepts"]:
        definition = concept.get("definition") or "TODO: keine Definition in der Concept-Datei."
        chapter = f", Kapitel {concept['chapter']}" if concept.get("chapter") is not None else ""
        lines.append(f"- **{concept['label']}** (`{concept['id']}`{chapter}, Status: {concept['status']}): {definition}")
    lines.extend(["", "## Manuskriptanker", ""])
    if data["anchors"]:
        for anchor in data["anchors"]:
            concepts = ", ".join(anchor["concepts"])
            lines.append(f"- `{anchor['file']}:{anchor['line']}` ({concepts}) — {anchor['excerpt']}")
    else:
        lines.append("- Keine Manuskriptanker gefunden.")
    lines.extend(["", "## Grenzen", ""])
    lines.extend(f"- {item}" for item in data["limits"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Erzeugt ein lesendes Begriffsnetz zu einem Thema.")
    parser.add_argument("theme", help="Thema oder Frage, z. B. 'Algorithmusidentität'")
    parser.add_argument("--depth", type=int, default=1, choices=[0, 1, 2], help="Relationstiefe ab erkannten Begriffen")
    parser.add_argument("--anchor-limit", type=int, default=12, help="maximale Zahl der Manuskriptanker")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path, help="optionale Ausgabedatei")
    args = parser.parse_args()

    data = build_json(args.theme, args.depth, args.anchor_limit)
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