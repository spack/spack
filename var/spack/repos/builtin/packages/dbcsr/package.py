# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dbcsr(CMakePackage, CudaPackage, ROCmPackage):
    """Distributed Block Compressed Sparse Row matrix library."""

    homepage = "https://github.com/cp2k/dbcsr"
    git = "https://github.com/cp2k/dbcsr.git"
    url = "https://github.com/cp2k/dbcsr/releases/download/v2.2.0/dbcsr-2.2.0.tar.gz"
    list_url = "https://github.com/cp2k/dbcsr/releases"

    maintainers("dev-zero")

    version("develop", branch="develop")
    version("2.5.0", sha256="91fda9b2502e5d0a2a6cdd5a73ef096253cc7e75bd01ba5189a4726ad86aef08")
    version("2.4.1", sha256="b3d5ae62ca582b72707a2c932e8074a4f2f61d61085d97bd374213c70b8dbdcf")
    version("2.4.0", sha256="cf2b774328c9a30677501f49b79955841bd08915a7ca53c8533bfdf14a8f9bd4")
    version("2.3.0", sha256="f750de586cffa66852b646f7f85eb831eeb64fa2d25ce50ed10e1df016dd3364")
    version("2.2.0", sha256="245b0382ddc7b80f85af8288f75bd03d56ec51cdfb6968acb4931529b35173ec")
    version("2.1.0", sha256="9e58fd998f224632f356e479d18b5032570d00d87b86736b6a6ac2d03f8d4b3c")
    version("2.0.1", sha256="61d5531b661e1dab043353a1d67939ddcde3893d3dc7b0ab3d05074d448b485c")

    variant("mpi", default=True, description="Compile with MPI")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("shared", default=True, description="Build shared library")
    variant(
        "smm",
        default="libxsmm",
        values=("libxsmm", "blas"),
        description="Library for small matrix multiplications",
    )
    variant(
        "cuda_arch_35_k20x",
        default=False,
        description=(
            "CP2K (resp. DBCSR) has specific parameter sets for"
            " different GPU models. Enable this when building"
            " with cuda_arch=35 for a K20x instead of a K40"
        ),
    )

    variant("opencl", default=False, description="Enable OpenCL backend")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("libxsmm@1.11:~header-only", when="smm=libxsmm")

    depends_on("cmake@3.17:", type="build", when="@2.1:")
    depends_on("cmake@3.10:", type="build")
    depends_on("py-fypp", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python@3.6:", type="build", when="+cuda")

    depends_on("hipblas", when="+rocm")

    depends_on("opencl", when="+opencl")

    # We only support specific gpu archs for which we have parameter files
    # for optimal kernels. Note that we don't override the parent class arch
    # properties, since the parent class defines constraints for different archs
    # Instead just mark all unsupported cuda archs as conflicting.
    dbcsr_cuda_archs = ("35", "37", "60", "70")
    cuda_msg = "dbcsr only supports cuda_arch {0}".format(dbcsr_cuda_archs)

    for arch in CudaPackage.cuda_arch_values:
        if arch not in dbcsr_cuda_archs:
            conflicts("+cuda", when="cuda_arch={0}".format(arch), msg=cuda_msg)

    conflicts("+cuda", when="cuda_arch=none", msg=cuda_msg)

    dbcsr_amdgpu_targets = "gfx906"
    amd_msg = "DBCSR only supports amdgpu_target {0}".format(dbcsr_amdgpu_targets)

    for arch in ROCmPackage.amdgpu_targets:
        if arch not in dbcsr_amdgpu_targets:
            conflicts("+rocm", when="amdgpu_target={0}".format(arch), msg=amd_msg)

    accel_msg = "CUDA, ROCm and OpenCL support are mutually exlusive"
    conflicts("+cuda", when="+rocm", msg=accel_msg)
    conflicts("+cuda", when="+opencl", msg=accel_msg)
    conflicts("+rocm", when="+opencl", msg=accel_msg)

    # Require openmp threading for OpenBLAS by making other options conflict
    conflicts("^openblas threads=pthreads", when="+openmp")
    conflicts("^openblas threads=none", when="+openmp")

    conflicts("smm=blas", when="+opencl")

    generator = "Ninja"
    depends_on("ninja@1.10:", type="build")

    def cmake_args(self):
        spec = self.spec

        if "+cuda" in spec and len(spec.variants["cuda_arch"].value) > 1:
            raise InstallError("dbcsr supports only one cuda_arch at a time")

        if "+rocm" in spec and len(spec.variants["amdgpu_target"].value) > 1:
            raise InstallError("DBCSR supports only one amdgpu_arch at a time")

        args = [
            "-DUSE_SMM=%s" % ("libxsmm" if "smm=libxsmm" in spec else "blas"),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define_from_variant("USE_OPENMP", "openmp"),
            # C API needs MPI
            self.define_from_variant("WITH_C_API", "mpi"),
            "-DBLAS_FOUND=true",
            "-DBLAS_LIBRARIES=%s" % (spec["blas"].libs.joined(";")),
            "-DLAPACK_FOUND=true",
            "-DLAPACK_LIBRARIES=%s" % (spec["lapack"].libs.joined(";")),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        # Switch necessary as a result of a bug.
        if "@2.1:2.2" in spec:
            args += ["-DBUILD_TESTING=ON"]

        if self.spec.satisfies("+cuda"):
            cuda_arch = self.spec.variants["cuda_arch"].value[0]

            gpu_map = {"35": "K40", "37": "K80", "60": "P100", "70": "V100"}

            if "@2.3:" in spec:
                gpu_map["80"] = "A100"

            gpuver = gpu_map[cuda_arch]

            if cuda_arch == "35" and self.spec.satisfies("+cuda_arch_35_k20x"):
                gpuver = "K20X"

            args += ["-DWITH_GPU=%s" % gpuver, "-DUSE_ACCEL=cuda"]

        if self.spec.satisfies("+rocm"):
            amd_arch = self.spec.variants["amdgpu_target"].value[0]

            gpuver = {"gfx906": "Mi50"}[amd_arch]

            args += ["-DWITH_GPU={0}".format(gpuver), "-DUSE_ACCEL=hip"]

        if self.spec.satisfies("+opencl"):
            args += ["-DUSE_ACCEL=opencl"]

        return args

    def check(self):
        """Override CMakePackage's check() to enforce seralized test runs
        since they are already parallelized"""
        with working_dir(self.build_directory):
            self._if_ninja_target_execute("test", parallel=False)
