#!/usr/bin/env python3
"""Structured critical review for generated philosophical theory records.

The reviewer is deliberately separate from the generator. It reads a generated
record, asks a critical model for a strict review object, verifies the object,
and writes a review next to the generated material without promoting it.
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ALLOWED_RECOMMENDATIONS = {"generated", "proposal", "rejected"}
ALLOWED_PRODUCTIVITY = {"unsupported", "plausible", "supported"}
MAX_REPAIR_ATTEMPTS = 2


class ReviewError(ValueError):
    """Raised when review input or model output violates the contract."""


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def _require(data: dict[str, Any], fields: set[str], name: str) -> None:
    missing = sorted(fields - data.keys())
    unexpected = sorted(data.keys() - fields)
    if missing:
        raise ReviewError(f"{name} missing fields: {', '.join(missing)}")
    if unexpected:
        raise ReviewError(f"{name} unexpected fields: {', '.join(unexpected)}")


def _strings(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ReviewError(f"{key} must be a list of non-empty strings")
    return value


def _objects(data: dict[str, Any], key: str, fields: set[str]) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ReviewError(f"{key} must be a list of objects")
    for index, item in enumerate(value):
        _require(item, fields, f"{key}[{index}]")
        for field in fields:
            if not isinstance(item[field], str) or not item[field].strip():
                raise ReviewError(f"{key}[{index}].{field} must be a non-empty string")
    return value


REVIEW_FIELDS = {
    "recommended_status",
    "novelty_assessment",
    "project_relevance_assessment",
    "philosophical_productivity_assessment",
    "validated_relations",
    "rejected_relations",
    "strong_objections",
    "countermodel_results",
    "method_assessment",
    "required_revisions",
    "resolved_binding_items",
    "new_binding_items",
    "requires_author_decision",
    "decision_reason",
}


def validate_review(data: dict[str, Any]) -> dict[str, Any]:
    _require(data, REVIEW_FIELDS, "ReviewResult")
    if data["recommended_status"] not in ALLOWED_RECOMMENDATIONS:
        raise ReviewError("recommended_status must be generated, proposal or rejected")
    for key in (
        "novelty_assessment",
        "project_relevance_assessment",
        "philosophical_productivity_assessment",
    ):
        if data[key] not in ALLOWED_PRODUCTIVITY:
            raise ReviewError(f"{key} must be unsupported, plausible or supported")
    for key in ("method_assessment", "decision_reason"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise ReviewError(f"{key} must be a non-empty string")
    for key in ("strong_objections", "required_revisions", "resolved_binding_items"):
        _strings(data, key)
    _objects(data, "validated_relations", {"from", "relation", "to", "reason"})
    _objects(data, "rejected_relations", {"from", "relation", "to", "reason"})
    _objects(data, "countermodel_results", {"target", "result", "consequence"})
    _objects(data, "new_binding_items", {"kind", "claim", "status"})
    if type(data["requires_author_decision"]) is not bool:
        raise ReviewError("requires_author_decision must be a boolean")
    if data["recommended_status"] == "proposal":
        if data["philosophical_productivity_assessment"] != "supported":
            raise ReviewError("proposal requires supported philosophical productivity")
        if data["strong_objections"]:
            raise ReviewError("proposal cannot retain unresolved strong objections")
    return data


def extract_json_object(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ReviewError(f"review must be exactly one JSON object: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewError("review must be a JSON object")
    return value


def parse_and_validate(raw: str) -> dict[str, Any]:
    return validate_review(extract_json_object(raw))


def api_call(messages: list[dict[str, str]], endpoint: str, model: str, api_key: str) -> str:
    url = endpoint.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.2,
    }).encode("utf-8")
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
        fail(f"model endpoint returned HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:500]}")
    except urllib.error.URLError as exc:
        fail(f"could not reach model endpoint: {exc}")
    try:
        return str(body["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError):
        fail("model endpoint returned an unexpected response")


def call_reviewer(messages: list[dict[str, str]], endpoint: str, model: str, api_key: str) -> dict[str, Any]:
    attempts = list(messages)
    last_error = "unknown review schema error"
    for repair in range(MAX_REPAIR_ATTEMPTS + 1):
        raw = api_call(attempts, endpoint, model, api_key)
        try:
            return parse_and_validate(raw)
        except ReviewError as exc:
            last_error = str(exc)
            if repair >= MAX_REPAIR_ATTEMPTS:
                break
            attempts.extend([
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"Repair only structure and types: {exc}. Return exactly one JSON object."},
            ])
    fail(f"review violates schema after repairs: {last_error}")


def load_yaml_object(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"{path} must contain a YAML object")
    return data


def resolve_generated_paths(record_path: Path, record: dict[str, Any]) -> tuple[Path, Path]:
    root = Path.cwd().resolve()
    if "generated" not in record_path.resolve().parts:
        fail("record must be below generated/")
    output_path = (root / str(record.get("output_file", ""))).resolve()
    graph_path = (root / str(record.get("graph_file", ""))).resolve()
    generated_root = (root / "generated").resolve()
    for path in (output_path, graph_path):
        if generated_root not in path.parents or not path.is_file():
            fail(f"record references invalid generated file: {path}")
    return output_path, graph_path


def system_prompt() -> str:
    return """You are the independent critical review stage of a philosophical research repository.
Do not reward novelty alone. Distinguish:
1. structural novelty,
2. relevance to the declared project,
3. defensible philosophical productivity.
A proposal recommendation requires supported philosophical productivity and no unresolved strong objection.
Return exactly one JSON object with these fields:
recommended_status; novelty_assessment; project_relevance_assessment;
philosophical_productivity_assessment; validated_relations; rejected_relations;
strong_objections; countermodel_results; method_assessment; required_revisions;
resolved_binding_items; new_binding_items; requires_author_decision; decision_reason.
Assessments are exactly unsupported, plausible or supported.
Relations contain from, relation, to, reason. Countermodel results contain target, result, consequence.
New binding items contain kind, claim, status."""


def build_messages(record: dict[str, Any], text: str, graph: dict[str, Any]) -> list[dict[str, str]]:
    payload = {
        "generation_record": record,
        "theory_text": text,
        "theory_graph": graph,
    }
    return [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False, indent=2)},
    ]


def write_review(record_path: Path, record: dict[str, Any], review: dict[str, Any]) -> Path:
    review_path = record_path.with_name(record_path.stem + "-review.yaml")
    data = {
        "type": "structured_critical_review",
        "status": "reviewed",
        "source_record": record_path.as_posix(),
        "model": os.environ.get("GENERATIVE_MODEL", "unknown"),
        **review,
    }
    review_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return review_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    record = load_yaml_object(args.record)
    output_path, graph_path = resolve_generated_paths(args.record, record)
    if args.validate_only:
        print(json.dumps({"record": str(args.record), "output": str(output_path), "graph": str(graph_path)}, indent=2))
        return
    endpoint = os.environ.get("GENERATIVE_API_ENDPOINT", "").strip()
    model = os.environ.get("GENERATIVE_MODEL", "").strip()
    api_key = os.environ.get("GENERATIVE_API_KEY", "").strip()
    if not endpoint or not model or not api_key:
        fail("GENERATIVE_API_ENDPOINT, GENERATIVE_MODEL and GENERATIVE_API_KEY are required")
    text = output_path.read_text(encoding="utf-8")
    graph = load_yaml_object(graph_path)
    review = call_reviewer(build_messages(record, text, graph), endpoint, model, api_key)
    print(write_review(args.record, record, review))


if __name__ == "__main__":
    main()
