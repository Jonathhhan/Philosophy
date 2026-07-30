#!/usr/bin/env python3
"""Philosophie-Automat: prüft, findet und entwirft Anschlüsse im Projekt.

Der Automat kann Gedanken gegen die lokale Wissensbasis prüfen, mögliche
Manuskriptanker finden, Vorschlagsdossiers schreiben und mit explizitem --apply
einen markierten Entwurf in eine angegebene Manuskriptstelle einfügen.
Er entscheidet keine Theoriefrage und ersetzt keine Autorenentscheidung.
"""

from __future__ import annotations

import argparse
import datetime as dt
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
PROPOSAL_DIR = ROOT / "recovered" / "proposals"

BOUNDARY_MARKERS = {
    "general_power_theory": {
        "terms": ["macht", "herrschaft", "legitimation", "gesellschaftstheorie"],
        "warning": "Macht, Herrschaft und Legitimation nur als abgeleitete Diagnosebegriffe organisierter Asymmetrie behandeln.",
    },
    "ai_authority": {
        "terms": ["codex entscheidet", "ki entscheidet", "autorersatz", "automatisch wahr", "orakel"],
        "warning": "Codex darf keine Autorentscheidung, Theorieautorität oder Wahrheitsgarantie ersetzen.",
    },
    "technical_reduction": {
        "terms": ["nur computer", "bloß technisch", "reine software", "nur code"],
        "warning": "Programm und Algorithmus nicht auf Computerprogramme oder bloße Technik reduzieren.",
    },
    "origin_claim": {
        "terms": ["anfang bei null", "voraussetzungsloser anfang", "ursprung ohne voraussetzung"],
        "warning": "Das Projekt beginnt nicht bei einem voraussetzungslosen Anfang; Anschlüsse setzen Bedingungen voraus.",
    },
}

ROLE_QUESTIONS = {
    "Genealoge": [
        "Welche Manuskriptstellen, Entscheidungen oder Primärquellen tragen den Gedanken?",
        "Ist die Aussage Quelle, begriffliche Entwicklung, Codex-Vorschlag oder bestätigte Position?",
    ],
    "Konsistenzprüfer": [
        "Verändert der Gedanke eine bestehende Definition oder nur ihre Anwendung?",
        "Welche Kapitel oder Concept-Dateien müssten bei Übernahme mitgeprüft werden?",
    ],
    "Kritiker": [
        "Welche Voraussetzung wird im Gedanken stillschweigend gemacht?",
        "Welche Alternative oder Gegenbeispiel könnte die Formulierung begrenzen?",
    ],
    "Material-technischer Prüfer": [
        "Bleibt die Herkunft aus Montage, Material, Programm, Algorithmus oder Implementierung sichtbar?",
        "Wird eine technische oder materielle Bedingung zu abstrakt behandelt?",
    ],
}

STATUS_HINTS = ["autorentscheidung", "entscheidung", "definition", "these", "vorschlag", "todo", "quelle", "rekonstruktion"]


@dataclass(frozen=True)
class Concept:
    id: str
    label: str
    status: str
    file: str
    chapter: Any | None
    definition: str | None
    working_definition: str | None
    depends_on: list[str]
    required_for: list[str]
    related: list[str]
    constraints: list[str]
    source_files: list[str]


def normalize(text: str) -> str:
    lowered = text.lower().replace("ß", "ss")
    for old, new in {"ä": "ae", "ö": "oe", "ü": "ue"}.items():
        lowered = lowered.replace(old, new)
    return lowered


def slugify(text: str, max_len: int = 48) -> str:
    slug = normalize(text)
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return (slug[:max_len].strip("-") or "gedanke")


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
            definition=data.get("definition"),
            working_definition=data.get("working_definition"),
            depends_on=list(data.get("depends_on", []) or []),
            required_for=list(data.get("required_for", []) or []),
            related=list(data.get("related", []) or []),
            constraints=list(data.get("constraints", []) or []),
            source_files=list(data.get("source_files", []) or []),
        ))
    return concepts


def concept_aliases(concept: Concept) -> set[str]:
    aliases = {concept.id, concept.label, concept.id.replace("ae", "ä").replace("oe", "ö").replace("ue", "ü")}
    if concept.id.endswith("en"):
        aliases.add(concept.id[:-2])
    special = {
        "anschliessen": {"anschließen", "anschluss", "anschluesse", "anschlüsse", "anschlussmoeglichkeit", "anschlussmöglichkeit"},
        "moeglichkeitsraum": {"möglichkeitsraum", "moeglichkeit", "möglichkeit", "anschlussmöglichkeiten", "anschlussmoeglichkeiten"},
        "organisieren": {"organisation", "organisiert", "organisierte", "organisierter", "organisierenden"},
        "kritisieren": {"kritik", "kritisch", "kritische", "kritischer", "kritisiert"},
        "beurteilen": {"urteil", "beurteilung", "beurteilt", "urteilen"},
        "revidieren": {"revision", "revidiert", "revidierbarkeit"},
        "reorganisieren": {"reorganisation", "reorganisiert", "reorganisierend"},
        "stabilisieren": {"stabilisierung", "stabilisiert", "stabile", "stabilität"},
        "verteilen": {"verteilung", "verteilt", "verteilte"},
        "asymmetrie": {"asymmetrisch", "asymmetrische", "asymmetrischer"},
        "program": {"programm", "programme", "programms"},
        "komposition": {"komponieren", "kompositorisch"},
    }
    aliases.update(special.get(concept.id, set()))
    return {normalize(alias) for alias in aliases if alias}


def mentioned_concepts(thought: str, concepts: list[Concept]) -> list[Concept]:
    haystack = normalize(thought)
    found = []
    for concept in concepts:
        if any(re.search(rf"(?<![a-z0-9_]){re.escape(alias)}(?![a-z0-9_])", haystack) for alias in concept_aliases(concept)):
            found.append(concept)
    return found


def boundary_warnings(thought: str) -> list[dict[str, str]]:
    haystack = normalize(thought)
    return [{"id": key, "warning": data["warning"]} for key, data in BOUNDARY_MARKERS.items() if any(normalize(term) in haystack for term in data["terms"])]


def status_guess(thought: str) -> str:
    haystack = normalize(thought)
    for hint in STATUS_HINTS:
        if normalize(hint) in haystack:
            return hint
    return "unbestimmt; als Vorschlag oder TODO behandeln, bis der Autor entscheidet"


def concept_to_dict(concept: Concept, compact: bool = False) -> dict[str, Any]:
    data: dict[str, Any] = {"id": concept.id, "label": concept.label, "status": concept.status, "file": concept.file}
    if concept.chapter is not None:
        data["chapter"] = concept.chapter
    if not compact:
        data.update({
            "definition": concept.definition or concept.working_definition,
            "depends_on": concept.depends_on,
            "required_for": concept.required_for,
            "related": concept.related,
            "constraints": concept.constraints,
            "source_files": concept.source_files,
        })
    return data


def find_anchors(thought: str, found: list[Concept], limit: int = 8) -> list[dict[str, Any]]:
    terms = {normalize(thought)}
    for concept in found:
        terms.update(concept_aliases(concept))
    anchors: list[dict[str, Any]] = []
    for path in sorted(MANUSCRIPT_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for idx, line in enumerate(lines, start=1):
            if not line.strip() or line.startswith("#"):
                continue
            haystack = normalize(line)
            hits = sorted({term for term in terms if term and len(term) > 3 and term in haystack})
            if hits:
                anchors.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": idx,
                    "score": len(hits),
                    "hits": hits[:8],
                    "excerpt": line.strip()[:240],
                })
    anchors.sort(key=lambda item: (-item["score"], item["file"], item["line"]))
    return anchors[:limit]


def adjacent_concepts(found: list[Concept], concepts: list[Concept]) -> list[Concept]:
    found_ids = {concept.id for concept in found}
    adjacent_ids: set[str] = set()
    for concept in found:
        adjacent_ids.update(concept.depends_on)
        adjacent_ids.update(concept.required_for)
        adjacent_ids.update(concept.related)
    by_id = {concept.id: concept for concept in concepts}
    return [by_id[item] for item in sorted(adjacent_ids - found_ids) if item in by_id]


def build_suggestion(thought: str, found: list[Concept], warnings: list[dict[str, str]]) -> str:
    names = ", ".join(concept.label for concept in found) or "die betroffene Anschlussstelle"
    warning_sentence = ""
    if warnings:
        warning_sentence = " Der Vorschlag bleibt begrenzt, weil die Projektgrenzen ausdrücklich mitzuprüfen sind."
    clean_thought = thought.strip().rstrip(".")
    return (
        "TODO: Vorschlag des Philosophie-Automaten; nicht als bestätigte Theorie behandeln.\n\n"
        f"Der Gedanke lautet: {clean_thought}. Er ist zunächst als mögliche Anschlussstelle zu prüfen. "
        f"Er berührt {names} und darf deshalb nicht als isolierte Formulierung übernommen werden. "
        "Zu klären ist, ob er eine bestehende Definition verändert, eine Anwendung präzisiert oder lediglich einen Einwand markiert."
        f"{warning_sentence}\n\n"
        "Für eine Übernahme müsste ausgewiesen werden, welche Bedingungen dadurch sichtbar, welche Relationen verschoben und welche späteren Anschlüsse begrenzt oder eröffnet werden."
    )


def recommended_steps(found: list[Concept], adjacent: list[Concept], anchors: list[dict[str, Any]]) -> list[str]:
    if not found:
        return [
            "Begriffliche Anschlussstelle noch unklar: als TODO markieren oder einen passenden Concept-Knoten bestimmen.",
            "Prüfen, ob der Gedanke eine neue Grundthese wäre; falls ja, Autorenentscheidung einholen.",
        ]
    steps = ["Gefundene Concept-Dateien und zugehörige Manuskriptstellen lesen, bevor eine Integration erwogen wird.", "Prüfen, ob der Gedanke Definition, Anwendung, Einwand oder Beispiel ist."]
    if adjacent:
        steps.append("Benachbarte Begriffe mitprüfen, weil der Gedanke Anschlussrelationen berühren kann.")
    if anchors:
        steps.append("Mögliche Manuskriptanker prüfen; automatische Einfügung nur mit explizitem Ziel und --apply verwenden.")
    steps.append("Bei Integration ein Change Event oder TODO mit Herkunft und Status anlegen.")
    return steps


def build_report(thought: str, include_anchors: bool = False, include_suggestion: bool = False) -> dict[str, Any]:
    concepts = load_concepts()
    found = mentioned_concepts(thought, concepts)
    adjacent = adjacent_concepts(found, concepts)
    anchors = find_anchors(thought, found) if include_anchors else []
    warnings = boundary_warnings(thought)
    report = {
        "thought": thought,
        "status_guess": status_guess(thought),
        "mentioned_concepts": [concept_to_dict(concept) for concept in found],
        "adjacent_concepts": [concept_to_dict(concept, compact=True) for concept in adjacent],
        "anchors": anchors,
        "boundary_warnings": warnings,
        "role_checks": ROLE_QUESTIONS,
        "recommended_next_steps": recommended_steps(found, adjacent, anchors),
        "limits": [
            "Der Automat schreibt nur mit explizitem --write-proposal oder --apply.",
            "Er ersetzt keine Autorenentscheidung.",
            "Er prüft deklarierte Anschlussbedingungen, nicht philosophische Wahrheit.",
        ],
    }
    if include_suggestion:
        report["text_suggestion"] = build_suggestion(thought, found, warnings)
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Philosophie-Automat", "", f"Gedanke: {report['thought']}", "", f"Status: {report['status_guess']}", ""]
    lines.append("## Erkannte Begriffe")
    if report["mentioned_concepts"]:
        for concept in report["mentioned_concepts"]:
            lines.append(f"- {concept['label']} (`{concept['id']}`), Status: {concept['status']}, Datei: `{concept['file']}`")
            if concept.get("definition"):
                lines.append(f"  - Definition/Arbeitsnotiz: {concept['definition']}")
            for constraint in concept.get("constraints", []):
                lines.append(f"  - Grenze: {constraint}")
    else:
        lines.append("- Keine deklarierte Begriffsadresse erkannt.")
    lines.extend(["", "## Benachbarte Anschlussstellen"])
    if report["adjacent_concepts"]:
        for concept in report["adjacent_concepts"]:
            lines.append(f"- {concept['label']} (`{concept['id']}`) — `{concept['file']}`")
    else:
        lines.append("- Keine weiteren deklarierten Nachbarbegriffe gefunden.")
    lines.extend(["", "## Manuskriptanker"])
    if report["anchors"]:
        for anchor in report["anchors"]:
            lines.append(f"- `{anchor['file']}:{anchor['line']}` Score {anchor['score']}: {anchor['excerpt']}")
    else:
        lines.append("- Keine Ankersuche ausgeführt oder kein Anker gefunden.")
    lines.extend(["", "## Projektgrenzen"])
    if report["boundary_warnings"]:
        for item in report["boundary_warnings"]:
            lines.append(f"- {item['warning']}")
    else:
        lines.append("- Keine automatische Grenzwarnung ausgelöst.")
    if report.get("text_suggestion"):
        lines.extend(["", "## Textvorschlag", "", report["text_suggestion"]])
    lines.extend(["", "## Prüfrollen"])
    for role, questions in report["role_checks"].items():
        lines.append(f"- {role}:")
        for question in questions:
            lines.append(f"  - {question}")
    lines.extend(["", "## Empfohlene nächste Schritte"])
    for step in report["recommended_next_steps"]:
        lines.append(f"- {step}")
    lines.extend(["", "## Grenzen des Automaten"])
    for limit in report["limits"]:
        lines.append(f"- {limit}")
    return "\n".join(lines) + "\n"


def write_proposal(report: dict[str, Any]) -> Path:
    PROPOSAL_DIR.mkdir(parents=True, exist_ok=True)
    date = dt.date.today().isoformat()
    path = PROPOSAL_DIR / f"{date}-{slugify(report['thought'])}.md"
    counter = 2
    while path.exists():
        path = PROPOSAL_DIR / f"{date}-{slugify(report['thought'])}-{counter}.md"
        counter += 1
    path.write_text(render_markdown(report), encoding="utf-8")
    return path


def safe_manuscript_path(value: str) -> Path:
    path = (ROOT / value).resolve()
    manuscript_root = MANUSCRIPT_DIR.resolve()
    if not path.is_file() or manuscript_root not in path.parents:
        raise SystemExit("--target-file muss auf eine vorhandene Datei unter manuskript/ zeigen.")
    return path


def apply_to_manuscript(report: dict[str, Any], target_file: str, after_heading: str) -> Path:
    path = safe_manuscript_path(target_file)
    text = path.read_text(encoding="utf-8")
    marker = after_heading.strip()
    if marker not in text:
        raise SystemExit("--after-heading wurde in der Zieldatei nicht gefunden.")
    suggestion = report.get("text_suggestion") or build_suggestion(report["thought"], [], report["boundary_warnings"])
    block = f"\n\n<!-- PHILOSOPHIE_AUTOMAT:BEGIN status=vorschlag -->\n{suggestion}\n<!-- PHILOSOPHIE_AUTOMAT:END -->\n"
    text = text.replace(marker, marker + block, 1)
    path.write_text(text, encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prüft und entwirft Anschlüsse im Buchprojekt.")
    parser.add_argument("thought", nargs="*", help="Zu prüfender Gedanke oder Satz.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--find-anchors", action="store_true", help="Mögliche Manuskriptanker suchen.")
    parser.add_argument("--suggest", action="store_true", help="Einen markierten Textvorschlag erzeugen.")
    parser.add_argument("--write-proposal", action="store_true", help="Ein Vorschlagsdossier unter recovered/proposals/ schreiben.")
    parser.add_argument("--apply", action="store_true", help="Den Vorschlag markiert ins Manuskript einfügen; benötigt --target-file und --after-heading.")
    parser.add_argument("--target-file", help="Zieldatei unter manuskript/ für --apply.")
    parser.add_argument("--after-heading", help="Exakte Überschrift oder Markerzeile, nach der eingefügt wird.")
    args = parser.parse_args(argv)
    thought = " ".join(args.thought).strip() or sys.stdin.read().strip()
    if not thought:
        parser.error("Bitte einen Gedanken als Argument oder über stdin übergeben.")
    if args.apply and not (args.target_file and args.after_heading):
        parser.error("--apply benötigt --target-file und --after-heading.")
    report = build_report(thought, include_anchors=args.find_anchors or args.write_proposal or args.apply, include_suggestion=args.suggest or args.write_proposal or args.apply)
    written: dict[str, str] = {}
    if args.write_proposal:
        written["proposal_file"] = str(write_proposal(report).relative_to(ROOT))
    if args.apply:
        written["applied_file"] = str(apply_to_manuscript(report, args.target_file or "", args.after_heading or "").relative_to(ROOT))
        report["application_note"] = "Automatisch eingefügter, markierter Vorschlag; nicht als bestätigte Theorie behandeln."
    if written:
        report["written"] = written
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
        for key, value in written.items():
            print(f"\n{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())