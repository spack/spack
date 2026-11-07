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
    "fftw": ("fftw-api",),
    "amdfftw": ("fftw-api",),
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


def test_splice_hashes_are_those_of_the_spliced_dag():
    """The result has correct hashes."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    replacement = node("zlib@2")

    out = checked_splice(spec, replacement, transitive=True)

    assert out.dag_hash() == recomputed_hash(out)


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


def test_splice_does_not_modify_its_input():
    """Splicing does not modify the inputs."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, ("build", "link")))
    curl = node("curl@1")
    spec = node("netcdf-c@1", (hdf5, "link"), (curl, "link"))
    replacement = node("curl@2")

    spec.splice(replacement, transitive=True)

    assert [e.parent for e in zlib.edges_from_dependents()] == [hdf5]


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


def test_intransitive_splice_does_not_make_the_root_a_provider():
    """A node provides only what its parents use it as."""
    hwloc = node("hwloc@1")
    spec = node("openmpi@1", (hwloc, "link"))
    mpich = node("mpich@1")
    replacement = node("hwloc@2", (mpich, "link", "mpi"))  # hwloc +netloc

    out = checked_splice(spec, replacement, transitive=False)

    assert [d.name for d in out["hwloc"].dependencies()] == ["mpich"]


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


def test_splice_target_disambiguates():
    """The target selects the node to replace."""
    libiconv = node("libiconv@1")
    linux_headers = node("linux-headers@1")
    glibc_2 = node("glibc@2", (libiconv, "link"), (linux_headers, "link"))
    spec = node("gettext@1", (glibc_2, "link", "iconv"))
    glibc_1 = node("glibc@1")
    replacement = node("libiconv@2", (glibc_1, "link"))

    out = spec.splice(replacement, transitive=False, target=Spec("glibc"))

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_depending_on_an_ancestor(transitive):
    """Splicing rejects two nodes of one package."""
    freetype = node("freetype@1")
    spec = node("harfbuzz@1", (freetype, "link"))
    harfbuzz = node("harfbuzz@2")
    replacement = node("freetype@2", (harfbuzz, "link"))

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_whose_dag_provides_what_the_target_is_used_as(transitive):
    """Splicing rejects two providers of one virtual."""
    mpich_1 = node("mpich@1")
    spec = node("hdf5@1", (mpich_1, "link", "mpi"))
    mpich_2 = node("mpich@2")
    replacement = node("charmpp@1", (mpich_2, "link", "mpi"))  # AMPI on top of MPI

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


def test_intransitive_splice_records_installed_build_specs():
    """The build spec is the installed spec."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    replacement = node("zlib@2")

    out = checked_splice(spec, replacement, transitive=False)

    assert recomputed_hash(out.build_spec) == spec.dag_hash()


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


def test_splicing_the_original_back_gives_the_original_spec():
    """Splicing the original back undoes the splice."""
    zlib_1 = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib_1, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    zlib_2 = node("zlib@2")

    spliced = checked_splice(spec, zlib_2, transitive=True)
    out = checked_splice(spliced, zlib_1, transitive=True)

    assert out.dag_hash() == spec.dag_hash()


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
def test_splice_rejects_provider_switch_if_the_old_provider_stays():
    """A node cannot switch provider if the old one stays among its dependencies."""
    fftw = node("fftw@3")
    pfft = node("pfft@1", (fftw, "link"))
    libvdwxc_1 = node("libvdwxc@1", (fftw, "link", "fftw-api"))
    spec = node("octopus@1", (fftw, "link", "fftw-api"), (pfft, "link"), (libvdwxc_1, "link"))
    amdfftw = node("amdfftw@3")
    replacement = node("libvdwxc@2", (amdfftw, "link", "fftw-api"))

    # octopus would use amdfftw, but pfft needs fftw: octopus has one fftw prefix for both
    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=True)


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


@pytest.mark.parametrize("transitive,provider", [(True, "openmpi"), (False, "mpich")])
def test_splice_resolves_clashing_providers_of_a_virtual(transitive, provider):
    """Clashing providers are reconciled like clashing nodes of one name."""
    mpich = node("mpich@1")
    hdf5_1 = node("hdf5@1", (mpich, "link", "mpi"))
    spec = node("netcdf-c@1", (hdf5_1, "link"), (mpich, "link", "mpi"))
    openmpi = node("openmpi@1")
    replacement = node("hdf5@2", (openmpi, "link", "mpi"))

    out = checked_splice(spec, replacement, transitive=transitive)

    # Right if the providers are ABI-compatible, like mpich and openmpi with the MPI ABI. Spack
    # cannot tell: openblas and mkl both provide blas, and cannot stand in for each other.
    providers = {
        e.spec.name for n in out.traverse() for e in n.edges_to_dependencies(virtuals="mpi")
    }
    assert providers == {provider}
