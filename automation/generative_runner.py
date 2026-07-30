#!/usr/bin/env python3
"""Autonomous theory-generation runner based on explicit connection decisions.

A request supplies only a seed and optional orientation. The runner may autonomously
create concepts, relations, distinctions, counter-movements and longer texts. Every
step is recorded as a revisable connection decision. Writes are restricted to
`generated/`; manuscript and confirmed knowledge are never modified directly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ALLOWED_TARGETS = {"essay", "chapter_seed", "continuation", "experiment", "theses", "dialogue", "theory"}
TARGET_DIRS = {
    "essay": "essays",
    "chapter_seed": "chapter-seeds",
    "continuation": "continuations",
    "experiment": "experiments",
    "theses": "experiments",
    "dialogue": "experiments",
    "theory": "theories",
}


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9äöüß]+", "-", value.lower().strip()).strip("-")
    return value[:64] or "autonome-theorie"


def load_request(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("request must be a YAML object")

    seed = str(data.get("seed", "")).strip()
    if not seed:
        fail("request.seed is required")

    mode = str(data.get("mode", "autonomous_theory_generation"))
    if mode not in {"autonomous_generative", "autonomous_theory_generation"}:
        fail("mode must be autonomous_generative or autonomous_theory_generation")

    target = str(data.get("target", "theory"))
    if target not in ALLOWED_TARGETS:
        fail(f"target must be one of {sorted(ALLOWED_TARGETS)}")

    max_cycles = int(data.get("max_cycles", data.get("max_passes", 5)))
    if not 1 <= max_cycles <= 12:
        fail("max_cycles must be between 1 and 12")

    return {
        "seed": seed,
        "mode": mode,
        "target": target,
        "max_cycles": max_cycles,
        "title": str(data.get("title", "")).strip(),
        "orientation": str(data.get("orientation", data.get("instructions", ""))).strip(),
        "start_review_after_generation": bool(data.get("start_review_after_generation", True)),
        "source_context": list(data.get("source_context", [])),
        "allow_new_concepts": bool(data.get("allow_new_concepts", True)),
        "allow_divergence": bool(data.get("allow_divergence", True)),
        "minimum_productive_decisions": int(data.get("minimum_productive_decisions", 3)),
    }


def api_call(messages: list[dict[str, str]], *, endpoint: str, model: str, api_key: str, temperature: float = 0.9) -> str:
    url = endpoint.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    payload = json.dumps({"model": model, "messages": messages, "temperature": temperature}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        fail(f"model endpoint returned HTTP {exc.code}: {details[:500]}")
    except urllib.error.URLError as exc:
        fail(f"could not reach model endpoint: {exc}")
    try:
        return str(body["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError):
        fail("model endpoint returned an unexpected response")


def parse_json_response(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            fail("theory cycle did not return valid JSON")
        data = json.loads(match.group(0))
    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        fail("theory cycle JSON requires a text field")
    return data


def system_prompt(config: dict[str, Any]) -> str:
    permissions = []
    if config["allow_new_concepts"]:
        permissions.append("Du darfst neue Begriffe und Unterscheidungen einführen.")
    if config["allow_divergence"]:
        permissions.append("Du darfst vom Ausgangsanschluss abweichen, wenn daraus eine stärkere theoretische Linie entsteht.")
    return f"""Du erzeugst autonom eine philosophische Theorie durch Anschlussentscheidungen.
Der Anfang ist kein Dogma, sondern die erste Bedingung eines rekursiven Prozesses.
In jedem Zyklus entscheidest du selbst, welche mögliche Fortsetzung theoretisch am produktivsten ist.
Du darfst Relationen setzen, Begriffe funktional bestimmen, Gegenbewegungen erzeugen, frühere Entscheidungen revidieren und lokale Widersprüche als produktive Spannungen bewahren.
{chr(10).join(permissions)}
Eine Anschlussentscheidung ist gut, wenn sie neue Erklärungs- oder Unterscheidungskraft erzeugt, nicht bloß sprachlich plausibel klingt.
Kein Ergebnis gilt automatisch als bestätigte Theorie. Alle Entscheidungen bleiben revidierbar.
Antworte ausschließlich als JSON-Objekt mit diesen Feldern:
- text: vollständiger aktueller Theorietext
- chosen_connection: kurze Beschreibung der gewählten Anschlussentscheidung
- alternatives_rejected: Liste verworfener möglicher Anschlüsse
- new_concepts: Liste neu eingeführter Begriffe
- new_relations: Liste von Objekten mit from, relation, to
- productive_difference: der Erkenntnisgewinn dieses Zyklus
- revisions: Liste revidierter früherer Entscheidungen
- tensions_preserved: Liste bewusst offengehaltener Spannungen
- continue: Boolean, ob ein weiterer Zyklus voraussichtlich produktiv ist
"""


def run_theory_cycles(config: dict[str, Any], endpoint: str, model: str, api_key: str) -> tuple[str, list[dict[str, Any]]]:
    current = ""
    decisions: list[dict[str, Any]] = []

    for cycle in range(1, config["max_cycles"] + 1):
        if cycle == 1:
            task = f"""ANFANG:
{config['seed']}

ORIENTIERUNG:
{config['orientation'] or 'keine äußere Vorgabe'}

Erzeuge einen ersten zusammenhängenden Theorieentwurf. Wähle selbst den produktivsten Anschluss und begründe ihn im JSON-Protokoll."""
        else:
            history = json.dumps(decisions[-3:], ensure_ascii=False, indent=2)
            task = f"""Setze die Theorie in einem neuen autonomen Zyklus fort.
Wähle nicht automatisch die naheliegendste Fortsetzung. Vergleiche Alternativen und entscheide nach theoretischer Produktivität.
Du darfst den bisherigen Text stark reorganisieren, Begriffe verwerfen oder eine neue Ebene einführen.

BISHERIGER TEXT:
{current}

LETZTE ANSCHLUSSENTSCHEIDUNGEN:
{history}"""

        result = parse_json_response(api_call(
            [
                {"role": "system", "content": system_prompt(config)},
                {"role": "user", "content": task},
            ],
            endpoint=endpoint,
            model=model,
            api_key=api_key,
        ))
        current = result["text"].strip()
        decision = {
            "cycle": cycle,
            "chosen_connection": result.get("chosen_connection"),
            "alternatives_rejected": result.get("alternatives_rejected", []),
            "new_concepts": result.get("new_concepts", []),
            "new_relations": result.get("new_relations", []),
            "productive_difference": result.get("productive_difference"),
            "revisions": result.get("revisions", []),
            "tensions_preserved": result.get("tensions_preserved", []),
            "continue": bool(result.get("continue", True)),
        }
        decisions.append(decision)

        productive_count = sum(bool(item.get("productive_difference")) for item in decisions)
        if not decision["continue"] and productive_count >= config["minimum_productive_decisions"]:
            break

    return current, decisions


def optional_review(text: str, decisions: list[dict[str, Any]], config: dict[str, Any], endpoint: str, model: str, api_key: str) -> str | None:
    if not config["start_review_after_generation"]:
        return None
    prompt = f"""Prüfe diese autonom erzeugte Theorie und ihre Anschlussentscheidungen.
Bewerte nicht primär Stil, sondern:
1. ob die Entscheidungen tatsächliche theoretische Unterschiede erzeugen,
2. ob Begriffe funktional bestimmt sind,
3. ob Relationen zirkulär oder bloß assoziativ bleiben,
4. welche stärksten Gegenmodelle bestehen,
5. welche Teile als proposal weitergeführt werden können,
6. welche Entscheidungen revidiert werden sollten.
Gib keine pauschale Bestätigung.

THEORIETEXT:
{text}

ENTSCHEIDUNGSPROTOKOLL:
{json.dumps(decisions, ensure_ascii=False, indent=2)}"""
    return api_call(
        [{"role": "system", "content": "Du bist der kritische Prüfmodus einer autonomen Theoriegenese."}, {"role": "user", "content": prompt}],
        endpoint=endpoint,
        model=model,
        api_key=api_key,
        temperature=0.3,
    )


def write_outputs(config: dict[str, Any], text: str, decisions: list[dict[str, Any]], review: str | None, request_path: Path) -> list[Path]:
    title = config["title"] or config["seed"].splitlines()[0][:72]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    directory = Path("generated") / TARGET_DIRS[config["target"]]
    directory.mkdir(parents=True, exist_ok=True)
    base = f"{stamp}-{slugify(title)}"
    text_path = directory / f"{base}.md"
    record_path = directory / f"{base}.yaml"
    graph_path = directory / f"{base}-graph.yaml"

    header = {
        "mode": "autonomous_theory_generation",
        "status": "generated",
        "seed": config["seed"],
        "created_by": "generative_runner",
        "model": os.environ.get("GENERATIVE_MODEL", "unknown"),
        "cycles": len(decisions),
        "source_context": config["source_context"],
        "next_possible_steps": ["critical_review", "revise_connections", "promote_selected_relations_to_proposal"],
    }
    text_path.write_text(
        "---\n" + yaml.safe_dump(header, allow_unicode=True, sort_keys=False).strip() + "\n---\n\n" + text.strip() + "\n",
        encoding="utf-8",
    )

    all_concepts = sorted({str(c) for d in decisions for c in d.get("new_concepts", []) if c})
    all_relations = [r for d in decisions for r in d.get("new_relations", []) if isinstance(r, dict)]
    graph_path.write_text(yaml.safe_dump({
        "status": "generated",
        "seed": config["seed"],
        "concepts": all_concepts,
        "relations": all_relations,
        "connection_decisions": decisions,
    }, allow_unicode=True, sort_keys=False), encoding="utf-8")

    record_path.write_text(yaml.safe_dump({
        **header,
        "request_file": str(request_path),
        "target": config["target"],
        "max_cycles": config["max_cycles"],
        "connection_decisions": decisions,
        "review_started": review is not None,
        "review": review,
        "output_file": str(text_path),
        "graph_file": str(graph_path),
    }, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return [text_path, graph_path, record_path]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    config = load_request(args.request)
    if args.validate_only:
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return

    endpoint = os.environ.get("GENERATIVE_API_ENDPOINT", "").strip()
    model = os.environ.get("GENERATIVE_MODEL", "").strip()
    api_key = os.environ.get("GENERATIVE_API_KEY", "").strip()
    if not endpoint or not model or not api_key:
        fail("GENERATIVE_API_ENDPOINT, GENERATIVE_MODEL and GENERATIVE_API_KEY are required")

    text, decisions = run_theory_cycles(config, endpoint, model, api_key)
    review = optional_review(text, decisions, config, endpoint, model, api_key)
    print("\n".join(str(path) for path in write_outputs(config, text, decisions, review, args.request)))


if __name__ == "__main__":
    main()
