#!/usr/bin/env python3
"""Autonomous theory generation with revisable connection rules.

The runner develops both a theory and the method by which theoretical
connections are selected. Every content decision and every change of heuristic
is recorded. Writes remain restricted to generated/.
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
    "essay": "essays", "chapter_seed": "chapter-seeds", "continuation": "continuations",
    "experiment": "experiments", "theses": "experiments", "dialogue": "experiments", "theory": "theories",
}
DEFAULT_STYLES = {
    "conservative": "Bevorzuge wenige neue Begriffe, hohe Anschlusskontinuität und explizite Konsistenz.",
    "exploratory": "Bevorzuge unerwartete, aber funktional erklärungskräftige neue Relationen.",
    "dialectical": "Suche produktive Widersprüche und entwickle Begriffe aus ihrer Spannung.",
    "genealogical": "Frage nach Entstehungsbedingungen, Verschiebungen und historischen Abhängigkeiten.",
    "aesthetic": "Bevorzuge einfache, elegante und formbildende theoretische Strukturen.",
    "pragmatic": "Bewerte Begriffe nach Erklärungskraft, Folgen und möglichen Anwendungen.",
}


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def slugify(value: str) -> str:
    return (re.sub(r"[^a-z0-9äöüß]+", "-", value.lower().strip()).strip("-")[:64] or "autonome-theorie")


def load_request(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("request must be a YAML object")
    seed = str(data.get("seed", "")).strip()
    if not seed:
        fail("request.seed is required")
    mode = str(data.get("mode", "autonomous_theory_generation"))
    if mode not in {"autonomous_generative", "autonomous_theory_generation"}:
        fail("unsupported mode")
    target = str(data.get("target", "theory"))
    if target not in ALLOWED_TARGETS:
        fail(f"target must be one of {sorted(ALLOWED_TARGETS)}")
    max_cycles = int(data.get("max_cycles", data.get("max_passes", 6)))
    if not 1 <= max_cycles <= 16:
        fail("max_cycles must be between 1 and 16")
    styles = list(data.get("epistemic_styles", ["exploratory", "dialectical", "conservative"]))
    unknown = [s for s in styles if s not in DEFAULT_STYLES]
    if unknown:
        fail(f"unknown epistemic styles: {unknown}")
    return {
        "seed": seed, "mode": mode, "target": target, "max_cycles": max_cycles,
        "title": str(data.get("title", "")).strip(),
        "orientation": str(data.get("orientation", data.get("instructions", ""))).strip(),
        "start_review_after_generation": bool(data.get("start_review_after_generation", True)),
        "source_context": list(data.get("source_context", [])),
        "allow_new_concepts": bool(data.get("allow_new_concepts", True)),
        "allow_divergence": bool(data.get("allow_divergence", True)),
        "minimum_productive_decisions": int(data.get("minimum_productive_decisions", 3)),
        "meta_agent": bool(data.get("meta_agent", True)),
        "meta_interval": max(1, int(data.get("meta_interval", 2))),
        "epistemic_styles": styles,
        "initial_heuristic": str(data.get("initial_heuristic", "Bevorzuge Anschlüsse mit neuer Unterscheidungs- oder Erklärungskraft.")),
    }


def api_call(messages: list[dict[str, str]], *, endpoint: str, model: str, api_key: str, temperature: float = 0.9) -> str:
    url = endpoint.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    payload = json.dumps({"model": model, "messages": messages, "temperature": temperature}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        fail(f"model endpoint returned HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:500]}")
    except urllib.error.URLError as exc:
        fail(f"could not reach model endpoint: {exc}")
    try:
        return str(body["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError):
        fail("model endpoint returned an unexpected response")


def parse_json_response(raw: str, required: str = "text") -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            fail("agent did not return valid JSON")
        data = json.loads(match.group(0))
    if not isinstance(data, dict) or required not in data:
        fail(f"agent JSON requires field {required}")
    return data


def theory_prompt(config: dict[str, Any], heuristic: str, style: str) -> str:
    permissions = []
    if config["allow_new_concepts"]:
        permissions.append("Du darfst neue Begriffe und Unterscheidungen einführen.")
    if config["allow_divergence"]:
        permissions.append("Du darfst vom Anfang abweichen, wenn eine stärkere theoretische Linie entsteht.")
    return f"""Du erzeugst autonom eine philosophische Theorie durch Anschlussentscheidungen.
Der Anfang ist kein Dogma, sondern die erste Bedingung eines rekursiven Prozesses.
Aktuelle Anschlussheuristik: {heuristic}
Aktueller Erkenntnisstil ({style}): {DEFAULT_STYLES[style]}
{chr(10).join(permissions)}
Wähle mehrere reale Alternativen und entscheide nach theoretischer Produktivität. Eine Entscheidung ist produktiv, wenn sie neue Erklärungs-, Unterscheidungs- oder Reorganisationskraft erzeugt.
Antworte ausschließlich als JSON mit:
text, chosen_connection, alternatives_rejected, new_concepts, new_relations,
productive_difference, revisions, tensions_preserved, heuristic_effect, continue.
new_relations ist eine Liste von Objekten mit from, relation, to."""


def meta_prompt(styles: list[str]) -> str:
    style_text = "\n".join(f"- {s}: {DEFAULT_STYLES[s]}" for s in styles)
    return f"""Du bist der Meta-Anschluss-Agent. Du schreibst nicht die Theorie selbst, sondern prüfst und veränderst gegebenenfalls ihre Erkenntnismethode.
Verfügbare Erkenntnisstile:
{style_text}
Eine Regeländerung ist nur zulässig, wenn bisherige Entscheidungen Wiederholung, blinde Flecken, Scheinkohärenz oder unproduktive Drift zeigen. Bewahre Kontinuität, wenn keine Änderung nötig ist.
Antworte ausschließlich als JSON mit:
assessment, current_rule_limit, proposed_heuristic, selected_style, reason,
alternatives_rejected, expected_gain, expected_risk, change_rule."""


def run_meta_agent(config: dict[str, Any], heuristic: str, style: str, text: str, decisions: list[dict[str, Any]], endpoint: str, model: str, api_key: str) -> dict[str, Any]:
    prompt = f"""AKTUELLE HEURISTIK: {heuristic}
AKTUELLER STIL: {style}
THEORIETEXT: {text}
LETZTE ENTSCHEIDUNGEN:
{json.dumps(decisions[-4:], ensure_ascii=False, indent=2)}
Prüfe, ob die Anschlussregel beibehalten oder begründet verändert werden soll."""
    result = parse_json_response(api_call([
        {"role": "system", "content": meta_prompt(config["epistemic_styles"])},
        {"role": "user", "content": prompt},
    ], endpoint=endpoint, model=model, api_key=api_key, temperature=0.35), required="change_rule")
    selected_style = str(result.get("selected_style", style))
    if selected_style not in config["epistemic_styles"]:
        selected_style = style
    proposed = str(result.get("proposed_heuristic", heuristic)).strip() or heuristic
    changed = bool(result.get("change_rule", False)) and (proposed != heuristic or selected_style != style)
    return {
        "assessment": result.get("assessment"),
        "current_rule_limit": result.get("current_rule_limit"),
        "previous_heuristic": heuristic,
        "proposed_heuristic": proposed,
        "previous_style": style,
        "selected_style": selected_style,
        "reason": result.get("reason"),
        "alternatives_rejected": result.get("alternatives_rejected", []),
        "expected_gain": result.get("expected_gain"),
        "expected_risk": result.get("expected_risk"),
        "change_rule": changed,
    }


def run_theory_cycles(config: dict[str, Any], endpoint: str, model: str, api_key: str) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    current = ""
    decisions: list[dict[str, Any]] = []
    meta_decisions: list[dict[str, Any]] = []
    heuristic = config["initial_heuristic"]
    style = config["epistemic_styles"][0]

    for cycle in range(1, config["max_cycles"] + 1):
        if cycle > 1 and config["meta_agent"] and (cycle - 1) % config["meta_interval"] == 0:
            meta = run_meta_agent(config, heuristic, style, current, decisions, endpoint, model, api_key)
            meta["before_cycle"] = cycle
            meta_decisions.append(meta)
            if meta["change_rule"]:
                heuristic = meta["proposed_heuristic"]
                style = meta["selected_style"]

        if cycle == 1:
            task = f"""ANFANG:\n{config['seed']}\n\nORIENTIERUNG:\n{config['orientation'] or 'keine äußere Vorgabe'}\nErzeuge einen ersten Theorieentwurf und protokolliere die gewählte Anschlussentscheidung."""
        else:
            task = f"""Setze die Theorie autonom fort. Du darfst sie stark reorganisieren und frühere Entscheidungen revidieren.
BISHERIGER TEXT:\n{current}
LETZTE ENTSCHEIDUNGEN:\n{json.dumps(decisions[-3:], ensure_ascii=False, indent=2)}"""
        result = parse_json_response(api_call([
            {"role": "system", "content": theory_prompt(config, heuristic, style)},
            {"role": "user", "content": task},
        ], endpoint=endpoint, model=model, api_key=api_key))
        current = str(result["text"]).strip()
        decision = {
            "cycle": cycle, "heuristic_version": len(meta_decisions) + 1,
            "heuristic": heuristic, "epistemic_style": style,
            "chosen_connection": result.get("chosen_connection"),
            "alternatives_rejected": result.get("alternatives_rejected", []),
            "new_concepts": result.get("new_concepts", []), "new_relations": result.get("new_relations", []),
            "productive_difference": result.get("productive_difference"), "revisions": result.get("revisions", []),
            "tensions_preserved": result.get("tensions_preserved", []), "heuristic_effect": result.get("heuristic_effect"),
            "continue": bool(result.get("continue", True)),
        }
        decisions.append(decision)
        productive_count = sum(bool(item.get("productive_difference")) for item in decisions)
        if not decision["continue"] and productive_count >= config["minimum_productive_decisions"]:
            break
    return current, decisions, meta_decisions


def optional_review(text: str, decisions: list[dict[str, Any]], meta_decisions: list[dict[str, Any]], config: dict[str, Any], endpoint: str, model: str, api_key: str) -> str | None:
    if not config["start_review_after_generation"]:
        return None
    prompt = f"""Prüfe Theorie, Anschlussentscheidungen und Methodenänderungen. Bewerte Erkenntnisgewinn, Scheinkohärenz, Drift, Gegenmodelle und ob Regeländerungen begründet waren. Gib keine pauschale Bestätigung.
THEORIE:\n{text}
ANSCHLUSSENTSCHEIDUNGEN:\n{json.dumps(decisions, ensure_ascii=False, indent=2)}
META-ENTSCHEIDUNGEN:\n{json.dumps(meta_decisions, ensure_ascii=False, indent=2)}"""
    return api_call([{"role": "system", "content": "Du bist der kritische Prüfmodus."}, {"role": "user", "content": prompt}], endpoint=endpoint, model=model, api_key=api_key, temperature=0.25)


def write_outputs(config: dict[str, Any], text: str, decisions: list[dict[str, Any]], meta_decisions: list[dict[str, Any]], review: str | None, request_path: Path) -> list[Path]:
    title = config["title"] or config["seed"].splitlines()[0][:72]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    directory = Path("generated") / TARGET_DIRS[config["target"]]
    directory.mkdir(parents=True, exist_ok=True)
    base = f"{stamp}-{slugify(title)}"
    text_path, graph_path = directory / f"{base}.md", directory / f"{base}-graph.yaml"
    record_path, method_path = directory / f"{base}.yaml", directory / f"{base}-method.yaml"
    header = {
        "mode": "autonomous_theory_generation", "status": "generated", "seed": config["seed"],
        "created_by": "generative_runner_with_meta_agent", "model": os.environ.get("GENERATIVE_MODEL", "unknown"),
        "cycles": len(decisions), "method_revisions": sum(bool(m.get("change_rule")) for m in meta_decisions),
        "source_context": config["source_context"],
        "next_possible_steps": ["critical_review", "compare_epistemic_styles", "revise_connections", "promote_selected_relations_to_proposal"],
    }
    text_path.write_text("---\n" + yaml.safe_dump(header, allow_unicode=True, sort_keys=False).strip() + "\n---\n\n" + text.strip() + "\n", encoding="utf-8")
    concepts = sorted({str(c) for d in decisions for c in d.get("new_concepts", []) if c})
    relations = [r for d in decisions for r in d.get("new_relations", []) if isinstance(r, dict)]
    graph_path.write_text(yaml.safe_dump({"status": "generated", "seed": config["seed"], "concepts": concepts, "relations": relations, "connection_decisions": decisions}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    method_path.write_text(yaml.safe_dump({"status": "generated", "initial_heuristic": config["initial_heuristic"], "available_styles": config["epistemic_styles"], "meta_decisions": meta_decisions}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    record_path.write_text(yaml.safe_dump({**header, "request_file": str(request_path), "target": config["target"], "max_cycles": config["max_cycles"], "connection_decisions": decisions, "meta_decisions": meta_decisions, "review_started": review is not None, "review": review, "output_file": str(text_path), "graph_file": str(graph_path), "method_file": str(method_path)}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return [text_path, graph_path, method_path, record_path]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    config = load_request(args.request)
    if args.validate_only:
        print(json.dumps(config, ensure_ascii=False, indent=2)); return
    endpoint = os.environ.get("GENERATIVE_API_ENDPOINT", "").strip()
    model = os.environ.get("GENERATIVE_MODEL", "").strip()
    api_key = os.environ.get("GENERATIVE_API_KEY", "").strip()
    if not endpoint or not model or not api_key:
        fail("GENERATIVE_API_ENDPOINT, GENERATIVE_MODEL and GENERATIVE_API_KEY are required")
    text, decisions, meta_decisions = run_theory_cycles(config, endpoint, model, api_key)
    review = optional_review(text, decisions, meta_decisions, config, endpoint, model, api_key)
    print("\n".join(str(p) for p in write_outputs(config, text, decisions, meta_decisions, review, args.request)))


if __name__ == "__main__":
    main()
