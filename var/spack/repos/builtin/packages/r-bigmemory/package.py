# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBigmemory(RPackage):
    """Manage Massive Matrices with Shared Memory and Memory-Mapped.

    Files Create, store, access, and manipulate massive matrices.  Matrices are
    allocated to shared memory and may use memory-mapped files. Packages
    'biganalytics', 'bigtabulate', 'synchronicity', and 'bigalgebra' provide
    advanced functionality."""

    cran = "bigmemory"

    version("4.6.1", sha256="b56e157c87ed6c4fc69d4cb9c697ae9a2001726e776e41aa7c48b35327b65141")
    version("4.5.36", sha256="18c67fbe6344b2f8223456c4f19ceebcf6c1166255eab81311001fd67a45ef0e")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-bigmemory-sri", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-uuid@1.0-2:", type=("build", "run"), when="@4.6.1:")
    depends_on("r-bh", type=("build", "run"))
    depends_on("uuid", when="@4.6.1:")
