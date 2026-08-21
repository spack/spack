# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Shared deprecation policy used by both the concretizer and the installer.

A version (or, more generally, a spec constraint) is marked deprecated via the ``deprecated()``
directive with a severity.

Whether a deprecation is tolerated is defined by
``packages:<name>:deprecation:allowed_severity``, which is either a single severity or a mapping
from deprecation reason to severity, falling back to ``packages:all`` and the legacy
``config:deprecated`` flag.  A directive that declares ``labels`` is skipped outright when every
one of them is listed in ``packages:<name>:deprecation:exempt_labels``.

This module centralizes that policy so the concretization-time gate and the install-time gate
cannot drift.
"""

import warnings
from typing import TYPE_CHECKING, Dict, Iterable, List, NamedTuple, Optional, Set, Union

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
    allowed: DeprecationSeverity


def is_exempt(entry: Deprecation, exempt_labels: Set[str]) -> bool:
    """A deprecation is skipped only when it declares labels and every one of them is exempt."""
    return bool(entry.labels) and exempt_labels.issuperset(entry.labels)


#: Allowed severity per deprecation reason. The ``None`` key covers the reasons not listed.
Thresholds = Dict[Optional[DeprecationReason], DeprecationSeverity]


def _parse_thresholds(value: Union[str, dict]) -> Thresholds:
    if isinstance(value, str):
        return {None: DeprecationSeverity(value)}  # type: ignore[arg-type]
    return {
        (None if key == "default" else DeprecationReason(key)): DeprecationSeverity(
            severity  # type: ignore[arg-type]
        )
        for key, severity in value.items()
    }


def _allowed(thresholds: Thresholds, reason: DeprecationReason) -> DeprecationSeverity:
    """Return the threshold for a reason, falling back to the default and finally to ``none``."""
    if reason in thresholds:
        return thresholds[reason]
    return thresholds.get(None, DeprecationSeverity.NONE)


def _default_thresholds(packages_yaml: dict, warn_on_legacy: bool = False) -> Thresholds:
    """Return the default thresholds from ``packages:all:deprecation``.

    Falls back to the legacy ``config:deprecated`` flag (mapped to ``critical``) and finally to
    ``none``, meaning every deprecation is disallowed.

    Args:
        packages_yaml: the ``packages`` configuration.
        warn_on_legacy: emit a warning when the deprecated ``config:deprecated`` flag is
            what relaxes the policy.
    """
    value = packages_yaml.get("all", {}).get("deprecation", {}).get("allowed_severity")
    if value is not None:
        return _parse_thresholds(value)

    if spack.config.CONFIG.get("config:deprecated", False):
        if warn_on_legacy:
            warnings.warn(
                "config:deprecated is deprecated. "
                "Use 'packages:all:deprecation:allowed_severity:critical' instead",
                UserWarning,
                stacklevel=2,
            )
        return {None: DeprecationSeverity.CRITICAL}

    return {None: DeprecationSeverity.NONE}


class Policy(NamedTuple):
    """Deprecation policy resolved from the ``packages`` configuration."""

    packages_yaml: dict
    #: Thresholds from ``packages:all``, used when a package has no ``allowed_severity``
    default_thresholds: Thresholds
    #: Global check scope from ``packages:all:deprecation:scope`` ("runtime" or "all")
    scope: str = "runtime"

    @staticmethod
    def from_config(warn_on_legacy: bool = False) -> "Policy":
        """Build a policy from the current ``packages`` config, read once.

        Args:
            warn_on_legacy: emit a warning when the deprecated ``config:deprecated`` flag is
                what relaxes the policy. Set only where the warning should fire once.
        """
        packages_yaml = spack.config.CONFIG.get_config("packages")
        scope = packages_yaml.get("all", {}).get("deprecation", {}).get("scope", "runtime")
        return Policy(packages_yaml, _default_thresholds(packages_yaml, warn_on_legacy), scope)

    @property
    def deptypes(self) -> int:
        """Dependency types to traverse for the configured deprecation scope."""
        return dt.ALL if self.scope == "all" else dt.LINK | dt.RUN

    def thresholds(self, pkg_name: str) -> Thresholds:
        """Return the thresholds for a package."""
        override = (
            self.packages_yaml.get(pkg_name, {}).get("deprecation", {}).get("allowed_severity")
        )
        return _parse_thresholds(override) if override is not None else self.default_thresholds

    def allowed_severity(self, pkg_name: str, reason: DeprecationReason) -> DeprecationSeverity:
        """Return the allowed severity for a reason on a package."""
        return _allowed(self.thresholds(pkg_name), reason)

    def exempt_labels(self, pkg_name: str) -> Set[str]:
        """Return the exempt labels for a package. A non-empty per-package list replaces the one
        under ``all``, like every other ``packages`` setting.
        """
        for name in (pkg_name, "all"):
            labels = self.packages_yaml.get(name, {}).get("deprecation", {}).get("exempt_labels")
            if labels:
                return set(labels)
        return set()

    def disallowed(self, spec: "spack.spec.Spec") -> List[Violation]:
        """Returns the list of deprecation-policy violations for a spec. External specs are
        exempted since they are not under Spack's control.
        """
        if spec.external:
            return []

        pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
        thresholds = self.thresholds(spec.name)
        exempt = self.exempt_labels(spec.name)
        return [
            Violation(constraint, entry.reason, entry.severity, _allowed(thresholds, entry.reason))
            for constraint, entries in pkg_cls.deprecations.items()
            if spec.satisfies(constraint)
            for entry in entries
            if entry.severity > _allowed(thresholds, entry.reason) and not is_exempt(entry, exempt)
        ]


def reusable(
    specs: Iterable["spack.spec.Spec"], *, policy: Optional[Policy] = None
) -> List["spack.spec.Spec"]:
    """Return the subset of ``specs`` that can be reused under the deprecation policy.

    A candidate is rejected when it, or any node in its checked closure, carries a disallowed
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
        try:
            violates = bool(resolved.disallowed(node))
        except spack.repo.UnknownPackageError:
            # The package is gone from the repository; it is dropped later in the solve anyway
            violates = False
        if violates or any(
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
            + "\n\n    Relax 'packages:<name>:deprecation:allowed_severity' in your "
            "configuration to install them anyway."
        )


def _format_violations(spec: "spack.spec.Spec", violations: List[Violation]) -> str:
    lines = [f"    {spec.cshort_spec}"]
    for constraint, reason, severity, allowed in violations:
        spec_str = f"{spec.name}{constraint}" if str(constraint) else spec.name
        lines.append(
            f"        {spec_str} is deprecated (reason: {reason.value}, "
            f"severity: {severity.name.lower()}); 'deprecation:allowed_severity' "
            f"is '{allowed.name.lower()}'"
        )
    return "\n".join(lines)
