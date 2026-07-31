#!/usr/bin/env python3
"""Create and verify an exact, hash-bound bundle of generated artifacts."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import zipfile
from pathlib import Path, PurePosixPath

import yaml

BUNDLE_PATH = Path("generated/autonomous-generative-output.zip")


def _safe_generated_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "generated":
        raise ValueError(f"unsafe generated artifact path: {raw}")
    return path


def create_bundle(paths: list[Path], bundle_path: Path = BUNDLE_PATH, root: Path = Path.cwd()) -> Path:
    entries = []
    seen = set()
    root = root.resolve()
    for path in paths:
        resolved = path.resolve()
        try:
            relative = _safe_generated_path(resolved.relative_to(root).as_posix())
        except ValueError as exc:
            raise ValueError(f"artifact escapes root: {path}") from exc
        if relative.as_posix() in seen or not path.is_file():
            raise ValueError(f"duplicate or missing artifact: {path}")
        seen.add(relative.as_posix())
        payload = path.read_bytes()
        entries.append({
            "path": relative.as_posix(),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "size": len(payload),
        })
    manifest = {
        "schema_version": 1,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "files": sorted(entries, key=lambda item: item["path"]),
    }
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.yaml", yaml.safe_dump(manifest, sort_keys=False))
        for entry in manifest["files"]:
            archive.write(root / Path(entry["path"]), entry["path"])
    return bundle_path


def verify_and_extract(bundle_path: Path, destination: Path) -> list[Path]:
    with zipfile.ZipFile(bundle_path) as archive:
        names = archive.namelist()
        if names.count("manifest.yaml") != 1:
            raise ValueError("bundle must contain exactly one manifest.yaml")
        manifest = yaml.safe_load(archive.read("manifest.yaml"))
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
            raise ValueError("unsupported artifact manifest")
        entries = manifest.get("files")
        if not isinstance(entries, list):
            raise ValueError("manifest files must be a list")
        expected = {"manifest.yaml"}
        outputs = []
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "size"}:
                raise ValueError("invalid manifest file entry")
            relative = _safe_generated_path(entry["path"])
            expected.add(relative.as_posix())
            payload = archive.read(relative.as_posix())
            if len(payload) != entry["size"] or hashlib.sha256(payload).hexdigest() != entry["sha256"]:
                raise ValueError(f"artifact hash mismatch: {relative}")
            target = destination.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            outputs.append(target)
        if set(names) != expected or len(names) != len(expected):
            raise ValueError("bundle contains unmanifested or duplicate entries")
        return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["verify-extract"])
    parser.add_argument("bundle", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    for path in verify_and_extract(args.bundle, args.destination):
        print(path)


if __name__ == "__main__":
    main()
