# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Compare two concrete environments.

The comparison has two independent layers:

1. Which input (user) specs are unique to each environment, and
2. Where the concrete DAGs of the ones they share diverge.

Only the first layer is specific to environments. The second is the generic spec comparison in
``spack.spec_diff``, which this module drives once per common input spec.
"""

from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import spack.environment.environment as ev
import spack.spec_diff
from spack.spec import Spec
from spack.util.lang import stable_partition

#: Version of the serialization produced by EnvironmentDiff.as_dict
DIFF_FORMAT_VERSION = 1


class UserSpecDivergence(NamedTuple):
    """The list of divergent nodes found for a single common user spec."""

    root: ev.UserSpecId
    nodes: List[spack.spec_diff.NodeDivergence]


class InputDiff(NamedTuple):
    """Comparison of the user specs of two environments."""

    only_in_a: List[ev.UserSpecId]
    only_in_b: List[ev.UserSpecId]
    common: List[ev.UserSpecId]


class EnvironmentDiff(NamedTuple):
    """Full result of comparing two concrete environments."""

    #: Separates the common user specs from the ones in only one of the two environments
    inputs: InputDiff
    #: Divergences for common inputs whose concrete DAGs differ
    divergences: List[UserSpecDivergence]
    #: Common inputs whose concrete roots differ, with no node to point at as the cause
    unresolved: List[ev.UserSpecId]

    def as_dict(self) -> Dict[str, Any]:
        """Canonical, deterministically ordered serialization of the comparison.

        One entry per user spec reaching a divergence; unlike the pretty output this does not
        merge equivalent findings, leaving a consumer free to group them as it sees fit. The
        identity of the two environments is the caller's to add, since it is not part of the
        comparison itself.
        """
        return {
            "_meta": {"file-type": "spack-environment-diff", "diff-version": DIFF_FORMAT_VERSION},
            "only_in_a": _roots_to_dict(self.inputs.only_in_a),
            "only_in_b": _roots_to_dict(self.inputs.only_in_b),
            "common": _roots_to_dict(self.inputs.common),
            "unresolved": _roots_to_dict(self.unresolved),
            "divergences": [
                {
                    "root": _root_to_dict(divergence.root),
                    "nodes": [
                        spack.spec_diff.node_to_dict(node)
                        for node in sorted(divergence.nodes, key=spack.spec_diff.node_sort_key)
                    ],
                }
                for divergence in sorted(self.divergences, key=lambda x: _root_sort_key(x.root))
            ],
        }


def input_spec_diff(roots_a: List[ev.UserSpecId], roots_b: List[ev.UserSpecId]) -> InputDiff:
    """Compare two lists of input specs by identity, preserving input order."""
    set_a, set_b = set(roots_a), set(roots_b)
    common, only_in_a = stable_partition(roots_a, lambda root: root in set_b)
    return InputDiff(
        only_in_a=only_in_a,
        only_in_b=[root for root in roots_b if root not in set_a],
        common=common,
    )


def _concretized_user_specs(env: ev.Environment) -> Dict[ev.UserSpecId, Spec]:
    """Map every user spec of an environment to the concrete spec it produced."""
    return {
        ev.UserSpecId(x.group, x.root): env.specs_by_hash[x.hash] for x in env.concretized_roots
    }


def _assert_comparable(env: ev.Environment, label: Optional[str] = None) -> None:
    """Raise if an environment is in a state this module cannot answer for.

    Args:
        env: environment to check
        label: how to name the environment in errors, when its own name would not mean anything
            to the caller (an environment materialized from a lockfile is a temporary directory)

    Raises:
        spack.environment.environment.SpackEnvironmentError: if the environment is not fully
            concretized, or was concretized before the package hash entered the dag hash
    """
    label = label or env.name

    # Asking for the roots left to concretize, rather than whether any were, catches specs added
    # since the last concretization, which would otherwise be dropped from the comparison silently
    concretized = {ev.UserSpecId(x.group, x.root) for x in env.concretized_roots}
    pending = sorted(str(x.spec) for x in env._all_user_specs_with_group() - concretized)
    if pending:
        raise ev.SpackEnvironmentError(
            f"environment '{label}' is not concretized. Run `spack concretize` first",
            "input specs not concretized:\n" + "\n".join(f"  {spec}" for spec in pending),
        )

    # Nodes without a package hash cannot be told apart when nothing in their configuration
    # differs, which is most of what this module reports. Rather than answer with a shrug on
    # every node, refuse the comparison.
    if any(not spack.spec_diff.recorded_package_hash(node) for node in env.all_specs_generator()):
        raise ev.SpackEnvironmentError(
            f"environment '{label}' was concretized by a version of Spack that did not record "
            f"package hashes (its lockfile predates them), so it cannot be compared",
            "Re-concretize it with `spack concretize --force` first.",
        )


def diff_environments(
    env_a: ev.Environment,
    env_b: ev.Environment,
    *,
    prune: bool = True,
    label_a: Optional[str] = None,
    label_b: Optional[str] = None,
) -> EnvironmentDiff:
    """Compare two concrete environments.

    Args:
        env_a: first concrete environment to compare
        env_b: second concrete environment to compare
        prune: when True, don't visit subDAGs when a difference on a node is found
        label_a: how to name the first environment in errors, defaulting to its own name
        label_b: how to name the second environment in errors, defaulting to its own name

    Raises:
        spack.environment.environment.SpackEnvironmentError: if either environment is not
            comparable
        spack.spec_diff.SpecDiffError: if two concrete DAGs cannot be compared
    """
    _assert_comparable(env_a, label_a)
    _assert_comparable(env_b, label_b)

    a_map = _concretized_user_specs(env_a)
    b_map = _concretized_user_specs(env_b)

    inputs = input_spec_diff(list(a_map), list(b_map))

    divergences: List[UserSpecDivergence] = []
    unresolved: List[ev.UserSpecId] = []
    # Input specs share most of their graph, so the same node pair is reached from many of them
    cache: spack.spec_diff.ComparisonCache = {}

    for root in inputs.common:
        concrete_a = a_map[root]
        concrete_b = b_map[root]
        nodes = spack.spec_diff.diff_concrete_dags(
            concrete_a, concrete_b, prune=prune, cache=cache
        )
        if nodes:
            divergences.append(UserSpecDivergence(root, nodes))
        elif concrete_a.dag_hash() != concrete_b.dag_hash():
            unresolved.append(root)

    return EnvironmentDiff(inputs=inputs, divergences=divergences, unresolved=unresolved)


def _root_sort_key(root: ev.UserSpecId) -> Tuple[str, str]:
    """Canonical order for user specs. The order they were concretized in is not stable."""
    return (root.group, str(root.spec))


def sorted_roots(roots: List[ev.UserSpecId]) -> List[ev.UserSpecId]:
    """Deduplicate and order user specs canonically.

    One user spec can reach several instances of the same package, so it can contribute more
    than once to an entry that merges them.
    """
    return sorted(set(roots), key=_root_sort_key)


def _root_to_dict(root: ev.UserSpecId) -> Dict[str, str]:
    """Serialize a user spec with its group as separate fields, for machine consumers."""
    return {"spec": str(root.spec), "group": root.group}


def _roots_to_dict(roots: List[ev.UserSpecId]) -> List[Dict[str, str]]:
    """Serialize a list of user specs, deduplicated and in canonical order."""
    return [_root_to_dict(root) for root in sorted_roots(roots)]
