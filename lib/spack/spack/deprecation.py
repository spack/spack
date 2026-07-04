# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Shared deprecation policy used by both the concretizer and the installer.

A version (or, more generally, a spec constraint) is marked deprecated via the ``deprecated()``
directive with a severity. Whether a deprecation is tolerated is controlled by
``packages:<name>:allowed_deprecation_severity``, falling back to ``packages:all`` and the legacy
``config:deprecated`` flag. This module centralizes that policy so the concretization-time gate and
the install-time gate cannot drift.
"""

import warnings
from typing import TYPE_CHECKING, Iterable, List, Optional, Tuple

import spack.config
import spack.deptypes as dt
import spack.error
import spack.repo
import spack.traverse
from spack.enums import DeprecationReason, DeprecationSeverity

if TYPE_CHECKING:
    import spack.spec


def default_allowed_severity(warn_on_legacy: bool = False) -> DeprecationSeverity:
    """Return the default allowed deprecation severity from ``packages:all``.

    Falls back to the legacy ``config:deprecated`` flag (mapped to ``critical``) and finally to
    ``none``, meaning every deprecation is disallowed.

    Args:
        warn_on_legacy: emit a warning when the deprecated ``config:deprecated`` flag is what
            relaxes the policy. Set only where the warning should fire once (concretizer setup).
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


def allowed_severity(pkg_name: str) -> DeprecationSeverity:
    """Return the allowed deprecation severity for a package, honoring per-package overrides."""
    pkg_cfg = spack.config.CONFIG.get_config("packages").get(pkg_name, {})
    override = pkg_cfg.get("allowed_deprecation_severity")
    if override is not None:
        return DeprecationSeverity(override)
    return default_allowed_severity()


def matching_severity(
    spec: "spack.spec.Spec",
) -> Optional[Tuple[DeprecationReason, DeprecationSeverity]]:
    """Return the highest-severity deprecation matching ``spec``, or None if not deprecated."""
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    matches: List[Tuple[DeprecationReason, DeprecationSeverity]] = [
        entry
        for constraint, entries in pkg_cls.deprecations.items()
        if spec.satisfies(constraint)
        for entry in entries
    ]
    if not matches:
        return None
    return max(matches, key=lambda entry: entry[1])


def disallowed(
    spec: "spack.spec.Spec",
) -> Optional[Tuple[DeprecationReason, DeprecationSeverity, DeprecationSeverity]]:
    """If a spec is deprecated, returns ``(reason, severity, allowed)`` else None. External specs
    are exempted since they are not under Spack's control.
    """
    if spec.external:
        return None
    match = matching_severity(spec)
    if match is None:
        return None
    reason, severity = match
    allowed = allowed_severity(spec.name)
    if severity > allowed:
        return reason, severity, allowed
    return None


def ensure_allowed(specs: Iterable["spack.spec.Spec"]) -> None:
    """Raise if any of the specs uses a deprecation disallowed by configuration."""
    violations = []
    for spec in specs:
        match = disallowed(spec)
        if match is None:
            continue
        reason, severity, allowed = match
        violations.append(
            f"    {spec.cshort_spec}\n"
            f"        deprecated (reason: {reason.value}, "
            f"severity: {severity.name.lower()}), but 'allowed_deprecation_severity' "
            f"is '{allowed.name.lower()}'"
        )

    if violations:
        raise spack.error.InstallError(
            "the following specs are deprecated and cannot be installed:\n\n"
            + "\n".join(violations)
            + "\n\n    Relax 'packages:<name>:allowed_deprecation_severity' in your "
            "configuration to install them anyway."
        )


def ensure_allowed_deployment(specs: Iterable["spack.spec.Spec"]) -> None:
    """Raise if any spec about to be installed has a disallowed deprecation in its runtime
    closure.
    """
    ensure_allowed(
        spack.traverse.traverse_nodes(
            list(specs), deptype=dt.LINK | dt.RUN, key=spack.traverse.by_dag_hash
        )
    )
