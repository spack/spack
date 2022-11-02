# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ChainB(Package):
    """
    Part of a collection of mock packages used for testing depth-first vs
    breadth-first traversal. The DAG they form:
    a --> b --> c --> d # a chain
    a --> c             # "skip" connection
    a --> d             # "skip" connection
    Spack's edge order is based on the child package name.
    In depth-first traversal we get a tree that looks like a chain:
    a
      b
        c
          d
    In breadth-first we get the tree:
    a
     b
     c
     d
    """

    homepage = "https://example.com"
    has_code = False
    version("1.0")
    depends_on("chain-c")
