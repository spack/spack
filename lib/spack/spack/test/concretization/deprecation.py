# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.config
import spack.enums
import spack.error
import spack.repo
import spack.spec
import spack.util.spack_yaml as syaml
from spack.concretize import concretize_one
from spack.solver.asp import UnsatisfiableSpecError
from spack.solver.variant_rewrite import apply_replacements_to_spec, rewrite_deprecated_variants


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
    with spack.config.override("config:deprecated", True):
        with pytest.warns(UserWarning, match="maintenance"):
            concretize_one("deprecated-old-style@1.0")

    with pytest.raises(UnsatisfiableSpecError, match="maintenance"):
        concretize_one("deprecated-old-style@1.0")


def test_version_deprecated_true_prefers_non_deprecated(default_mock_concretization):
    """Solver picks @0.9 (non-deprecated) over @1.0 (deprecated) by default."""
    spec = default_mock_concretization("deprecated-old-style")
    assert spec.satisfies("@0.9")


def test_version_deprecated_true_registers_in_deprecations(mock_packages):
    """Tests that version(..., deprecated=True) populates pkg.deprecations with reason=maintenance
    and severity=critical.
    """
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-old-style")
    all_entries = [(r, s) for entries in pkg_cls.deprecations.values() for r, s, _ in entries]
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
        concretize_one("deprecated-with-reason@1.0")
    messages = [str(w.message) for w in warning_list]
    assert any("cve" in m for m in messages)
    assert any("high" in m for m in messages)


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
        concretize_one("deprecated-with-reason@1.0")


def test_allowed_deprecation_severity_all_blocks(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that the all:allowed_deprecation_severity applies when no per-package
    override exists.
    """
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: low
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-reason@1.0")


def test_allowed_deprecation_severity_critical_config_warns_not_errors(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that when explicitly set to critical, all deprecation warns, not errors."""
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: critical
""")
    with pytest.warns(UserWarning, match="cve"):
        concretize_one("deprecated-severity-conflict@2.0")


def test_solver_severity_criterion_overrides_version_preference(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that severity is taken into account when a deprecation is allowed.

    deprecated-severity-conflict has:
      @2.0 deprecated at CRITICAL severity
      @1.0 deprecated at LOW severity

    Both versions are deprecated, but due to the severity criterion, the solver picks @1.0.
    """
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: critical
""")
    spec = concretize_one("deprecated-severity-conflict")
    assert spec.satisfies("@1.0")


def test_coexistence_old_and_new_deprecation(mock_packages, mutable_config):
    """Tests that version(..., deprecated=True) and deprecated() on the same version coexist."""
    # The solver should prefer @2.0 (non-deprecated) over @1.0.
    spec = concretize_one("deprecated-dual")
    assert spec.satisfies("@2.0")

    # Check that the deprecation reason from the directive is shown
    with spack.config.override("config:deprecated", True):
        with pytest.warns(UserWarning, match="cve"):
            concretize_one("deprecated-dual@1.0")


# ---------------------------------------------------------------------------
# Integration tests: root input spec rewriting (Task 3)
# ---------------------------------------------------------------------------


def test_solver_setup_rewrites_deprecated_variant(mock_packages, concretize_scope):
    """Concretizing 'deprecated-with-replace+shared' rewrites +shared to libs=shared."""
    with pytest.warns(UserWarning, match="deprecated"):
        spec = concretize_one("deprecated-with-replace+shared")
    assert "shared" not in spec.variants
    assert spec.satisfies("libs=shared")


def test_solver_setup_rewrites_false_variant(mock_packages, concretize_scope):
    """Concretizing 'deprecated-with-replace~shared' rewrites ~shared to libs=static."""
    with pytest.warns(UserWarning, match="deprecated"):
        spec = concretize_one("deprecated-with-replace~shared")
    assert "shared" not in spec.variants
    assert spec.satisfies("libs=static")


def test_solver_setup_no_warning_when_no_deprecated_variant(mock_packages, concretize_scope):
    """Concretizing without the deprecated variant emits no warning."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        concretize_one("deprecated-with-replace libs=shared")


# ---------------------------------------------------------------------------
# Integration tests: packages.yaml rewriting (Task 4)
# ---------------------------------------------------------------------------


def test_packages_yaml_prefer_deprecated_variant_is_rewritten(
    mock_packages, concretize_scope, packages_yaml_write
):
    """prefer: ['+shared'] in packages.yaml is rewritten to libs=shared before concretization."""
    packages_yaml_write("""
packages:
  deprecated-with-replace:
    prefer: ['+shared']
""")
    with pytest.warns(UserWarning, match="deprecated"):
        spec = concretize_one("deprecated-with-replace")
    assert spec.satisfies("libs=shared")


def test_packages_yaml_require_deprecated_variant_is_rewritten(
    mock_packages, concretize_scope, packages_yaml_write
):
    """require: ['+shared'] in packages.yaml is rewritten to libs=shared before concretization."""
    packages_yaml_write("""
packages:
  deprecated-with-replace:
    require: ['+shared']
""")
    with pytest.warns(UserWarning, match="deprecated"):
        spec = concretize_one("deprecated-with-replace")
    assert spec.satisfies("libs=shared")


# ---------------------------------------------------------------------------
# Integration tests: package-recipe directive rewriting (Task 5)
# ---------------------------------------------------------------------------


def test_directive_depends_on_target_variant_rewritten(mock_packages, concretize_scope):
    """depends_on('deprecated-with-replace+shared') is rewritten at fact-emission time."""
    with pytest.warns(UserWarning, match="deprecated"):
        spec = concretize_one("uses-deprecated-replace")
    assert spec["deprecated-with-replace"].satisfies("libs=shared")
    assert "shared" not in spec["deprecated-with-replace"].variants


def test_directive_conflict_variant_rewritten(mock_packages, concretize_scope):
    """conflicts('libs=shared') still fires even when the input was originally +shared."""
    with pytest.raises(UnsatisfiableSpecError, match="libs=shared conflict fired"):
        concretize_one("self-conflict-deprecated+shared")


def test_directive_rewriting_does_not_mutate_class_state(mock_packages, concretize_scope):
    """Two consecutive solves must see the same pkg.dependencies (no mutation of class state)."""
    pkg_cls = spack.repo.PATH.get_pkg_class("uses-deprecated-replace")
    before = {
        str(k): {n: str(d.spec) for n, d in v.items()} for k, v in pkg_cls.dependencies.items()
    }
    with pytest.warns(UserWarning):
        concretize_one("uses-deprecated-replace")
    with pytest.warns(UserWarning):
        concretize_one("uses-deprecated-replace")
    after = {
        str(k): {n: str(d.spec) for n, d in v.items()} for k, v in pkg_cls.dependencies.items()
    }
    assert before == after


# ---------------------------------------------------------------------------
# Unit tests for variant_rewrite module
# ---------------------------------------------------------------------------


def test_rewrite_second_trigger_sees_original_spec(mock_packages):
    """Both triggers are evaluated against the original spec, even if the first removes values.

    Bug: phase 2 was applied inside the outer trigger loop, so the second trigger
    would check an already-mutated spec and fail to fire when the first trigger had
    fully removed the variant.
    """
    # trigger1 handles both libs values at once, completely consuming the variant
    # trigger2 is a separate rule that also matches libs=static
    trigger1 = spack.spec.Spec("libs=shared,static")
    trigger2 = spack.spec.Spec("libs=static")
    replacements = {
        trigger1: (
            spack.enums.DeprecationReason.RENAME,
            {"libs=shared": "+shared", "libs=static": "+static"},
            None,
        ),
        trigger2: (spack.enums.DeprecationReason.RENAME, {"libs=static": "+static_extra"}, None),
    }
    spec = spack.spec.Spec("deprecated-with-replace libs=shared,static")
    with pytest.warns(UserWarning):
        rewrite_deprecated_variants(spec, replacements, "test")
    assert "libs" not in spec.variants
    assert "shared" in spec.variants
    assert "static" in spec.variants
    # trigger2 must fire because it matched the original spec,
    # even though trigger1 already removed the libs variant
    assert "static_extra" in spec.variants


def test_rewrite_multi_value_partial_deletion(mock_packages):
    """Extracting one value from a multi-valued variant preserves the remaining values.

    replace={"libs=shared": "+shared_extracted"} on a spec with libs=shared,static
    should remove only 'shared' from libs, leaving libs=static, not delete libs entirely.
    """
    replacements = {
        spack.spec.Spec("libs=shared"): (
            spack.enums.DeprecationReason.RENAME,
            {"libs=shared": "+shared_extracted"},
            None,
        )
    }
    spec = spack.spec.Spec("deprecated-with-replace libs=shared,static")
    with pytest.warns(UserWarning):
        changed = rewrite_deprecated_variants(spec, replacements, "test")
    assert changed
    # 'shared' was extracted into a boolean; 'static' must remain in the libs variant
    assert "libs" in spec.variants
    assert spec.variants["libs"].values == ("static",)
    assert "shared_extracted" in spec.variants
    assert spec.variants["shared_extracted"].value is True


def test_rewrite_multi_value_full_deletion_when_all_values_extracted(mock_packages):
    """When all values of a multi-valued variant are extracted, the variant is removed entirely."""
    replacements = {
        spack.spec.Spec("libs=shared"): (
            spack.enums.DeprecationReason.RENAME,
            {"libs=shared": "+shared_extracted"},
            None,
        )
    }
    spec = spack.spec.Spec("deprecated-with-replace libs=shared")
    with pytest.warns(UserWarning):
        changed = rewrite_deprecated_variants(spec, replacements, "test")
    assert changed
    assert "libs" not in spec.variants
    assert "shared_extracted" in spec.variants


def test_rewrite_multi_value_split_all_keys_fire(mock_packages):
    """All keys in replace= that match the original spec fire, even for multi-valued variants.

    replace={"libs=shared": "+shared", "libs=static": "+static"} must turn
    libs=shared,static into +shared+static -- both keys must fire.
    The bug: without the fix, the second key fails because the first key already
    deleted the 'libs' variant from the spec.
    """
    replacements = {
        spack.spec.Spec("libs=shared"): (
            spack.enums.DeprecationReason.RENAME,
            {"libs=shared": "+shared", "libs=static": "+static"},
            None,
        )
    }
    spec = spack.spec.Spec("deprecated-with-replace libs=shared,static")
    with pytest.warns(UserWarning):
        changed = rewrite_deprecated_variants(spec, replacements, "test")
    assert changed
    assert "libs" not in spec.variants
    assert spec.satisfies("+shared")
    assert spec.satisfies("+static")


def test_rewrite_simple_substitution(mock_packages):
    """Tests that +shared is rewritten to libs=shared in place."""
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-with-replace")
    spec = spack.spec.Spec("deprecated-with-replace+shared")
    with pytest.warns(UserWarning, match="deprecated"):
        changed = rewrite_deprecated_variants(spec, pkg_cls.replacements, "test")
    assert changed
    assert "shared" not in spec.variants
    assert spec.satisfies("libs=shared")


def test_rewrite_false_value_substitution(mock_packages):
    """Tests that ~shared is rewritten to libs=static."""
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-with-replace")
    spec = spack.spec.Spec("deprecated-with-replace~shared")
    with pytest.warns(UserWarning, match="deprecated"):
        changed = rewrite_deprecated_variants(spec, pkg_cls.replacements, "test")
    assert changed
    assert "shared" not in spec.variants
    assert spec.satisfies("libs=static")


def test_rewrite_drop_variant(mock_packages):
    """Tests that mapping a key to '' drops the variant."""
    replacements = {
        spack.spec.Spec("+shared"): (spack.enums.DeprecationReason.RENAME, {"+shared": ""}, None)
    }
    spec = spack.spec.Spec("deprecated-with-replace+shared")
    with pytest.warns(UserWarning, match="deprecated"):
        changed = rewrite_deprecated_variants(spec, replacements, "test")
    assert changed
    assert "shared" not in spec.variants


def test_rewrite_no_op_when_variant_absent(mock_packages):
    """Tests that a spec without the deprecated variant is unchanged."""
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-with-replace")
    spec = spack.spec.Spec("deprecated-with-replace libs=shared")
    changed = rewrite_deprecated_variants(spec, pkg_cls.replacements, "test")
    assert not changed
    assert "shared" not in spec.variants


def test_rewrite_warning_contains_provenance(mock_packages):
    """Tests that the warning message includes the provenance string."""
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-with-replace")
    spec = spack.spec.Spec("deprecated-with-replace+shared")
    with pytest.warns(UserWarning, match="my-provenance"):
        rewrite_deprecated_variants(spec, pkg_cls.replacements, "my-provenance")


def test_apply_replacements_noop_for_unknown_package(mock_packages):
    """Tests that apply_replacements_to_spec is a no-op for packages without replacements."""
    spec = spack.spec.Spec("deprecated-with-reason+shared")
    changed = apply_replacements_to_spec(spec, provenance="test")
    assert not changed


# ---------------------------------------------------------------------------
# Tests for msg= parameter
# ---------------------------------------------------------------------------


def test_deprecated_solver_path_custom_message_in_warning(
    mock_packages, concretize_scope, packages_yaml_write
):
    """When msg= is set, the solver-path warning includes the custom message text."""
    packages_yaml_write("""
packages:
  all:
    allowed_deprecation_severity: critical
""")
    with pytest.warns(UserWarning, match="Please upgrade to 2.0."):
        concretize_one("deprecated-with-message@1.0")


def test_deprecated_replace_path_custom_message_in_warning(mock_packages):
    """When msg= is set on a replace= entry, the rewrite warning includes the message."""
    replacements = {
        spack.spec.Spec("+shared"): (
            spack.enums.DeprecationReason.RENAME,
            {"+shared": "libs=shared"},
            "Use libs=shared instead of +shared.",
        )
    }
    spec = spack.spec.Spec("deprecated-with-replace+shared")
    with pytest.warns(UserWarning, match="Use libs=shared instead of"):
        rewrite_deprecated_variants(spec, replacements, "test")


# ---------------------------------------------------------------------------
# Tests for None sentinel (removed variant, no replacement)
# ---------------------------------------------------------------------------

_REMOVED_REPLACEMENTS = {
    spack.spec.Spec("~shared"): (
        spack.enums.DeprecationReason.MAINTENANCE,
        {"~shared": None},
        "Static builds are no longer supported.",
    )
}


def test_rewrite_none_value_collects_error(mock_packages):
    """With errors=[], a None-mapped variant appends an error and does not warn."""
    spec = spack.spec.Spec("deprecated-with-removed-variant~shared")
    errors = []
    changed = rewrite_deprecated_variants(spec, _REMOVED_REPLACEMENTS, "test", errors=errors)
    assert changed
    assert "shared" not in spec.variants
    assert len(errors) == 1
    assert "Static builds" in errors[0]


def test_rewrite_none_value_raises_without_errors_list(mock_packages):
    """Without an errors list, a None-mapped variant raises SpackError immediately."""
    spec = spack.spec.Spec("deprecated-with-removed-variant~shared")
    with pytest.raises(spack.error.SpackError):
        rewrite_deprecated_variants(spec, _REMOVED_REPLACEMENTS, "test")


def test_solver_setup_raises_for_removed_variant_input_spec(mock_packages, concretize_scope):
    """Concretizing a spec with a None-mapped removed variant raises at setup time."""
    with pytest.raises(spack.error.SpackError, match="no replacement"):
        concretize_one("deprecated-with-removed-variant~shared")


# ---------------------------------------------------------------------------
# Bug fix: deprecated-variant rewriting and toolchain expansion in 'when' clauses
# ---------------------------------------------------------------------------


def test_packages_yaml_prefer_when_deprecated_variant_is_rewritten(
    mock_packages, concretize_scope, packages_yaml_write
):
    """The 'when:' clause in a packages.yaml prefer entry is rewritten for deprecated variants.

    prefer: [{spec: '@1.0', when: '~shared'}] should be treated as
    prefer: [{spec: '@1.0', when: 'libs=static'}] because ~shared is deprecated.
    When the user requests libs=static, the rewritten condition fires and @1.0 is preferred
    over the default @2.0.
    """
    packages_yaml_write("""
packages:
  deprecated-with-replace:
    prefer:
    - spec: "@1.0"
      when: "~shared"
""")
    with pytest.warns(UserWarning, match="deprecated"):
        spec = concretize_one("deprecated-with-replace libs=static")
    assert spec.satisfies("@1.0")


def test_packages_yaml_conflict_when_deprecated_variant_is_rewritten(
    mock_packages, concretize_scope, packages_yaml_write
):
    """The 'when:' clause in a packages.yaml conflict entry is rewritten for deprecated variants.

    conflict: [{spec: '@2.0', when: '~shared'}] should be treated as
    conflict: [{spec: '@2.0', when: 'libs=static'}] because ~shared is deprecated.
    When requesting libs=static, the rewritten condition fires, conflicting with @2.0,
    so @1.0 is selected.
    """
    packages_yaml_write("""
packages:
  deprecated-with-replace:
    conflict:
    - spec: "@2.0"
      when: "~shared"
""")
    with pytest.warns(UserWarning, match="deprecated"):
        spec = concretize_one("deprecated-with-replace libs=static")
    assert spec.satisfies("@1.0")


def test_solver_setup_raises_for_removed_variant_in_packages_yaml(
    mock_packages, concretize_scope, packages_yaml_write
):
    """A packages.yaml require: entry with a removed variant raises at setup time."""
    packages_yaml_write("""
packages:
  deprecated-with-removed-variant:
    require: ['~shared']
""")
    with pytest.raises(spack.error.SpackError, match="no replacement"):
        concretize_one("deprecated-with-removed-variant")


def test_solver_setup_raises_for_removed_variant_in_directive(mock_packages, concretize_scope):
    """A depends_on() using a removed variant raises at setup time."""
    with pytest.raises(spack.error.SpackError, match="no replacement"):
        concretize_one("uses-deprecated-removed-variant")
