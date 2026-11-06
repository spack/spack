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


@pytest.mark.xfail(strict=True, reason="stale hashes, #53303")
def test_splice_hashes_are_those_of_the_spliced_dag():
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    replacement = node("zlib@2")

    out = spec.splice(replacement, transitive=True)

    assert out.dag_hash() == recomputed_hash(out)


@pytest.mark.xfail(strict=True, reason="split edges, #53303")
def test_splice_keeps_build_link_edges_of_unspliced_nodes():
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, ("build", "link")))
    spec = node("netcdf-c@1", (hdf5, "link"), (node("curl@1"), "link"))
    replacement = node("curl@2")

    out = spec.splice(replacement, transitive=True)

    edges = out["hdf5"].edges_to_dependencies("zlib")
    assert [e.depflag for e in edges] == [dt.BUILD | dt.LINK]


@pytest.mark.xfail(strict=True, reason="re-added build edges point into the input spec")
def test_splice_does_not_modify_its_input():
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, ("build", "link")))
    spec = node("netcdf-c@1", (hdf5, "link"), (node("curl@1"), "link"))
    replacement = node("curl@2")

    spec.splice(replacement, transitive=True)

    assert [e.parent for e in zlib.edges_from_dependents()] == [hdf5]


@pytest.mark.xfail(strict=True, reason="unrelated providers replaced, #53304")
def test_splice_keeps_other_providers_of_virtuals_the_replacement_can_provide():
    spec = node("libxml2@1", (node("glibc@1"), "link"), (node("libiconv@1"), "link", "iconv"))
    replacement = node("glibc@2")

    out = spec.splice(replacement, transitive=True)

    assert sorted(d.name for d in out.dependencies()) == ["glibc", "libiconv"]


@pytest.mark.xfail(
    strict=True, reason="the root counts as provider of what its package can provide"
)
def test_intransitive_splice_does_not_make_the_root_a_provider():
    spec = node("openmpi@1", (node("hwloc@1"), "link"))
    replacement = node("hwloc@2", (node("mpich@1"), "link", "mpi"))  # hwloc +netloc

    out = spec.splice(replacement, transitive=False)

    assert [d.name for d in out["hwloc"].dependencies()] == ["mpich"]


@pytest.mark.xfail(
    strict=True, reason="intransitive splice recurses forever", raises=RecursionError
)
def test_intransitive_splice_of_provider_that_depends_on_the_target_package():
    glibc = node("glibc@2", (node("libiconv@1"), "link"), (node("linux-headers@1"), "link"))
    spec = node("gettext@1", (glibc, "link", "iconv"))
    replacement = node("libiconv@2", (node("glibc@1"), "link"))

    # libiconv@2 replaces libiconv@1, the node of its name, and needs glibc@2: a cycle
    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=False)


@pytest.mark.xfail(strict=True, reason="impossible splices are accepted")
@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_depending_on_an_ancestor(transitive):
    spec = node("harfbuzz@1", (node("freetype@1"), "link"))
    replacement = node("freetype@2", (node("harfbuzz@2"), "link"))

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.xfail(strict=True, reason="impossible splices are accepted")
@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_whose_dag_provides_what_the_target_is_used_as(transitive):
    spec = node("hdf5@1", (node("mpich@1"), "link", "mpi"))
    replacement = node("charmpp@1", (node("mpich@2"), "link", "mpi"))  # AMPI on top of MPI

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.xfail(strict=True, reason="intransitive splices record half-spliced build specs")
def test_intransitive_splice_records_installed_build_specs():
    zlib = node("zlib@1")
    hdf5 = node("hdf5@1", (zlib, "link"))
    spec = node("netcdf-c@1", (hdf5, "link"))
    replacement = node("zlib@2")

    out = spec.splice(replacement, transitive=False)

    assert recomputed_hash(out.build_spec) == spec.dag_hash()


@pytest.mark.xfail(strict=True, reason="build-only deps are copied and matched as link/run deps")
def test_splice_ignores_build_only_dependencies():
    glib = node("glib@2", (node("python@2"), "build"))
    pygobject = node("py-pygobject@1", (node("python@1"), "link"), (glib, "link"))
    spec = node("meld@1", (pygobject, "link"))
    replacement = node("python@3", (node("zlib@1"), "link"))

    out = spec.splice(replacement, transitive=True)

    assert not out["glib"].spliced


@pytest.mark.xfail(strict=True, reason="name match takes the role of the target")
def test_splice_provider_that_depends_on_another_version_of_the_target_package():
    spec = node("gettext@1", (node("glibc@1"), "link", "iconv"))
    replacement = node("libiconv@1", (node("glibc@2"), "link"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.xfail(strict=True, reason="a replacement depending on the target is not spliced")
def test_splice_provider_that_depends_on_the_target():
    glibc = node("glibc@1")
    spec = node("gettext@1", (glibc, "link", "iconv"))
    replacement = node("libiconv@1", (glibc, "link"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.xfail(strict=True, reason="a provider shared by name hides a clash on its virtual")
def test_transitive_splice_resolves_virtual_clash_with_a_shared_node():
    glibc = node("glibc@2")
    spec = node("libxslt@1", (node("libxml2@2"), "link"), (glibc, "link", "iconv"))
    replacement = node("libxml2@1", (glibc, "link"), (node("libiconv@1"), "link", "iconv"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"
