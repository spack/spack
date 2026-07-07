# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Resolve abstract hash references in Specs to concrete specs.

This module is free of spack.solver imports. It locates matching specs by
searching the active environment, the installed store, the binary cache, and
configured externals (via spack.externals_config).
"""

from typing import List

import spack.binary_distribution
import spack.config
import spack.environment
import spack.error
import spack.externals_config
import spack.spec
import spack.store
from spack.enums import InstallRecordStatus


def _matching_external_specs(spec: "spack.spec.Spec") -> List["spack.spec.Spec"]:
    """Return configured externals from packages.yaml that match spec by abstract hash."""
    config = spack.config.CONFIG
    try:
        packages_with_externals = spack.externals_config.external_config_with_implicit_externals(
            config
        )
        completion_mode = config.get("concretizer:externals:completion")
        parser = spack.externals_config.create_external_parser(
            packages_with_externals, completion_mode
        )
    except spack.error.SpackError:
        return []
    return parser.query(spec)


def _lookup_one(spec: "spack.spec.Spec") -> "spack.spec.Spec":
    """Return the single concrete spec matching an abstract-hash spec.

    Searches in order: active environment, configured externals, installed store, binary cache.
    Raises InvalidHashError if nothing matches, AmbiguousHashError if more than one matches.
    """
    active_env = spack.environment.active_environment()

    matches = (
        (active_env.all_matching_specs(spec) if active_env else [])
        or _matching_external_specs(spec)
        or spack.store.STORE.db.query(spec, installed=InstallRecordStatus.ANY)
        or spack.binary_distribution.BinaryCacheQuery(True)(spec)
    )

    if not matches:
        raise spack.spec.InvalidHashError(spec, spec.abstract_hash)

    if len(matches) != 1:
        raise spack.spec.AmbiguousHashError(
            f"Multiple packages specify hash beginning '{spec.abstract_hash}'.", *matches
        )

    return matches[0]


def lookup_hash(spec: "spack.spec.Spec") -> "spack.spec.Spec":
    """Return a copy of spec with all abstract-hash nodes replaced by their concrete counterparts.

    Non-destructive: always returns a new Spec object. If spec is already concrete or has no
    abstract-hash nodes, returns spec unchanged.
    """
    if spec.concrete or not any(node.abstract_hash for node in spec.traverse()):
        return spec

    result = spec.copy(deps=False)
    if result.abstract_hash:
        result._dup(_lookup_one(spec))
        return result

    node_lookup = {
        id(node): _lookup_one(node) for node in spec.traverse(root=False) if node.abstract_hash
    }

    for edge in spec.traverse_edges(root=False):
        key = edge.parent.name
        current_node = result if key == result.name else result[key]
        child_node = node_lookup.get(id(edge.spec), edge.spec.copy())
        current_node._add_dependency(
            child_node, depflag=edge.depflag, virtuals=edge.virtuals, direct=edge.direct
        )

    return result


def replace_hash(spec: "spack.spec.Spec") -> None:
    """Populate spec in-place by resolving all abstract-hash nodes.

    Destructive counterpart to lookup_hash. No-op if spec has no abstract-hash nodes.
    """
    if not any(node for node in spec.traverse(order="post") if node.abstract_hash):
        return

    spec._dup(lookup_hash(spec))
