# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.enums
import spack.repo
import spack.util.spack_yaml as syaml
from spack.concretize import concretize_one
from spack.solver.asp import UnsatisfiableSpecError


@pytest.fixture
def packages_yaml_write(mutable_config):
    def _set(conf_str):
        conf = syaml.load_config(conf_str)
        mutable_config.set("packages", conf["packages"])

    return _set


def test_config_deprecated_with_old_style_version_deprecation(mock_packages, mutable_config):
    """Tests that config:deprecated:true allows old-style deprecated versions, and that
    config:deprecated:false blocks them.
    """
    with mutable_config.override("config:deprecated", True):
        assert concretize_one("deprecated-old-style@1.0").satisfies("@1.0")

    with pytest.raises(UnsatisfiableSpecError, match="maintenance"):
        concretize_one("deprecated-old-style@1.0")


def test_version_deprecated_true_prefers_non_deprecated(config, mock_packages):
    """Solver picks @0.9 (non-deprecated) over @1.0 (deprecated) by default."""
    spec = concretize_one("deprecated-old-style")
    assert spec.satisfies("@0.9")


def test_version_deprecated_true_registers_in_deprecations(mock_packages):
    """Tests that version(..., deprecated=True) populates pkg.deprecations with reason=maintenance
    and severity=critical.
    """
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-old-style")
    all_entries = [(r, s) for entries in pkg_cls.deprecations.values() for r, s in entries]
    assert all(
        x == (spack.enums.DeprecationReason.MAINTENANCE, spack.enums.DeprecationSeverity.CRITICAL)
        for x in all_entries
    )


def test_allowed_deprecation_concretizes_without_warning(
    mock_packages, concretize_scope, packages_yaml_write, recwarn
):
    """An allowed deprecation (severity <= threshold) concretizes silently, with no warning."""
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: critical
""")
    spec = concretize_one("deprecated-with-reason@2.0")
    assert spec.satisfies("@2.0")
    assert not any(
        "deprecat" in str(w.message).lower() or "cve" in str(w.message).lower()
        for w in recwarn.list
    )


def test_allowed_deprecation_severity_per_package_blocks(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that when the allowed_deprecation_severity < severity, concretization fails."""
    packages_yaml_write("""
packages:
  deprecated-with-reason:
    allowed_deprecation_severity: medium
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-reason@2.0")


def test_allowed_deprecation_severity_all_blocks(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that the all:allowed_deprecation_severity applies when no per-package override
    exists.
    """
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: low
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-reason@2.0")


def test_coexistence_old_and_new_deprecation(mock_packages, mutable_config):
    """Tests that version(..., deprecated=True) and deprecated() on the same version coexist."""
    # The solver avoids the deprecated @1.0 and picks @2.0 by default.
    spec = concretize_one("deprecated-dual")
    assert spec.satisfies("@2.0")

    # With deprecations allowed, @1.0 concretizes without error.
    with mutable_config.override("config:deprecated", True):
        assert concretize_one("deprecated-dual@1.0").satisfies("@1.0")


def test_deprecation_scope_runtime_ignores_build_only_dep(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that with the default 'runtime' scope, a deprecated node reachable only through a
    build edge is outside the checked closure, so concretization succeeds even though the node
    is in the DAG.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation_scope: runtime
""")
    spec = concretize_one("deprecated-buildtool-client")
    assert spec.satisfies("@1.0")
    # The deprecated node is present in the DAG, reachable only through the build edge.
    assert any(s.satisfies("deprecated-versions@1.1.0") for s in spec.traverse())


def test_deprecation_scope_all_gates_build_only_dep(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that with the 'all' scope, a deprecated node reachable only through a build edge
    is gated.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation_scope: all
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-buildtool-client")
