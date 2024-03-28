# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exawind(CMakePackage, CudaPackage, ROCmPackage):
    """Multi-application driver for Exawind project."""

    homepage = "https://github.com/Exawind/exawind-driver"
    git = "https://github.com/Exawind/exawind-driver.git"

    maintainers("jrood-nrel")

    tags = ["ecp", "ecp-apps"]

    # Testing is currently always enabled, but should be optional in the future
    # to avoid cloning the mesh submodule
    version("master", branch="main", submodules=True)
    version("1.0.0", tag="v1.0.0", submodules=True)
    license("Apache-2.0")

    variant("openfast", default=False, description="Enable OpenFAST integration")
    variant("hypre", default=True, description="Enable hypre solver")
    variant("stk_simd", default=False, description="Enable SIMD in STK")
    variant("umpire", default=False, description="Enable Umpire")
    variant("tiny_profile", default=False, description="Turn on AMR-wind with tiny profile")
    variant("sycl", default=False, description="Enable SYCL backend for AMR-Wind")
    variant("gpu-aware-mpi", default=False, description="gpu-aware-mpi")

    conflicts("amr-wind+hypre", when="+sycl")

    for arch in CudaPackage.cuda_arch_values:
        depends_on("amr-wind+cuda cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)
        depends_on("nalu-wind+cuda cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)

    for arch in ROCmPackage.amdgpu_targets:
        depends_on("amr-wind+rocm amdgpu_target=%s" % arch, when="+rocm amdgpu_target=%s" % arch)
        depends_on("nalu-wind+rocm amdgpu_target=%s" % arch, when="+rocm amdgpu_target=%s" % arch)

    depends_on("nalu-wind+tioga")
    depends_on("amr-wind+netcdf+mpi")
    depends_on("tioga~nodegid")
    depends_on("yaml-cpp@0.6:")
    depends_on("nalu-wind+openfast", when="+openfast")
    depends_on("amr-wind+hypre", when="+hypre~sycl")
    depends_on("amr-wind~hypre", when="~hypre")
    depends_on("nalu-wind+hypre", when="+hypre")
    depends_on("nalu-wind~hypre", when="~hypre")
    depends_on("amr-wind+sycl", when="+sycl")
    depends_on("nalu-wind+umpire", when="+umpire")
    depends_on("amr-wind+umpire", when="+umpire")
    depends_on("amr-wind+tiny_profile", when="+tiny_profile")
    depends_on("nalu-wind+gpu-aware-mpi", when="+gpu-aware-mpi")
    depends_on("amr-wind+gpu-aware-mpi", when="+gpu-aware-mpi")
    depends_on("nalu-wind@2.0.0:", when="@1.0.0:")
    depends_on("amr-wind@0.9.0:", when="@1.0.0:")
    depends_on("tioga@1.0.0:", when="@1.0.0:")

    def cmake_args(self):
        spec = self.spec

        args = [self.define("MPI_HOME", spec["mpi"].prefix)]

        if "+umpire" in self.spec:
            args.append(self.define_from_variant("EXAWIND_ENABLE_UMPIRE", "umpire"))
            args.append(self.define("UMPIRE_DIR", self.spec["umpire"].prefix))

        if spec.satisfies("+cuda"):
            args.append(self.define("EXAWIND_ENABLE_CUDA", True))
            args.append(self.define("CUDAToolkit_ROOT", self.spec["cuda"].prefix))
            args.append(self.define("EXAWIND_CUDA_ARCH", self.spec.variants["cuda_arch"].value))

        if spec.satisfies("+rocm"):
            targets = self.spec.variants["amdgpu_target"].value
            args.append(self.define("EXAWIND_ENABLE_ROCM", True))
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
            args.append(self.define("CMAKE_HIP_ARCHITECTURES", ";".join(str(x) for x in targets)))
            args.append(self.define("AMDGPU_TARGETS", ";".join(str(x) for x in targets)))
            args.append(self.define("GPU_TARGETS", ";".join(str(x) for x in targets)))

        if spec.satisfies("^amr-wind+hdf5"):
            args.append(self.define("H5Z_ZFP_USE_STATIC_LIBS", True))

        if spec.satisfies("^amr-wind+ascent"):
            args.append(self.define("CMAKE_EXE_LINKER_FLAGS", self.compiler.openmp_flag))

        return args

    def setup_build_environment(self, env):
        if "~stk_simd" in self.spec:
            env.append_flags("CXXFLAGS", "-DUSE_STK_SIMD_NONE")
        if "+rocm" in self.spec:
            env.set("OMPI_CXX", self.spec["hip"].hipcc)
            env.set("MPICH_CXX", self.spec["hip"].hipcc)
            env.set("MPICXX_CXX", self.spec["hip"].hipcc)
