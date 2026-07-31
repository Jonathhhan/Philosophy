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
    from automation import artifact_bundle, generative_schemas
except ModuleNotFoundError:  # direct script execution
    import artifact_bundle
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
PROJECT_BINDING_PATH = Path("knowledge/project_binding.yaml")
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
        sampling_seed = int(data.get("sampling_seed", 0))
        style_repetitions = int(data.get("style_repetitions", 1))
        temperature = float(data.get("temperature", 0.9))
    except (TypeError, ValueError):
        fail("cycle and interval fields must be integers")
    if not 1 <= max_cycles <= 16:
        fail("max_cycles must be between 1 and 16")
    if not 1 <= minimum_productive <= max_cycles:
        fail("minimum_productive_decisions must be between 1 and max_cycles")
    if not 1 <= meta_interval <= max_cycles:
        fail("meta_interval must be between 1 and max_cycles")
    if not 1 <= style_repetitions <= 10:
        fail("style_repetitions must be between 1 and 10")
    if not 0 <= temperature <= 2:
        fail("temperature must be between 0 and 2")
    model_revision = str(data.get("model_revision", "unspecified")).strip()
    if not model_revision:
        fail("model_revision must be a non-empty string")
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
        "sampling_seed": sampling_seed, "style_repetitions": style_repetitions,
        "temperature": temperature, "model_revision": model_revision,
    }


def api_call(messages: list[dict[str, str]], *, endpoint: str, model: str, api_key: str, temperature: float = 0.9, seed: int | None = None) -> str:
    url = endpoint.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    body_payload = {"model": model, "messages": messages, "temperature": temperature}
    if seed is not None:
        body_payload["seed"] = seed
    payload = json.dumps(body_payload).encode("utf-8")
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
    text, provenance = load_source_context(list(PROJECT_BINDING_FILES), root)
    binding_text, binding_provenance = load_source_context([PROJECT_BINDING_PATH.as_posix()], root)
    binding = yaml.safe_load((root / PROJECT_BINDING_PATH).read_text(encoding="utf-8"))
    if not isinstance(binding, dict) or binding.get("schema_version") != 1:
        fail("knowledge/project_binding.yaml must use schema_version 1")
    return text + "\n\n" + binding_text, provenance + binding_provenance


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
    seed: int | None = None,
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
            seed=seed,
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


def verify_productivity(result: dict[str, Any], prior: list[dict[str, Any]], protected_concepts: set[str] | None = None) -> dict[str, Any]:
    evidence: list[dict[str, str]] = []
    protected = {item.casefold() for item in (protected_concepts or set())}
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
    relevance = []
    for relation in result["new_relations"]:
        if relation["from"].casefold() in protected or relation["to"].casefold() in protected:
            relevance.append({"kind": "protected_concept_relation", "detail": relation})
    for item in result["definition_refinements"]:
        if item["concept"].casefold() in protected:
            relevance.append({"kind": "protected_definition", "detail": item["concept"]})
    for item in result["countermodels"]:
        if any(concept in item["claim"].casefold() for concept in protected):
            relevance.append({"kind": "project_countermodel", "detail": item["claim"]})
    return {
        "novelty_verified": bool(evidence),
        "novelty_evidence": evidence,
        "project_relevance_verified": bool(relevance),
        "project_relevance_evidence": relevance,
        "philosophical_productivity_verified": False,
        "philosophical_evidence": [],
        "model_claim": result["productive_difference"],
        "verification_rule": "epistemic_levels_v1",
    }


def update_binding_matrix(previous: dict[str, list[dict[str, Any]]], result: dict[str, Any], cycle: int) -> dict[str, list[dict[str, Any]]]:
    matrix = {key: [dict(item) for item in value] for key, value in previous.items()}
    for kind in matrix:
        existing = {item["value"] for item in matrix[kind]}
        for value in result[kind]:
            if value not in existing:
                record_id = hashlib.sha256(f"{kind}:{value}".encode()).hexdigest()[:16]
                matrix[kind].append({
                    "id": record_id, "value": value,
                    "status": "open" if kind != "preserved_definitions" else "active",
                    "introduced_in_cycle": cycle, "resolved_in_cycle": None, "resolution": None,
                })
                existing.add(value)
    for update in result["binding_updates"]:
        records = matrix[update["kind"]]
        match = next((item for item in records if item["id"] == update["id"]), None)
        if update["action"] == "add":
            if match is not None:
                fail(f"binding id already exists: {update['id']}")
            records.append({
                "id": update["id"], "value": update["value"], "status": "open",
                "introduced_in_cycle": cycle, "resolved_in_cycle": None, "resolution": None,
            })
        else:
            if match is None:
                fail(f"binding id does not exist: {update['id']}")
            match["status"] = "resolved" if update["action"] == "resolve" else "superseded"
            match["resolved_in_cycle"] = cycle
            match["resolution"] = update["resolution"]
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
unresolved_source_conflicts, open_objections, binding_updates.
binding_updates enthält kind, id, action (add|resolve|supersede), value und resolution.
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
        seed=config["sampling_seed"] + 10000 + len(decisions),
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
            temperature=config["temperature"],
            seed=config["sampling_seed"] + cycle,
        )
        current = result["text"].strip()
        protected = set(config["project_binding"].get("protected_concepts", {}).keys())
        verification = verify_productivity(result, decisions, protected)
        binding_matrix = update_binding_matrix(binding_matrix, result, cycle)
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
            item["productivity_verification"]["novelty_verified"]
            and item["productivity_verification"]["project_relevance_verified"]
            for item in decisions
        )
        if not decision["continue"] and productive_count >= config["minimum_productive_decisions"]:
            break
    return current, decisions, meta_decisions


def optional_review(text: str, decisions: list[dict[str, Any]], meta_decisions: list[dict[str, Any]], config: dict[str, Any], endpoint: str, model: str, api_key: str) -> dict[str, Any] | None:
    if not config["start_review_after_generation"]:
        return None
    review_input = [{
        key: value for key, value in decision.items()
        if key not in {"productive_difference", "productivity_verification"}
    } for decision in decisions]
    prompt = f"""Prüfe unabhängig Theorie, Relationen, Gegenmodelle und Methode. Die Selbstbeschreibung des Generators wird dir absichtlich nicht gezeigt.
PROJEKTBINDUNG:\n{config['project_binding_text']}
THEORIE:\n{text}
ANSCHLUSSENTSCHEIDUNGEN:\n{json.dumps(review_input, ensure_ascii=False, indent=2)}
META-ENTSCHEIDUNGEN:\n{json.dumps(meta_decisions, ensure_ascii=False, indent=2)}
Antworte exakt mit recommended_status, validated_relations, rejected_relations,
strong_objections, countermodel_results, method_assessment, requires_author_decision."""
    return call_structured_agent(
        [{"role": "system", "content": "Du bist ein rollengetrennter kritischer Prüfer."}, {"role": "user", "content": prompt}],
        schema="review", endpoint=endpoint, model=model, api_key=api_key,
        temperature=0.25, seed=config["sampling_seed"] + 20000,
    )


def apply_review_verification(decisions: list[dict[str, Any]], review: dict[str, Any] | None) -> None:
    if review is None:
        return
    validated = {(r["from"], r["relation"], r["to"]) for r in review["validated_relations"]}
    passed_claims = {r["claim"] for r in review["countermodel_results"] if r["result"] == "passed"}
    for decision in decisions:
        evidence = [
            {"kind": "review_validated_relation", "detail": relation}
            for relation in decision["new_relations"]
            if (relation["from"], relation["relation"], relation["to"]) in validated
        ]
        evidence += [
            {"kind": "review_passed_countermodel", "detail": item["claim"]}
            for item in decision["countermodels"] if item["claim"] in passed_claims
        ]
        decision["productivity_verification"]["philosophical_productivity_verified"] = bool(evidence)
        decision["productivity_verification"]["philosophical_evidence"] = evidence


def write_outputs(config: dict[str, Any], text: str, decisions: list[dict[str, Any]], meta_decisions: list[dict[str, Any]], review: dict[str, Any] | None, request_path: Path) -> list[Path]:
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
        "verified_productive_cycles": sum(bool(d["productivity_verification"]["philosophical_productivity_verified"]) for d in decisions),
        "source_context": config["source_context"],
        "source_provenance": config["source_provenance"],
        "project_binding_provenance": config["project_binding_provenance"],
        "binding_matrix": decisions[-1]["binding_matrix"] if decisions else config["initial_binding_matrix"],
        "sampling_seed": config["sampling_seed"], "temperature": config["temperature"],
        "model_revision": config["model_revision"],
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
            "initial_style": run["style"],
            "final_style": decisions[-1]["epistemic_style"] if decisions else run["style"],
            "style_changes": sum(
                bool(item.get("change_rule")) and item.get("previous_style") != item.get("selected_style")
                for item in run["meta_decisions"]
            ),
            "repetition": run.get("repetition", 1),
            "sampling_seed": run.get("sampling_seed"),
            "cycles": len(decisions),
            "verified_productive_cycles": sum(
                bool(item["productivity_verification"]["philosophical_productivity_verified"])
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
        "temperature": config["temperature"], "model_revision": config["model_revision"],
        "style_repetitions": config["style_repetitions"],
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
    config["project_binding"] = yaml.safe_load(PROJECT_BINDING_PATH.read_text(encoding="utf-8"))
    definitions = list(config["project_binding"].get("protected_concepts", {}).keys())
    config["initial_binding_matrix"] = {
        "preserved_definitions": [{
            "id": f"definition-{slugify(value)}", "value": value, "status": "active",
            "introduced_in_cycle": 0, "resolved_in_cycle": None, "resolution": None,
        } for value in definitions],
        "claims_in_tension": [], "departures_from_sources": [],
        "unresolved_source_conflicts": [], "open_objections": [],
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
        for repetition in range(config["style_repetitions"]):
            for style in config["epistemic_styles"]:
                run_config = dict(config)
                run_config["sampling_seed"] = config["sampling_seed"] + repetition * 1000
                run_config["initial_style"] = style
                run_config["title"] = f"{base_title or config['seed'].splitlines()[0][:72]} [{style} r{repetition + 1}]"
                text, decisions, meta_decisions = run_theory_cycles(run_config, endpoint, model, api_key)
                review = optional_review(text, decisions, meta_decisions, run_config, endpoint, model, api_key)
                apply_review_verification(decisions, review)
                paths.extend(write_outputs(run_config, text, decisions, meta_decisions, review, args.request))
                runs.append({
                    "style": style, "repetition": repetition + 1,
                    "sampling_seed": run_config["sampling_seed"],
                    "decisions": decisions, "meta_decisions": meta_decisions,
                })
        paths.append(write_style_comparison(config, runs))
        paths.append(artifact_bundle.create_bundle(paths))
        print("\n".join(str(path) for path in paths))
        return
    text, decisions, meta_decisions = run_theory_cycles(config, endpoint, model, api_key)
    review = optional_review(text, decisions, meta_decisions, config, endpoint, model, api_key)
    apply_review_verification(decisions, review)
    paths = write_outputs(config, text, decisions, meta_decisions, review, args.request)
    paths.append(artifact_bundle.create_bundle(paths))
    print("\n".join(str(path) for path in paths))


if __name__ == "__main__":
    main()
