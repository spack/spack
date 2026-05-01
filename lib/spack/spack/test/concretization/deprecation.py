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
        with pytest.warns(UserWarning, match="maintenance"):
            concretize_one("deprecated-old-style@1.0")

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


def test_deprecated_directive_warns_on_concretize(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that concretizing a spec that matches a deprecated() constraint emits a warning."""
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: critical
""")
    with pytest.warns(UserWarning) as warning_list:
        concretize_one("deprecated-with-reason@2.0")
    messages = [str(w.message) for w in warning_list]
    assert any("cve" in m for m in messages)
    assert any("critical" in m for m in messages)


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


def test_solver_severity_criterion_overrides_version_preference(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that severity is taken into account when a deprecation is allowed.

    deprecated-with-reason has @2.0 deprecated at critical severity and @1.0 at low
    severity. Both are allowed here, but the solver picks @1.0 due to the lower severity,
    even though @2.0 is the higher version.
    """
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: critical
""")
    spec = concretize_one("deprecated-with-reason")
    assert spec.satisfies("@1.0")


def test_coexistence_old_and_new_deprecation(mock_packages, mutable_config):
    """Tests that version(..., deprecated=True) and deprecated() on the same version coexist."""
    # The solver should prefer @2.0 (non-deprecated) over @1.0.
    spec = concretize_one("deprecated-dual")
    assert spec.satisfies("@2.0")

    # Check that the deprecation reason from the directive is shown
    with mutable_config.override("config:deprecated", True):
        with pytest.warns(UserWarning, match="cve"):
            concretize_one("deprecated-dual@1.0")
