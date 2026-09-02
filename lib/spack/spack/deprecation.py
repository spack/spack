# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Shared deprecation policy used by both the concretizer and the installer.

A version (or, more generally, a spec constraint) is marked deprecated via the ``deprecated()``
directive, with a reason, a severity, and the advisory labels it refers to.

Which deprecations are tolerated is defined by ``packages:<name>:deprecation:allow``, a list of
selectors falling back to ``packages:all`` and finally to the legacy ``config:deprecated`` flag.
A directive is skipped when at least one selector matches it.

This module centralizes that policy so the concretization-time gate and the install-time gate
cannot drift.
"""

import warnings
from typing import TYPE_CHECKING, Dict, FrozenSet, Iterable, List, NamedTuple, Optional, Set

import spack.config
import spack.deptypes as dt
import spack.error
import spack.repo
import spack.traverse
from spack.enums import Deprecation, DeprecationReason, DeprecationSeverity

if TYPE_CHECKING:
    import spack.spec


class Violation(NamedTuple):
    """A single disallowed deprecation on a spec"""

    constraint: "spack.spec.Spec"
    reason: DeprecationReason
    severity: DeprecationSeverity
    msg: Optional[str] = None


class Selector(NamedTuple):
    """One entry of ``packages:<name>:deprecation:allow``.

    The attributes are AND-ed, and an attribute left empty matches any deprecation.
    """

    #: Reasons this entry selects
    reasons: FrozenSet[DeprecationReason] = frozenset()
    #: Maximum severity this entry selects
    severity: Optional[DeprecationSeverity] = None
    #: Labels the user assessed. A deprecation is selected only if it declares labels, and all
    #: of them are listed here.
    labels: FrozenSet[str] = frozenset()

    @staticmethod
    def from_config(data: dict) -> "Selector":
        reasons = data.get("reason", [])
        if isinstance(reasons, str):
            reasons = [reasons]
        severity = data.get("severity")
        return Selector(
            reasons=frozenset(DeprecationReason(x) for x in reasons),
            severity=DeprecationSeverity(severity) if severity is not None else None,
            labels=frozenset(data.get("labels", ())),
        )

    def matches(self, entry: Deprecation) -> bool:
        if self.reasons and entry.reason not in self.reasons:
            return False
        if self.severity is not None and entry.severity > self.severity:
            return False
        if self.labels and not (entry.labels and self.labels.issuperset(entry.labels)):
            return False
        return True


def _default_selectors(packages_yaml: dict, warn_on_legacy: bool = False) -> List[Selector]:
    """Return the selectors from ``packages:all:deprecation:allow``.

    Falls back to the legacy ``config:deprecated`` flag (which allows any severity) and finally
    to the empty list, meaning every deprecation is disallowed.

    Args:
        packages_yaml: the ``packages`` configuration.
        warn_on_legacy: emit a warning when the deprecated ``config:deprecated`` flag is
            what relaxes the policy.
    """
    value = packages_yaml.get("all", {}).get("deprecation", {}).get("allow")
    if value is not None:
        return [Selector.from_config(x) for x in value]

    if spack.config.CONFIG.get("config:deprecated", False):
        if warn_on_legacy:
            warnings.warn(
                "config:deprecated is deprecated. Use an entry with 'severity: critical' under "
                "'packages:all:deprecation:allow' instead",
                UserWarning,
                stacklevel=2,
            )
        return [Selector(severity=DeprecationSeverity.CRITICAL)]

    return []


class Policy:
    """Deprecation policy resolved from the ``packages`` configuration."""

    def __init__(
        self, packages_yaml: dict, default_selectors: List[Selector], scope: str = "runtime"
    ) -> None:
        """
        Args:
            packages_yaml: the ``packages`` configuration.
            default_selectors: selectors from ``packages:all``, used for the packages that
                declare none of their own.
            scope: check scope from ``packages:all:deprecation:scope`` ("runtime" or "all").
        """
        self.packages_yaml = packages_yaml
        self.default_selectors = default_selectors
        self.scope = scope
        self._selectors: Dict[str, List[Selector]] = {}

    @staticmethod
    def from_config(warn_on_legacy: bool = False) -> "Policy":
        """Build a policy from the current ``packages`` config, read once.

        Args:
            warn_on_legacy: emit a warning when the deprecated ``config:deprecated`` flag is
                what relaxes the policy. Set only where the warning should fire once.
        """
        packages_yaml = spack.config.CONFIG.get_config("packages")
        scope = packages_yaml.get("all", {}).get("deprecation", {}).get("scope", "runtime")
        return Policy(packages_yaml, _default_selectors(packages_yaml, warn_on_legacy), scope)

    @property
    def deptypes(self) -> int:
        """Dependency types to traverse for the configured deprecation scope."""
        return dt.ALL if self.scope == "all" else dt.LINK | dt.RUN

    def selectors(self, pkg_name: str) -> List[Selector]:
        """Return the selectors for a package. A package that declares an ``allow`` list
        replaces the one under ``all``, like every other ``packages`` setting.
        """
        if pkg_name not in self._selectors:
            override = self.packages_yaml.get(pkg_name, {}).get("deprecation", {}).get("allow")
            self._selectors[pkg_name] = (
                [Selector.from_config(x) for x in override]
                if override is not None
                else self.default_selectors
            )
        return self._selectors[pkg_name]

    def allows(self, pkg_name: str, entry: Deprecation) -> bool:
        """Return True if a deprecation is allowed on a package, hence skipped."""
        return any(x.matches(entry) for x in self.selectors(pkg_name))

    def disallowed(self, spec: "spack.spec.Spec") -> List[Violation]:
        """Returns the list of deprecation-policy violations for a spec. External specs are
        exempted since they are not under Spack's control.
        """
        if spec.external:
            return []

        try:
            pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
        except spack.repo.UnknownPackageError:
            return []

        return [
            Violation(constraint, entry.reason, entry.severity, entry.msg)
            for constraint, entries in pkg_cls.deprecations.items()
            if spec.satisfies(constraint)
            for entry in entries
            if not self.allows(spec.name, entry)
        ]


def deprecated_spec_str(pkg_name: str, constraint: "spack.spec.Spec") -> str:
    """Format the spec a ``deprecated()`` directive refers to."""
    constraint_str = str(constraint)
    if not constraint_str:
        return pkg_name
    return constraint_str if constraint.name else f"{pkg_name}{constraint_str}"


def reusable(
    specs: Iterable["spack.spec.Spec"], *, policy: Optional[Policy] = None
) -> List["spack.spec.Spec"]:
    """Return the subset of ``specs`` that can be reused under the deprecation policy.

    A candidate is rejected when it, or any node in its checked closure, has a disallowed
    deprecation. The closure is the link/run one under the ``runtime`` scope, and the whole DAG
    under ``all``, so ``all`` additionally rejects artifacts built with a deprecated tool.

    Args:
        specs: the reuse candidates.
        policy: the policy to apply; defaults to the configured one.
    """
    resolved = policy or Policy.from_config()
    deptypes = resolved.deptypes
    candidates = list(specs)

    # One post-order pass over the union of the candidate DAGs, keyed by hash so a node shared
    # by many candidates is evaluated once.
    rejected: Set[str] = set()
    for node in spack.traverse.traverse_nodes(
        candidates, deptype=deptypes, order="post", key=spack.traverse.by_dag_hash
    ):
        if resolved.disallowed(node) or any(
            edge.spec.dag_hash() in rejected
            for edge in node.edges_to_dependencies(depflag=deptypes)
        ):
            rejected.add(node.dag_hash())

    return [s for s in candidates if s.dag_hash() not in rejected]


def check_deprecations(
    seeds: Iterable["spack.spec.Spec"], *, policy: Optional[Policy] = None
) -> None:
    """Raise if the DAG reachable from any seed contains a disallowed deprecation.

    Args:
        seeds: the specs to check, together with the DAG reachable from them.
        policy: the policy to apply, together with the closure it checks; defaults to the
            configured one.
    """
    resolved = policy or Policy.from_config()

    violations: List[str] = []
    for node in spack.traverse.traverse_nodes(list(seeds), deptype=resolved.deptypes):
        found = resolved.disallowed(node)
        if found:
            violations.append(_format_violations(node, found))

    if violations:
        raise spack.error.InstallError(
            "the following specs are deprecated and cannot be installed:\n\n"
            + "\n".join(violations)
            + "\n\n    Add an entry to 'packages:<name>:deprecation:allow' in your "
            "configuration to install them anyway."
        )


def _format_violations(spec: "spack.spec.Spec", violations: List[Violation]) -> str:
    lines = [f"    {spec.cshort_spec}"]
    for constraint, reason, severity, msg in violations:
        spec_str = deprecated_spec_str(spec.name, constraint)
        lines.append(
            f"        {spec_str} is deprecated (reason: {reason.value}, "
            f"severity: {severity.name.lower()}); not allowed by "
            f"'packages:{spec.name}:deprecation:allow'"
        )
        if msg:
            lines.append(f"            {msg}")
    return "\n".join(lines)
