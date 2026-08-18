# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Unit tests for the spec comparison core (spack.spec_diff)."""

from typing import Optional

import pytest

import spack.concretize
import spack.deptypes as dt
import spack.spec
from spack import spec_diff


def _first_attribute(
    divergence: spec_diff.NodeDivergence,
    category: spec_diff.DiffCategory,
    key: Optional[str] = None,
) -> Optional[spec_diff.AttributeDiff]:
    for attr in divergence.attributes:
        if attr.category == category and (key is None or attr.key == key):
            return attr
    return None


def test_diff_identical_dags(mock_packages, config):
    """Tests that diffing identical DAGs reports no differences."""
    spec = spack.concretize.concretize_one("mpileaks")
    assert spec_diff.diff_concrete_dags(spec, spec) == []
    assert spec_diff.diff_concrete_dags(spec, spec.copy()) == []


def test_diff_root_variant_is_pruned(mock_packages, config):
    """Tests a difference in the root specs"""
    a = spack.concretize.concretize_one("mpileaks~debug")
    b = spack.concretize.concretize_one("mpileaks+debug")

    divergences = spec_diff.diff_concrete_dags(a, b)

    # The only intrinsic difference is at the root
    assert len(divergences) == 1
    assert divergences[0].node_a.name == "mpileaks"

    variant = _first_attribute(divergences[0], spec_diff.DiffCategory.VARIANT, "debug")
    assert variant is not None
    assert variant.value_a == "~debug"
    assert variant.value_b == "+debug"


def test_diff_deep_difference_is_localized(mock_packages, config):
    """Tests finding a difference in the dependencies of a root spec"""
    # mpich is a shared (diamond) dependency, reached from mpileaks directly and through
    # callpath. Only its version changes, so all ancestors are intrinsically identical and
    # the divergence must be reported exactly once, at mpich.
    a = spack.concretize.concretize_one("mpileaks ^mpich@3.0.4")
    b = spack.concretize.concretize_one("mpileaks ^mpich@1.0")

    divergences = spec_diff.diff_concrete_dags(a, b)

    assert len(divergences) == 1
    node = divergences[0]
    assert node.node_a.name == "mpich"
    version = _first_attribute(node, spec_diff.DiffCategory.VERSION)
    assert version is not None
    assert version.value_a == "3.0.4"
    assert version.value_b == "1.0"


def test_diff_concrete_dags_requires_concrete(mock_packages, config):
    """Tests that diffing a non-concrete spec is rejected."""
    concrete = spack.concretize.concretize_one("mpileaks")
    with pytest.raises(spec_diff.SpecDiffError):
        spec_diff.diff_concrete_dags(concrete, spack.spec.Spec("mpileaks"))


def test_diff_reports_variant_present_on_one_side_only(mock_packages, config):
    """Tests that a variant present on only one node is reported as a difference"""
    # "version_based" only exists for @2.0:, so @1.0 does not have it at all.
    a = spack.concretize.concretize_one("conditional-variant-pkg@1.0")
    b = spack.concretize.concretize_one("conditional-variant-pkg@2.0")

    divergences = spec_diff.diff_concrete_dags(a, b)

    assert len(divergences) == 1
    variant = _first_attribute(divergences[0], spec_diff.DiffCategory.VARIANT, "version_based")
    assert variant is not None
    assert variant.value_a == ""
    assert variant.value_b == "+version_based"


def test_diff_reports_flag_difference(mock_packages, config):
    """Tests that a compiler-flag difference is reported at the node that carries it"""
    a = spack.concretize.concretize_one("mpileaks cflags=-O2")
    b = spack.concretize.concretize_one("mpileaks cflags=-O3")

    divergences = spec_diff.diff_concrete_dags(a, b)

    node = next(d for d in divergences if d.node_a.name == "mpileaks")
    flags = _first_attribute(node, spec_diff.DiffCategory.FLAGS, "cflags")
    assert flags is not None
    assert flags.value_a == "-O2"
    assert flags.value_b == "-O3"


def test_diff_reports_added_dependency(mock_packages, config):
    """Tests that a direct dependency present on only one side is reported as a structural diff."""
    # simple-inheritance depends on openblas only when +openblas.
    a = spack.concretize.concretize_one("simple-inheritance+openblas")
    b = spack.concretize.concretize_one("simple-inheritance~openblas")

    divergences = spec_diff.diff_concrete_dags(a, b)

    node = next(d for d in divergences if d.node_a.name == "simple-inheritance")
    dependency = _first_attribute(node, spec_diff.DiffCategory.DEPENDENCY, "openblas")
    assert dependency is not None
    assert dependency.value_a != ""  # openblas is a direct dependency on the +openblas side
    assert dependency.value_b == ""  # and absent on the ~openblas side


def test_diff_reports_recipe_change(mock_packages, config):
    """Test that we report a node whose recipe changed, with an otherwise identical DAG node."""
    spec_a = spack.concretize.concretize_one("mpileaks")
    spec_b = spack.concretize.concretize_one("mpileaks")

    # Drop the cached dag hashes so they are recomputed, then change one node's recipe only
    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    spec_b["callpath"]._package_hash = "0" * 32

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert len(divergences) == 1
    assert divergences[0].node_a.name == "callpath"
    assert [x.category for x in divergences[0].attributes] == [spec_diff.DiffCategory.RECIPE]


def test_diff_does_not_prune_below_a_recipe_change(mock_packages, config):
    """Tests that we never prune on a recipe-only change."""
    spec_a = spack.concretize.concretize_one("mpileaks")
    spec_b = spack.concretize.concretize_one("mpileaks")

    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    # `libelf` is reached through `callpath`, so pruning at `callpath` would hide it
    spec_b["callpath"]._package_hash = "0" * 32
    spec_b["libelf"]._package_hash = "1" * 32

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert sorted(x.node_a.name for x in divergences) == ["callpath", "libelf"]


def test_diff_reports_recipe_change_only_as_a_last_resort(mock_packages, config):
    """Tests that a node difference explained by the DAG is not also reported as a
    recipe change.
    """
    spec_a = spack.concretize.concretize_one("mpileaks ^mpich@3.0.4")
    spec_b = spack.concretize.concretize_one("mpileaks ^mpich@1.0")

    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    spec_b["mpich"]._package_hash = "0" * 32

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert len(divergences) == 1
    assert divergences[0].node_a.name == "mpich"
    categories = {x.category for x in divergences[0].attributes}
    assert spec_diff.DiffCategory.VERSION in categories
    assert spec_diff.DiffCategory.RECIPE not in categories


def test_diff_prunes_downstream_of_a_configuration_difference(mock_packages, config):
    """Tests that by default we report where a difference first appears, and prune below it."""
    # `dyninst` is reached only through `callpath`, which itself differs, so pruning hides it
    spec_a = spack.concretize.concretize_one("mpileaks ^callpath@1.0 ^dyninst@8.2")
    spec_b = spack.concretize.concretize_one("mpileaks ^callpath@0.9 ^dyninst@8.1.2")

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert [x.node_a.name for x in divergences] == ["callpath"]


def test_diff_without_pruning_reports_downstream_differences(mock_packages, config):
    """With pruning off, the consequences of a difference are reported as well."""
    spec_a = spack.concretize.concretize_one("mpileaks ^callpath@1.0 ^dyninst@8.2")
    spec_b = spack.concretize.concretize_one("mpileaks ^callpath@0.9 ^dyninst@8.1.2")

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b, prune=False)

    assert sorted(x.node_a.name for x in divergences) == ["callpath", "dyninst"]


def test_diff_tolerates_specs_without_a_package_hash(mock_packages, config):
    """Tests that specs concretized before package hashes existed are compared without raising."""
    spec_a = spack.concretize.concretize_one("mpileaks")
    spec_b = spack.concretize.concretize_one("mpileaks")

    # Reproduce what reading a lockfile older than package hashes leaves behind
    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    spec_b["callpath"]._package_hash = None

    # The node carries no package hash at all, the way an old lockfile leaves it
    assert "package_hash" not in spec_b["callpath"].to_node_dict()

    # `callpath` now hashes differently, but nothing about it can be explained
    assert spec_diff.diff_concrete_dags(spec_a, spec_b) == []


def test_diff_reports_a_differing_external_path(mock_packages, config):
    """Tests that two external specs answering the same request with a different prefix really
    do differ.
    """
    spec_a = spack.concretize.concretize_one("externaltool")
    spec_b = spack.concretize.concretize_one("externaltool")

    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    spec_b._external_path = "/opt/local"

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert len(divergences) == 1
    attribute = _first_attribute(divergences[0], spec_diff.DiffCategory.EXTERNAL, "path")
    assert attribute is not None
    # Read both sides through the property, as the comparison does: it normalizes separators,
    # so the prefix set above comes back as `\opt\local` on Windows.
    assert attribute.value_a == spec_a.external_path
    assert attribute.value_b == spec_b.external_path
    assert attribute.value_a != attribute.value_b


def test_diff_reports_differing_extra_attributes(mock_packages, config):
    """Tests that what was recorded about an external is part of it, and is a nested structure."""
    spec_a = spack.concretize.concretize_one("externaltool")
    spec_b = spack.concretize.concretize_one("externaltool")

    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    spec_b.extra_attributes = {"compilers": {"c": "/usr/bin/gcc"}}

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    attribute = _first_attribute(divergences[0], spec_diff.DiffCategory.EXTERNAL, "attributes")
    assert attribute is not None
    assert "/usr/bin/gcc" in attribute.value_b


def test_diff_names_node_state_that_nothing_else_explains(mock_packages, config):
    """Tests that state reaching the dag hash without a comparison of its own is still named."""
    spec_a = spack.concretize.concretize_one("mpileaks")
    spec_b = spack.concretize.concretize_one("mpileaks")

    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    # as reading an environment written by an older Spack would leave it
    spec_b["callpath"].annotations.original_spec_format = 4

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert [x.node_a.name for x in divergences] == ["callpath"]
    attribute = _first_attribute(divergences[0], spec_diff.DiffCategory.OTHER, "annotations")
    assert attribute is not None


def test_diff_safety_net_ignores_the_dependencies_of_a_node(mock_packages, config):
    """Tests that we don't count the hash for the differences. Each node that depends on a node
    with a change would have the hash changed, so counting hashes as node state would report each
    node instead of localizing the difference.
    """
    spec_a = spack.concretize.concretize_one("mpileaks ^mpich@3.0.4")
    spec_b = spack.concretize.concretize_one("mpileaks ^mpich@1.0")

    # `mpileaks` and `callpath` sit above the change and hash differently because of it
    assert spec_a["callpath"].dag_hash() != spec_b["callpath"].dag_hash()
    assert spec_diff._serialized_difference(spec_a["callpath"], spec_b["callpath"]) == []

    assert [x.node_a.name for x in spec_diff.diff_concrete_dags(spec_a, spec_b)] == ["mpich"]


def test_diff_reports_a_differing_namespace(mock_packages, config):
    """Tests that we consider the namespace when computing the diff."""
    spec_a = spack.concretize.concretize_one("mpileaks")
    spec_b = spack.concretize.concretize_one("mpileaks")

    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    spec_b["callpath"].namespace = "other.repo"

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert [x.node_a.name for x in divergences] == ["callpath"]
    attribute = _first_attribute(divergences[0], spec_diff.DiffCategory.NAMESPACE)
    assert attribute is not None
    assert attribute.value_b == "other.repo"


def test_diff_reports_a_differing_architecture_part(mock_packages, config):
    """Architecture is compared part by part, so a diff can point at the one that changed."""
    spec_a = spack.concretize.concretize_one("mpileaks")
    spec_b = spack.concretize.concretize_one("mpileaks")

    for node in spec_b.traverse():
        node.clear_caches(ignore=("_package_hash",))
    spec_b["callpath"].architecture.os = "ubuntu99"

    divergences = spec_diff.diff_concrete_dags(spec_a, spec_b)

    assert [x.node_a.name for x in divergences] == ["callpath"]
    # the os changed, so neither the platform nor the target is reported
    assert [(x.category, x.key) for x in divergences[0].attributes] == [
        (spec_diff.DiffCategory.ARCHITECTURE, "os")
    ]
    assert divergences[0].attributes[0].value_b == "ubuntu99"


def test_every_category_is_classified_as_pruning_or_not():
    """This test will fail if we ever add another DiffCategory and forget to categorize it
    with respect to its default pruning behavior.
    """
    not_pruning = {spec_diff.DiffCategory.RECIPE, spec_diff.DiffCategory.OTHER}

    assert spec_diff._PRUNING_SUBDAGS | not_pruning == set(spec_diff.DiffCategory)
    assert not spec_diff._PRUNING_SUBDAGS & not_pruning


def test_split_dependencies_are_refused_rather_than_paired_wrongly(mock_packages, config):
    """This test will fail as soon as we allow split dependencies, and is a reminder that actions
    have to be taken in the diff too.
    """
    root = spack.spec.Spec("mpileaks")
    # The shape concretize.lp describes: one name, two specs, told apart by dependency type
    root.add_dependency_edge(
        spack.concretize.concretize_one("mpich@1.0"), depflag=dt.LINK, virtuals=()
    )
    root.add_dependency_edge(
        spack.concretize.concretize_one("mpich@3.0.4"), depflag=dt.BUILD, virtuals=()
    )

    with pytest.raises(spec_diff.SpecDiffError, match="split dependencies") as exc_info:
        spec_diff._direct_children(root)

    assert "two different 'mpich' specs" in exc_info.value.long_message
