# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Regression tests for Spec.splice on hand-built concrete specs, which need no repository."""

import pytest

import spack.deptypes as dt
import spack.traverse
from spack.spec import Spec, SpliceError

#: Virtuals each package can provide
PROVIDES = {
    "glibc": ("libc", "iconv"),
    "libiconv": ("iconv",),
    "libblastrampoline": ("blas", "lapack"),
    "mpich": ("mpi",),
    "openmpi": ("mpi",),
    "charmpp": ("mpi",),
    "openblas": ("blas", "lapack"),
    "intel-oneapi-mkl": ("blas", "lapack"),
}


def node(name_version: str, *edges) -> Spec:
    """A concrete node with edges (child, deptypes) or (child, deptypes, virtual)"""
    name, version = name_version.split("@")
    spec = Spec(f"{name}@={version} arch=linux-ubuntu26.04-x86_64")
    spec._provided_virtuals = tuple(Spec(v) for v in PROVIDES.get(name, ()))
    spec._package_hash = f"{name}{version}".ljust(32, "0")
    for child, deptypes, *virtuals in edges:
        spec._add_dependency(child, depflag=dt.canonicalize(deptypes), virtuals=tuple(virtuals))
    spec._mark_concrete()
    return spec


def recomputed_hash(spec: Spec) -> str:
    copy = spec.copy()
    for n in copy.traverse():
        n.clear_caches(keep_package_hash=True)
    return copy.dag_hash()


def checked_splice(spec: Spec, replacement: Spec, *, transitive: bool) -> Spec:
    """Splice, and check that the result has one node per name and one provider per virtual"""
    out = spec.splice(replacement, transitive=transitive)
    nodes = list(out.traverse(deptype=("link", "run"), key=spack.traverse.by_dag_hash))
    names = [n.name for n in nodes]
    assert len(names) == len(set(names))
    providers = {
        (v, e.spec.name)
        for n in nodes
        for e in n.edges_to_dependencies(depflag=dt.LINK | dt.RUN)
        for v in e.virtuals
    }
    assert len(providers) == len({v for v, _ in providers})
    return out


@pytest.mark.xfail(strict=True, reason="stale hashes, #53303")
def test_splice_hashes_are_those_of_the_spliced_dag():
    """The result has correct hashes."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    replacement = node("zlib@2")

    out = checked_splice(spec, replacement, transitive=True)

    assert out.dag_hash() == recomputed_hash(out)


@pytest.mark.xfail(strict=True, reason="split edges, #53303")
def test_splice_keeps_build_link_edges_of_unspliced_nodes():
    """Unchanged nodes keep their build edges."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, ("build", "link")))
    curl = node("curl@1")
    spec = node("netcdf-c@1", (hdf5, "link"), (curl, "link"))
    replacement = node("curl@2")

    out = checked_splice(spec, replacement, transitive=True)

    edges = out["hdf5"].edges_to_dependencies("zlib")
    assert [e.depflag for e in edges] == [dt.BUILD | dt.LINK]


@pytest.mark.xfail(strict=True, reason="re-added build edges point into the input spec")
def test_splice_does_not_modify_its_input():
    """Splicing does not modify the inputs."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, ("build", "link")))
    curl = node("curl@1")
    spec = node("netcdf-c@1", (hdf5, "link"), (curl, "link"))
    replacement = node("curl@2")

    spec.splice(replacement, transitive=True)

    assert [e.parent for e in zlib.edges_from_dependents()] == [hdf5]


@pytest.mark.xfail(strict=True, reason="unrelated providers replaced, #53304")
def test_splice_keeps_other_providers_of_virtuals_the_replacement_can_provide():
    """Splicing replaces only the target."""
    glibc = node("glibc@1")
    libiconv = node("libiconv@1")
    spec = node("libxml2@1", (glibc, "link"), (libiconv, "link", "iconv"))
    replacement = node("glibc@2")

    out = checked_splice(spec, replacement, transitive=True)

    assert sorted(d.name for d in out.dependencies()) == ["glibc", "libiconv"]


@pytest.mark.parametrize("transitive", [True, False])
def test_splice_replaces_provider_by_one_with_another_backend(transitive):
    """A replacement of the same package brings its own dependencies."""
    openblas = node("openblas@1")
    lbt_openblas = node("libblastrampoline@5", (openblas, "link"))  # provider=openblas
    suite_sparse = node("suite-sparse@1", (lbt_openblas, "link", "blas", "lapack"))
    spec = node("petsc@1", (suite_sparse, "link"), (lbt_openblas, "link", "blas", "lapack"))
    mkl = node("intel-oneapi-mkl@1")
    lbt_mkl = node("libblastrampoline@5", (mkl, "link"))  # provider=mkl

    out = checked_splice(spec, lbt_mkl, transitive=transitive)

    # petsc and suite-sparse link libblastrampoline, whatever it forwards to
    names = sorted(n.name for n in out.traverse(root=False, deptype=("link", "run")))
    assert names == ["intel-oneapi-mkl", "libblastrampoline", "suite-sparse"]
    assert out["suite-sparse"]["libblastrampoline"] == lbt_mkl


@pytest.mark.xfail(
    strict=True, reason="the root counts as provider of what its package can provide"
)
def test_intransitive_splice_does_not_make_the_root_a_provider():
    """A node provides only what its parents use it as."""
    hwloc = node("hwloc@1")
    spec = node("openmpi@1", (hwloc, "link"))
    mpich = node("mpich@1")
    replacement = node("hwloc@2", (mpich, "link", "mpi"))  # hwloc +netloc

    out = checked_splice(spec, replacement, transitive=False)

    assert [d.name for d in out["hwloc"].dependencies()] == ["mpich"]


@pytest.mark.xfail(strict=True, reason="impossible splices are accepted")
def test_intransitive_splice_rejects_dependency_cycle():
    """Splicing rejects cycles."""
    hwloc_1 = node("hwloc@1")
    openmpi = node("openmpi@1", (hwloc_1, "link"))
    spec = node("hdf5@1", (openmpi, "link", "mpi"))
    openmpi_internal_hwloc = node("openmpi@1")
    replacement = node("hwloc@2", (openmpi_internal_hwloc, "link", "mpi"))  # hwloc +netloc

    # hwloc@2 would use the openmpi of the spec, which depends on hwloc
    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=False)


@pytest.mark.xfail(strict=True, reason="impossible splices are accepted")
@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_depending_on_an_ancestor(transitive):
    """Splicing rejects two nodes of one package."""
    freetype = node("freetype@1")
    spec = node("harfbuzz@1", (freetype, "link"))
    harfbuzz = node("harfbuzz@2")
    replacement = node("freetype@2", (harfbuzz, "link"))

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.xfail(strict=True, reason="impossible splices are accepted")
@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_whose_dag_provides_what_the_target_is_used_as(transitive):
    """Splicing rejects two providers of one virtual."""
    mpich_1 = node("mpich@1")
    spec = node("hdf5@1", (mpich_1, "link", "mpi"))
    mpich_2 = node("mpich@2")
    replacement = node("charmpp@1", (mpich_2, "link", "mpi"))  # AMPI on top of MPI

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.xfail(strict=True, reason="intransitive splices record half-spliced build specs")
def test_intransitive_splice_records_installed_build_specs():
    """The build spec is the installed spec."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    replacement = node("zlib@2")

    out = checked_splice(spec, replacement, transitive=False)

    assert recomputed_hash(out.build_spec) == spec.dag_hash()


@pytest.mark.xfail(strict=True, reason="build-only deps are copied and matched as link/run deps")
def test_splice_ignores_build_only_dependencies():
    """Splicing ignores build dependencies."""
    python_2 = node("python@2")
    glib = node("glib@2", (python_2, "build"))
    python_1 = node("python@1")
    pygobject = node("py-pygobject@1", (python_1, "link"), (glib, "link"))
    spec = node("meld@1", (pygobject, "link"))
    zlib = node("zlib@1")
    replacement = node("python@3", (zlib, "link"))

    out = checked_splice(spec, replacement, transitive=True)

    assert not out["glib"].spliced
    assert out["glib"].dependencies(deptype="build") == [python_2]


@pytest.mark.parametrize("transitive,provider", [(True, "openmpi"), (False, "mpich")])
def test_splice_resolves_clashing_providers_of_a_virtual(transitive, provider):
    """Clashing providers are reconciled like clashing nodes of one name."""
    mpich = node("mpich@1")
    hdf5_1 = node("hdf5@1", (mpich, "link", "mpi"))
    spec = node("netcdf-c@1", (hdf5_1, "link"), (mpich, "link", "mpi"))
    openmpi = node("openmpi@1")
    replacement = node("hdf5@2", (openmpi, "link", "mpi"))

    out = checked_splice(spec, replacement, transitive=transitive)

    # the caller vouches that either can stand in for the other, as with the MPI ABI
    providers = {
        e.spec.name for n in out.traverse() for e in n.edges_to_dependencies(virtuals="mpi")
    }
    assert providers == {provider}


@pytest.mark.xfail(strict=True, reason="nodes rewired to their build dependencies stay spliced")
def test_splicing_the_original_back_gives_the_original_spec():
    """Splicing the original back undoes the splice."""
    zlib_1 = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib_1, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    zlib_2 = node("zlib@2")

    spliced = checked_splice(spec, zlib_2, transitive=True)
    out = checked_splice(spliced, zlib_1, transitive=True)

    assert out.dag_hash() == spec.dag_hash()


@pytest.mark.xfail(strict=True, reason="the replacement gets the providers of the target")
def test_intransitive_splice_keeps_provider_of_virtual_only_the_target_used():
    """The replacement keeps its provider of a virtual that no remaining node uses."""
    glibc = node("glibc@2")  # shared by spec and replacement
    libxml2_1 = node("libxml2@1", (glibc, "link", "iconv", "libc"))
    spec = node("fontconfig@1", (glibc, "link", "libc"), (libxml2_1, "link"))
    libiconv = node("libiconv@1")
    replacement = node("libxml2@2", (glibc, "link", "libc"), (libiconv, "link", "iconv"))

    # only libxml2@1 took iconv from glibc
    out = checked_splice(spec, replacement, transitive=False)

    assert out["libxml2"].edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.xfail(strict=True, reason="edges are split by virtual")
def test_splice_rejects_moving_part_of_an_edge():
    """Relocation maps each old dependency to one new dependency."""
    glibc = node("glibc@2")
    libxml2 = node("libxml2@1", (glibc, "link", "libc"))
    spec = node("libxslt@1", (glibc, "link", "libc", "iconv"), (libxml2, "link"))
    libiconv = node("libiconv@1")
    replacement = node("libxml2@2", (glibc, "link", "libc"), (libiconv, "link", "iconv"))

    # libxslt has one glibc prefix, which would have to become both glibc and libiconv
    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=True)


@pytest.mark.xfail(strict=True, reason="dependencies by name are replaced by other packages")
@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacing_a_dependency_by_name_with_another_package(transitive):
    """A dependency by name keeps its package."""
    openblas = node("openblas@1")
    suite_sparse = node("suite-sparse@1", (openblas, "link", "blas", "lapack"))
    spec = node("julia@1", (openblas, "link"), (suite_sparse, "link"))
    replacement = node("intel-oneapi-mkl@1")

    # julia needs openblas, not just blas and lapack
    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)
