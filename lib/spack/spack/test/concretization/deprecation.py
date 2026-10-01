# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.deprecation
import spack.enums
import spack.error
import spack.repo
import spack.spec
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

    with pytest.raises(UnsatisfiableSpecError, match="unspecified"):
        concretize_one("deprecated-old-style@1.0")


def test_version_deprecated_true_prefers_non_deprecated(config, mock_packages):
    """Solver picks @0.9 (non-deprecated) over @1.0 (deprecated) by default."""
    spec = concretize_one("deprecated-old-style")
    assert spec.satisfies("@0.9")


def test_version_deprecated_true_registers_in_deprecations(mock_packages):
    """Tests that version(..., deprecated=True) populates pkg.deprecations with
    reason=unspecified, severity=critical, and the label marking where it comes from.
    """
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-old-style")
    all_entries = [x for entries in pkg_cls.deprecations.values() for x in entries]
    assert all(
        x
        == spack.enums.Deprecation(
            spack.enums.DeprecationReason.UNSPECIFIED,
            spack.enums.DeprecationSeverity.CRITICAL,
            (spack.enums.LEGACY_DEPRECATION_LABEL,),
        )
        for x in all_entries
    )


def test_allowed_deprecation_concretizes_without_warning(
    mock_packages, concretize_scope, packages_yaml_write, recwarn
):
    """A deprecation matched by a selector concretizes silently, with no warning."""
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - severity: critical
""")
    spec = concretize_one("deprecated-with-reason@2.0")
    assert spec.satisfies("@2.0")
    assert not any(
        "deprecat" in str(w.message).lower() or "vuln" in str(w.message).lower()
        for w in recwarn.list
    )


def test_per_package_selector_blocks_a_higher_severity(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that when a severity exceeds the one a selector allows, concretization fails."""
    packages_yaml_write("""
packages:
  deprecated-with-reason:
    deprecation:
      allow:
      - severity: medium
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-reason@2.0")


def test_selector_under_all_blocks_a_higher_severity(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that the selectors under all:deprecation:allow apply when a package declares none
    of its own.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - severity: low
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-reason@2.0")


def test_coexistence_old_and_new_deprecation(mock_packages, mutable_config):
    """Tests that version(..., deprecated=True) and deprecated() on the same version coexist."""
    # The solver avoids the deprecated @1.0 and picks @2.0 by default.
    spec = concretize_one("deprecated-dual")
    assert spec.satisfies("@2.0")

    # With deprecations allowed, @1.0 concretizes without error.
    with mutable_config.override("packages:all:deprecation:allow", [{"severity": "critical"}]):
        assert concretize_one("deprecated-dual@1.0").satisfies("@1.0")


def test_deprecation_scope_runtime_gates_deps_that_would_be_built(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that with the default 'runtime' scope, a deprecated node reachable only through a
    build edge is still gated when it would be built, since building it means compiling
    deprecated code. Only nodes that come from reuse are exempt.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      scope: runtime
""")
    # the deprecated node is only reachable through a build edge, and it is pinned, so there is
    # no alternative version the solver could pick instead
    with pytest.raises(UnsatisfiableSpecError, match="deprecated spec"):
        concretize_one("deprecated-buildtool-client")


def test_deprecation_scope_all_gates_build_only_dep(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that with the 'all' scope, a deprecated node reachable only through a build edge
    is gated.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      scope: all
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-buildtool-client")


def test_old_style_deprecation_uses_exact_version(mock_packages):
    """Tests that version(..., deprecated=True) must map to an exact '@=X.Y' constraint, so that
    the range '@X.Y' does not spuriously match a sub-version such as 'X.Y.Z'.
    """
    pkg_cls = spack.repo.PATH.get_pkg_class("deprecated-old-style")
    (constraint,) = pkg_cls.deprecations  # only @1.0 is deprecated
    assert spack.spec.Spec("deprecated-old-style@=1.0").satisfies(constraint)
    assert not spack.spec.Spec("deprecated-old-style@=1.0.1").satisfies(constraint)


def test_label_selector_skips_deprecation(mock_packages, concretize_scope, packages_yaml_write):
    """Tests that a selector listing the only label of a deprecation skips it, without allowing
    any severity.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0001]
""")
    assert concretize_one("deprecated-with-labels@3.0").satisfies("@3.0")


def test_partially_listed_labels_do_not_skip_deprecation(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that a deprecation citing two labels stays an error until both are allowed."""
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0002]
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-labels@2.0")

    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0002, GHSA-aaaa-bbbb-cccc]
""")
    assert concretize_one("deprecated-with-labels@2.0").satisfies("@2.0")

    # Labels can be allowed on different entries
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0002]
      - labels: [GHSA-aaaa-bbbb-cccc]
""")
    assert concretize_one("deprecated-with-labels@2.0").satisfies("@2.0")


def test_per_package_label_selector_replaces_the_one_under_all(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that a per-package list replaces the one under 'all', like every other 'packages'
    setting.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0001]
  deprecated-with-labels:
    deprecation:
      allow:
      - labels: [CVE-2026-0002, GHSA-aaaa-bbbb-cccc]
""")
    # @2.0 deprecation is skipped by the per-package list
    assert concretize_one("deprecated-with-labels@2.0").satisfies("@2.0")
    # @3.0 is not, because 'all' is no longer consulted
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-labels@3.0")


def test_reason_list_allows_only_the_reasons_it_names(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that a selector naming several reasons holds the ones it omits to the strictest
    policy, whatever their severity.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - reason: [rename, retired, unspecified]
        severity: critical
""")
    # @2.0 is deprecated with reason=vuln, which the selector omits
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-reason@2.0")

    # @1.0 is deprecated with reason=rename, which the selector names
    assert concretize_one("deprecated-with-reason@1.0").satisfies("@1.0")


def test_a_selector_naming_a_reason_allows_no_other(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that a selector constrained to one reason does not allow the others."""
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - reason: vuln
        severity: critical
""")
    # reason=vuln is allowed up to critical
    assert concretize_one("deprecated-with-reason@2.0").satisfies("@2.0")

    # reason=rename is matched by no selector, so it stays disallowed
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-reason@1.0")


def test_per_package_allow_replaces_the_one_under_all(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that a per-package list replaces the one under 'all' outright, so the global
    selectors are not consulted for a package with its own list, while a package without one is
    still judged by 'all'.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - reason: [rename, retired, unspecified]
        severity: high
  deprecated-with-reason:
    deprecation:
      allow:
      - severity: critical
""")
    # the package with its own list is not bound by the reasons the global one names
    assert concretize_one("deprecated-with-reason@2.0").satisfies("@2.0")

    # a package without one is still blocked by it, so the override is scoped to the one package
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-labels@3.0")


def test_selector_without_a_reason_matches_every_reason(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that a selector that constrains only the severity applies to every reason."""
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - severity: critical
""")
    # @2.0 is deprecated with reason=vuln, @1.0 with reason=rename
    assert concretize_one("deprecated-with-reason@2.0").satisfies("@2.0")
    assert concretize_one("deprecated-with-reason@1.0").satisfies("@1.0")


def test_old_and_new_deprecation_are_checked_independently(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that version(..., deprecated=True) and deprecated() on the same version do not
    override one another: each is matched against the selectors on its own, and either one left
    unmatched refuses the version.
    """
    # deprecated-dual@1.0 has unspecified/critical from the keyword and vuln/high from the
    # directive. Allowing unspecified is not enough, because vuln is still forbidden.
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - reason: unspecified
        severity: critical
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-dual@1.0")

    # Symmetrically, allowing only vuln leaves the keyword deprecation in force.
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - reason: vuln
        severity: critical
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-dual@1.0")

    # A selector for each of them is what it takes.
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - reason: unspecified
        severity: critical
      - reason: vuln
        severity: high
""")
    assert concretize_one("deprecated-dual@1.0").satisfies("@1.0")


def test_legacy_config_deprecated_flag_warns(mock_packages, mutable_config):
    """Tests that the legacy config:deprecated fallback still relaxes the policy, and warns."""
    with mutable_config.override("config:deprecated", True):
        with pytest.warns(UserWarning, match="config:deprecated is deprecated"):
            assert concretize_one("deprecated-old-style@1.0").satisfies("@1.0")


@pytest.fixture
def lib_built_with_deprecated_tool(mutable_config, temporary_store):
    """Install deprecated-tool-lib built against the deprecated deprecated-tool@1.0.

    Models a library installed back when the tool it was built with was still allowed.
    """
    with mutable_config.override("packages:all:deprecation:allow", [{"severity": "critical"}]):
        spec = concretize_one("deprecated-tool-lib ^deprecated-tool@1.0")
    assert spec["deprecated-tool"].satisfies("@1.0")
    for node in spec.traverse():
        temporary_store.layout.create_install_directory(node)
        temporary_store.db.add(node, explicit=node.name == spec.name)
    return spec


def test_runtime_scope_does_not_build_with_a_deprecated_tool(
    mock_packages, mutable_config, lib_built_with_deprecated_tool
):
    """Under 'runtime', the deprecation of a build tool is out of scope for an already built
    library, so deprecated-tool-lib stays reusable. It is not out of scope for a build we are
    about to run, so the client must be built with deprecated-tool@2.0.
    """
    mutable_config.set("packages:all:deprecation:scope", "runtime")
    mutable_config.set("concretizer:reuse", True)

    client = concretize_one("deprecated-tool-client")

    # the installed library is reused, its build provenance is not inspected
    assert client["deprecated-tool-lib"].dag_hash() == lib_built_with_deprecated_tool.dag_hash()
    # but the tool we are about to run is not the deprecated one
    assert client["deprecated-tool"].satisfies("@2.0")


def test_all_scope_rebuilds_a_library_built_with_a_deprecated_tool(
    mock_packages, mutable_config, lib_built_with_deprecated_tool
):
    """Under 'all', the build provenance of a reused artifact is in scope, so the installed
    deprecated-tool-lib cannot be used and is rebuilt against deprecated-tool@2.0.
    """
    mutable_config.set("packages:all:deprecation:scope", "all")
    mutable_config.set("concretizer:reuse", True)

    client = concretize_one("deprecated-tool-client")

    # the installed library was built with the deprecated tool, so it is not reused
    assert client["deprecated-tool-lib"].dag_hash() != lib_built_with_deprecated_tool.dag_hash()
    # and nothing in the DAG refers to the deprecated tool any more
    assert all(x.satisfies("@2.0") for x in client.traverse() if x.name == "deprecated-tool")


def test_deprecation_gate_outranks_build_dep_preferences(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that under the 'runtime' scope a deprecated and fresh build dependency is refused,
    even if a preference for it exists.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      scope: runtime
      allow:
      - severity: critical
  deprecated-tool:
    prefer: ["@1.0"]
""")
    # with the deprecation allowed, the preference decides
    assert concretize_one("deprecated-tool-client")["deprecated-tool"].satisfies("@1.0")

    packages_yaml_write("""
packages:
  all:
    deprecation:
      scope: runtime
      allow: []
  deprecated-tool:
    prefer: ["@1.0"]
""")
    # with it disallowed, the gate outranks the preference, which is soft, and @2.0 is selected
    assert concretize_one("deprecated-tool-client")["deprecated-tool"].satisfies("@2.0")


def test_runtime_scope_errors_on_forced_deprecated_build_dep(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that under the 'runtime' scope a deprecated and fresh build dependency is an error,
    whether the version is forced on the command line or by configuration.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      scope: runtime
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated spec"):
        concretize_one("deprecated-tool-client %deprecated-tool@1.0")

    packages_yaml_write("""
packages:
  all:
    deprecation:
      scope: runtime
  deprecated-tool:
    require: "@1.0"
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated spec"):
        concretize_one("deprecated-tool-client")


def test_directive_message_is_reported_on_refusal(mock_packages, mutable_config):
    """Tests that the guidance a recipe attaches with msg= reaches the concretization error."""
    with pytest.raises(UnsatisfiableSpecError, match="use @2.0, which is maintained"):
        concretize_one("deprecated-with-message@1.0")


def test_directive_without_message_reports_only_the_policy(mock_packages, mutable_config):
    """Tests that a deprecation with no msg= names the configuration to change, and nothing
    more.
    """
    with pytest.raises(UnsatisfiableSpecError) as exc_info:
        concretize_one("deprecated-with-reason@2.0")

    config_path = "'packages:deprecated-with-reason:deprecation:allow'"
    message = str(exc_info.value)
    assert f"is not allowed by {config_path}" in message
    assert message.rstrip().endswith(config_path)


def test_every_message_behind_one_error_term_is_reported(mock_packages, mutable_config):
    """Tests that two deprecations agreeing on constraint, reason and severity report both of
    their msg=, and that the error names the deprecated spec rather than only the package.
    """
    with pytest.raises(UnsatisfiableSpecError) as exc_info:
        concretize_one("deprecated-with-message@0.9")

    message = str(exc_info.value)
    assert "'deprecated-with-message@=0.9'" in message
    assert "move to @2.0" in message
    assert "also affects the ABI" in message


def test_selector_attributes_are_conjunctive(mock_packages, concretize_scope, packages_yaml_write):
    """Tests that the attributes of one selector all have to match. deprecated-with-labels@3.0
    is a critical vulnerability labeled CVE-2026-0001, so a selector naming that label matches
    only while its other attributes do too.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0001]
""")
    assert concretize_one("deprecated-with-labels@3.0").satisfies("@3.0")

    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0001]
        severity: high
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-labels@3.0")

    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0001]
        reason: rename
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-labels@3.0")


def test_one_matching_selector_is_enough(mock_packages, concretize_scope, packages_yaml_write):
    """Tests that a deprecation is skipped as soon as one selector in the list matches it."""
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - reason: vuln
        severity: critical
      - reason: rename
        severity: low
""")
    # @2.0 is vuln/critical, @1.0 is rename/low, and each is matched by a different selector
    assert concretize_one("deprecated-with-reason@2.0").satisfies("@2.0")
    assert concretize_one("deprecated-with-reason@1.0").satisfies("@1.0")


def test_legacy_deprecations_are_selectable_alone(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that the reserved label selects the deprecations coming from
    version(..., deprecated=True), without selecting the ones a recipe declares with
    reason="unspecified".
    """
    packages_yaml_write(
        f"""
packages:
  all:
    deprecation:
      allow:
      - labels: [{spack.enums.LEGACY_DEPRECATION_LABEL}]
"""
    )
    assert concretize_one("deprecated-old-style@1.0").satisfies("@1.0")

    # deprecated-with-labels@1.0 is unspecified/critical too, but has no labels
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-labels@1.0")


def test_each_label_needs_a_selector_matching_every_attribute(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that a label is allowed only by a selector whose other attributes also match the
    deprecation.
    """
    #  deprecated-with-labels@2.0 is critical, so the selector naming GHSA-aaaa-bbbb-cccc
    #  with a lower severity does not allow that label.
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0002]
      - labels: [GHSA-aaaa-bbbb-cccc]
        severity: high
""")
    with pytest.raises(UnsatisfiableSpecError, match="deprecated"):
        concretize_one("deprecated-with-labels@2.0")


def test_refusal_reports_only_the_labels_not_allowed(
    mock_packages, concretize_scope, packages_yaml_write
):
    """Tests that the concretization error lists the labels that are still refused, and omits
    the ones the configuration allows.
    """
    packages_yaml_write("""
packages:
  all:
    deprecation:
      allow:
      - labels: [CVE-2026-0002]
""")
    with pytest.raises(UnsatisfiableSpecError) as exc_info:
        concretize_one("deprecated-with-labels@2.0")

    message = str(exc_info.value)
    assert "GHSA-aaaa-bbbb-cccc" in message
    assert "CVE-2026-0002" not in message


def test_patch_fixing_every_label_allows_a_deprecated_spec(mock_packages, mutable_config):
    """Tests that a spec deprecated with labels concretizes when a patch applied to it fixes all
    of them.
    """
    spec = concretize_one("deprecated-patched@1.0")

    assert [x.fixes for x in spec.patches] == [("CVE-2026-1234",)]


def test_refusal_reports_only_the_labels_no_patch_fixes(mock_packages, mutable_config):
    """Tests that a deprecation with a label no patch fixes is refused, and that the error omits
    the labels fixed by the applied patches.
    """
    with pytest.raises(UnsatisfiableSpecError) as exc_info:
        concretize_one("deprecated-patched@0.9")

    message = str(exc_info.value)
    assert "CVE-2026-5678" in message
    assert "CVE-2026-1234" not in message


def test_dependency_patch_fixes_labels_only_under_the_patching_parent(
    mock_packages, mutable_config
):
    """Tests that a patch applied through depends_on(patches=) fixes the labels of the dependency
    under that parent, and nowhere else.
    """
    spec = concretize_one("patches-deprecated-dep")
    assert [x.fixes for x in spec["deprecated-patched-dep"].patches] == [("CVE-2026-4321",)]

    with pytest.raises(UnsatisfiableSpecError, match="CVE-2026-4321"):
        concretize_one("deprecated-patched-dep@1.0")


def test_install_gate_and_reuse_filter_honor_labels_fixed_by_applied_patches(
    mock_packages, mutable_config
):
    """Tests that the install-time gate and the reuse filter let through a spec whose applied
    patches fix every label of its deprecation, and refuse the same version built without them.
    """
    patched = concretize_one("patches-deprecated-dep")
    with mutable_config.override("packages:all:deprecation:allow", [{"severity": "critical"}]):
        unpatched = concretize_one("deprecated-patched-dep@1.0")

    spack.deprecation.check_deprecations([patched])
    with pytest.raises(spack.error.InstallError, match="CVE-2026-4321"):
        spack.deprecation.check_deprecations([unpatched])

    assert spack.deprecation.reusable([patched, unpatched]) == [patched]


def test_installed_spec_without_the_fixing_patch_is_not_reused(
    mock_packages, mutable_config, temporary_store
):
    """Tests that an installed spec lacking the patch that fixes its deprecation is not reused,
    and the dependency is built with the patch instead.
    """
    with mutable_config.override("packages:all:deprecation:allow", [{"severity": "critical"}]):
        unpatched = concretize_one("deprecated-patched-dep@1.0")
    temporary_store.layout.create_install_directory(unpatched)
    temporary_store.db.add(unpatched, explicit=True)
    mutable_config.set("concretizer:reuse", True)

    spec = concretize_one("patches-deprecated-dep")

    assert spec["deprecated-patched-dep"].dag_hash() != unpatched.dag_hash()
    assert [x.fixes for x in spec["deprecated-patched-dep"].patches] == [("CVE-2026-4321",)]


def test_installed_spec_with_the_fixing_patch_is_reused_on_its_own(
    mock_packages, mutable_config, temporary_store
):
    """Tests that an installed spec whose applied patches fix its deprecation can be reused,
    also where the package that applied the patch is not part of the solve.
    """
    parent = concretize_one("patches-deprecated-dep")
    for node in parent.traverse():
        temporary_store.layout.create_install_directory(node)
        temporary_store.db.add(node, explicit=node.name == parent.name)
    mutable_config.set("concretizer:reuse", True)

    spec = concretize_one("deprecated-patched-dep@1.0")

    assert spec.dag_hash() == parent["deprecated-patched-dep"].dag_hash()
