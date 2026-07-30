#!/usr/bin/env python3
"""Selbstprogrammierendes Kunstwerk der Anschlussunterscheidungen.

Der Automat laeuft von einer ersten Unterscheidung durch eine Folge weiterer
Unterscheidungen, bis eine Abbruchbedingung erreicht ist. Er veraendert nicht
seinen Quellcode. Stattdessen schreibt er waehrend des Laufs einen eigenen
Score: Jede Operation erzeugt die naechste Programmanweisung der Auffuehrung.

Status: Kunst-/Pruefautomat; keine Manuskriptintegration und keine
Theorieentscheidung.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("Missing dependency: PyYAML")

ROOT = Path(__file__).resolve().parents[1]
CONCEPT_DIR = ROOT / "knowledge" / "concepts"


@dataclass(frozen=True)
class Concept:
    id: str
    label: str
    status: str
    definition: str
    depends_on: tuple[str, ...]
    required_for: tuple[str, ...]
    related: tuple[str, ...]
    constraints: tuple[str, ...]
    file: str


def load_concepts() -> dict[str, Concept]:
    concepts: dict[str, Concept] = {}
    for path in sorted(CONCEPT_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        concept_id = str(data.get("id", path.stem))
        concepts[concept_id] = Concept(
            id=concept_id,
            label=str(data.get("label", concept_id)),
            status=str(data.get("status", "unknown")),
            definition=str(data.get("definition") or data.get("working_definition") or ""),
            depends_on=tuple(data.get("depends_on", []) or []),
            required_for=tuple(data.get("required_for", []) or []),
            related=tuple(data.get("related", []) or []),
            constraints=tuple(data.get("constraints", []) or []),
            file=str(path.relative_to(ROOT)),
        )
    return concepts


def normalize(value: str) -> str:
    return value.casefold().replace("ß", "ss").translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue"}))


def choose_start(marked: str, concepts: dict[str, Concept]) -> str | None:
    needle = normalize(marked)
    exact = [cid for cid, c in concepts.items() if normalize(cid) == needle or normalize(c.label) == needle]
    if exact:
        return exact[0]
    partial = [cid for cid, c in concepts.items() if needle in normalize(cid + " " + c.label + " " + c.definition)]
    return partial[0] if partial else None


def candidate_edges(concept: Concept, concepts: dict[str, Concept]) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for target in concept.required_for:
        if target in concepts:
            edges.append(("required_for", target))
    for target in concept.related:
        if target in concepts:
            edges.append(("related", target))
    for target in concept.depends_on:
        if target in concepts:
            edges.append(("depends_on", target))
    return edges


def inverse_edges(current_id: str, concepts: dict[str, Concept]) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for other_id, other in concepts.items():
        if other_id == current_id:
            continue
        if current_id in other.depends_on:
            edges.append(("inverse_depends_on", other_id))
        if current_id in other.related:
            edges.append(("inverse_related", other_id))
    return edges


def choose_next(current_id: str, concepts: dict[str, Concept], visited: set[str], step: int) -> tuple[str, str] | None:
    current = concepts[current_id]
    edges = candidate_edges(current, concepts) + inverse_edges(current_id, concepts)
    edges = [(rel, target) for rel, target in edges if target not in visited]
    if not edges:
        return None
    priority = {"required_for": 0, "related": 1, "inverse_depends_on": 2, "inverse_related": 3, "depends_on": 4}
    edges.sort(key=lambda item: (priority.get(item[0], 99), item[1]))
    return edges[step % len(edges)]


def unmarked_for(concept: Concept, relation: str, previous_unmarked: str) -> str:
    if relation == "required_for":
        return f"das durch {concept.label} noch nicht Organisierte"
    if relation == "depends_on":
        return f"die Voraussetzung von {concept.label}"
    if relation == "related":
        return f"die Nachbarschaft von {concept.label}"
    if relation.startswith("inverse"):
        return f"die Rueckwirkung auf {concept.label}"
    return previous_unmarked or f"nicht-{concept.label}"


def imperative(step: int, concept: Concept, unmarked: str, relation: str | None) -> str:
    rel = f" ueber {relation}" if relation else ""
    return f"{step:02d}: markiere {concept.label}; fuehre {unmarked} als unmarkierte Seite mit{rel}."


def run(marked: str, unmarked: str, max_steps: int) -> dict[str, Any]:
    concepts = load_concepts()
    start = choose_start(marked, concepts) or "anschliessen"
    if start not in concepts:
        raise SystemExit("No usable start concept found; expected knowledge/concepts/anschliessen.yaml")

    visited: set[str] = set()
    trace: list[dict[str, Any]] = []
    score: list[str] = []
    current_id = start
    current_unmarked = unmarked
    relation: str | None = None

    for index in range(1, max_steps + 1):
        current = concepts[current_id]
        visited.add(current_id)
        instruction = imperative(index, current, current_unmarked, relation)
        score.append(instruction)
        trace.append({
            "step": index,
            "marked": current.label,
            "concept_id": current.id,
            "unmarked": current_unmarked,
            "relation_from_previous": relation,
            "definition": current.definition,
            "constraints": list(current.constraints[:3]),
            "program_line": instruction,
            "source_file": current.file,
        })
        next_edge = choose_next(current_id, concepts, visited, index)
        if next_edge is None:
            break
        relation, next_id = next_edge
        current_unmarked = unmarked_for(current, relation, current_unmarked)
        current_id = next_id

    terminal = "letzte erreichbare deklarierte Anschlussstelle" if len(trace) < max_steps else "gesetzte Schrittgrenze"
    return {
        "title": "Selbstprogrammierendes Kunstwerk der Anschlussunterscheidungen",
        "status": "Auffuehrungsspur; keine Manuskriptintegration und keine Theorieentscheidung",
        "first_distinction": {"marked": marked, "unmarked": unmarked},
        "terminal_condition": terminal,
        "steps": trace,
        "generated_score": score,
        "limits": [
            "Der Automat veraendert nicht seinen Quellcode, sondern erzeugt einen auffuehrbaren Score.",
            "Die Folge nutzt deklarierte Concept-Relationen und bleibt dadurch projektgebunden.",
            "Die letzte Station ist eine Abbruchbedingung, keine philosophische Letztbegruendung.",
            "Manuskriptintegration braucht einen gesonderten Auftrag, Quellenpruefung und Autorentscheidung.",
        ],
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [f"# {data['title']}", "", f"Status: {data['status']}", "", "## Erste Unterscheidung", ""]
    first = data["first_distinction"]
    lines.append(f"- markiert: {first['marked']}")
    lines.append(f"- unmarkiert: {first['unmarked']}")
    lines.extend(["", "## Lauf", ""])
    for step in data["steps"]:
        lines.append(f"### {step['step']}. {step['marked']}")
        lines.append("")
        lines.append(f"- Unmarkierte Seite: {step['unmarked']}")
        if step["relation_from_previous"]:
            lines.append(f"- Anschlussrelation: {step['relation_from_previous']}")
        lines.append(f"- Concept-Datei: `{step['source_file']}`")
        if step["definition"]:
            lines.append(f"- Arbeitsdefinition: {step['definition']}")
        if step["constraints"]:
            lines.append("- Grenzen:")
            for constraint in step["constraints"]:
                lines.append(f"  - {constraint}")
        lines.append(f"- Programmiert naechste Auffuehrung: `{step['program_line']}`")
        lines.append("")
    lines.extend(["## Generierter Score", "", "```text"])
    lines.extend(data["generated_score"])
    lines.extend(["```", "", "## Abbruch", "", f"Der Lauf endet durch: {data['terminal_condition']}.", "", "## Grenzen", ""])
    lines.extend(f"- {limit}" for limit in data["limits"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Laesst ein selbstprogrammierendes Kunstwerk von einer ersten Unterscheidung aus laufen.")
    parser.add_argument("marked", nargs="?", default="Anschliessen", help="markierte Seite der ersten Unterscheidung")
    parser.add_argument("unmarked", nargs="?", default="Nicht-Anschluss", help="unmarkierte Seite der ersten Unterscheidung")
    parser.add_argument("--max-steps", type=int, default=17, help="maximale Anzahl der Auffuehrungsschritte")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = run(args.marked, args.unmarked, max(1, args.max_steps))
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