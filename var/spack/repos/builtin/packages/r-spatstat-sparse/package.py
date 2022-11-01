# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatSparse(RPackage):
    """Sparse Three-Dimensional Arrays and Linear Algebra Utilities.

    Defines sparse three-dimensional arrays and supports standard operations on
    them. The package also includes utility functions for matrix calculations
    that are common in statistics, such as quadratic forms."""

    cran = "spatstat.sparse"

    version("2.1-1", sha256="9a35ad69715b767b3ae60b02dce05ccf108fcccdf95bbc8f7d02557bcbde7303")
    version("2.1-0", sha256="0019214418668cba9f01ee5901ed7f4dba9cfee5ff62d5c7e1c914adfbea0e91")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-tensor", type=("build", "run"))
    depends_on("r-spatstat-utils@2.1-0:", type=("build", "run"))
