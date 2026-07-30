#!/usr/bin/env python3
"""Core and STDIO protocol tests for the read-only recursive project graph."""

from __future__ import annotations

import asyncio
import hashlib
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
MCP_DIR = ROOT / "scripts" / "mcp"
SERVER = MCP_DIR / "recursive_graph_server.py"
sys.path.insert(0, str(MCP_DIR))

from recursive_graph_core import ProjectGraph, build_graph


EXPECTED_TOOLS = {"graph_summary", "search_nodes", "get_node", "trace_relations"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def snapshot() -> dict[str, str]:
    roots = [ROOT / ".agents", ROOT / ".codex", ROOT / "knowledge", ROOT / "scripts"]
    files = [ROOT / "requirements-dev.txt"]
    for base in roots:
        if not base.exists():
            continue
        files.extend(
            path
            for path in base.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
        )
    return {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(set(files))
    }


def test_core() -> None:
    graph = build_graph(ROOT)
    summary = graph.summary()
    require(not summary["partial"], f"graph must not be partial: {summary['diagnostics']}")
    require(summary["node_count"] > 100, "graph unexpectedly small")
    require(sum(summary["event_edges_by_status"].values()) > 0, "event edges not identified")
    require(summary["event_edges_by_status"].get("stabilized", 0) > 0, "stabilized event edges not identified")

    current = graph.get("concept:algorithmus")["node"]
    historical = graph.get("historical:algorithmus")["node"]
    require(current["declared"] and current["kind"] == "concept", "current algorithmus missing")
    require(historical["declared"] and historical["kind"] == "historical_concept", "historical algorithmus missing")
    require(graph.get("concept:montage")["node"]["declared"] is True, "current montage concept missing")
    require(graph.get("historical:montage")["node"]["declared"] is True, "historical montage missing")
    require(graph.get("directory:knowledge/")["node"]["kind"] == "directory", "directory path misclassified")

    algorithm_edges = graph.get("concept:algorithmus")["outgoing"]
    require(any(edge["relation"] == "depends_on" for edge in algorithm_edges), "depends_on edge missing")
    require(all("[" in edge["field"] or edge["field"] == "$document" for edge in algorithm_edges), "list provenance lacks index")
    require(
        any(edge["metadata"].get("event_status") in {"tested", "stabilized"} for edge in graph.edges),
        "affected relation event status missing",
    )

    bounded = graph.trace("concept:algorithmus", max_nodes=1)
    require(len(bounded["nodes"]) == 1 and len(bounded["edges"]) == 0 and bounded["truncated"], "trace boundary is inconsistent")

    safe_graph = ProjectGraph(ROOT)
    invalid_id = safe_graph.add_project_path_node("../outside-project")
    require(invalid_id.startswith("invalid_path:"), "parent traversal was accepted")
    require(safe_graph.diagnostics, "invalid path did not produce diagnostics")


async def test_protocol() -> None:
    before = snapshot()
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-B", str(SERVER)],
        cwd=ROOT / "interaktiv",
        encoding="utf-8",
        encoding_error_handler="strict",
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            initialized = await session.initialize()
            require(
                initialized.instructions is not None and "explicitly declared" in initialized.instructions,
                "server instructions missing declared-only boundary",
            )

            listed = await session.list_tools()
            tools = {tool.name: tool for tool in listed.tools}
            require(set(tools) == EXPECTED_TOOLS, f"unexpected tool set: {sorted(tools)}")
            for tool in tools.values():
                annotations = tool.annotations
                require(annotations is not None, f"{tool.name} annotations missing")
                require(annotations.readOnlyHint is True, f"{tool.name} is not marked read-only")
                require(annotations.destructiveHint is False, f"{tool.name} destructive hint incorrect")
                require(annotations.openWorldHint is False, f"{tool.name} open-world hint incorrect")
                require(tool.outputSchema is not None, f"{tool.name} output schema missing")
                require(tool.outputSchema.get("additionalProperties") is False, f"{tool.name} output schema is open")

            summary = await session.call_tool("graph_summary", {})
            require(not summary.isError and summary.structuredContent is not None, "graph_summary failed")
            require(summary.structuredContent["partial"] is False, "protocol summary unexpectedly partial")

            search = await session.call_tool("search_nodes", {"query": "algorithmus", "limit": 10})
            require(not search.isError and search.structuredContent is not None, "search_nodes failed")
            ids = {item["id"] for item in search.structuredContent["results"]}
            require({"concept:algorithmus", "historical:algorithmus"}.issubset(ids), "search omitted current or historical algorithmus")

            node = await session.call_tool("get_node", {"node_id": "concept:algorithmus"})
            require(not node.isError and node.structuredContent is not None, "get_node failed")
            require(node.structuredContent["node"]["id"] == "concept:algorithmus", "get_node returned wrong node")

            trace = await session.call_tool(
                "trace_relations",
                {
                    "start_id": "concept:algorithmus",
                    "direction": "outgoing",
                    "max_depth": 1,
                    "relations": ["depends_on"],
                    "max_nodes": 20,
                },
            )
            require(not trace.isError and trace.structuredContent is not None, "trace_relations failed")
            require(all(edge["relation"] == "depends_on" for edge in trace.structuredContent["edges"]), "trace filter failed")

            invalid = await session.call_tool("search_nodes", {"limit": 0})
            require(invalid.isError is True, "invalid bounded input was accepted")
            unknown = await session.call_tool("get_node", {"node_id": "concept:not-present"})
            require(unknown.isError is True, "unknown node was accepted")

    after = snapshot()
    require(before == after, "MCP server or protocol test modified repository files")


def main() -> int:
    test_core()
    asyncio.run(test_protocol())
    print("RECURSIVE GRAPH TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
