# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Regression tests for Spec.splice on hand-built concrete specs, which need no repository."""

import re
from typing import Dict, List

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


def dags(*texts: str) -> List[Spec]:
    """Concrete DAGs from lines ``parent -> child [deptypes] as virtuals``, or ``node`` for a DAG
    of one node. The first node of each DAG is its root. Nodes with the same name and version are
    the same node, also across DAGs."""
    edges: Dict[str, list] = {}
    roots = []
    for text in texts:
        lines = text.strip().splitlines()
        roots.append(lines[0].split()[0])
        for line in lines:
            match = re.fullmatch(r"\s*(\S+)(?: -> (\S+) \[([\w,]+)\](?: as ([\w,]+))?)?\s*", line)
            assert match, f"invalid line: {line}"
            parent, child, deptypes, virtuals = match.groups()
            edges.setdefault(parent, [])
            if child:
                edges.setdefault(child, [])
                virtuals = tuple(virtuals.split(",")) if virtuals else ()
                edges[parent].append((child, dt.canonicalize(deptypes.split(",")), virtuals))

    nodes: Dict[str, Spec] = {}

    def make(name_version: str) -> Spec:
        if name_version not in nodes:
            name, version = name_version.split("@")
            spec = Spec(f"{name}@={version} arch=linux-ubuntu26.04-x86_64")
            spec._provided_virtuals = tuple(Spec(v) for v in PROVIDES.get(name, ()))
            spec._package_hash = f"{name}{version}".ljust(32, "0")
            for child, depflag, virtuals in edges[name_version]:
                spec._add_dependency(make(child), depflag=depflag, virtuals=virtuals)
            spec._mark_concrete()
            nodes[name_version] = spec
        return nodes[name_version]

    return [make(root) for root in roots]


def recomputed_hash(spec: Spec) -> str:
    copy = spec.copy()
    for n in copy.traverse():
        n.clear_caches(keep_package_hash=True)
    return copy.dag_hash()


@pytest.mark.xfail(strict=True, reason="stale hashes, #53303")
def test_splice_hashes_are_those_of_the_spliced_dag():
    spec, replacement = dags(
        """
        zmpi@1 -> musl@2 [link]
        musl@2 -> libiconv@1 [run]
        """,
        "libiconv@2",
    )

    out = spec.splice(replacement, transitive=True)

    assert out.dag_hash() == recomputed_hash(out)


@pytest.mark.xfail(strict=True, reason="split edges, #53303")
def test_splice_keeps_build_link_edges_of_unspliced_nodes():
    spec, replacement = dags(
        """
        b@2 -> zmpi@2 [link]
        b@2 -> musl@2 [link]
        zmpi@2 -> mpich@1 [build,link]
        """,
        "musl@1",
    )

    out = spec.splice(replacement, transitive=True)

    edges = out["zmpi"].edges_to_dependencies("mpich")
    assert [e.depflag for e in edges] == [dt.BUILD | dt.LINK]


@pytest.mark.xfail(strict=True, reason="re-added build edges point into the input spec")
def test_splice_does_not_modify_its_input():
    spec, replacement = dags(
        """
        b@2 -> zmpi@2 [link]
        b@2 -> musl@2 [link]
        zmpi@2 -> mpich@1 [build,link]
        """,
        "musl@1",
    )
    mpich = spec["mpich"]

    spec.splice(replacement, transitive=True)

    assert [e.parent for e in mpich.edges_from_dependents()] == [spec["zmpi"]]


@pytest.mark.xfail(strict=True, reason="unrelated providers replaced, #53304")
def test_splice_keeps_other_providers_of_virtuals_the_replacement_can_provide():
    spec, replacement = dags(
        """
        glibc@2 -> mpich@1 [link]
        glibc@2 -> zmpi@1 [run] as mpi
        """,
        "mpich@2",
    )

    out = spec.splice(replacement, transitive=True)

    assert sorted(d.name for d in out.dependencies()) == ["mpich", "zmpi"]


@pytest.mark.xfail(
    strict=True, reason="the root counts as provider of what its package can provide"
)
def test_intransitive_splice_does_not_make_the_root_a_provider():
    spec, replacement = dags(
        "mpich@1 -> musl@1 [link]",
        """
        musl@2 -> c@2 [link]
        c@2 -> zmpi@1 [run] as mpi
        """,
    )

    out = spec.splice(replacement, transitive=False)

    assert [d.name for d in out["c"].dependencies()] == ["zmpi"]


@pytest.mark.xfail(
    strict=True, reason="intransitive splice recurses forever", raises=RecursionError
)
def test_intransitive_splice_of_provider_that_depends_on_the_target_package():
    spec, replacement = dags(
        """
        a@2 -> glibc@2 [run] as iconv
        glibc@2 -> mpich@2 [link]
        glibc@2 -> libiconv@1 [run]
        """,
        """
        libiconv@2 -> zmpi@2 [link]
        zmpi@2 -> glibc@1 [link]
        """,
    )

    out = spec.splice(replacement, transitive=False)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.xfail(strict=True, reason="impossible splices are accepted")
@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_depending_on_an_ancestor(transitive):
    spec, replacement = dags("a@1 -> b@1 [link]", "b@2 -> a@2 [link]")

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.xfail(strict=True, reason="impossible splices are accepted")
@pytest.mark.parametrize("transitive", [True, False])
def test_splice_rejects_replacement_whose_dag_provides_what_the_target_is_used_as(transitive):
    spec, replacement = dags("d@2 -> glibc@1 [run] as libc", "musl@2 -> glibc@2 [link] as libc")

    with pytest.raises(SpliceError):
        spec.splice(replacement, transitive=transitive)


@pytest.mark.xfail(strict=True, reason="intransitive splices record half-spliced build specs")
def test_intransitive_splice_records_installed_build_specs():
    spec, replacement = dags(
        """
        zmpi@1 -> musl@2 [link]
        musl@2 -> libiconv@1 [run]
        """,
        "libiconv@2",
    )

    out = spec.splice(replacement, transitive=False)

    assert recomputed_hash(out.build_spec) == spec.dag_hash()


@pytest.mark.xfail(strict=True, reason="build-only deps are copied and matched as link/run deps")
def test_splice_ignores_build_only_dependencies():
    spec, replacement = dags(
        """
        glibc@1 -> zmpi@2 [link]
        zmpi@2 -> d@1 [link]
        zmpi@2 -> libiconv@2 [link]
        libiconv@2 -> d@2 [build]
        """,
        "d@3 -> musl@1 [link]",
    )

    out = spec.splice(replacement, transitive=True)

    assert not out["libiconv"].spliced


@pytest.mark.xfail(strict=True, reason="name match takes the role of the target")
def test_splice_provider_that_depends_on_another_version_of_the_target_package():
    spec, replacement = dags("musl@1 -> glibc@1 [link] as iconv", "libiconv@1 -> glibc@2 [link]")

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"


@pytest.mark.xfail(strict=True, reason="a replacement depending on the target is not spliced")
def test_splice_provider_that_depends_on_the_target():
    spec, replacement = dags(
        "d@2 -> zmpi@1 [link] as mpi",
        """
        mpich@1 -> glibc@1 [link]
        glibc@1 -> zmpi@1 [link]
        """,
    )

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="mpi")[0].spec.name == "mpich"


@pytest.mark.xfail(strict=True, reason="a provider shared by name hides a clash on its virtual")
def test_transitive_splice_resolves_virtual_clash_with_a_shared_node():
    spec, replacement = dags(
        """
        a@2 -> d@2 [link]
        a@2 -> glibc@2 [link] as iconv
        """,
        """
        d@1 -> glibc@2 [link]
        d@1 -> libiconv@1 [link] as iconv
        """,
    )

    out = spec.splice(replacement, transitive=True)

    assert out.edges_to_dependencies(virtuals="iconv")[0].spec.name == "libiconv"
