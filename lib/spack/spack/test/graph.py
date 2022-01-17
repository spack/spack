# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import six

import spack.graph
import spack.repo
import spack.spec


@pytest.mark.parametrize('spec_str', ['mpileaks', 'callpath'])
def test_topo_sort(spec_str, config, mock_packages):
    """Ensure nodes are ordered topologically"""
    s = spack.spec.Spec(spec_str).concretized()
    nodes = spack.graph.topological_sort(s)
    for idx, current in enumerate(nodes):
        assert all(following not in current for following in nodes[idx + 1:])


def test_static_graph_mpileaks(config, mock_packages):
    """Test a static spack graph for a simple package."""
    s = spack.spec.Spec('mpileaks').normalized()

    stream = six.StringIO()
    spack.graph.graph_dot([s], static=True, out=stream)

    dot = stream.getvalue()

    assert '  "mpileaks" [label="mpileaks"]\n' in dot
    assert '  "dyninst" [label="dyninst"]\n'   in dot
    assert '  "callpath" [label="callpath"]\n' in dot
    assert '  "libelf" [label="libelf"]\n'     in dot
    assert '  "libdwarf" [label="libdwarf"]\n' in dot

    mpi_providers = spack.repo.path.providers_for('mpi')
    for spec in mpi_providers:
        assert ('"mpileaks" -> "%s"' % spec.name) in dot
        assert ('"callpath" -> "%s"' % spec.name) in dot

    assert '  "dyninst" -> "libdwarf"\n'  in dot
    assert '  "callpath" -> "dyninst"\n'  in dot
    assert '  "libdwarf" -> "libelf"\n'   in dot
    assert '  "mpileaks" -> "callpath"\n' in dot
    assert '  "dyninst" -> "libelf"\n'    in dot


def test_dynamic_dot_graph_mpileaks(mock_packages, config):
    """Test dynamically graphing the mpileaks package."""
    s = spack.spec.Spec('mpileaks').concretized()
    stream = six.StringIO()
    spack.graph.graph_dot([s], static=False, out=stream)
    dot = stream.getvalue()

    nodes_to_check = ['mpileaks', 'mpi', 'callpath', 'dyninst', 'libdwarf', 'libelf']
    hashes = {}
    for name in nodes_to_check:
        current = s[name]
        current_hash = current.dag_hash()
        hashes[name] = current_hash
        assert '  "{0}" [label="{1}"]\n'.format(
            current_hash, spack.graph.node_label(current)
        ) in dot

    dependencies_to_check = [
        ('dyninst', 'libdwarf'),
        ('callpath', 'dyninst'),
        ('mpileaks', 'mpi'),
        ('libdwarf', 'libelf'),
        ('callpath', 'mpi'),
        ('mpileaks', 'callpath'),
        ('dyninst', 'libelf')
    ]
    for parent, child in dependencies_to_check:
        assert '  "{0}" -> "{1}"\n'.format(hashes[parent], hashes[child]) in dot


def test_ascii_graph_mpileaks(config, mock_packages, monkeypatch):
    monkeypatch.setattr(
        spack.graph.AsciiGraph, '_node_label',
        lambda self, node: node.name
    )
    s = spack.spec.Spec('mpileaks').concretized()

    stream = six.StringIO()
    graph = spack.graph.AsciiGraph()
    graph.write(s, out=stream, color=False)
    graph_str = stream.getvalue()
    graph_str = '\n'.join([line.rstrip() for line in graph_str.split('\n')])

    assert graph_str == r'''o mpileaks
|\
| o callpath
|/|
o | mpich
 /
o dyninst
|\
o | libdwarf
|/
o libelf
'''


def test_topological_sort_filtering_dependency_types(config, mock_packages):
    s = spack.spec.Spec('both-link-and-build-dep-a').concretized()

    nodes = spack.graph.topological_sort(s, deptype=('link',))
    names = [s.name for s in nodes]
    assert names == ['both-link-and-build-dep-c', 'both-link-and-build-dep-a']
