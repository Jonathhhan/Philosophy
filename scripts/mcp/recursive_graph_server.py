#!/usr/bin/env python3
"""Read-only MCP server for the declared Recursive Codex project graph."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field

from recursive_graph_core import build_graph


NodeKind = Literal[
    "concept",
    "historical_concept",
    "decision",
    "change_event",
    "file",
    "directory",
    "source",
    "invalid_path",
]
Direction = Literal["outgoing", "incoming", "both"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GraphNode(StrictModel):
    id: str
    kind: NodeKind
    label: str
    declared: bool
    metadata: dict[str, Any]


class TraceNode(GraphNode):
    depth: int


class GraphEdge(StrictModel):
    id: str
    source: str
    relation: str
    target: str
    declared_in: str
    field: str
    metadata: dict[str, Any]


class GraphSummaryResult(StrictModel):
    node_count: int
    edge_count: int
    nodes_by_kind: dict[str, int]
    edges_by_relation: dict[str, int]
    event_edges_by_status: dict[str, int]
    undeclared_nodes: list[str]
    missing_path_nodes: list[str]
    diagnostics: list[str]
    partial: bool
    scope: str


class SearchNodesResult(StrictModel):
    count: int
    results: list[GraphNode]
    truncated: bool
    partial: bool
    diagnostics: list[str]


class GetNodeResult(StrictModel):
    node: GraphNode
    outgoing: list[GraphEdge]
    incoming: list[GraphEdge]
    partial: bool
    diagnostics: list[str]


class TraceRelationsResult(StrictModel):
    start: str
    direction: Direction
    max_depth: int
    relation_filter: list[str]
    nodes: list[TraceNode]
    edges: list[GraphEdge]
    truncated: bool
    partial: bool
    diagnostics: list[str]


ROOT = Path(__file__).resolve().parents[2]
READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)
INSTRUCTIONS = (
    "Use this read-only graph only for relations explicitly declared in project YAML. "
    "Undeclared placeholder nodes mark gaps, not inferred concepts. Every edge includes "
    "declaration provenance and event status where applicable. The graph does not prove "
    "philosophical completeness: read cited files before changing theory."
)

mcp = FastMCP("recursive-project-graph", instructions=INSTRUCTIONS, log_level="WARNING")


def current_graph():
    return build_graph(ROOT)


@mcp.tool(
    title="Summarize declared project graph",
    description=(
        "Summarize node kinds, relation types, event-edge status, undeclared references, "
        "missing project paths, and graph diagnostics."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def graph_summary() -> GraphSummaryResult:
    return GraphSummaryResult.model_validate(current_graph().summary())


@mcp.tool(
    title="Search graph nodes",
    description=(
        "Find nodes by ID, label, or declared status text. kind and status are exact filters; "
        "use this before get_node when the stable typed node ID is unknown."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def search_nodes(
    query: Annotated[str, Field(max_length=200)] = "",
    kind: NodeKind | None = None,
    status: Annotated[str | None, Field(max_length=100)] = None,
    limit: Annotated[int, Field(ge=1, le=100)] = 25,
) -> SearchNodesResult:
    result = current_graph().search(query, kind=kind, status=status, limit=limit)
    return SearchNodesResult.model_validate(result)


@mcp.tool(
    title="Get graph node and direct relations",
    description=(
        "Return one node plus all directly incoming and outgoing declared edges, including "
        "declared_in and exact YAML field provenance. Accepts typed IDs or an unambiguous raw ID/path."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def get_node(node_id: Annotated[str, Field(min_length=1, max_length=500)]) -> GetNodeResult:
    return GetNodeResult.model_validate(current_graph().get(node_id))


@mcp.tool(
    title="Trace declared project relations",
    description=(
        "Traverse only explicitly declared edges. Direction controls traversal, not declaration "
        "direction; transitive paths are never returned as new direct relations."
    ),
    annotations=READ_ONLY,
    structured_output=True,
)
def trace_relations(
    start_id: Annotated[str, Field(min_length=1, max_length=500)],
    direction: Direction = "both",
    max_depth: Annotated[int, Field(ge=0, le=4)] = 2,
    relations: list[str] | None = None,
    max_nodes: Annotated[int, Field(ge=1, le=200)] = 50,
) -> TraceRelationsResult:
    result = current_graph().trace(
        start_id,
        direction=direction,
        max_depth=max_depth,
        relations=relations,
        max_nodes=max_nodes,
    )
    return TraceRelationsResult.model_validate(result)


if __name__ == "__main__":
    mcp.run(transport="stdio")
