# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Quandary(CachedCMakePackage, CudaPackage, ROCmPackage):
    """Optimal control for open quantum systems"""

    homepage = "https://github.com/LLNL/quandary"
    git = "https://github.com/LLNL/quandary.git"

    maintainers("steffi7574", "tdrwenski")

    license("MIT", checked_by="tdrwenski")

    version("main", branch="main")

    depends_on("cxx", type="build")

    depends_on("petsc~hypre~metis~fortran")
    depends_on("petsc+debug", when="+debug")
    depends_on("slepc", when="+slepc")

    depends_on("blt", type="build")
    conflicts("^blt@:0.3.6", when="+rocm")

    with when("+rocm"):
        depends_on("petsc+rocm")
        for arch_ in ROCmPackage.amdgpu_targets:
            depends_on("petsc amdgpu_target={0}".format(arch_), when="amdgpu_target={0}".format(arch_))

    with when("+cuda"):
        depends_on("petsc+cuda")
        for sm_ in CudaPackage.cuda_arch_values:
            depends_on("petsc cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))

    variant("slepc", default=False, description="Build with Slepc library")
    variant("debug", default=False, description="Debug mode")

    variant("test", default=False, description="Add dependencies needed for testing")

    with when("+test"):
        depends_on("python", type="run")
        depends_on("py-pip", type="run")
        depends_on("mpi", type="run")

    build_targets = ["all"]
    install_targets = ["install"]


    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec["blt"].prefix))

        return entries


    def cmake_args(self):
        args = []
        if '+slepc' in self.spec:
            args.append('-DWITH_SLEPC=ON')
        return args
