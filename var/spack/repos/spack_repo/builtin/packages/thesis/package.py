# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Thesis(CMakePackage):
    """3dThesis is a heat transfer code utilizing a nondimensionalized
    semi-analytic solution to moving heat sources with a 3D Gaussian power density"""

    homepage = "https://github.com/ORNL-MDF/3dThesis"
    git = "https://github.com/ORNL-MDF/3dThesis.git"
    url = "https://github.com/ORNL-MDF/3dThesis/archive/4.0.0.tar.gz"

    maintainers("streeve", "gknapp1", "JamieStumpORNL")

    license("BSD-3-Clause")

    # Versions prior to 4.0 are yet not supported here
    # (could be added with multiple build systems: CMakePackage and MakefilePackage)
    version("master", branch="master")
    version("4.0.0", sha256="94f309e2f41f29dc5551c606de4cb68097fd71e6979858d1615e257b3cba8a85")

    variant("shared", default=True, description="Build shared libraries")
    variant("mpi", default=False, description="Build with MPI support")

    depends_on("cxx", type="build")  # generated
    depends_on("cmake@3.9:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("llvm-openmp", when="%apple-clang", type=("build", "run"))

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("Thesis_REQUIRE_MPI", "mpi"),
        ]
