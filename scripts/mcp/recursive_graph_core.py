#!/usr/bin/env python3
"""Build a read-only graph from explicitly declared project YAML relations."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, deque
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Literal

import yaml


Direction = Literal["outgoing", "incoming", "both"]


def scalar(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): scalar(item) for key, item in value.items()}
    if isinstance(value, list):
        return [scalar(item) for item in value]
    return value


def declared_string_list(
    value: Any,
    diagnostics: list[str],
    declared_in: str,
    field: str,
) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        diagnostics.append(f"{declared_in}: {field} must be a list")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            diagnostics.append(f"{declared_in}: {field}[{index}] must be a non-empty string")
            continue
        result.append(item)
    return result


def load_mapping(path: Path, root: Path, diagnostics: list[str]) -> dict[str, Any] | None:
    relative = path.relative_to(root).as_posix()
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        diagnostics.append(f"{relative}: {exc}")
        return None
    if not isinstance(value, dict):
        diagnostics.append(f"{relative}: document root is not a mapping")
        return None
    return value


class ProjectGraph:
    """In-memory graph whose edges retain their declaration provenance."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []
        self.diagnostics: list[str] = []
        self._edge_ids: set[str] = set()
        self._aliases: dict[str, set[str]] = {}

    def _alias(self, alias: str, node_id: str) -> None:
        if alias:
            self._aliases.setdefault(alias.casefold(), set()).add(node_id)

    def add_node(
        self,
        node_id: str,
        kind: str,
        label: str,
        *,
        declared: bool,
        metadata: dict[str, Any] | None = None,
        aliases: Iterable[str] = (),
    ) -> dict[str, Any]:
        normalized_metadata = scalar(metadata or {})
        existing = self.nodes.get(node_id)
        if existing is None:
            existing = {
                "id": node_id,
                "kind": kind,
                "label": label,
                "declared": declared,
                "metadata": normalized_metadata,
            }
            self.nodes[node_id] = existing
        else:
            if declared and not existing["declared"]:
                existing["label"] = label
                existing["kind"] = kind
                existing["metadata"] = normalized_metadata
            elif declared:
                existing["metadata"].update(normalized_metadata)
            existing["declared"] = bool(existing["declared"] or declared)

        self._alias(node_id, node_id)
        self._alias(label, node_id)
        for alias in aliases:
            self._alias(alias, node_id)
        return existing

    def add_project_path_node(self, project_path: str) -> str:
        raw = project_path.replace("\\", "/").strip()
        directory_hint = raw.endswith("/")
        pure = PurePosixPath(raw.rstrip("/"))
        invalid_reason: str | None = None
        if not raw:
            invalid_reason = "empty path"
        elif pure.is_absolute() or raw.startswith("//") or re.match(r"^[A-Za-z]:/", raw):
            invalid_reason = "absolute path is not allowed"
        elif ".." in pure.parts:
            invalid_reason = "parent traversal is not allowed"

        parts = tuple(part for part in pure.parts if part not in {"", "."})
        normalized = "/".join(parts) + ("/" if directory_hint else "")
        if invalid_reason is None:
            resolved = (self.root.joinpath(*parts)).resolve(strict=False)
            try:
                resolved.relative_to(self.root)
            except ValueError:
                invalid_reason = "resolved path leaves the project root"

        if invalid_reason is not None:
            digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
            node_id = f"invalid_path:{digest}"
            self.add_node(
                node_id,
                "invalid_path",
                raw,
                declared=True,
                metadata={"path": raw, "exists": False, "invalid_reason": invalid_reason},
                aliases=(raw,),
            )
            self.diagnostics.append(f"invalid declared project path {raw!r}: {invalid_reason}")
            return node_id

        kind = "directory" if directory_hint else "file"
        node_id = f"{kind}:{normalized}"
        self.add_node(
            node_id,
            kind,
            normalized,
            declared=True,
            metadata={"path": normalized, "path_type": kind, "exists": resolved.exists()},
            aliases=(normalized,),
        )
        return node_id

    def add_source_node(self, label: str) -> str:
        digest = hashlib.sha256(label.encode("utf-8")).hexdigest()[:16]
        node_id = f"source:{digest}"
        self.add_node(node_id, "source", label, declared=True, metadata={"citation": label, "verified": False})
        return node_id

    def add_edge(
        self,
        source: str,
        relation: str,
        target: str,
        *,
        declared_in: str,
        field: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = {
            "source": source,
            "relation": relation,
            "target": target,
            "declared_in": declared_in.replace("\\", "/"),
            "field": field,
            "metadata": scalar(metadata or {}),
        }
        digest_source = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        edge_id = f"edge:{hashlib.sha256(digest_source.encode('utf-8')).hexdigest()[:20]}"
        if edge_id in self._edge_ids:
            return next(edge for edge in self.edges if edge["id"] == edge_id)
        edge = {"id": edge_id, **payload}
        self._edge_ids.add(edge_id)
        self.edges.append(edge)
        return edge

    def resolve_node_id(self, reference: str) -> str:
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError("node reference must be a non-empty string")
        value = reference.strip()
        if value in self.nodes:
            return value
        candidates = sorted(self._aliases.get(value.casefold(), set()))
        if not candidates:
            normalized = value.replace("\\", "/")
            for prefix in ("file", "directory"):
                path_id = f"{prefix}:{normalized}"
                if path_id in self.nodes:
                    return path_id
            raise ValueError(f"unknown node reference: {reference}")
        if len(candidates) > 1:
            raise ValueError(f"ambiguous node reference {reference!r}: {', '.join(candidates)}")
        return candidates[0]

    def resolve_declared_reference(self, reference: str) -> str:
        value = reference.strip()
        for prefix in (
            "concept:",
            "historical:",
            "decision:",
            "change:",
            "file:",
            "directory:",
            "source:",
        ):
            if value.startswith(prefix):
                return value
        if "/" in value or "\\" in value or value.endswith((".md", ".yaml", ".json", ".py", ".toml")):
            return self.add_project_path_node(value)
        if value.startswith("decision-"):
            node_id = f"decision:{value}"
            self.add_node(node_id, "decision", value, declared=False, metadata={}, aliases=(value,))
            return node_id
        if value.startswith("change-"):
            node_id = f"change:{value}"
            self.add_node(node_id, "change_event", value, declared=False, metadata={}, aliases=(value,))
            return node_id
        node_id = f"concept:{value}"
        self.add_node(node_id, "concept", value, declared=False, metadata={"status": "undeclared"}, aliases=(value,))
        return node_id

    def summary(self) -> dict[str, Any]:
        kind_counts = Counter(node["kind"] for node in self.nodes.values())
        relation_counts = Counter(edge["relation"] for edge in self.edges)
        event_status_counts = Counter(
            str(edge["metadata"]["event_status"])
            for edge in self.edges
            if edge["metadata"].get("event_status")
        )
        undeclared = sorted(node["id"] for node in self.nodes.values() if not node["declared"])
        missing_files = sorted(
            node["id"]
            for node in self.nodes.values()
            if node["kind"] in {"file", "directory"} and not node["metadata"].get("exists", False)
        )
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes_by_kind": dict(sorted(kind_counts.items())),
            "edges_by_relation": dict(sorted(relation_counts.items())),
            "event_edges_by_status": dict(sorted(event_status_counts.items())),
            "undeclared_nodes": undeclared,
            "missing_path_nodes": missing_files,
            "diagnostics": sorted(self.diagnostics),
            "partial": bool(self.diagnostics),
            "scope": "explicit YAML declarations and their file provenance; no manuscript-text inference",
        }

    def search(
        self,
        query: str = "",
        *,
        kind: str | None = None,
        status: str | None = None,
        limit: int = 25,
    ) -> dict[str, Any]:
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        needle = query.casefold().strip()
        matches: list[dict[str, Any]] = []
        for node in self.nodes.values():
            if kind and node["kind"] != kind:
                continue
            node_status = str(node["metadata"].get("status", ""))
            if status and node_status != status:
                continue
            haystack = " ".join((node["id"], node["label"], node_status)).casefold()
            if needle and needle not in haystack:
                continue
            matches.append(node)
        matches.sort(key=lambda item: (item["kind"], item["label"].casefold(), item["id"]))
        return {
            "count": len(matches),
            "results": matches[:limit],
            "truncated": len(matches) > limit,
            "partial": bool(self.diagnostics),
            "diagnostics": sorted(self.diagnostics),
        }

    def get(self, reference: str) -> dict[str, Any]:
        node_id = self.resolve_node_id(reference)
        outgoing = sorted(
            (edge for edge in self.edges if edge["source"] == node_id),
            key=lambda item: (item["relation"], item["target"], item["id"]),
        )
        incoming = sorted(
            (edge for edge in self.edges if edge["target"] == node_id),
            key=lambda item: (item["relation"], item["source"], item["id"]),
        )
        return {
            "node": self.nodes[node_id],
            "outgoing": outgoing,
            "incoming": incoming,
            "partial": bool(self.diagnostics),
            "diagnostics": sorted(self.diagnostics),
        }

    def trace(
        self,
        reference: str,
        *,
        direction: Direction = "both",
        max_depth: int = 2,
        relations: list[str] | None = None,
        max_nodes: int = 50,
    ) -> dict[str, Any]:
        if direction not in {"outgoing", "incoming", "both"}:
            raise ValueError("direction must be outgoing, incoming, or both")
        if max_depth < 0 or max_depth > 4:
            raise ValueError("max_depth must be between 0 and 4")
        if max_nodes < 1 or max_nodes > 200:
            raise ValueError("max_nodes must be between 1 and 200")
        relation_filter = set(relations or [])
        start = self.resolve_node_id(reference)
        queue: deque[tuple[str, int]] = deque([(start, 0)])
        visited: dict[str, int] = {start: 0}
        selected_edges: dict[str, dict[str, Any]] = {}
        truncated = False

        while queue:
            current, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for edge in self.edges:
                if relation_filter and edge["relation"] not in relation_filter:
                    continue
                neighbor: str | None = None
                if direction in {"outgoing", "both"} and edge["source"] == current:
                    neighbor = edge["target"]
                elif direction in {"incoming", "both"} and edge["target"] == current:
                    neighbor = edge["source"]
                if neighbor is None:
                    continue
                if neighbor not in visited:
                    if len(visited) >= max_nodes:
                        truncated = True
                        continue
                    visited[neighbor] = depth + 1
                    queue.append((neighbor, depth + 1))
                selected_edges[edge["id"]] = edge

        nodes = [self.nodes[node_id] | {"depth": visited[node_id]} for node_id in sorted(visited)]
        edges = [selected_edges[edge_id] for edge_id in sorted(selected_edges)]
        return {
            "start": start,
            "direction": direction,
            "max_depth": max_depth,
            "relation_filter": sorted(relation_filter),
            "nodes": nodes,
            "edges": edges,
            "truncated": truncated,
            "partial": bool(self.diagnostics),
            "diagnostics": sorted(self.diagnostics),
        }


def build_graph(root: Path) -> ProjectGraph:
    graph = ProjectGraph(root)
    concept_dir = graph.root / "knowledge" / "concepts"
    decision_dir = graph.root / "knowledge" / "decisions"
    event_dir = graph.root / "knowledge" / "change-events"

    concept_records: list[tuple[Path, dict[str, Any]]] = []
    decision_records: list[tuple[Path, dict[str, Any]]] = []
    event_records: list[tuple[Path, dict[str, Any]]] = []

    for path in sorted(concept_dir.glob("*.yaml")):
        data = load_mapping(path, graph.root, graph.diagnostics)
        if data is None:
            continue
        relative = path.relative_to(graph.root).as_posix()
        if not isinstance(data.get("id"), str) or not data["id"].strip():
            graph.diagnostics.append(f"{relative}: concept id must be a non-empty string")
            continue
        concept_id = data["id"]
        metadata = {
            key: data[key]
            for key in ("status", "chapter", "definition", "working_definition", "central_claim", "constraints")
            if key in data
        }
        graph.add_node(
            f"concept:{concept_id}",
            "concept",
            str(data.get("label") or concept_id),
            declared=True,
            metadata=metadata,
            aliases=(concept_id,),
        )
        graph.add_project_path_node(relative)
        concept_records.append((path, data))

    for path in sorted(decision_dir.glob("*.yaml")):
        data = load_mapping(path, graph.root, graph.diagnostics)
        if data is None:
            continue
        relative = path.relative_to(graph.root).as_posix()
        if not isinstance(data.get("id"), str) or not data["id"].strip():
            graph.diagnostics.append(f"{relative}: decision id must be a non-empty string")
            continue
        decision_id = data["id"]
        metadata = {
            key: data[key]
            for key in ("date", "title", "status", "decision", "reason")
            if key in data
        }
        graph.add_node(
            f"decision:{decision_id}",
            "decision",
            str(data.get("title") or decision_id),
            declared=True,
            metadata=metadata,
            aliases=(decision_id,),
        )
        graph.add_project_path_node(relative)
        decision_records.append((path, data))

    for path in sorted(event_dir.glob("*.yaml")):
        data = load_mapping(path, graph.root, graph.diagnostics)
        if data is None:
            continue
        relative = path.relative_to(graph.root).as_posix()
        if not isinstance(data.get("id"), str) or not data["id"].strip():
            graph.diagnostics.append(f"{relative}: change-event id must be a non-empty string")
            continue
        event_id = data["id"]
        metadata = {
            key: data[key]
            for key in ("created_at", "goal", "operation", "status", "authority", "possibilities", "uncertainties")
            if key in data
        }
        graph.add_node(
            f"change:{event_id}",
            "change_event",
            str(data.get("goal") or event_id),
            declared=True,
            metadata=metadata,
            aliases=(event_id,),
        )
        graph.add_project_path_node(relative)
        event_records.append((path, data))

    relation_graph_path = graph.root / "knowledge" / "concept-relations.yaml"
    relation_graph = load_mapping(relation_graph_path, graph.root, graph.diagnostics)
    if relation_graph is not None:
        relative = relation_graph_path.relative_to(graph.root).as_posix()
        relation_file_id = graph.add_project_path_node(relative)
        graph.nodes[relation_file_id]["metadata"].update(
            {
                "graph_status": relation_graph.get("status"),
                "purpose": relation_graph.get("purpose"),
                "open_questions": scalar(relation_graph.get("open_questions", [])),
            }
        )

        historical_nodes = relation_graph.get("nodes")
        if not isinstance(historical_nodes, list):
            graph.diagnostics.append(f"{relative}: nodes must be a list")
            historical_nodes = []
        for index, item in enumerate(historical_nodes):
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                graph.diagnostics.append(f"{relative}: nodes[{index}] must contain a string id")
                continue
            historical_id = item["id"]
            node_id = f"historical:{historical_id}"
            graph.add_node(
                node_id,
                "historical_concept",
                historical_id,
                declared=True,
                metadata={
                    "stage": item.get("stage"),
                    "minimal_definition": item.get("minimal_definition"),
                    "evidence": item.get("evidence", []),
                    "status": item.get("status"),
                    "graph_status": relation_graph.get("status"),
                },
                aliases=(f"historical:{historical_id}",),
            )
            graph.add_edge(
                node_id,
                "declared_in",
                relation_file_id,
                declared_in=relative,
                field=f"nodes[{index}]",
            )

        historical_edges = relation_graph.get("edges")
        if not isinstance(historical_edges, list):
            graph.diagnostics.append(f"{relative}: edges must be a list")
            historical_edges = []
        for index, item in enumerate(historical_edges):
            if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in ("from", "to", "type")):
                graph.diagnostics.append(f"{relative}: edges[{index}] requires string from, to, and type")
                continue
            source_id = f"historical:{item['from']}"
            target_id = f"historical:{item['to']}"
            for node_id, label in ((source_id, item["from"]), (target_id, item["to"])):
                if node_id not in graph.nodes:
                    graph.add_node(
                        node_id,
                        "historical_concept",
                        label,
                        declared=False,
                        metadata={"status": "undeclared_in_concept_relations"},
                    )
            graph.add_edge(
                source_id,
                item["type"],
                target_id,
                declared_in=relative,
                field=f"edges[{index}]",
                metadata={
                    "basis": item.get("basis"),
                    "evidence": item.get("evidence", []),
                    "graph_status": relation_graph.get("status"),
                },
            )

        translations = relation_graph.get("book_translations")
        if not isinstance(translations, list):
            graph.diagnostics.append(f"{relative}: book_translations must be a list")
            translations = []
        for index, item in enumerate(translations):
            if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in ("from", "to", "relation")):
                graph.diagnostics.append(
                    f"{relative}: book_translations[{index}] requires string from, to, and relation"
                )
                continue
            source_id = f"historical:{item['from']}"
            target_id = f"historical:{item['to']}"
            for node_id, label in ((source_id, item["from"]), (target_id, item["to"])):
                if node_id not in graph.nodes:
                    graph.add_node(
                        node_id,
                        "historical_concept",
                        label,
                        declared=False,
                        metadata={"status": "undeclared_in_concept_relations"},
                    )
            graph.add_edge(
                source_id,
                item["relation"],
                target_id,
                declared_in=relative,
                field=f"book_translations[{index}]",
                metadata={
                    "rule": item.get("rule"),
                    "graph_status": relation_graph.get("status"),
                },
            )

    for path, data in concept_records:
        relative = path.relative_to(graph.root).as_posix()
        source = f"concept:{data['id']}"
        graph.add_edge(source, "declared_in", f"file:{relative}", declared_in=relative, field="$document")
        for field in ("depends_on", "required_for", "related"):
            for index, reference in enumerate(declared_string_list(data.get(field), graph.diagnostics, relative, field)):
                target = graph.resolve_declared_reference(reference)
                graph.add_edge(source, field, target, declared_in=relative, field=f"{field}[{index}]")
        for index, project_path in enumerate(declared_string_list(data.get("source_files"), graph.diagnostics, relative, "source_files")):
            target = graph.add_project_path_node(project_path)
            graph.add_edge(source, "sourced_from", target, declared_in=relative, field=f"source_files[{index}]")

    for path, data in decision_records:
        relative = path.relative_to(graph.root).as_posix()
        source = f"decision:{data['id']}"
        graph.add_edge(source, "declared_in", f"file:{relative}", declared_in=relative, field="$document")
        for index, project_path in enumerate(declared_string_list(data.get("affected"), graph.diagnostics, relative, "affected")):
            target = graph.add_project_path_node(project_path)
            graph.add_edge(source, "affects", target, declared_in=relative, field=f"affected[{index}]")
        for index, reference in enumerate(declared_string_list(data.get("supersedes"), graph.diagnostics, relative, "supersedes")):
            target = graph.resolve_declared_reference(reference)
            graph.add_edge(source, "supersedes", target, declared_in=relative, field=f"supersedes[{index}]")

    for path, data in event_records:
        relative = path.relative_to(graph.root).as_posix()
        source = f"change:{data['id']}"
        graph.add_edge(source, "declared_in", f"file:{relative}", declared_in=relative, field="$document")

        scope = data.get("scope") if isinstance(data.get("scope"), dict) else {}
        if not isinstance(data.get("scope"), dict):
            graph.diagnostics.append(f"{relative}: scope must be a mapping")
        for index, project_path in enumerate(declared_string_list(scope.get("allowed_files"), graph.diagnostics, relative, "scope.allowed_files")):
            target = graph.add_project_path_node(project_path)
            graph.add_edge(source, "allows_change_to", target, declared_in=relative, field=f"scope.allowed_files[{index}]")
        for index, project_path in enumerate(declared_string_list(scope.get("protected_files"), graph.diagnostics, relative, "scope.protected_files")):
            target = graph.add_project_path_node(project_path)
            graph.add_edge(source, "protects", target, declared_in=relative, field=f"scope.protected_files[{index}]")

        basis = data.get("basis") if isinstance(data.get("basis"), dict) else {}
        if not isinstance(data.get("basis"), dict):
            graph.diagnostics.append(f"{relative}: basis must be a mapping")
        for index, project_path in enumerate(declared_string_list(basis.get("project_files"), graph.diagnostics, relative, "basis.project_files")):
            target = graph.add_project_path_node(project_path)
            graph.add_edge(source, "based_on", target, declared_in=relative, field=f"basis.project_files[{index}]")
        for index, reference in enumerate(declared_string_list(basis.get("decisions"), graph.diagnostics, relative, "basis.decisions")):
            target = graph.resolve_declared_reference(reference)
            graph.add_edge(source, "based_on_decision", target, declared_in=relative, field=f"basis.decisions[{index}]")
        for index, citation in enumerate(declared_string_list(basis.get("sources"), graph.diagnostics, relative, "basis.sources")):
            target = graph.add_source_node(citation)
            graph.add_edge(source, "sourced_from", target, declared_in=relative, field=f"basis.sources[{index}]")

        changes = data.get("changes") if isinstance(data.get("changes"), list) else []
        if not isinstance(data.get("changes"), list):
            graph.diagnostics.append(f"{relative}: changes must be a list")
        for index, change in enumerate(changes):
            if not isinstance(change, dict) or not isinstance(change.get("file"), str):
                graph.diagnostics.append(f"{relative}: changes[{index}] requires a string file")
                continue
            target = graph.add_project_path_node(change["file"])
            graph.add_edge(
                source,
                "changes",
                target,
                declared_in=relative,
                field=f"changes[{index}]",
                metadata={"summary": change.get("summary")},
            )

        relations = data.get("affected_relations") if isinstance(data.get("affected_relations"), list) else []
        if not isinstance(data.get("affected_relations"), list):
            graph.diagnostics.append(f"{relative}: affected_relations must be a list")
        for index, relation in enumerate(relations):
            if not isinstance(relation, dict) or not all(
                isinstance(relation.get(key), str) for key in ("from", "relation", "to")
            ):
                graph.diagnostics.append(
                    f"{relative}: affected_relations[{index}] requires string from, relation, and to"
                )
                continue
            edge_source = graph.resolve_declared_reference(relation["from"])
            edge_target = graph.resolve_declared_reference(relation["to"])
            graph.add_edge(
                edge_source,
                relation["relation"],
                edge_target,
                declared_in=relative,
                field=f"affected_relations[{index}]",
                metadata={
                    "event_node": source,
                    "event_id": data["id"],
                    "event_status": data.get("status"),
                    "effect": relation.get("effect"),
                    "note": relation.get("note"),
                },
            )


    graph.edges.sort(key=lambda edge: edge["id"])
    return graph
