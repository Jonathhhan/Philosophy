#!/usr/bin/env python3
"""Fuehrt laengere Theorie-Codex-Ketten bis zu einer produktiven Differenz.

Die Kette bildet keine philosophische Operation mechanisch ab. Sie erzwingt
lediglich, dass zwischen Befund, Urteil, Revision und Reorganisation jeweils
ein eigener, nachweisbarer Uebergang liegt. Ein spaeter Schritt darf nicht aus
der blossen Existenz des vorherigen Schritts abgeleitet werden.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "recovered" / "state" / "produktive-ketten.json"

STAGES = (
    "anschliessen",
    "rekonstruieren",
    "beurteilen",
    "revidieren",
    "reorganisieren",
    "kritisieren",
)

REQUIRED_OUTPUTS = {
    "anschliessen": "evidence",
    "rekonstruieren": "relation",
    "beurteilen": "criterion",
    "revidieren": "changed_condition",
    "reorganisieren": "changed_relations",
    "kritisieren": "new_question",
}


@dataclass
class StageResult:
    stage: str
    status: str
    output_kind: str
    output: str
    evidence: list[str] = field(default_factory=list)
    opened: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)


@dataclass
class ChainResult:
    chain_id: str
    subject: str
    status: str
    productive_difference: bool
    stages: list[StageResult]
    next_step: str


def stable_id(subject: str, context: str) -> str:
    digest = hashlib.sha256(f"{subject}\n{context}".encode("utf-8")).hexdigest()
    return digest[:16]


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"chains": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"chains": {}}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_stage(stage: StageResult) -> list[str]:
    problems: list[str] = []
    expected = REQUIRED_OUTPUTS[stage.stage]
    if stage.output_kind != expected:
        problems.append(f"{stage.stage}: erwartet {expected}, erhalten {stage.output_kind}")
    if not stage.output.strip():
        problems.append(f"{stage.stage}: leerer Output")
    if stage.status not in {"productive", "review", "blocked"}:
        problems.append(f"{stage.stage}: ungueltiger Status {stage.status}")
    return problems


def evaluate(subject: str, context: str, raw_stages: list[dict[str, Any]], state_path: Path) -> ChainResult:
    chain_id = stable_id(subject, context)
    state = load_state(state_path)
    previous = state.setdefault("chains", {}).get(chain_id, {})

    stages: list[StageResult] = []
    problems: list[str] = []
    for index, stage_name in enumerate(STAGES):
        if index >= len(raw_stages):
            break
        raw = raw_stages[index]
        stage = StageResult(
            stage=stage_name,
            status=str(raw.get("status", "review")),
            output_kind=str(raw.get("output_kind", "")),
            output=str(raw.get("output", "")),
            evidence=[str(item) for item in raw.get("evidence", [])],
            opened=[str(item) for item in raw.get("opened", [])],
            blocked=[str(item) for item in raw.get("blocked", [])],
        )
        stages.append(stage)
        problems.extend(validate_stage(stage))
        if stage.status == "blocked":
            break

    signatures = [
        hashlib.sha256(f"{s.stage}|{s.output_kind}|{s.output}".encode("utf-8")).hexdigest()
        for s in stages
        if s.status == "productive"
    ]
    old_signatures = set(previous.get("productive_signatures", []))
    new_signatures = [signature for signature in signatures if signature not in old_signatures]

    complete = len(stages) == len(STAGES)
    productive = complete and not problems and bool(new_signatures)

    if problems:
        status = "blocked"
        next_step = "Kettenfehler beheben: " + "; ".join(problems)
    elif any(stage.status == "blocked" for stage in stages):
        status = "blocked"
        next_step = "Fehlende Evidenz oder Entscheidung beschaffen; keinen Folgeschritt simulieren."
    elif not complete:
        status = "review"
        next_stage = STAGES[len(stages)]
        next_step = f"Naechste Schwelle bearbeiten: {next_stage}."
    elif productive:
        status = "productive"
        next_step = "Produktive Differenz integrieren und ihre Folgebeziehungen erneut anschliessen."
    else:
        status = "exhausted"
        next_step = "Keine neue Differenz: Gegenstand wechseln oder neue Evidenz zufuehren."

    state["chains"][chain_id] = {
        "subject": subject,
        "context": context,
        "productive_signatures": sorted(old_signatures | set(signatures)),
        "last_status": status,
        "stage_count": len(stages),
    }
    save_state(state_path, state)

    return ChainResult(
        chain_id=chain_id,
        subject=subject,
        status=status,
        productive_difference=productive,
        stages=stages,
        next_step=next_step,
    )


def markdown(result: ChainResult) -> str:
    lines = [
        "# Produktive Theorie-Codex-Kette",
        "",
        f"- Gegenstand: {result.subject}",
        f"- Ketten-ID: `{result.chain_id}`",
        f"- Status: **{result.status}**",
        f"- Produktive Differenz: **{'ja' if result.productive_difference else 'nein'}**",
        f"- Naechster Schritt: {result.next_step}",
        "",
        "## Schwellen",
        "",
    ]
    for stage in result.stages:
        lines.extend(
            [
                f"### {stage.stage}",
                f"- Status: {stage.status}",
                f"- Outputtyp: `{stage.output_kind}`",
                f"- Output: {stage.output}",
            ]
        )
        if stage.evidence:
            lines.append("- Evidenz: " + "; ".join(stage.evidence))
        if stage.opened:
            lines.append("- Eroeffnet: " + "; ".join(stage.opened))
        if stage.blocked:
            lines.append("- Blockiert: " + "; ".join(stage.blocked))
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prueft eine laengere produktive Theorie-Codex-Kette.")
    parser.add_argument("subject")
    parser.add_argument("--context", default="")
    parser.add_argument("--input", type=Path, required=True, help="JSON-Datei mit stages[]")
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    source = args.input if args.input.is_absolute() else ROOT / args.input
    payload = json.loads(source.read_text(encoding="utf-8"))
    result = evaluate(args.subject, args.context, payload.get("stages", []), args.state_file)
    rendered = (
        json.dumps(asdict(result), ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else markdown(result)
    )
    if args.output:
        target = args.output if args.output.is_absolute() else ROOT / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if result.status == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
