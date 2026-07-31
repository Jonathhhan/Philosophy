#!/usr/bin/env python3
"""Automatenverbund fuer Anschlussfaehigkeit.

Kombiniert die vorhandenen lesenden Automaten dort, wo Anschluesse nachweisbar
sind. Im iterativen Modus verfolgt der Verbund selbst weitere Begriffsadressen,
erkennt bereits gepruefte Zustaende und laeuft bis zu einer produktiven
Differenz oder bis der erreichbare Suchraum erschoepft ist.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DEFAULT_STATE = ROOT / "recovered" / "state" / "automatenverbund-state.json"


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
    return {
        f"{item.get('file')}:{item.get('line')}"
        for item in items
        if item.get("file") and item.get("line")
    }


def relation_bridge(source: dict[str, Any], target: dict[str, Any]) -> list[str]:
    source_ids = (
        concept_ids(source.get("marked_concepts", []))
        | concept_ids(source.get("unmarked_concepts", []))
        | concept_ids(source.get("concepts", []))
    )
    target_ids = concept_ids(target.get("concepts", []))
    for step in target.get("steps", []):
        if step.get("concept_id"):
            target_ids.add(str(step["concept_id"]))

    bridges: list[str] = []
    shared = sorted(source_ids & target_ids)
    if shared:
        bridges.append("gemeinsame Begriffsadressen: " + ", ".join(shared))

    shared_anchors = sorted(
        anchor_keys(source.get("anchors", []))
        & anchor_keys(target.get("anchors", []))
    )
    if shared_anchors:
        bridges.append(
            "gemeinsame Manuskriptanker: " + ", ".join(shared_anchors[:5])
        )

    return bridges


def combine(marked: str, unmarked: str, context: str, max_steps: int) -> dict[str, Any]:
    unterscheidung = load_module("unterscheidungsautomat", "unterscheidungsautomat.py")
    tractatus = load_module("tractatus_automat", "tractatus_automat.py")
    kunstwerk = load_module("kunstwerk_automat", "kunstwerk_automat.py")

    topic = " / ".join(part for part in [marked, unmarked] if part)
    if context:
        topic = f"{topic}: {context}"

    distinction_data = unterscheidung.analyze(
        marked, unmarked, context, anchor_limit=8
    )
    tractatus_data = tractatus.analyze(topic, concept_limit=8, anchor_limit=8)
    artwork_data = kunstwerk.run(
        marked, unmarked or "Nicht-" + marked, max_steps=max_steps
    )

    d_to_t = relation_bridge(distinction_data, tractatus_data)
    t_to_a = relation_bridge(tractatus_data, artwork_data)
    d_to_a = relation_bridge(distinction_data, artwork_data)

    enabled = []
    blocked = []
    if d_to_t:
        enabled.append(
            {
                "from": "unterscheidungsautomat",
                "to": "tractatus_automat",
                "bridges": d_to_t,
            }
        )
    else:
        blocked.append(
            {
                "from": "unterscheidungsautomat",
                "to": "tractatus_automat",
                "reason": "keine gemeinsame Begriffsadresse oder kein gemeinsamer Manuskriptanker",
            }
        )
    if t_to_a or d_to_a:
        enabled.append(
            {
                "from": "tractatus_automat",
                "to": "kunstwerk_automat",
                "bridges": list(dict.fromkeys(t_to_a + d_to_a)),
            }
        )
    else:
        blocked.append(
            {
                "from": "tractatus_automat",
                "to": "kunstwerk_automat",
                "reason": "keine geteilte deklarierte Anschlussstelle",
            }
        )

    return {
        "title": "Automatenverbund der Anschlussfaehigkeit",
        "status": "kombinierte Pruef- und Auffuehrungsspur; keine automatische Theorieentscheidung",
        "input": {
            "marked": marked,
            "unmarked": unmarked,
            "context": context,
            "topic": topic,
        },
        "enabled_connections": enabled,
        "blocked_connections": blocked,
        "sequence": [
            {
                "stage": "unterscheiden",
                "summary": distinction_data["distinction"],
                "warnings": distinction_data.get("warnings", []),
            },
            {
                "stage": "propositional_ordnen",
                "summary": tractatus_data["propositions"][:4],
                "warnings": tractatus_data.get("warnings", []),
            },
            {
                "stage": "auffuehren",
                "summary": artwork_data["generated_score"],
                "terminal_condition": artwork_data["terminal_condition"],
            },
        ],
        "outputs": {
            "distinction": distinction_data,
            "tractatus": tractatus_data,
            "artwork": artwork_data,
        },
        "limits": [
            "Der Verbund kombiniert Automaten nur ueber ausgewiesene Anschlussbruecken.",
            "Eine blockierte Verbindung ist ein Pruefbefund, kein Fehler.",
            "Eine produktive Differenz ist ein neuer Begriff, Manuskriptanker oder Anschluss.",
            "Manuskriptintegration bleibt eine explizite editorische Operation.",
        ],
    }


def features(data: dict[str, Any]) -> dict[str, set[str]]:
    distinction = data["outputs"]["distinction"]
    tractatus = data["outputs"]["tractatus"]
    artwork = data["outputs"]["artwork"]

    concepts = (
        concept_ids(distinction.get("marked_concepts", []))
        | concept_ids(distinction.get("unmarked_concepts", []))
        | concept_ids(tractatus.get("concepts", []))
        | concept_ids(artwork.get("concepts", []))
    )
    for step in artwork.get("steps", []):
        if step.get("concept_id"):
            concepts.add(str(step["concept_id"]))

    anchors = (
        anchor_keys(distinction.get("anchors", []))
        | anchor_keys(tractatus.get("anchors", []))
        | anchor_keys(artwork.get("anchors", []))
    )
    bridges = {
        f"{connection['from']}->{connection['to']}:{bridge}"
        for connection in data.get("enabled_connections", [])
        for bridge in connection.get("bridges", [])
    }
    return {"concepts": concepts, "anchors": anchors, "bridges": bridges}


def load_state(path: Path) -> dict[str, set[str]]:
    if not path.exists():
        return {"concepts": set(), "anchors": set(), "bridges": set(), "inputs": set()}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {
        "concepts": set(raw.get("concepts", [])),
        "anchors": set(raw.get("anchors", [])),
        "bridges": set(raw.get("bridges", [])),
        "inputs": set(raw.get("inputs", [])),
    }


def save_state(path: Path, state: dict[str, set[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {key: sorted(values) for key, values in state.items()}
    path.write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def input_key(marked: str, unmarked: str, context: str) -> str:
    return json.dumps([marked, unmarked, context], ensure_ascii=False)


def next_inputs(data: dict[str, Any], context: str) -> list[tuple[str, str, str]]:
    found = sorted(features(data)["concepts"])
    current = data["input"]["marked"]
    candidates: list[tuple[str, str, str]] = []
    for concept in found:
        if concept == current:
            continue
        candidates.append((concept, current, context))
    return candidates


def run_until_new(
    marked: str,
    unmarked: str,
    context: str,
    max_steps: int,
    max_runs: int,
    state_path: Path,
) -> dict[str, Any]:
    state = load_state(state_path)
    queue: deque[tuple[str, str, str]] = deque([(marked, unmarked, context)])
    trace: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None

    for run_number in range(1, max_runs + 1):
        while queue:
            candidate = queue.popleft()
            key = input_key(*candidate)
            if key not in state["inputs"]:
                break
        else:
            break

        data = combine(*candidate, max_steps=max_steps)
        current = features(data)
        novelty = {
            name: sorted(current[name] - state[name])
            for name in ("concepts", "anchors", "bridges")
        }
        productive = any(novelty.values()) and bool(trace)

        trace.append(
            {
                "run": run_number,
                "input": data["input"],
                "new_concepts": novelty["concepts"],
                "new_anchors": novelty["anchors"],
                "new_bridges": novelty["bridges"],
                "productive_difference": productive,
            }
        )

        state["inputs"].add(key)
        for name in ("concepts", "anchors", "bridges"):
            state[name].update(current[name])

        for candidate_input in next_inputs(data, context):
            candidate_key = input_key(*candidate_input)
            if candidate_key not in state["inputs"]:
                queue.append(candidate_input)

        result = data
        if productive:
            break

    save_state(state_path, state)

    if result is None:
        result = combine(marked, unmarked, context, max_steps=max_steps)

    result["iterative_run"] = {
        "initial_input": {
            "marked": marked,
            "unmarked": unmarked,
            "context": context,
        },
        "terminal_input": result["input"],
        "trace": trace,
        "state_file": display_path(state_path),
        "terminal_condition": (
            "produktive Differenz gefunden"
            if trace and trace[-1]["productive_difference"]
            else "erreichbarer neuer Suchraum erschoepft oder Laufgrenze erreicht"
        ),
    }
    return result


def markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# {data['title']}",
        "",
        f"Status: {data['status']}",
        "",
        "## Eingabe",
        "",
    ]
    iterative = data.get("iterative_run")
    entry = (
        iterative.get("initial_input", data["input"])
        if iterative
        else data["input"]
    )
    lines.append(f"- markiert: {entry['marked']}")
    lines.append(f"- unmarkiert: {entry['unmarked'] or 'TODO'}")
    if entry["context"]:
        lines.append(f"- Kontext: {entry['context']}")

    if iterative:
        lines.extend(["", "## Iterativer Lauf", ""])
        for run in iterative["trace"]:
            lines.append(
                f"- Lauf {run['run']}: {run['input']['marked']} / "
                f"{run['input']['unmarked'] or 'TODO'}"
            )
            if run["new_concepts"]:
                lines.append("  - neue Begriffe: " + ", ".join(run["new_concepts"]))
            if run["new_anchors"]:
                lines.append("  - neue Manuskriptanker: " + ", ".join(run["new_anchors"][:8]))
            if run["new_bridges"]:
                lines.append("  - neue Anschluesse: " + ", ".join(run["new_bridges"][:8]))
        lines.append(f"- Abbruch: {iterative['terminal_condition']}")
        terminal = iterative.get("terminal_input", {})
        if terminal and terminal.get("marked") != entry.get("marked"):
            lines.append(
                "- terminale Eingabe: "
                f"{terminal.get('marked')} / {terminal.get('unmarked') or 'TODO'}"
            )
        lines.append(f"- Zustand: `{iterative['state_file']}`")

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
            lines.append(
                f"- `{connection['from']}` -> `{connection['to']}`: "
                f"{connection['reason']}"
            )

    lines.extend(["", "## Verbundlauf", ""])
    distinction = data["outputs"]["distinction"]
    lines.append(f"### 1. Unterscheiden: {distinction['distinction']}")
    if distinction.get("marked_concepts"):
        lines.append(
            "- Markierte Begriffsadressen: "
            + ", ".join(item["id"] for item in distinction["marked_concepts"][:6])
        )
    if distinction.get("unmarked_concepts"):
        lines.append(
            "- Unmarkierte Begriffsadressen: "
            + ", ".join(item["id"] for item in distinction["unmarked_concepts"][:6])
        )

    tractatus = data["outputs"]["tractatus"]
    lines.extend(["", "### 2. Propositional ordnen", ""])
    for proposition in tractatus["propositions"][:6]:
        lines.append(
            f"- {proposition['number']} {proposition['kind']}: {proposition['text']}"
        )

    artwork = data["outputs"]["artwork"]
    lines.extend(["", "### 3. Auffuehren / Score erzeugen", "", "```text"])
    lines.extend(artwork["generated_score"])
    lines.extend(["```", "", f"Abbruch: {artwork['terminal_condition']}"])

    lines.extend(["", "## Grenzen", ""])
    lines.extend(f"- {limit}" for limit in data["limits"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Kombiniert Codex-Automaten und verfolgt neue Anschluesse."
    )
    parser.add_argument("marked", help="markierte Seite / Startbegriff")
    parser.add_argument("unmarked", nargs="?", default="", help="unmarkierte Seite")
    parser.add_argument("--context", default="", help="Kontext oder Fragestellung")
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument("--until-new", action="store_true", help="weiterlaufen bis eine produktive Differenz entsteht")
    parser.add_argument("--max-runs", type=int, default=12, help="maximale Zahl verketteter Automatenlaeufe")
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE, help="persistenter Zustand bereits gepruefter Begriffe, Anker und Anschluesse")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    state_path = args.state_file if args.state_file.is_absolute() else ROOT / args.state_file
    if args.until_new:
        data = run_until_new(
            args.marked,
            args.unmarked,
            args.context,
            max(1, args.max_steps),
            max(1, args.max_runs),
            state_path,
        )
    else:
        data = combine(args.marked, args.unmarked, args.context, max(1, args.max_steps))

    output = (
        json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else markdown(data)
    )
    if args.output:
        target = args.output if args.output.is_absolute() else ROOT / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
