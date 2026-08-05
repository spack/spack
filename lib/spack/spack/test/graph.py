# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import io

import spack.concretize
import spack.graph
import spack.repo


def test_dynamic_dot_graph_mpileaks(config, mock_packages):
    """Test dynamically graphing the mpileaks package."""
    s = spack.concretize.concretize_one("mpileaks")
    stream = io.StringIO()
    spack.graph.graph_dot([s], out=stream)
    dot = stream.getvalue()

    nodes_to_check = ["mpileaks", "mpi", "callpath", "dyninst", "libdwarf", "libelf"]
    hashes, builder = {}, spack.graph.SimpleDAG()
    for name in nodes_to_check:
        current = s[name]
        current_hash = current.dag_hash()
        hashes[name] = current_hash
        node_options = builder.node_entry(current)[1]
        assert node_options in dot

    dependencies_to_check = [
        ("dyninst", "libdwarf"),
        ("callpath", "dyninst"),
        ("mpileaks", "mpi"),
        ("libdwarf", "libelf"),
        ("callpath", "mpi"),
        ("mpileaks", "callpath"),
        ("dyninst", "libelf"),
    ]
    for parent, child in dependencies_to_check:
        assert '  "{0}" -> "{1}"\n'.format(hashes[parent], hashes[child]) in dot


def test_ascii_graph_mpileaks(config, mock_packages, monkeypatch):
    monkeypatch.setattr(spack.graph.AsciiGraph, "_node_label", lambda self, node: node.name)
    s = spack.concretize.concretize_one("mpileaks")

    stream = io.StringIO()
    graph = spack.graph.AsciiGraph()
    graph.write(s, out=stream, color=False)
    graph_str = stream.getvalue()
    graph_str = "\n".join([line.rstrip() for line in graph_str.split("\n")])

    assert (
        graph_str
        == r"""o mpileaks
|\
| |\
| | |\
| | | |\
| | | | o callpath
| |_|_|/|
|/| |_|/|
| |/| |/|
| | |/|/|
| | | | o dyninst
| | |_|/|
| |/| |/|
| | |/|/|
| | | | |\
o | | | | | mpich
|\| | | | |
|\ \ \ \ \ \
| |_|/ / / /
|/| | | | |
| |/ / / /
| | | | o libdwarf
| |_|_|/|
|/| |_|/|
| |/| |/|
| | |/|/
| | | o libelf
| |_|/|
|/| |/|
| |/|/
| o | compiler-wrapper
|  /
| o gcc-runtime
|/
o gcc
"""
        or graph_str
        == r"""o mpileaks
|\
| |\
| | |\
| | | o callpath
| |_|/|
|/| |/|
| |/|/|
| | | o dyninst
| | |/|
| |/|/|
| | | |\
o | | | | mpich
|\| | | |
| |/ / /
|/| | |
| | | o libdwarf
| |_|/|
|/| |/|
| |/|/
| | o libelf
| |/|
|/|/
| o gcc-runtime
|/
o gcc
"""
    )


def test_ascii_graph_cyclic_run_deps(config, mock_packages, repo_builder, monkeypatch):
    """`spack graph` (ASCII) renders a spec containing a circular run dependency.

    ``graph-cyc-a <-> graph-cyc-b`` depend on each other at runtime. The edge that closes the
    cycle cannot be drawn, so its source node is marked with ``*`` and a footnote explains it. The
    graph must render (without crashing) and mention both members of the cycle.
    """
    repo_builder.add_package("graph-cyc-a", dependencies=[("graph-cyc-b", "run", None)])
    repo_builder.add_package("graph-cyc-b", dependencies=[("graph-cyc-a", "run", None)])

    with spack.repo.use_repositories(repo_builder.root):
        s = spack.concretize.concretize_one("graph-cyc-a")

    stream = io.StringIO()
    spack.graph.AsciiGraph().write(s, out=stream, color=False)
    graph_str = stream.getvalue()

    # Both cycle members are rendered.
    assert "graph-cyc-a" in graph_str
    assert "graph-cyc-b" in graph_str

    # Exactly one node is marked with '*' (the source of the cycle-closing back edge), and the
    # footnote explaining the marker is printed.
    node_lines = [line for line in graph_str.splitlines() if "graph-cyc-" in line]
    assert sum(line.rstrip().endswith("*") for line in node_lines) == 1
    assert "circular run dependency that is not shown" in graph_str

    # Footnote contains test description of skipped edge
    spec_format = "{name}@{version}/{hash:7}"
    assert f"{s['graph-cyc-b'].format(spec_format)} -> {s.format(spec_format)}" in graph_str
