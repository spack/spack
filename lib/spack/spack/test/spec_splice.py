# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Regression tests for Spec.splice on hand-built concrete specs, which need no repository."""

import pytest

import spack.deptypes as dt
from spack.spec import Spec, SpliceError

#: Virtuals each package can provide
PROVIDES = {
    "glibc": ("libc", "iconv"),
    "libiconv": ("iconv",),
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


def test_splice_hashes_are_those_of_the_spliced_dag():
    """The result has correct hashes."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    replacement = node("zlib@2")

    out = spec.splice(replacement, transitive=True)

    assert out.dag_hash() == recomputed_hash(out)


def test_splice_keeps_build_link_edges_of_unspliced_nodes():
    """Unchanged nodes keep their build edges."""
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, ("build", "link")))
    curl = node("curl@1")
    spec = node("netcdf-c@1", (hdf5, "link"), (curl, "link"))
    replacement = node("curl@2")

    out = spec.splice(replacement, transitive=True)

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

    out = spec.splice(replacement, transitive=True)

    assert sorted(d.name for d in out.dependencies()) == ["glibc", "libiconv"]


def test_intransitive_splice_does_not_make_the_root_a_provider():
    """A node provides only what its parents use it as."""
    hwloc = node("hwloc@1")
    spec = node("openmpi@1", (hwloc, "link"))
    mpich = node("mpich@1")
    replacement = node("hwloc@2", (mpich, "link", "mpi"))  # hwloc +netloc

    out = spec.splice(replacement, transitive=False)

    assert [d.name for d in out["hwloc"].dependencies()] == ["mpich"]


def test_intransitive_splice_of_provider_that_depends_on_the_target_package():
    """Splicing rejects cycles."""
    libiconv = node("libiconv@1")
    linux_headers = node("linux-headers@1")
    glibc_2 = node("glibc@2", (libiconv, "link"), (linux_headers, "link"))
    spec = node("gettext@1", (glibc_2, "link", "iconv"))
    glibc_1 = node("glibc@1")
    replacement = node("libiconv@2", (glibc_1, "link"))

    # libiconv@2 replaces libiconv@1, the node of its name, and needs glibc@2: a cycle
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

    out = spec.splice(replacement, transitive=False)

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

    out = spec.splice(replacement, transitive=True)

    assert not out["glib"].spliced


def test_splice_provider_that_depends_on_another_version_of_the_target_package():
    """The replacement takes over the target's virtuals."""
    glibc_1 = node("glibc@1")
    spec = node("gettext@1", (glibc_1, "link", "iconv"))
    glibc_2 = node("glibc@2")
    replacement = node("libiconv@1", (glibc_2, "link"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


def test_splice_provider_that_depends_on_the_target():
    """The replacement takes over the target's virtuals."""
    glibc = node("glibc@1")  # shared by spec and replacement
    spec = node("gettext@1", (glibc, "link", "iconv"))
    replacement = node("libiconv@1", (glibc, "link"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


def test_transitive_splice_resolves_virtual_clash_with_a_shared_node():
    """Transitive splices use the replacement's providers."""
    glibc = node("glibc@2")  # shared by spec and replacement
    libxml2 = node("libxml2@2")
    spec = node("libxslt@1", (libxml2, "link"), (glibc, "link", "iconv"))
    libiconv = node("libiconv@1")
    replacement = node("libxml2@1", (glibc, "link"), (libiconv, "link", "iconv"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


def test_splicing_the_original_back_gives_the_original_spec():
    """Splicing the original back undoes the splice."""
    zlib_1 = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib_1, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    zlib_2 = node("zlib@2")

    out = spec.splice(zlib_2, transitive=True).splice(zlib_1, transitive=True)

    assert out.dag_hash() == spec.dag_hash()


def test_intransitive_splice_ignores_virtuals_only_the_target_uses():
    """Intransitive splices ignore how the target used its dependencies."""
    glibc = node("glibc@2")  # shared by spec and replacement
    libxml2_1 = node("libxml2@1", (glibc, "link", "iconv", "libc"))
    spec = node("fontconfig@1", (glibc, "link", "libc"), (libxml2_1, "link"))
    libiconv = node("libiconv@1")
    replacement = node("libxml2@2", (glibc, "link", "libc"), (libiconv, "link", "iconv"))

    out = spec.splice(replacement, transitive=False)

    assert out["libxml2"].edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.xfail(strict=True, reason="edges are split by virtual")
def test_splice_rejects_moving_part_of_an_edge():
    """Relocation maps each old dependency to one new dependency."""
    glibc = node("glibc@2")
    libxml2 = node("libxml2@1", (glibc, "link", "libc"))
    spec = node("libxslt@1", (glibc, "link", "libc", "iconv"), (libxml2, "link"))
    libiconv = node("libiconv@1")
    replacement = node("libxml2@2", (glibc, "link", "libc"), (libiconv, "link", "iconv"))

    # libxslt would link libiconv for iconv, but its binary takes iconv from glibc
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
