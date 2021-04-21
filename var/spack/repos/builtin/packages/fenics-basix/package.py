# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FenicsBasix(CMakePackage):
    """FEniCS element and quadrature runtime"""

    homepage = "https://github.com/FEniCS/basix"
    git = "https://github.com/FEniCS/basix.git"
    maintainers = ["mscroggs", "chrisrichardson"]

    version("main", branch="main")
    # version("0.1.0", sha256="")

    depends_on("cmake@3.16:", type="build")
    depends_on("xtensor@0.23.4:", type="build")
    depends_on("blas", type="run")
