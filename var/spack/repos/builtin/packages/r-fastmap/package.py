# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastmap(RPackage):
    """Fast Implementation of a Key-Value Store.

    Fast implementation of a key-value store. Environments are commonly used as
    key-value stores, but every time a new key is used, it is added to R's
    global symbol table, causing a small amount of memory leakage. This can be
    problematic in cases where many different keys are used. Fastmap avoids
    this memory leak issue by implementing the map using data structures in
    C++."""

    cran = "fastmap"

    version("1.1.0", sha256="9113e526b4c096302cfeae660a06de2c4c82ae4e2d3d6ef53af6de812d4c822b")
    version("1.0.1", sha256="4778b05dfebd356f8df980dfeff3b973a72bca14898f870e5c40c1d84db9faec")
