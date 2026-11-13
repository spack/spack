# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Compare two concrete environments.

Input specs are first matched across the two environments, then the concrete DAGs of each matched
pair are compared with ``spack.spec_diff``.
"""

import shlex
from typing import Any, Callable, Dict, Hashable, Iterable, List, NamedTuple, Optional, Set, Tuple

import spack.environment.environment as ev
import spack.spec_diff
from spack.spec import Spec
from spack.util.lang import index_by, stable_partition


class UserSpecDivergence(NamedTuple):
    """The divergent nodes found for an input spec matched in both environments."""

    root: ev.UserSpecId
    nodes: List[spack.spec_diff.NodeDivergence]


class ProviderChange(NamedTuple):
    """An input spec for a virtual package, provided by a different package on each side."""

    root: ev.UserSpecId
    spec_a: Spec
    spec_b: Spec


class InputChange(NamedTuple):
    """An input spec written differently in the two environments, paired by what it produced."""

    before: ev.UserSpecId
    after: ev.UserSpecId


class InputDiff(NamedTuple):
    """Comparison of the input specs of two environments."""

    only_in_a: List[ev.UserSpecId]
    only_in_b: List[ev.UserSpecId]
    common: List[ev.UserSpecId]
    changed: List[InputChange]


class EnvironmentDiff(NamedTuple):
    """Full result of comparing two concrete environments."""

    #: Matches the input specs of the two environments
    inputs: InputDiff
    #: Matched input specs provided by a different package on each side, not compared further
    providers: List[ProviderChange]
    #: Matched input specs whose concrete DAGs differ, with the nodes where they diverge
    divergences: List[UserSpecDivergence]
    #: Matched input specs whose concrete roots differ, with no node to point at as the cause
    unresolved: List[ev.UserSpecId]

    @property
    def equivalent(self) -> bool:
        """Whether the comparison found no difference between the two environments."""
        return not (
            self.inputs.only_in_a
            or self.inputs.only_in_b
            or self.inputs.changed
            or self.providers
            or self.divergences
            or self.unresolved
        )

    def as_dict(self) -> Dict[str, Any]:
        """Serialize the comparison in a deterministic order, without environment identities."""
        return {
            "_meta": {
                "file-type": "spack-environment-diff",
                "diff-version": spack.spec_diff.DIFF_FORMAT_VERSION,
            },
            "only_in_a": _roots_to_dict(self.inputs.only_in_a),
            "only_in_b": _roots_to_dict(self.inputs.only_in_b),
            "common": _roots_to_dict(self.inputs.common),
            "changed": [
                {"before": _root_to_dict(change.before), "after": _root_to_dict(change.after)}
                for change in sorted(self.inputs.changed, key=lambda x: root_sort_key(x.after))
            ],
            "providers": [
                {
                    "root": _root_to_dict(change.root),
                    "a": {"name": change.spec_a.name, "hash": change.spec_a.dag_hash()},
                    "b": {"name": change.spec_b.name, "hash": change.spec_b.dag_hash()},
                }
                for change in sorted(self.providers, key=lambda x: root_sort_key(x.root))
            ],
            "unresolved": _roots_to_dict(self.unresolved),
            "divergences": [
                {
                    "root": _root_to_dict(divergence.root),
                    "nodes": [
                        spack.spec_diff.node_to_dict(node)
                        for node in sorted(divergence.nodes, key=spack.spec_diff.node_sort_key)
                    ],
                }
                for divergence in sorted(self.divergences, key=lambda x: root_sort_key(x.root))
            ],
        }


def _unique_by(
    roots: List[ev.UserSpecId],
    concrete: Dict[ev.UserSpecId, Spec],
    spec_key: Callable[[Spec], Hashable],
) -> Dict[Hashable, ev.UserSpecId]:
    """Map each key that exactly one input spec has within its group to that input spec."""
    by_key = index_by(roots, lambda root: (root.group, spec_key(concrete[root])))
    return {key: matches[0] for key, matches in by_key.items() if len(matches) == 1}


def input_spec_diff(
    roots_a: Dict[ev.UserSpecId, Spec], roots_b: Dict[ev.UserSpecId, Spec]
) -> InputDiff:
    """Compare the input specs of two environments, each mapped to its concrete root."""
    common, only_in_a = stable_partition(list(roots_a), lambda root: root in roots_b)
    only_in_b = [root for root in roots_b if root not in roots_a]

    changed: List[InputChange] = []
    for spec_key in (lambda spec: spec.dag_hash(), lambda spec: spec.name):
        unique_b = _unique_by(only_in_b, roots_b, spec_key)
        pairs = [
            InputChange(root, unique_b[key])
            for key, root in _unique_by(only_in_a, roots_a, spec_key).items()
            if key in unique_b
        ]
        paired = {x.before for x in pairs} | {x.after for x in pairs}
        only_in_a = [root for root in only_in_a if root not in paired]
        only_in_b = [root for root in only_in_b if root not in paired]
        changed.extend(pairs)

    return InputDiff(only_in_a=only_in_a, only_in_b=only_in_b, common=common, changed=changed)


def _concretized_user_specs(env: ev.Environment) -> Dict[ev.UserSpecId, Spec]:
    """Map every input spec of an environment to the concrete spec it produced."""
    return {
        ev.UserSpecId(x.group, x.root): env.specs_by_hash[x.hash] for x in env.concretized_roots
    }


def _concretize_command(label: str, *flags: str) -> Optional[str]:
    """Command concretizing the environment that label names, or None if it names none."""
    if not (ev.exists(label) or ev.is_env_dir(label)):
        return None
    return " ".join(["spack", "-e", shlex.quote(label), "concretize", *flags])


def _assert_concretized(
    env: ev.Environment, concretized: Iterable[ev.UserSpecId], label: str
) -> None:
    """Raise if an environment has input specs without a concrete spec."""
    # Also catches specs added since the last concretization
    pending = sorted(str(x.spec) for x in env._all_user_specs_with_group().difference(concretized))
    if pending:
        hint = "input specs not concretized:\n" + "\n".join(f"  {spec}" for spec in pending)
        command = _concretize_command(label)
        if command:
            hint += f"\nRun `{command}` first."
        raise ev.SpackEnvironmentError(f"environment '{label}' is not concretized", hint)


def _included_roots(env: ev.Environment) -> Set[Tuple[str, Spec, str]]:
    """Group, input spec and DAG hash of every root of the concrete environments env includes."""
    return {
        (x.group, x.root, x.hash)
        for roots in env.included_concretized_roots.values()
        for x in roots
    }


def _included_paths(env: ev.Environment, label: str) -> str:
    """Lines listing the concrete environments that env includes, for an error message."""
    paths = sorted(path for path, roots in env.included_concretized_roots.items() if roots)
    if not paths:
        return f"'{label}' includes no concrete environment"
    return f"'{label}' includes:\n" + "\n".join(f"  {path}" for path in paths)


def _assert_same_includes(
    env_a: ev.Environment, env_b: ev.Environment, label_a: str, label_b: str
) -> None:
    """Raise if two environments include concrete environments with different roots.

    Included roots are not compared, so the result is only complete when they are the same.
    """
    if _included_roots(env_a) != _included_roots(env_b):
        raise ev.SpackEnvironmentError(
            f"environments '{label_a}' and '{label_b}' include different concrete environments, "
            f"which `spack diff` cannot compare yet",
            f"{_included_paths(env_a, label_a)}\n{_included_paths(env_b, label_b)}",
        )


def _assert_package_hashes(env: ev.Environment, label: str) -> None:
    """Raise if a node of an environment has no recorded package hash."""
    # Without package hashes, nodes with equal configuration cannot be told apart
    if any(not spack.spec_diff.recorded_package_hash(node) for node in env.all_specs_generator()):
        command = _concretize_command(label, "--force")
        if command:
            hint = f"Re-concretize it with `{command}` first."
        else:
            hint = "Concretize the environment it was written from again, and compare the result."
        raise ev.SpackEnvironmentError(
            f"environment '{label}' was concretized by a version of Spack that did not record "
            f"package hashes (its lockfile predates them), so it cannot be compared",
            hint,
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
        prune: when True, don't visit the subDAG of a node whose configuration differs
        label_a: how to name the first environment in errors, defaulting to its own name
        label_b: how to name the second environment in errors, defaulting to its own name

    Raises:
        spack.environment.environment.SpackEnvironmentError: if either environment is not
            comparable, or if the two include concrete environments with different roots
        spack.spec_diff.SpecDiffError: if two concrete DAGs cannot be compared
    """
    label_a, label_b = label_a or env_a.name, label_b or env_b.name
    a_map = _concretized_user_specs(env_a)
    b_map = _concretized_user_specs(env_b)
    _assert_concretized(env_a, a_map, label_a)
    _assert_concretized(env_b, b_map, label_b)
    _assert_same_includes(env_a, env_b, label_a, label_b)
    _assert_package_hashes(env_a, label_a)
    _assert_package_hashes(env_b, label_b)

    inputs = input_spec_diff(a_map, b_map)

    providers: List[ProviderChange] = []
    divergences: List[UserSpecDivergence] = []
    unresolved: List[ev.UserSpecId] = []
    # Input specs share most of their graph, so the same node pair is reached from many of them
    cache: spack.spec_diff.ComparisonCache = {}

    # A changed input is reported under how the second environment writes it
    pairs = [(root, root) for root in inputs.common]
    pairs.extend((change.before, change.after) for change in inputs.changed)
    for root_a, root in pairs:
        concrete_a = a_map[root_a]
        concrete_b = b_map[root]
        # Only a virtual input can be two different packages, and they are not comparable
        if concrete_a.name != concrete_b.name:
            providers.append(ProviderChange(root, concrete_a, concrete_b))
            continue
        nodes = spack.spec_diff.diff_concrete_dags(
            concrete_a, concrete_b, prune=prune, cache=cache
        )
        if nodes:
            divergences.append(UserSpecDivergence(root, nodes))
        elif concrete_a.dag_hash() != concrete_b.dag_hash():
            unresolved.append(root)

    return EnvironmentDiff(
        inputs=inputs, providers=providers, divergences=divergences, unresolved=unresolved
    )


def root_sort_key(root: ev.UserSpecId) -> Tuple[str, str]:
    """Canonical order for input specs. The order they were concretized in is not stable."""
    return (root.group, str(root.spec))


def sorted_roots(roots: List[ev.UserSpecId]) -> List[ev.UserSpecId]:
    """Deduplicate and order input specs canonically.

    One input spec can reach several instances of the same package, so it can contribute more
    than once to an entry that merges them.
    """
    return sorted(set(roots), key=root_sort_key)


def _root_to_dict(root: ev.UserSpecId) -> Dict[str, str]:
    return {"spec": str(root.spec), "group": root.group}


def _roots_to_dict(roots: List[ev.UserSpecId]) -> List[Dict[str, str]]:
    return [_root_to_dict(root) for root in sorted_roots(roots)]
