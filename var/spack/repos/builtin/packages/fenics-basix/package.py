# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FenicsBasix(CMakePackage):
    """FEniCS element and quadrature runtime"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers = ["mscroggs", "chrisrichardson", "garth-wells"]

    version("main", branch="main")
    version("0.3.0", sha256="9b148fd2a5485c94011fc6ca977ebdef0e51782a62b3654fc044f35b60e2bd07")
    version("0.2.0", sha256="e1ec537737adb283717060221635092474e3f2b5b5ba79dfac74aa496bec2fcb")
    version("0.1.0", sha256="2ab41fe6ad4f6c42f01b17a6e7c39debb4e0ae61c334d1caebee78b741bca4e7")

    depends_on("cmake@3.18:", type="build")
    depends_on("xtl@0.7.2:")
    depends_on("xtensor@0.23.10:")
    depends_on("blas")
    depends_on("lapack")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@main"):
            return "cpp"
        return self.stage.source_path
