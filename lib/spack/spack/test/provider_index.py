# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for provider index cache files.

Tests assume that mock packages provide this::

  {'blas':   {
       blas: set([netlib-blas, openblas, openblas-with-lapack])},
   'lapack': {lapack: set([netlib-lapack, openblas-with-lapack])},
   'mpi': {mpi@:1: set([mpich@:1]),
                    mpi@:2.0: set([mpich2]),
                    mpi@:2.1: set([mpich2@1.1:]),
                    mpi@:2.2: set([mpich2@1.2:]),
                    mpi@:3: set([mpich@3:]),
                    mpi@:10.0: set([zmpi])},
    'stuff': {stuff: set([externalvirtual])}}
"""

import io

import spack.repo
import spack.spec
from spack.provider_index import ProviderIndex
from spack.spec import Spec


def _build_index(pkg_names, repository):
    index = ProviderIndex()
    index.update_packages(pkg_names, repository)
    return index


def _providers_for(index, virtual):
    """Materialize the providers of a virtual spec from the raw node dicts in the index."""
    return {
        spack.spec.SpecfileLatest.from_node_dict(node)
        for vpkg_node, provider_nodes in index.providers.get(virtual.name, [])
        if spack.spec.SpecfileLatest.from_node_dict(vpkg_node).intersects(virtual, deps=False)
        for node in provider_nodes
    }


def test_provider_index_round_trip(mock_packages):
    p = _build_index(spack.repo.all_package_names(), spack.repo.PATH)

    ostream = io.StringIO()
    p.to_json(ostream)

    istream = io.StringIO(ostream.getvalue())
    q = ProviderIndex.from_json(istream)

    assert p == q


def test_providers_for_simple(mock_packages):
    p = _build_index(spack.repo.all_package_names(), spack.repo.PATH)

    blas_providers = _providers_for(p, Spec("blas"))
    assert Spec("netlib-blas") in blas_providers
    assert Spec("openblas") in blas_providers
    assert Spec("openblas-with-lapack") in blas_providers

    lapack_providers = _providers_for(p, Spec("lapack"))
    assert Spec("netlib-lapack") in lapack_providers
    assert Spec("openblas-with-lapack") in lapack_providers


def test_provider_names_for(mock_packages):
    assert set(spack.repo.PATH.provider_names_for("blas")) >= {
        "netlib-blas",
        "openblas",
        "openblas-with-lapack",
    }
    assert set(spack.repo.PATH.provider_names_for("mpi")) >= {"mpich", "mpich2", "zmpi"}


def test_mpi_providers(mock_packages):
    p = _build_index(spack.repo.all_package_names(), spack.repo.PATH)

    mpi_2_providers = _providers_for(p, Spec("mpi@2"))
    assert Spec("mpich2") in mpi_2_providers
    assert Spec("mpich@3:") in mpi_2_providers

    mpi_3_providers = _providers_for(p, Spec("mpi@3"))
    assert Spec("mpich2") not in mpi_3_providers
    assert Spec("mpich@3:") in mpi_3_providers
    assert Spec("zmpi") in mpi_3_providers


def test_equal(mock_packages):
    p = _build_index(spack.repo.all_package_names(), spack.repo.PATH)
    q = _build_index(spack.repo.all_package_names(), spack.repo.PATH)
    assert p == q


def test_copy(mock_packages):
    p = _build_index(spack.repo.all_package_names(), spack.repo.PATH)
    q = p.copy()
    assert p == q


def test_remove_providers(mock_packages):
    """Test removing providers from the index."""
    p = _build_index(["mpich"], spack.repo.PATH)
    # Check that mpich is a provider for mpi
    assert any(
        node["name"] == "mpich" for _, providers in p.providers["mpi"] for node in providers
    )
    p.remove_providers({"mpich"})
    # After removal, mpich should no longer be a provider for mpi
    assert "mpi" not in p
