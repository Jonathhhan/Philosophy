#!/usr/bin/env python3
"""Controlled autonomous generative runner.

Reads a YAML request, calls an OpenAI-compatible chat completions endpoint for a
bounded number of passes, and writes only below generated/. It never edits the
manuscript or confirmed knowledge directly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ALLOWED_TARGETS = {"essay", "chapter_seed", "continuation", "experiment", "theses", "dialogue"}
TARGET_DIRS = {
    "essay": "essays",
    "chapter_seed": "chapter-seeds",
    "continuation": "continuations",
    "experiment": "experiments",
    "theses": "experiments",
    "dialogue": "experiments",
}


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9äöüß]+", "-", value)
    value = value.strip("-")
    return value[:64] or "generativer-lauf"


def load_request(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("request must be a YAML object")

    seed = str(data.get("seed", "")).strip()
    if not seed:
        fail("request.seed is required")

    mode = data.get("mode", "autonomous_generative")
    if mode != "autonomous_generative":
        fail("mode must be autonomous_generative")

    target = data.get("target", "essay")
    if target not in ALLOWED_TARGETS:
        fail(f"target must be one of {sorted(ALLOWED_TARGETS)}")

    max_passes = int(data.get("max_passes", 3))
    if not 1 <= max_passes <= 6:
        fail("max_passes must be between 1 and 6")

    return {
        "seed": seed,
        "mode": mode,
        "target": target,
        "max_passes": max_passes,
        "title": str(data.get("title", "")).strip(),
        "instructions": str(data.get("instructions", "")).strip(),
        "start_review_after_generation": bool(data.get("start_review_after_generation", False)),
        "source_context": list(data.get("source_context", [])),
    }


def api_call(messages: list[dict[str, str]], *, endpoint: str, model: str, api_key: str) -> str:
    url = endpoint.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.85,
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
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


def build_system_prompt(target: str) -> str:
    return f"""Du arbeitest im rein generativen autonomen Modus eines philosophischen Forschungsprojekts.
Aus einem Anfang entwickelst du einen eigenständigen deutschen Text vom Typ {target}.
Du darfst neue Begriffe, Relationen, Beispiele und Gegenbewegungen erproben.
Der Text soll eine längere innere Bewegung bilden und nicht bloß paraphrasieren.
Bewahre besonders produktive Spannungen, statt sie vorschnell aufzulösen.
Kennzeichne keine Aussage als bestätigte Theorie. Schreibe nur den Text selbst, ohne Metakommentar."""


def generate(config: dict[str, Any], endpoint: str, model: str, api_key: str) -> tuple[str, list[str]]:
    current = ""
    pass_notes: list[str] = []

    for index in range(1, config["max_passes"] + 1):
        if index == 1:
            task = f"Anfang:\n{config['seed']}\n\nEntwickle daraus einen neuen zusammenhängenden Text."
            if config["instructions"]:
                task += f"\n\nZusätzliche Vorgaben:\n{config['instructions']}"
        else:
            task = f"""Überarbeite den folgenden generierten Text in einem weiteren rekursiven Durchgang.
Vertiefe seine produktivste Differenz, verbessere Übergänge und entferne Wiederholungen.
Bewahre den Ausgangsimpuls erkennbar, ohne ihn mechanisch zu wiederholen.

TEXT:
{current}"""

        current = api_call(
            [
                {"role": "system", "content": build_system_prompt(config["target"])},
                {"role": "user", "content": task},
            ],
            endpoint=endpoint,
            model=model,
            api_key=api_key,
        )
        pass_notes.append(f"pass_{index}: completed")

    return current, pass_notes


def optional_review(text: str, config: dict[str, Any], endpoint: str, model: str, api_key: str) -> str | None:
    if not config["start_review_after_generation"]:
        return None

    prompt = f"""Prüfe den folgenden generierten philosophischen Text, ohne ihn umzuschreiben.
Gib knapp aus:
1. neue produktive Differenzen,
2. plausible Anschlüsse an den Anfang,
3. begriffliche Verschiebungen,
4. starke offene Einwände,
5. empfohlener nächster Status: generated oder proposal.
Bestätige den Text nicht automatisch.

ANFANG:
{config['seed']}

TEXT:
{text}"""
    return api_call(
        [{"role": "system", "content": "Du bist der prüfende Modus eines philosophischen Forschungsautomaten."},
         {"role": "user", "content": prompt}],
        endpoint=endpoint,
        model=model,
        api_key=api_key,
    )


def write_outputs(config: dict[str, Any], text: str, passes: list[str], review: str | None, request_path: Path) -> list[Path]:
    title = config["title"] or config["seed"].splitlines()[0][:72]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = slugify(title)
    directory = Path("generated") / TARGET_DIRS[config["target"]]
    directory.mkdir(parents=True, exist_ok=True)

    text_path = directory / f"{stamp}-{slug}.md"
    record_path = directory / f"{stamp}-{slug}.yaml"

    header = {
        "mode": "autonomous_generative",
        "status": "generated",
        "seed": config["seed"],
        "created_by": "generative_runner",
        "model": os.environ.get("GENERATIVE_MODEL", "unknown"),
        "source_context": config["source_context"],
        "divergences": [],
        "next_possible_steps": ["review", "revise", "promote_to_proposal"],
    }
    text_path.write_text(
        "---\n" + yaml.safe_dump(header, allow_unicode=True, sort_keys=False).strip() + "\n---\n\n" + text.strip() + "\n",
        encoding="utf-8",
    )

    record = {
        **header,
        "request_file": str(request_path),
        "target": config["target"],
        "max_passes": config["max_passes"],
        "passes": passes,
        "review_started": review is not None,
        "review": review,
        "output_file": str(text_path),
    }
    record_path.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return [text_path, record_path]


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

    text, passes = generate(config, endpoint, model, api_key)
    review = optional_review(text, config, endpoint, model, api_key)
    outputs = write_outputs(config, text, passes, review, args.request)
    print("\n".join(str(path) for path in outputs))


if __name__ == "__main__":
    main()
