# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Shared deprecation policy used by both the concretizer and the installer.

A version (or, more generally, a spec constraint) is marked deprecated via the ``deprecated()``
directive with a severity.

Whether a deprecation is tolerated is defined by ``packages:<name>:allowed_deprecation_severity``,
falling back to ``packages:all`` and the legacy ``config:deprecated`` flag.

This module centralizes that policy so the concretization-time gate and the install-time gate
cannot drift.
"""

import functools
import warnings
from typing import TYPE_CHECKING, Callable, Iterable, List, NamedTuple, Optional, Set

import spack.config
import spack.deptypes as dt
import spack.error
import spack.repo
from spack.enums import DeprecationReason, DeprecationSeverity

if TYPE_CHECKING:
    import spack.spec


class Violation(NamedTuple):
    """A single disallowed deprecation on a spec"""

    constraint: "spack.spec.Spec"
    reason: DeprecationReason
    severity: DeprecationSeverity
    allowed: DeprecationSeverity


def default_allowed_severity(warn_on_legacy: bool = False) -> DeprecationSeverity:
    """Return the default allowed deprecation severity from ``packages:all``.

    Falls back to the legacy ``config:deprecated`` flag (mapped to ``critical``) and finally to
    ``none``, meaning every deprecation is disallowed.

    Args:
        warn_on_legacy: emit a warning when the deprecated ``config:deprecated`` flag is
            what relaxes the policy.
    """
    packages_yaml = spack.config.CONFIG.get_config("packages")
    severity_str = packages_yaml.get("all", {}).get("allowed_deprecation_severity")
    if severity_str is not None:
        return DeprecationSeverity(severity_str)

    if spack.config.CONFIG.get("config:deprecated", False):
        if warn_on_legacy:
            warnings.warn(
                "config:deprecated is deprecated. "
                "Use 'packages:all:allowed_deprecation_severity:critical' instead",
                UserWarning,
                stacklevel=2,
            )
        return DeprecationSeverity.CRITICAL

    return DeprecationSeverity.NONE


def allowed_severity(pkg_name: str, default: DeprecationSeverity) -> DeprecationSeverity:
    """Return the allowed deprecation severity for a package, honoring per-package overrides."""
    pkg_cfg = spack.config.CONFIG.get_config("packages").get(pkg_name, {})
    override = pkg_cfg.get("allowed_deprecation_severity")
    return DeprecationSeverity(override) if override is not None else default


def disallowed(
    spec: "spack.spec.Spec", *, default_allowed: DeprecationSeverity
) -> List[Violation]:
    """Returns the list of violations on deprecation policies for a given spec. External specs are
    exempted since they are not under Spack's control.
    """
    if spec.external:
        return []

    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    allowed = allowed_severity(spec.name, default_allowed)
    return [
        Violation(constraint, reason, severity, allowed)
        for constraint, entries in pkg_cls.deprecations.items()
        if spec.satisfies(constraint)
        for reason, severity in entries
        if severity > allowed
    ]


def creates_new_prefix(installed: bool, dag_hash: str, overwrite: Set[str]) -> bool:
    """Whether installing a spec creates a fresh prefix: it is not already installed, or it is
    being overwritten.
    """
    return not installed or dag_hash in overwrite


def specs_to_deploy(
    specs: List["spack.spec.Spec"], overwrite: Set[str]
) -> List["spack.spec.Spec"]:
    """Filters the specs in input down to those that will get a fresh prefix, preserving order."""
    return [s for s in specs if creates_new_prefix(s.installed, s.dag_hash(), overwrite)]


class DeprecationGate:
    """Refuses to install specs whose runtime DAG contains a deprecation disallowed by
    configuration.
    """

    def __init__(
        self, policy: Optional[Callable[["spack.spec.Spec"], List[Violation]]] = None
    ) -> None:
        # Compute the packages:all fallback once here
        self._policy = policy or functools.partial(
            disallowed, default_allowed=default_allowed_severity()
        )
        self._checked: Set[str] = set()

    def check(self, seeds: Iterable["spack.spec.Spec"]) -> None:
        """Raises if the runtime DAG of any seed contains a disallowed deprecation."""
        violations: List[str] = []
        stack = [s for s in seeds if s.dag_hash() not in self._checked]
        while stack:
            node = stack.pop()
            key = node.dag_hash()
            if key in self._checked:
                continue

            self._checked.add(key)
            found = self._policy(node)
            if found:
                violations.append(self._format_violations(node, found))

            stack.extend(
                dep
                for dep in node.dependencies(deptype=dt.LINK | dt.RUN)
                if dep.dag_hash() not in self._checked
            )

        if violations:
            raise spack.error.InstallError(
                "the following specs are deprecated and cannot be installed:\n\n"
                + "\n".join(violations)
                + "\n\n    Relax 'packages:<name>:allowed_deprecation_severity' in your "
                "configuration to install them anyway."
            )

    @staticmethod
    def _format_violations(spec: "spack.spec.Spec", violations: List[Violation]) -> str:
        lines = [f"    {spec.cshort_spec}"]
        for constraint, reason, severity, allowed in violations:
            spec_str = f"{spec.name}{constraint}" if str(constraint) else spec.name
            lines.append(
                f"        {spec_str} is deprecated (reason: {reason.value}, "
                f"severity: {severity.name.lower()}); 'allowed_deprecation_severity' "
                f"is '{allowed.name.lower()}'"
            )
        return "\n".join(lines)
