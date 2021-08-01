# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FenicsBasix(CMakePackage):
    """FEniCS element and quadrature runtime"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers = ["mscroggs", "chrisrichardson", "garth-wells"]

    version("main", branch="main")
    version("0.1.0", sha256="2ab41fe6ad4f6c42f01b17a6e7c39debb4e0ae61c334d1caebee78b741bca4e7")

    depends_on("cmake@3.18:", type="build")
    depends_on("xtl@0.7.2:")
    depends_on("xtensor@0.23.10:")
    depends_on("blas", type=("build", "run"))
