# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAltgraph(PythonPackage):
    """
    altgraph is a fork of graphlib: a graph (network)
    package for constructing graphs, BFS and DFS traversals,
    topological sort, shortest paths, etc. with graphviz output.
    """

    pypi = "altgraph/altgraph-0.16.1.tar.gz"

    license("MIT")

    version(
        "0.16.1",
        sha256="d6814989f242b2b43025cba7161fc1b8fb487a62cd49c49245d6fd01c18ac997",
        url="https://pypi.org/packages/0a/cc/646187eac4b797069e2e6b736f14cdef85dbe405c9bfc7803ef36e4f62ef/altgraph-0.16.1-py2.py3-none-any.whl",
    )
