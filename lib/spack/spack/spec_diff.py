# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Compare two concrete specs, and localize where their DAGs diverge.

Nodes are compared for "visible" DAG properties first, and only after that first pass, for
changes in package recipes or other attributes.
"""

import collections
import enum
from typing import Any, Callable, Dict, List, Mapping, NamedTuple, Optional, Set, Tuple

import spack.deptypes as dt
import spack.error
import spack.util.spack_json as sjson
from spack.spec import Spec

#: Architecture sub-parts compared independently so a diff can point at the exact part.
_ARCH_PARTS = ("platform", "os", "target")


class SpecDiffError(spack.error.SpackError):
    """Raised when two specs cannot be compared."""


class DiffCategory(enum.Enum):
    """Which node-local property differs between two nodes."""

    VERSION = "version"
    NAMESPACE = "namespace"
    ARCHITECTURE = "architecture"
    VARIANT = "variant"
    FLAGS = "flags"
    DEPENDENCY = "dependency"
    EXTERNAL = "external"
    RECIPE = "recipe"
    OTHER = "other"


_PRUNING_SUBDAGS = frozenset(
    {
        DiffCategory.VERSION,
        DiffCategory.NAMESPACE,
        DiffCategory.ARCHITECTURE,
        DiffCategory.VARIANT,
        DiffCategory.FLAGS,
        DiffCategory.DEPENDENCY,
        DiffCategory.EXTERNAL,
    }
)


class AttributeDiff(NamedTuple):
    """A single differing node-local property, described in display form."""

    category: DiffCategory
    #: sub-key within the category (variant name, arch part, flag type, dep name); may be ""
    key: str
    #: value on side a, or "" when absent
    value_a: str
    #: value on side b, or "" when absent
    value_b: str


class NodeDivergence(NamedTuple):
    """A node where the two DAGs diverge."""

    node_a: Spec
    node_b: Spec
    attributes: List[AttributeDiff]


#: (hash_a, hash_b) -> (list of diffs)
ComparisonCache = Dict[Tuple[str, str], List[AttributeDiff]]


def recorded_package_hash(node: Spec) -> Optional[str]:
    """Returns the package hash of a concrete node, or None if it does not have one."""
    return getattr(node, "_package_hash", None)


def _serialize(value) -> str:
    """Render a piece of node state for display."""
    if not value:
        return ""
    return sjson.dumps(value) if isinstance(value, (dict, list)) else str(value)


def _direct_children(node: Spec) -> Dict[str, Spec]:
    """Map each direct dependency name to its spec.

    Raises:
        SpecDiffError: if the node has edges to two different specs of the same name
    """
    children: Dict[str, Spec] = {}
    for edge in node.edges_to_dependencies():
        current = children.setdefault(edge.spec.name, edge.spec)
        if current.dag_hash() != edge.spec.dag_hash():
            raise SpecDiffError(
                f"cannot compare '{node.name}': comparing split dependencies is not supported yet",
                f"it has edges to two different '{edge.spec.name}' specs "
                f"({current.dag_hash(7)}, {edge.spec.dag_hash(7)}).",
            )
    return children


class EdgeSignature(NamedTuple):
    """Aggregated attributes of the direct edges from a node to one dependency name."""

    depflag: dt.DepFlag
    virtuals: Tuple[str, ...]

    def __str__(self) -> str:
        """Renders as spec edge attributes, so it can be used inside a ``%[...]name`` literal."""
        parts = ["deptypes=" + ",".join(dt.flag_to_tuple(self.depflag))]
        if self.virtuals:
            parts.append("virtuals=" + ",".join(self.virtuals))
        return " ".join(parts)


def _edge_signatures(node: Spec) -> Dict[str, EdgeSignature]:
    """Map each direct dependency name to its aggregated edge attributes.

    Only the edge is captured, not the child's contents, so a dependency being added, removed,
    or re-typed shows up here while a mere change deeper inside a dependency does not (that is
    found by descending).
    """
    aggregated: Dict[str, Tuple[dt.DepFlag, Set[str]]] = {}
    for edge in node.edges_to_dependencies():
        name = edge.spec.name
        depflag, virtuals = aggregated.get(name, (0, set()))
        aggregated[name] = (depflag | edge.depflag, virtuals | set(edge.virtuals))

    return {
        name: EdgeSignature(depflag, tuple(sorted(virtuals)))
        for name, (depflag, virtuals) in aggregated.items()
    }


def _text(value) -> str:
    """Default rendering of a compared value, with an absent one rendered as nothing."""
    return "" if value is None else str(value)


def _join(values) -> str:
    """Rendering of a compared value that is a sequence of words, absent or not."""
    return " ".join(values or [])


def _attribute_difference(
    category: DiffCategory, key: str, value_a, value_b, render: Callable[[Any], str] = _text
) -> List[AttributeDiff]:
    """Compare one attribute of two nodes, as a list so it composes with _mapping_difference."""
    if value_a == value_b:
        return []
    return [AttributeDiff(category, key, render(value_a), render(value_b))]


def _mapping_difference(
    category: DiffCategory, map_a: Mapping, map_b: Mapping, render: Callable[[Any], str] = _text
) -> List[AttributeDiff]:
    """Compare two mappings key by key. The union of the keys is walked, so a key held by one side
    alone is reported too, against an empty value.
    """
    return [
        AttributeDiff(category, key, render(map_a.get(key)), render(map_b.get(key)))
        for key in sorted(set(map_a) | set(map_b))
        if map_a.get(key) != map_b.get(key)
    ]


def _architecture(node: Spec) -> Dict[str, Any]:
    """Architecture as its parts, so a diff can point at the one that changed."""
    return {part: getattr(node.architecture, part) for part in _ARCH_PARTS}


def _node_local_difference(node_a: Spec, node_b: Spec) -> List[AttributeDiff]:
    """Returns the node-local attribute differences (empty list if intrinsically equal)."""
    attributes = _attribute_difference(DiffCategory.VERSION, "", node_a.version, node_b.version)
    attributes += _attribute_difference(
        DiffCategory.NAMESPACE, "", node_a.namespace, node_b.namespace
    )
    attributes += _mapping_difference(
        DiffCategory.ARCHITECTURE, _architecture(node_a), _architecture(node_b)
    )
    attributes += _mapping_difference(DiffCategory.VARIANT, node_a.variants, node_b.variants)
    attributes += _mapping_difference(
        DiffCategory.FLAGS, node_a.compiler_flags, node_b.compiler_flags, render=_join
    )

    attributes += _attribute_difference(
        DiffCategory.EXTERNAL, "path", node_a.external_path, node_b.external_path
    )
    attributes += _attribute_difference(
        DiffCategory.EXTERNAL,
        "modules",
        node_a.external_modules,
        node_b.external_modules,
        render=_join,
    )
    attributes += _attribute_difference(
        DiffCategory.EXTERNAL,
        "attributes",
        node_a.extra_attributes,
        node_b.extra_attributes,
        render=_serialize,
    )

    attributes += _mapping_difference(
        DiffCategory.DEPENDENCY, _edge_signatures(node_a), _edge_signatures(node_b)
    )

    return attributes


def _serialized_difference(node_a: Spec, node_b: Spec) -> List[AttributeDiff]:
    """Checks OTHER differences between two nodes."""
    # Any state that lands in the hash without a comparison of its own surfaces here instead of
    # leaving the caller with two different hashes and nothing to say about them.
    dropped = {"dependencies", "package_hash", "name"}
    state_a = {k: v for k, v in node_a.to_node_dict().items() if k not in dropped}
    state_b = {k: v for k, v in node_b.to_node_dict().items() if k not in dropped}
    return _mapping_difference(DiffCategory.OTHER, state_a, state_b, render=_serialize)


def _compare_nodes(node_a: Spec, node_b: Spec) -> List[AttributeDiff]:
    """Returns what differs between two nodes, empty when nothing does."""
    attributes = _node_local_difference(node_a, node_b)
    if attributes:
        return attributes

    hash_a, hash_b = recorded_package_hash(node_a), recorded_package_hash(node_b)
    if hash_a and hash_b and hash_a != hash_b:
        return [AttributeDiff(DiffCategory.RECIPE, "", hash_a, hash_b)]

    return _serialized_difference(node_a, node_b)


def diff_concrete_dags(
    root_a: Spec, root_b: Spec, *, prune: bool = True, cache: Optional[ComparisonCache] = None
) -> List[NodeDivergence]:
    """Parallel BFS over two concrete DAGs, reporting divergent nodes.

    Both roots must be concrete, so node-local comparisons can rely on concrete-spec invariants
    (a fully specified architecture, a version, a namespace) without defensive fallbacks.

    Args:
        root_a: first concrete spec to compare
        root_b: second concrete spec to compare
        prune: when True stop at the first node difference and don't descend into subDAGs
        cache: comparisons of node pairs to reuse across calls

    Raises:
        SpecDiffError: if either of the two roots is not concrete
    """
    if not root_a.concrete or not root_b.concrete:
        raise SpecDiffError("diff_concrete_dags requires two concrete specs")

    if cache is None:
        cache = {}

    queue = collections.deque([(root_a, root_b)])
    visited, divergences = set(), []

    while queue:
        node_a, node_b = queue.popleft()

        key = (node_a.dag_hash(), node_b.dag_hash())
        if key in visited:
            continue
        visited.add(key)

        # Identical subtree: the dag hash covers build/link/run/test deps and the package
        # hash, so equal hashes guarantee identical subgraphs. Nothing to report.
        if key[0] == key[1]:
            continue

        if key not in cache:
            cache[key] = _compare_nodes(node_a, node_b)
        attributes = cache[key]

        if attributes:
            divergences.append(NodeDivergence(node_a, node_b, attributes))
            if prune and any(x.category in _PRUNING_SUBDAGS for x in attributes):
                continue

        # When pruning we are ensured that the two nodes have the same list of dependencies,
        # because any difference in that sense would be caught in the parent. When not pruning
        # using the intersection of nodes is what makes sense to compare.
        a_children = _direct_children(node_a)
        b_children = _direct_children(node_b)
        for name in sorted(set(a_children) & set(b_children)):
            queue.append((a_children[name], b_children[name]))

    return divergences


def node_sort_key(node: NodeDivergence) -> Tuple[str, str, str]:
    """Canonical order for divergent nodes, of which one package can have several instances."""
    return node.node_a.name, node.node_a.dag_hash(), node.node_b.dag_hash()


def node_to_dict(node: NodeDivergence) -> Dict[str, Any]:
    """Serialize a divergent node: the two dag hashes and the differing attributes."""
    return {
        "name": node.node_a.name,
        "hash_a": node.node_a.dag_hash(),
        "hash_b": node.node_b.dag_hash(),
        "attributes": [
            {
                "category": attribute.category.value,
                "key": attribute.key,
                "value_a": attribute.value_a,
                "value_b": attribute.value_b,
            }
            for attribute in node.attributes
        ],
    }
