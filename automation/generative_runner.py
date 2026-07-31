#!/usr/bin/env python3
"""Autonomous theory generation with revisable connection rules.

The runner develops both a theory and the method by which theoretical
connections are selected. Every content decision and every change of heuristic
is recorded. Writes remain restricted to generated/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

try:
    from automation import generative_schemas
except ModuleNotFoundError:  # direct script execution
    import generative_schemas

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

MAX_SOURCE_FILE_CHARS = 24_000
MAX_SOURCE_CONTEXT_CHARS = 64_000
PROJECT_GUARDRAILS = """Projektgrenzen:
- Generiertes Material bleibt Status generated und ist keine bestätigte Theorie.
- Bestehende Definitionen dürfen nicht stillschweigend ersetzt werden.
- Neue Grundbegriffe, Grundthesen und Theorieachsen sind ausdrücklich als Vorschläge zu markieren.
- Programm und Algorithmus bleiben eigenständige Begriffe.
- Montage ist ein epistemisches Modell und nicht bloß ein Beispiel.
- Unsicherheiten und unbelegte Quellenbehauptungen bleiben offen."""

PROJECT_BINDING_FILES = ("CONSTITUTION.md", "PROJECT.md", "GLOSSAR.md")
MAX_REPAIR_ATTEMPTS = 2



def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def slugify(value: str) -> str:
    return (re.sub(r"[^a-z0-9äöüß]+", "-", value.lower().strip()).strip("-")[:64] or "autonome-theorie")


def load_source_context(paths: list[str], root: Path | None = None) -> tuple[str, list[dict[str, Any]]]:
    root = (root or Path.cwd()).resolve()
    blocks: list[str] = []
    provenance: list[dict[str, Any]] = []
    total = 0
    for raw_path in paths:
        relative = Path(str(raw_path))
        if relative.is_absolute():
            fail(f"source_context path must be relative: {raw_path}")
        resolved = (root / relative).resolve()
        if resolved != root and root not in resolved.parents:
            fail(f"source_context path escapes repository: {raw_path}")
        if not resolved.is_file():
            fail(f"source_context file not found: {raw_path}")
        content = resolved.read_text(encoding="utf-8")
        included = content[:min(MAX_SOURCE_FILE_CHARS, MAX_SOURCE_CONTEXT_CHARS - total)]
        provenance.append({
            "path": relative.as_posix(),
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "characters": len(content),
            "included_characters": len(included),
            "truncated": len(included) < len(content),
        })
        if included:
            blocks.append(f"--- QUELLE: {relative.as_posix()} ---\n{included}")
            total += len(included)
        if total >= MAX_SOURCE_CONTEXT_CHARS:
            break
    return "\n\n".join(blocks), provenance


def load_request(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("request must be a YAML object")
    seed = data.get("seed")
    if not isinstance(seed, str) or not seed.strip():
        fail("request.seed must be a non-empty string")
    mode = data.get("mode", "autonomous_theory_generation")
    if not isinstance(mode, str) or mode not in {"autonomous_generative", "autonomous_theory_generation"}:
        fail("unsupported mode")
    target = data.get("target", "theory")
    if not isinstance(target, str) or target not in ALLOWED_TARGETS:
        fail(f"target must be one of {sorted(ALLOWED_TARGETS)}")
    try:
        max_cycles = int(data.get("max_cycles", data.get("max_passes", 6)))
        minimum_productive = int(data.get("minimum_productive_decisions", 3))
        meta_interval = int(data.get("meta_interval", 2))
    except (TypeError, ValueError):
        fail("cycle and interval fields must be integers")
    if not 1 <= max_cycles <= 16:
        fail("max_cycles must be between 1 and 16")
    if not 1 <= minimum_productive <= max_cycles:
        fail("minimum_productive_decisions must be between 1 and max_cycles")
    if not 1 <= meta_interval <= max_cycles:
        fail("meta_interval must be between 1 and max_cycles")
    styles = data.get("epistemic_styles", ["exploratory", "dialectical", "conservative"])
    if not isinstance(styles, list) or not styles or any(not isinstance(item, str) for item in styles):
        fail("epistemic_styles must be a non-empty list of strings")
    unknown = [style for style in styles if style not in DEFAULT_STYLES]
    if unknown:
        fail(f"unknown epistemic styles: {unknown}")
    source_context = data.get("source_context", [])
    if not isinstance(source_context, list) or any(not isinstance(item, str) for item in source_context):
        fail("source_context must be a list of relative path strings")
    boolean_fields = {
        "start_review_after_generation": True,
        "allow_new_concepts": True,
        "allow_divergence": True,
        "meta_agent": True,
        "compare_epistemic_styles": False,
    }
    booleans = {}
    for key, default in boolean_fields.items():
        value = data.get(key, default)
        if type(value) is not bool:
            fail(f"{key} must be a boolean")
        booleans[key] = value
    initial_heuristic = data.get(
        "initial_heuristic",
        "Bevorzuge Anschlüsse mit neuer Unterscheidungs- oder Erklärungskraft.",
    )
    if not isinstance(initial_heuristic, str) or not initial_heuristic.strip():
        fail("initial_heuristic must be a non-empty string")
    return {
        "seed": seed.strip(), "mode": mode, "target": target, "max_cycles": max_cycles,
        "title": str(data.get("title", "")).strip(),
        "orientation": str(data.get("orientation", data.get("instructions", ""))).strip(),
        "start_review_after_generation": booleans["start_review_after_generation"],
        "source_context": source_context,
        "allow_new_concepts": booleans["allow_new_concepts"],
        "allow_divergence": booleans["allow_divergence"],
        "minimum_productive_decisions": minimum_productive,
        "meta_agent": booleans["meta_agent"],
        "compare_epistemic_styles": booleans["compare_epistemic_styles"],
        "meta_interval": meta_interval,
        "epistemic_styles": styles,
        "initial_heuristic": initial_heuristic.strip(),
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


def load_project_binding_context(root: Path | None = None) -> tuple[str, list[dict[str, Any]]]:
    root = (root or Path.cwd()).resolve()
    return load_source_context(list(PROJECT_BINDING_FILES), root)


def parse_json_response(raw: str, required: str = "text") -> dict[str, Any]:
    schema = "theory" if required == "text" else "meta" if required == "change_rule" else required
    try:
        return generative_schemas.parse_and_validate(raw, schema)
    except generative_schemas.SchemaError as exc:
        fail(f"agent JSON violates {schema} schema: {exc}")


def call_structured_agent(
    messages: list[dict[str, str]],
    *,
    schema: str,
    endpoint: str,
    model: str,
    api_key: str,
    temperature: float,
) -> dict[str, Any]:
    attempts = list(messages)
    last_error = "unknown schema error"
    for repair in range(MAX_REPAIR_ATTEMPTS + 1):
        raw = api_call(
            attempts,
            endpoint=endpoint,
            model=model,
            api_key=api_key,
            temperature=temperature,
        )
        try:
            return generative_schemas.parse_and_validate(raw, schema)
        except generative_schemas.SchemaError as exc:
            last_error = str(exc)
            if repair >= MAX_REPAIR_ATTEMPTS:
                break
            attempts.extend([
                {"role": "assistant", "content": raw},
                {
                    "role": "user",
                    "content": (
                        f"Die Antwort verletzt das Schema {schema}: {exc}. "
                        "Repariere nur Struktur und Typen. Antworte mit genau einem JSON-Objekt."
                    ),
                },
            ])
    fail(f"agent JSON violates {schema} schema after repairs: {last_error}")


def verify_productivity(result: dict[str, Any], prior: list[dict[str, Any]]) -> dict[str, Any]:
    evidence: list[dict[str, str]] = []
    known_relations = {
        (item.get("from"), item.get("relation"), item.get("to"))
        for decision in prior
        for item in decision.get("new_relations", [])
        if isinstance(item, dict)
    }
    for relation in result["new_relations"]:
        key = (relation["from"], relation["relation"], relation["to"])
        if key not in known_relations:
            evidence.append({"kind": "new_relation", "detail": " | ".join(key)})
    for item in result["definition_refinements"]:
        if item["previous"].strip() != item["refined"].strip():
            evidence.append({"kind": "definition_refinement", "detail": item["concept"]})
    for item in result["countermodels"]:
        evidence.append({"kind": "countermodel", "detail": item["claim"]})
    for item in result["merged_nodes"]:
        evidence.append({"kind": "merged_nodes", "detail": item["result"]})
    for item in result["removed_categories"]:
        evidence.append({"kind": "removed_category", "detail": item["category"]})
    prior_text = json.dumps(prior, ensure_ascii=False)
    for item in result["revisions"]:
        if item["target"] in prior_text:
            evidence.append({"kind": "revision", "detail": item["target"]})
    return {
        "productive": bool(evidence),
        "evidence": evidence,
        "model_claim": result["productive_difference"],
        "independent_rule": "structured_novelty_v1",
    }


def update_binding_matrix(
    previous: dict[str, list[str]], result: dict[str, Any]
) -> dict[str, list[str]]:
    matrix = {key: list(value) for key, value in previous.items()}
    mapping = {
        "preserved_definitions": "preserved_definitions",
        "claims_in_tension": "claims_in_tension",
        "departures_from_sources": "departures_from_sources",
        "unresolved_source_conflicts": "unresolved_source_conflicts",
        "open_objections": "open_objections",
    }
    for target, source in mapping.items():
        matrix[target] = list(dict.fromkeys(matrix.get(target, []) + result[source]))
    return matrix


def theory_prompt(config: dict[str, Any], heuristic: str, style: str) -> str:
    permissions = []
    if config["allow_new_concepts"]:
        permissions.append("Du darfst neue Begriffe und Unterscheidungen als Vorschläge einführen.")
    if config["allow_divergence"]:
        permissions.append("Du darfst vom Anfang abweichen, wenn du die Abweichung vom Quellenstand markierst.")
    return f"""Du erzeugst autonom philosophisches Werkstattmaterial durch Anschlussentscheidungen.
Der Anfang ist kein Dogma, sondern die erste Bedingung eines rekursiven Prozesses.
{PROJECT_GUARDRAILS}
VERBINDLICHER PROJEKTKONTEXT:
{config['project_binding_text']}
Aktuelle Anschlussheuristik: {heuristic}
Aktueller Erkenntnisstil ({style}): {DEFAULT_STYLES[style]}
{chr(10).join(permissions)}
Wähle mehrere reale Alternativen. Behaupte Produktivität nicht als erwiesen; ein separater Prüfer zählt nur strukturierte Evidenz.
Antworte ausschließlich als JSON mit:
text, chosen_connection, alternatives_rejected, new_concepts, new_relations,
definition_refinements, countermodels, merged_nodes, removed_categories,
productive_difference, revisions, tensions_preserved, heuristic_effect, continue,
preserved_definitions, claims_in_tension, departures_from_sources,
unresolved_source_conflicts, open_objections.
new_relations enthält Objekte mit from, relation, to. revisions enthält target und reason.
Definitionen, Gegenmodelle, Zusammenführungen und Entfernungen verwenden die im Schema verlangten Objektfelder."""


def meta_prompt(config: dict[str, Any]) -> str:
    style_text = "\n".join(f"- {s}: {DEFAULT_STYLES[s]}" for s in config["epistemic_styles"])
    return f"""Du bist der Meta-Anschluss-Agent. Du prüfst die Erkenntnismethode, bestätigst aber keine Theorie.
{PROJECT_GUARDRAILS}
VERFASSUNG, PROJEKT UND BESTÄTIGTE DEFINITIONEN:
{config['project_binding_text']}
VERFÜGBARE ERKENNTNISSTILE:
{style_text}
Eine Regeländerung ist nur zulässig, wenn Wiederholung, blinde Flecken, Scheinkohärenz oder Drift nachweisbar sind. Sie darf keine geschützte Projektrelation gefährden und keine offene Autorenentscheidung vorwegnehmen.
Antworte ausschließlich als JSON mit:
assessment, current_rule_limit, proposed_heuristic, selected_style, reason,
alternatives_rejected, expected_gain, expected_risk, change_rule,
constitutional_compatibility (exactly compatible, incompatible or uncertain), project_relations_preserved,
project_relations_endangered, requires_author_decision."""


def run_meta_agent(config: dict[str, Any], heuristic: str, style: str, text: str, decisions: list[dict[str, Any]], endpoint: str, model: str, api_key: str) -> dict[str, Any]:
    binding_matrix = decisions[-1]["binding_matrix"] if decisions else config["initial_binding_matrix"]
    prompt = f"""AKTUELLE HEURISTIK: {heuristic}
AKTUELLER STIL: {style}
THEORIETEXT: {text}
QUELLENPROVENIENZ:
{json.dumps(config['source_provenance'], ensure_ascii=False, indent=2)}
DEKLARIERTER QUELLENKONTEXT:
{config['source_context_text'] or 'kein deklarierter Quellenkontext'}
AKTUELLE BINDUNGSMATRIX:
{json.dumps(binding_matrix, ensure_ascii=False, indent=2)}
LETZTE ENTSCHEIDUNGEN:
{json.dumps(decisions[-4:], ensure_ascii=False, indent=2)}
Prüfe, ob die Anschlussregel beibehalten oder begründet verändert werden soll."""
    result = call_structured_agent(
        [
            {"role": "system", "content": meta_prompt(config)},
            {"role": "user", "content": prompt},
        ],
        schema="meta",
        endpoint=endpoint,
        model=model,
        api_key=api_key,
        temperature=0.35,
    )
    selected_style = result["selected_style"]
    if selected_style not in config["epistemic_styles"]:
        fail(f"meta agent selected unknown epistemic style: {selected_style}")
    proposed = result["proposed_heuristic"].strip() or heuristic
    blocked_reasons = []
    if result["project_relations_endangered"]:
        blocked_reasons.append("project_relations_endangered")
    if result["requires_author_decision"]:
        blocked_reasons.append("requires_author_decision")
    compatibility = result["constitutional_compatibility"].strip().lower()
    if compatibility not in {"compatible", "vereinbar", "preserved"}:
        blocked_reasons.append("constitutional_incompatibility")
    changed = (
        result["change_rule"]
        and not blocked_reasons
        and (proposed != heuristic or selected_style != style)
    )
    return {
        "assessment": result["assessment"],
        "current_rule_limit": result["current_rule_limit"],
        "previous_heuristic": heuristic,
        "proposed_heuristic": proposed,
        "previous_style": style,
        "selected_style": selected_style,
        "reason": result["reason"],
        "alternatives_rejected": result["alternatives_rejected"],
        "expected_gain": result["expected_gain"],
        "expected_risk": result["expected_risk"],
        "constitutional_compatibility": result["constitutional_compatibility"],
        "project_relations_preserved": result["project_relations_preserved"],
        "project_relations_endangered": result["project_relations_endangered"],
        "requires_author_decision": result["requires_author_decision"],
        "change_blocked_reasons": blocked_reasons,
        "change_rule": changed,
    }


def run_theory_cycles(config: dict[str, Any], endpoint: str, model: str, api_key: str) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    current = ""
    decisions: list[dict[str, Any]] = []
    meta_decisions: list[dict[str, Any]] = []
    heuristic = config["initial_heuristic"]
    style = config.get("initial_style", config["epistemic_styles"][0])
    if style not in config["epistemic_styles"]:
        fail(f"unknown initial epistemic style: {style}")
    heuristic_version = 1
    binding_matrix = config["initial_binding_matrix"]

    for cycle in range(1, config["max_cycles"] + 1):
        if cycle > 1 and config["meta_agent"] and (cycle - 1) % config["meta_interval"] == 0:
            meta = run_meta_agent(config, heuristic, style, current, decisions, endpoint, model, api_key)
            meta["before_cycle"] = cycle
            meta_decisions.append(meta)
            if meta["change_rule"]:
                heuristic = meta["proposed_heuristic"]
                style = meta["selected_style"]
                heuristic_version += 1

        if cycle == 1:
            task = f"""ANFANG:
{config['seed']}

ORIENTIERUNG:
{config['orientation'] or 'keine äußere Vorgabe'}

DEKLARIERTER QUELLENKONTEXT:
{config['source_context_text'] or 'kein deklarierter Quellenkontext'}

QUELLENPROVENIENZ:
{json.dumps(config['source_provenance'], ensure_ascii=False, indent=2)}

BINDUNGSMATRIX:
{json.dumps(binding_matrix, ensure_ascii=False, indent=2)}

Behandle den Quellenkontext als bestehenden Projektstand, nicht pauschal als bestätigte Wahrheit. Markiere Abweichungen und neue Setzungen."""
        else:
            task = f"""Setze das generierte Werkstattmaterial fort. Reorganisation und Revision müssen ihre Projekt- und Quellenfolgen ausweisen.
BISHERIGER TEXT:
{current}
QUELLENPROVENIENZ:
{json.dumps(config['source_provenance'], ensure_ascii=False, indent=2)}
AKTUELLE BINDUNGSMATRIX:
{json.dumps(binding_matrix, ensure_ascii=False, indent=2)}
LETZTE ENTSCHEIDUNGEN:
{json.dumps(decisions[-3:], ensure_ascii=False, indent=2)}"""
        result = call_structured_agent(
            [
                {"role": "system", "content": theory_prompt(config, heuristic, style)},
                {"role": "user", "content": task},
            ],
            schema="theory",
            endpoint=endpoint,
            model=model,
            api_key=api_key,
            temperature=0.9,
        )
        current = result["text"].strip()
        verification = verify_productivity(result, decisions)
        binding_matrix = update_binding_matrix(binding_matrix, result)
        decision = {
            "cycle": cycle,
            "heuristic_version": heuristic_version,
            "heuristic": heuristic,
            "epistemic_style": style,
            "chosen_connection": result["chosen_connection"],
            "alternatives_rejected": result["alternatives_rejected"],
            "new_concepts": result["new_concepts"],
            "new_relations": result["new_relations"],
            "definition_refinements": result["definition_refinements"],
            "countermodels": result["countermodels"],
            "merged_nodes": result["merged_nodes"],
            "removed_categories": result["removed_categories"],
            "productive_difference": result["productive_difference"],
            "productivity_verification": verification,
            "revisions": result["revisions"],
            "tensions_preserved": result["tensions_preserved"],
            "heuristic_effect": result["heuristic_effect"],
            "binding_matrix": binding_matrix,
            "continue": result["continue"],
        }
        decisions.append(decision)
        productive_count = sum(
            bool(item["productivity_verification"]["productive"])
            for item in decisions
        )
        if not decision["continue"] and productive_count >= config["minimum_productive_decisions"]:
            break
    return current, decisions, meta_decisions


def optional_review(text: str, decisions: list[dict[str, Any]], meta_decisions: list[dict[str, Any]], config: dict[str, Any], endpoint: str, model: str, api_key: str) -> str | None:
    if not config["start_review_after_generation"]:
        return None
    prompt = f"""Prüfe Theorie, Anschlussentscheidungen und Methodenänderungen. Bewerte Erkenntnisgewinn, Scheinkohärenz, Drift, Gegenmodelle und ob Regeländerungen begründet waren. Gib keine pauschale Bestätigung.
PROJEKTGRENZEN:\n{PROJECT_GUARDRAILS}
DEKLARIERTER QUELLENKONTEXT:\n{config['source_context_text'] or 'keiner'}
THEORIE:\n{text}
ANSCHLUSSENTSCHEIDUNGEN:\n{json.dumps(decisions, ensure_ascii=False, indent=2)}
META-ENTSCHEIDUNGEN:\n{json.dumps(meta_decisions, ensure_ascii=False, indent=2)}"""
    return api_call([{"role": "system", "content": "Du bist der kritische Prüfmodus."}, {"role": "user", "content": prompt}], endpoint=endpoint, model=model, api_key=api_key, temperature=0.25)


def write_outputs(config: dict[str, Any], text: str, decisions: list[dict[str, Any]], meta_decisions: list[dict[str, Any]], review: str | None, request_path: Path) -> list[Path]:
    title = config["title"] or config["seed"].splitlines()[0][:72]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    directory = Path("generated") / "active" / TARGET_DIRS[config["target"]]
    base = f"{stamp}-{slugify(title)}"
    text_path, graph_path = directory / f"{base}.md", directory / f"{base}-graph.yaml"
    record_path, method_path = directory / f"{base}.yaml", directory / f"{base}-method.yaml"
    header = {
        "mode": config["mode"], "status": "generated", "seed": config["seed"],
        "created_by": "generative_runner_with_meta_agent", "model": os.environ.get("GENERATIVE_MODEL", "unknown"),
        "cycles": len(decisions), "method_revisions": sum(bool(m.get("change_rule")) for m in meta_decisions),
        "verified_productive_cycles": sum(bool(d["productivity_verification"]["productive"]) for d in decisions),
        "source_context": config["source_context"],
        "source_provenance": config["source_provenance"],
        "project_binding_provenance": config["project_binding_provenance"],
        "binding_matrix": decisions[-1]["binding_matrix"] if decisions else config["initial_binding_matrix"],
        "next_possible_steps": ["critical_review", "compare_epistemic_styles", "revise_connections", "promote_selected_relations_to_proposal"],
    }
    concepts = sorted({str(c) for d in decisions for c in d.get("new_concepts", []) if c})
    relations = [r for d in decisions for r in d.get("new_relations", [])]
    graph_data = {
        "status": "generated", "seed": config["seed"], "concepts": concepts,
        "relations": relations, "connection_decisions": decisions,
    }
    method_data = {
        "status": "generated", "initial_heuristic": config["initial_heuristic"],
        "available_styles": config["epistemic_styles"], "meta_decisions": meta_decisions,
    }
    record_data = {
        **header, "request_file": str(request_path), "target": config["target"],
        "max_cycles": config["max_cycles"], "connection_decisions": decisions,
        "meta_decisions": meta_decisions, "review_started": review is not None,
        "review": review, "output_file": str(text_path), "graph_file": str(graph_path),
        "method_file": str(method_path),
    }
    generative_schemas.validate_theory_graph(graph_data)
    generative_schemas.validate_generation_record(record_data)
    directory.mkdir(parents=True, exist_ok=True)
    text_path.write_text("---\n" + yaml.safe_dump(header, allow_unicode=True, sort_keys=False).strip() + "\n---\n\n" + text.strip() + "\n", encoding="utf-8")
    graph_path.write_text(yaml.safe_dump(graph_data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    method_path.write_text(yaml.safe_dump(method_data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    record_path.write_text(yaml.safe_dump(record_data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return [text_path, graph_path, method_path, record_path]


def style_comparison_summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    summaries = []
    for run in runs:
        decisions = run["decisions"]
        summaries.append({
            "style": run["style"],
            "cycles": len(decisions),
            "verified_productive_cycles": sum(
                bool(item["productivity_verification"]["productive"])
                for item in decisions
            ),
            "new_relations": sum(len(item["new_relations"]) for item in decisions),
            "definition_refinements": sum(len(item["definition_refinements"]) for item in decisions),
            "countermodels": sum(len(item["countermodels"]) for item in decisions),
            "method_revisions": sum(bool(item.get("change_rule")) for item in run["meta_decisions"]),
        })
    return {
        "status": "generated_comparison",
        "selection": "none; metrics do not establish philosophical superiority",
        "runs": summaries,
    }


def write_style_comparison(config: dict[str, Any], runs: list[dict[str, Any]]) -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    title = config["title"] or config["seed"].splitlines()[0][:72]
    path = Path("generated") / "active" / "comparisons" / f"{stamp}-{slugify(title)}-comparison.yaml"
    data = {
        **style_comparison_summary(runs),
        "seed": config["seed"],
        "model": os.environ.get("GENERATIVE_MODEL", "unknown"),
        "source_provenance": config["source_provenance"],
        "project_binding_provenance": config["project_binding_provenance"],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    config = load_request(args.request)
    config["source_context_text"], config["source_provenance"] = load_source_context(config["source_context"])
    config["project_binding_text"], config["project_binding_provenance"] = load_project_binding_context()
    config["initial_binding_matrix"] = {
        "preserved_definitions": ["Anschluss", "Programm", "Algorithmus", "Montage", "Kritik", "Reorganisation"],
        "claims_in_tension": [],
        "departures_from_sources": [],
        "unresolved_source_conflicts": [],
        "open_objections": [],
    }
    if args.validate_only:
        hidden = {"source_context_text", "project_binding_text"}
        validation = {key: value for key, value in config.items() if key not in hidden}
        print(json.dumps(validation, ensure_ascii=False, indent=2)); return
    endpoint = os.environ.get("GENERATIVE_API_ENDPOINT", "").strip()
    model = os.environ.get("GENERATIVE_MODEL", "").strip()
    api_key = os.environ.get("GENERATIVE_API_KEY", "").strip()
    if not endpoint or not model or not api_key:
        fail("GENERATIVE_API_ENDPOINT, GENERATIVE_MODEL and GENERATIVE_API_KEY are required")
    if config["compare_epistemic_styles"]:
        runs = []
        paths = []
        base_title = config["title"]
        for style in config["epistemic_styles"]:
            run_config = dict(config)
            run_config["initial_style"] = style
            run_config["title"] = f"{base_title or config['seed'].splitlines()[0][:72]} [{style}]"
            text, decisions, meta_decisions = run_theory_cycles(run_config, endpoint, model, api_key)
            review = optional_review(text, decisions, meta_decisions, run_config, endpoint, model, api_key)
            paths.extend(write_outputs(run_config, text, decisions, meta_decisions, review, args.request))
            runs.append({"style": style, "decisions": decisions, "meta_decisions": meta_decisions})
        paths.append(write_style_comparison(config, runs))
        print("\n".join(str(path) for path in paths))
        return
    text, decisions, meta_decisions = run_theory_cycles(config, endpoint, model, api_key)
    review = optional_review(text, decisions, meta_decisions, config, endpoint, model, api_key)
    print("\n".join(str(path) for path in write_outputs(config, text, decisions, meta_decisions, review, args.request)))


if __name__ == "__main__":
    main()
