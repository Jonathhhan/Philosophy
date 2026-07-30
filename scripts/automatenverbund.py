#!/usr/bin/env python3
"""Automatenverbund fuer Anschlussfaehigkeit.

Kombiniert die vorhandenen lesenden Automaten nur dort, wo Anschluesse
nachweisbar sind: gemeinsame Begriffsadressen, Manuskriptanker oder deklarierte
Concept-Relationen. Der Verbund schreibt nicht ins Manuskript und stabilisiert
keine Theorieentscheidung.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_module(name: str, filename: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def concept_ids(items: list[dict[str, Any]]) -> set[str]:
    return {str(item.get("id")) for item in items if item.get("id")}


def anchor_keys(items: list[dict[str, Any]]) -> set[str]:
    return {f"{item.get('file')}:{item.get('line')}" for item in items if item.get("file") and item.get("line")}


def relation_bridge(source: dict[str, Any], target: dict[str, Any]) -> list[str]:
    source_ids = concept_ids(source.get("marked_concepts", [])) | concept_ids(source.get("unmarked_concepts", [])) | concept_ids(source.get("concepts", []))
    target_ids = concept_ids(target.get("concepts", []))
    for step in target.get("steps", []):
        if step.get("concept_id"):
            target_ids.add(str(step["concept_id"]))

    bridges: list[str] = []
    shared = sorted(source_ids & target_ids)
    if shared:
        bridges.append("gemeinsame Begriffsadressen: " + ", ".join(shared))

    shared_anchors = sorted(anchor_keys(source.get("anchors", [])) & anchor_keys(target.get("anchors", [])))
    if shared_anchors:
        bridges.append("gemeinsame Manuskriptanker: " + ", ".join(shared_anchors[:5]))

    return bridges


def combine(marked: str, unmarked: str, context: str, max_steps: int) -> dict[str, Any]:
    unterscheidung = load_module("unterscheidungsautomat", "unterscheidungsautomat.py")
    tractatus = load_module("tractatus_automat", "tractatus_automat.py")
    kunstwerk = load_module("kunstwerk_automat", "kunstwerk_automat.py")

    topic = " / ".join(part for part in [marked, unmarked] if part)
    if context:
        topic = f"{topic}: {context}"

    distinction_data = unterscheidung.analyze(marked, unmarked, context, anchor_limit=8)
    tractatus_data = tractatus.analyze(topic, concept_limit=8, anchor_limit=8)
    artwork_data = kunstwerk.run(marked, unmarked or "Nicht-" + marked, max_steps=max_steps)

    d_to_t = relation_bridge(distinction_data, tractatus_data)
    t_to_a = relation_bridge(tractatus_data, artwork_data)
    d_to_a = relation_bridge(distinction_data, artwork_data)

    enabled = []
    blocked = []
    if d_to_t:
        enabled.append({"from": "unterscheidungsautomat", "to": "tractatus_automat", "bridges": d_to_t})
    else:
        blocked.append({"from": "unterscheidungsautomat", "to": "tractatus_automat", "reason": "keine gemeinsame Begriffsadresse oder kein gemeinsamer Manuskriptanker"})
    if t_to_a or d_to_a:
        enabled.append({"from": "tractatus_automat", "to": "kunstwerk_automat", "bridges": list(dict.fromkeys(t_to_a + d_to_a))})
    else:
        blocked.append({"from": "tractatus_automat", "to": "kunstwerk_automat", "reason": "keine geteilte deklarierte Anschlussstelle"})

    return {
        "title": "Automatenverbund der Anschlussfaehigkeit",
        "status": "kombinierte Pruef- und Auffuehrungsspur; keine Manuskriptintegration und keine Theorieentscheidung",
        "input": {"marked": marked, "unmarked": unmarked, "context": context, "topic": topic},
        "enabled_connections": enabled,
        "blocked_connections": blocked,
        "sequence": [
            {"stage": "unterscheiden", "summary": distinction_data["distinction"], "warnings": distinction_data.get("warnings", [])},
            {"stage": "propositional_ordnen", "summary": tractatus_data["propositions"][:4], "warnings": tractatus_data.get("warnings", [])},
            {"stage": "auffuehren", "summary": artwork_data["generated_score"], "terminal_condition": artwork_data["terminal_condition"]},
        ],
        "outputs": {
            "distinction": distinction_data,
            "tractatus": tractatus_data,
            "artwork": artwork_data,
        },
        "limits": [
            "Der Verbund kombiniert Automaten nur ueber ausgewiesene Anschlussbruecken.",
            "Eine blockierte Verbindung ist ein Pruefbefund, kein Fehler.",
            "Die Ausgabe bleibt Vorschlag, Pruefstruktur oder Auffuehrungsspur.",
            "Manuskriptintegration verlangt einen gesonderten Auftrag, Quellenpruefung und Autorentscheidung.",
        ],
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [f"# {data['title']}", "", f"Status: {data['status']}", "", "## Eingabe", ""]
    entry = data["input"]
    lines.append(f"- markiert: {entry['marked']}")
    lines.append(f"- unmarkiert: {entry['unmarked'] or 'TODO'}")
    if entry["context"]:
        lines.append(f"- Kontext: {entry['context']}")
    lines.extend(["", "## Ermoeglichte Anschluesse", ""])
    if data["enabled_connections"]:
        for connection in data["enabled_connections"]:
            lines.append(f"- `{connection['from']}` -> `{connection['to']}`")
            for bridge in connection["bridges"]:
                lines.append(f"  - {bridge}")
    else:
        lines.append("- Keine Verbindung wurde automatisch ermoeglicht.")
    if data["blocked_connections"]:
        lines.extend(["", "## Blockierte Anschluesse", ""])
        for connection in data["blocked_connections"]:
            lines.append(f"- `{connection['from']}` -> `{connection['to']}`: {connection['reason']}")

    lines.extend(["", "## Verbundlauf", ""])
    distinction = data["outputs"]["distinction"]
    lines.append(f"### 1. Unterscheiden: {distinction['distinction']}")
    if distinction.get("marked_concepts"):
        lines.append("- Markierte Begriffsadressen: " + ", ".join(item["id"] for item in distinction["marked_concepts"][:6]))
    if distinction.get("unmarked_concepts"):
        lines.append("- Unmarkierte Begriffsadressen: " + ", ".join(item["id"] for item in distinction["unmarked_concepts"][:6]))

    tractatus = data["outputs"]["tractatus"]
    lines.extend(["", "### 2. Propositional ordnen", ""])
    for proposition in tractatus["propositions"][:6]:
        lines.append(f"- {proposition['number']} {proposition['kind']}: {proposition['text']}")

    artwork = data["outputs"]["artwork"]
    lines.extend(["", "### 3. Auffuehren / Score erzeugen", "", "```text"])
    lines.extend(artwork["generated_score"])
    lines.extend(["```", "", f"Abbruch: {artwork['terminal_condition']}"])

    lines.extend(["", "## Grenzen", ""])
    lines.extend(f"- {limit}" for limit in data["limits"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Kombiniert Codex-Automaten, wo Anschlussbruecken bestehen.")
    parser.add_argument("marked", help="markierte Seite / Startbegriff")
    parser.add_argument("unmarked", nargs="?", default="", help="unmarkierte Seite")
    parser.add_argument("--context", default="", help="Kontext oder Fragestellung")
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = combine(args.marked, args.unmarked, args.context, max(1, args.max_steps))
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