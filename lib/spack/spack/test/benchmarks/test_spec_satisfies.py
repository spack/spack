# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Micro-benchmarks for Spec.satisfies.

Run with:
    pytest lib/spack/spack/test/benchmarks/test_spec_satisfies.py --benchmark-only
"""

import pytest

import spack.concretize
import spack.spec

# Cache concretized specs by their abstract string — concretization is expensive and
# several test cases share the same lhs package.
_CONCRETIZED: dict = {}

pytestmark = pytest.mark.benchmark

# id -> (lhs, rhs, expected) — parsed once at module scope, never inside the timed call
_ABSTRACT_LHS = {
    # root-only, no virtuals
    "name-only": ("zlib", "zlib", True),
    "version-satisfied": ("zlib@1.2.13", "zlib@1.2:", True),
    "version-not-satisfied": ("zlib@1.2.13", "zlib@2:", False),
    "variant-satisfied": ("zlib@1.2.13+shared", "zlib+shared", True),
    "variant-not-satisfied": ("zlib@1.2.13~shared", "zlib+shared", False),
    "version-and-variant": ("zlib@1.2.13+shared", "zlib@1.2:+shared", True),
    # direct and transitive dependencies, no virtuals
    "direct-dep-satisfied-with-direct": ("hdf5 %zlib@1.2.13", "hdf5 %zlib@1.2:", True),
    "direct-dep-satisfied-with-transitive": ("hdf5 %zlib@1.2.13", "hdf5 ^zlib@1.2:", True),
    "direct-dep-not-satisfied": ("hdf5 %zlib@1.2.13", "hdf5 ^zlib@2:", False),
    "transitive-dep-satisfied": ("hdf5 ^openmpi@4 ^zlib@1.2.13", "hdf5 ^zlib@1.2:", True),
    # virtuals — root
    "mpi-provider-satisfies-virtual": ("openmpi@2.0.0", "mpi", True),
    "mpi-provider-satisfies-versioned-virtual": ("openmpi@2.0.0", "mpi@2:", True),
    "mpi-provider-does-not-satisfy-unrelated-virtual": ("openmpi@2.0.0", "blas", False),
    "non-provider-does-not-satisfy-virtual": ("zlib@1.2.13", "mpi", False),
    "blas-provider-satisfies-virtual": ("openblas", "blas", True),
    # virtuals — dependency edge
    "virtual-dep-provider-satisfies-virtual": (
        "hdf5 ^[virtuals=mpi] openmpi@2.0.0",
        "hdf5 ^mpi",
        True,
    ),
    "virtual-dep-provider-satisfies-versioned-virtual": (
        "hdf5 ^[virtuals=mpi] openmpi@2.0.0",
        "hdf5 ^mpi@2:",
        True,
    ),
    "virtual-dep-different-provider-satisfies-virtual": (
        "hdf5 ^[virtuals=mpi] mpich@4",
        "hdf5 ^mpi",
        True,
    ),
}


@pytest.fixture(scope="module", params=list(_ABSTRACT_LHS.values()), ids=list(_ABSTRACT_LHS))
def abstract_lhs(request):
    """Abstract lhs vs. abstract rhs"""
    lhs_str, rhs_str, expected = request.param
    return spack.spec.Spec(lhs_str), spack.spec.Spec(rhs_str), expected


def test_satisfies_abstract_lhs(benchmark, abstract_lhs):
    lhs, rhs, expected = abstract_lhs
    result = benchmark(lhs.satisfies, rhs)
    assert result == expected


_CONCRETE_LHS = {
    # root-only, no virtuals
    "version-satisfied": ("zlib", "zlib@1.2:", True),
    "version-not-satisfied": ("zlib", "zlib@2:", False),
    "variant-satisfied": ("zlib", "zlib+shared", True),
    # direct and transitive dependencies, no virtuals
    "direct-dep-satisfied": ("hdf5+mpi", "hdf5 ^zlib-ng@1.2:", True),
    "direct-dep-not-satisfied": ("hdf5+mpi", "hdf5 ^zlib-ng@99:", False),
    "transitive-dep-satisfied": ("hdf5+mpi", "hdf5 ^openmpi ^zlib-ng@1:", True),
    # virtuals — root
    "provider-satisfies-virtual": ("openmpi", "mpi", True),
    "provider-satisfies-versioned-virtual": ("openmpi", "mpi@3:", True),
    # virtuals — dependency edge
    "dep-satisfies-virtual-constraint": ("hdf5+mpi", "hdf5 ^mpi", True),
    "dep-satisfies-versioned-virtual-constraint": ("hdf5+mpi", "hdf5 ^mpi@3:", True),
    "dep-satisfies-named-provider-constraint": ("hdf5+mpi", "hdf5 ^[virtuals=mpi] openmpi", True),
}


@pytest.fixture(scope="module", params=list(_CONCRETE_LHS.values()), ids=list(_CONCRETE_LHS))
def concrete_lhs(request):
    """Concrete lhs vs. abstract rhs"""
    lhs_str, rhs_str, expected = request.param
    if lhs_str not in _CONCRETIZED:
        _CONCRETIZED[lhs_str] = spack.concretize.concretize_one(spack.spec.Spec(lhs_str))
    return _CONCRETIZED[lhs_str], spack.spec.Spec(rhs_str), expected


def test_satisfies_concrete_lhs(benchmark, concrete_lhs):
    lhs, rhs, expected = concrete_lhs
    result = benchmark(lhs.satisfies, rhs)
    assert result == expected
