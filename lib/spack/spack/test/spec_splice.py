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
    "musl": ("libc",),
    "libiconv": ("iconv",),
    "mpich": ("mpi",),
    "zmpi": ("mpi",),
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
    libiconv = node("libiconv@1")
    musl = node("musl@2", (libiconv, "run"))
    spec = node("zmpi@1", (musl, "link"))
    replacement = node("libiconv@2")

    out = spec.splice(replacement, transitive=True)

    assert out.dag_hash() == recomputed_hash(out)


def test_splice_keeps_build_link_edges_of_unspliced_nodes():
    mpich = node("mpich@1")
    zmpi = node("zmpi@2", (mpich, ("build", "link")))
    spec = node("b@2", (zmpi, "link"), (node("musl@2"), "link"))
    replacement = node("musl@1")

    out = spec.splice(replacement, transitive=True)

    edges = out["zmpi"].edges_to_dependencies("mpich")
    assert [e.depflag for e in edges] == [dt.BUILD | dt.LINK]


def test_splice_does_not_modify_its_input():
    mpich = node("mpich@1")
    zmpi = node("zmpi@2", (mpich, ("build", "link")))
    spec = node("b@2", (zmpi, "link"), (node("musl@2"), "link"))
    replacement = node("musl@1")

    spec.splice(replacement, transitive=True)

    assert [e.parent for e in mpich.edges_from_dependents()] == [zmpi]


def test_splice_keeps_other_providers_of_virtuals_the_replacement_can_provide():
    spec = node("glibc@2", (node("mpich@1"), "link"), (node("zmpi@1"), "run", "mpi"))
    replacement = node("mpich@2")

    out = spec.splice(replacement, transitive=True)

    assert sorted(d.name for d in out.dependencies()) == ["mpich", "zmpi"]


def test_intransitive_splice_does_not_make_the_root_a_provider():
    spec = node("mpich@1", (node("musl@1"), "link"))
    c = node("c@2", (node("zmpi@1"), "run", "mpi"))
    replacement = node("musl@2", (c, "link"))

    out = spec.splice(replacement, transitive=False)

    assert [d.name for d in out["c"].dependencies()] == ["zmpi"]


def test_intransitive_splice_of_provider_that_depends_on_the_target_package():
    glibc = node("glibc@2", (node("mpich@2"), "link"), (node("libiconv@1"), "run"))
    spec = node("a@2", (glibc, "run", "iconv"))
    zmpi = node("zmpi@2", (node("glibc@1"), "link"))
    replacement = node("libiconv@2", (zmpi, "link"))

    # libiconv@2 replaces libiconv@1, the node of its name, and needs glibc@2: a cycle
    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=False)


def test_splice_target_disambiguates():
    glibc = node("glibc@2", (node("mpich@2"), "link"), (node("libiconv@1"), "run"))
    spec = node("a@2", (glibc, "run", "iconv"))
    zmpi = node("zmpi@2", (node("glibc@1"), "link"))
    replacement = node("libiconv@2", (zmpi, "link"))

    out = spec.splice(replacement, transitive=False, target=Spec("glibc"))

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_depending_on_an_ancestor(transitive):
    spec = node("a@1", (node("b@1"), "link"))
    replacement = node("b@2", (node("a@2"), "link"))

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_whose_dag_provides_what_the_target_is_used_as(transitive):
    spec = node("d@2", (node("glibc@1"), "run", "libc"))
    replacement = node("musl@2", (node("glibc@2"), "link", "libc"))

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


def test_intransitive_splice_records_installed_build_specs():
    libiconv = node("libiconv@1")
    musl = node("musl@2", (libiconv, "run"))
    spec = node("zmpi@1", (musl, "link"))
    replacement = node("libiconv@2")

    out = spec.splice(replacement, transitive=False)

    assert recomputed_hash(out.build_spec) == spec.dag_hash()


def test_splice_ignores_build_only_dependencies():
    libiconv = node("libiconv@2", (node("d@2"), "build"))
    zmpi = node("zmpi@2", (node("d@1"), "link"), (libiconv, "link"))
    spec = node("glibc@1", (zmpi, "link"))
    replacement = node("d@3", (node("musl@1"), "link"))

    out = spec.splice(replacement, transitive=True)

    assert not out["libiconv"].spliced


def test_splice_provider_that_depends_on_another_version_of_the_target_package():
    spec = node("musl@1", (node("glibc@1"), "link", "iconv"))
    replacement = node("libiconv@1", (node("glibc@2"), "link"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


def test_splice_provider_that_depends_on_the_target():
    zmpi = node("zmpi@1")
    spec = node("d@2", (zmpi, "link", "mpi"))
    glibc = node("glibc@1", (zmpi, "link"))
    replacement = node("mpich@1", (glibc, "link"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="mpi")[0].spec.name == "mpich"


def test_transitive_splice_resolves_virtual_clash_with_a_shared_node():
    glibc = node("glibc@2")
    spec = node("a@2", (node("d@2"), "link"), (glibc, "link", "iconv"))
    replacement = node("d@1", (glibc, "link"), (node("libiconv@1"), "link", "iconv"))

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"
