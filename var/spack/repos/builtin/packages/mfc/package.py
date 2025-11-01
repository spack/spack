# Copyright 2013-2025 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Mfc(CMakePackage):
    """MFC (Multicomponent Flow Code) is an exascale multiphase/multiphysics
    compressible flow solver. It scales ideally to 43K+ GPUs on leadership-class
    supercomputers and supports high-order WENO/TENO schemes, immersed boundary
    methods, phase change, surface tension, and MHD."""

    homepage = "https://mflowcode.github.io/"
    url = "https://github.com/MFlowCode/MFC/archive/refs/tags/v5.1.0.tar.gz"
    git = "https://github.com/MFlowCode/MFC.git"

    maintainers("sbryngelson")

    license("MIT")

    version("master", branch="master")
    version("5.1.0", sha256="4684bee6a529287f243f8929fb7edb0dfebbb04df7c1806459761c9a6c9261cf")

    # Build options
    variant("mpi", default=True, description="Build with MPI support")
    variant("openacc", default=False, description="Build with OpenACC GPU support")
    variant("openmp", default=False, description="Build with OpenMP GPU support")
    variant(
        "precision",
        default="double",
        values=("single", "double"),
        description="Floating point precision",
    )
    variant("post_process", default=True, description="Build post-processing tool")

    # Required dependencies
    depends_on("cmake@3.20:", type="build")
    depends_on("py-fypp", type="build")
    depends_on("python@3:", type="build")

    # Runtime dependencies
    depends_on("fftw@3:")
    depends_on("lapack")

    # Optional dependencies
    depends_on("mpi", when="+mpi")
    depends_on("hdf5", when="+post_process")
    depends_on("silo", when="+post_process")

    # GPU dependencies
    depends_on("cuda", when="+openacc ^nvhpc")
    depends_on("hip", when="+openacc ^cce")
    depends_on("hip", when="+openmp ^cce")

    # Compiler requirements
    conflicts("%gcc@:4", msg="MFC requires GCC 5.0 or newer")
    conflicts("%nvhpc@:21.6", msg="MFC requires NVHPC 21.7 or newer")
    conflicts("%apple-clang", msg="MFC does not support Apple Clang")
    conflicts("+openacc", when="%gcc", msg="OpenACC requires NVHPC or Cray compilers")

    def cmake_args(self):
        args = [
            self.define_from_variant("MFC_MPI", "mpi"),
            self.define_from_variant("MFC_OpenACC", "openacc"),
            self.define_from_variant("MFC_OpenMP", "openmp"),
            self.define("MFC_PRE_PROCESS", True),
            self.define("MFC_SIMULATION", True),
            self.define_from_variant("MFC_POST_PROCESS", "post_process"),
        ]

        if self.spec.variants["precision"].value == "single":
            args.append(self.define("MFC_SINGLE_PRECISION", True))

        return args

    def setup_build_environment(self, env):
        # Fypp is required for preprocessing
        env.prepend_path("PATH", self.spec["py-fypp"].prefix.bin)
