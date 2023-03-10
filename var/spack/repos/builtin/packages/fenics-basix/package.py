# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FenicsBasix(CMakePackage):
    """Basix is a finite element definition and tabulation runtime library"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers("mscroggs", "chrisrichardson", "garth-wells", "jhale")

    version("main", branch="main")
    version("0.6.0", sha256="687ae53153c98facac4080dcdc7081701db1dcea8c5e7ae3feb72aec17f83304")
    version("0.5.1", sha256="69133476ac35f0bd0deccb480676030378c341d7dfb2adaca22cd16b7e1dc1cb")
    version("0.4.2", sha256="a54f5e442b7cbf3dbb6319c682f9161272557bd7f42e2b8b8ccef88bc1b7a22f")
    version(
        "0.3.0",
        sha256="9b148fd2a5485c94011fc6ca977ebdef0e51782a62b3654fc044f35b60e2bd07",
        deprecated=True,
    )
    version(
        "0.2.0",
        sha256="e1ec537737adb283717060221635092474e3f2b5b5ba79dfac74aa496bec2fcb",
        deprecated=True,
    )
    version(
        "0.1.0",
        sha256="2ab41fe6ad4f6c42f01b17a6e7c39debb4e0ae61c334d1caebee78b741bca4e7",
        deprecated=True,
    )

    depends_on("cmake@3.19:", type="build")
    depends_on("blas")
    depends_on("lapack")

    depends_on("xtensor@0.23.10:", when="@:0.4")
    depends_on("xtl@0.7.2:", when="@:0.4")
    depends_on("xtensor-blas@0.19.1:", when="@:0.3")

    conflicts(
        "%gcc@:9.10", when="@0.5.0:", msg="fenics-basix requires GCC-10 or newer for C++20 support"
    )
    conflicts(
        "%clang@:9.10",
        when="@0.5.0:",
        msg="fenics-basix requires Clang-10 or newer for C++20 support",
    )

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@0.4.0:"):
            return "cpp"
        return self.stage.source_path
