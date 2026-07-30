#!/usr/bin/env python3
"""Build a single Markdown reading copy from the manuscript chapters."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuskript"
OUT = ROOT / "build" / "manuskript-lesefassung.md"

CHAPTERS = [
    "01-anschliessen.md",
    "02-unterbrechen.md",
    "03-problematisieren.md",
    "04-form.md",
    "05-aktualisieren.md",
    "06-improvisieren.md",
    "07-programm.md",
    "08-algorithmus.md",
    "09-komponieren.md",
    "10-stabilisieren.md",
    "11-organisieren.md",
    "12-verteilen.md",
    "13-asymmetrie.md",
    "14-kritisieren.md",
    "15-beurteilen.md",
    "16-revidieren.md",
    "17-reorganisieren.md",
    "schluss.md",
]

TITLE = "Zur Kritik der Organisation von Anschlussmoeglichkeiten"
SUBTITLE = "Lesefassung aus dem aktuellen Manuskriptstand"


def read_chapter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.strip() + "\n"


def chapter_title(text: str, filename: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not match:
        raise SystemExit(f"{filename}: missing level-1 chapter title")
    return match.group(1)


def validate_footnotes(filename: str, text: str) -> None:
    refs = set(re.findall(r"\[\^([^\]]+)\]", text))
    defs = set(re.findall(r"^\[\^([^\]]+)\]:", text, re.MULTILINE))
    missing = sorted(refs - defs)
    unused = sorted(defs - refs)
    if missing:
        raise SystemExit(f"{filename}: missing footnote definitions: {', '.join(missing)}")
    if unused:
        raise SystemExit(f"{filename}: unused footnote definitions: {', '.join(unused)}")


def validate_fences(filename: str, text: str) -> None:
    fence_count = len(re.findall(r"^```", text, re.MULTILINE))
    if fence_count % 2:
        raise SystemExit(f"{filename}: uneven fenced code block count")


def anchor_for(title: str) -> str:
    anchor = (
        title.casefold()
        .replace("ä", "a")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("ß", "ss")
    )
    anchor = re.sub(r"[^a-z0-9\s-]", "", anchor)
    return re.sub(r"\s+", "-", anchor.strip())


def main() -> int:
    missing_files = [name for name in CHAPTERS if not (MANUSCRIPT / name).is_file()]
    if missing_files:
        raise SystemExit(f"missing manuscript files: {', '.join(missing_files)}")

    chapters: list[tuple[str, str, str]] = []
    for name in CHAPTERS:
        text = read_chapter(MANUSCRIPT / name)
        validate_footnotes(name, text)
        validate_fences(name, text)
        chapters.append((name, chapter_title(text, name), text))

    lines: list[str] = [
        f"# {TITLE}",
        "",
        f"_{SUBTITLE}_",
        "",
        "> Diese Datei wird durch `python scripts/build_manuscript.py` erzeugt.",
        "> Bearbeitet werden die Einzelkapitel unter `manuskript/`.",
        "",
        "## Inhaltsverzeichnis",
        "",
    ]
    for _, title, _ in chapters:
        lines.append(f"- [{title}](#{anchor_for(title)})")

    lines.extend(["", "---", ""])
    for index, (name, _, text) in enumerate(chapters):
        if index:
            lines.extend(["", "---", ""])
        lines.append(f"<!-- Quelle: manuskript/{name} -->")
        lines.append("")
        lines.append(text)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
