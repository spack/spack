# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dihydrogen(CMakePackage, CudaPackage, ROCmPackage):
    """DiHydrogen is the second version of the Hydrogen fork of the
    well-known distributed linear algebra library,
    Elemental. DiHydrogen aims to be a basic distributed
    multilinear algebra interface with a particular emphasis on the
    needs of the distributed machine learning effort, LBANN."""

    homepage = "https://github.com/LLNL/DiHydrogen.git"
    url = "https://github.com/LLNL/DiHydrogen/archive/v0.1.tar.gz"
    git = "https://github.com/LLNL/DiHydrogen.git"
    tags = ["ecp", "radiuss"]

    maintainers("bvanessen")

    version("develop", branch="develop")
    version("master", branch="master")

    version("0.2.1", sha256="11e2c0f8a94ffa22e816deff0357dde6f82cc8eac21b587c800a346afb5c49ac")
    version("0.2.0", sha256="e1f597e80f93cf49a0cb2dbc079a1f348641178c49558b28438963bd4a0bdaa4")
    version("0.1", sha256="171d4b8adda1e501c38177ec966e6f11f8980bf71345e5f6d87d0a988fef4c4e")

    variant("al", default=True, description="Builds with Aluminum communication library")
    variant(
        "developer",
        default=False,
        description="Enable extra warnings and force tests to be enabled.",
    )
    variant("half", default=False, description="Enable FP16 support on the CPU.")
    variant(
        "distconv",
        default=False,
        description="Support distributed convolutions: spatial, channel, " "filter.",
    )
    variant("nvshmem", default=False, description="Builds with support for NVSHMEM")
    variant("openmp", default=False, description="Enable CPU acceleration with OpenMP threads.")
    variant("rocm", default=False, description="Enable ROCm/HIP language features.")
    variant("shared", default=True, description="Enables the build of shared libraries")

    # Variants related to BLAS
    variant(
        "openmp_blas", default=False, description="Use OpenMP for threading in the BLAS library"
    )
    variant("int64_blas", default=False, description="Use 64bit integers for BLAS.")
    variant(
        "blas",
        default="openblas",
        values=("openblas", "mkl", "accelerate", "essl", "libsci"),
        description="Enable the use of OpenBlas/MKL/Accelerate/ESSL/LibSci",
    )

    conflicts("~cuda", when="+nvshmem")

    depends_on("mpi")
    depends_on("catch2", type="test")

    # Specify the correct version of Aluminum
    depends_on("aluminum@0.4.0:0.4", when="@0.1 +al")
    depends_on("aluminum@0.5.0:0.5", when="@0.2.0 +al")
    depends_on("aluminum@0.7.0:0.7", when="@0.2.1 +al")
    depends_on("aluminum@0.7.0:", when="@:0.0,0.2.1: +al")

    # Add Aluminum variants
    depends_on("aluminum +cuda +nccl +cuda_rma", when="+al +cuda")
    depends_on("aluminum +rocm +rccl", when="+al +rocm")
    depends_on("aluminum +ht", when="+al +distconv")

    for arch in CudaPackage.cuda_arch_values:
        depends_on("aluminum cuda_arch=%s" % arch, when="+al +cuda cuda_arch=%s" % arch)
        depends_on("nvshmem cuda_arch=%s" % arch, when="+nvshmem +cuda cuda_arch=%s" % arch)

    # variants +rocm and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    for val in ROCmPackage.amdgpu_targets:
        depends_on("aluminum amdgpu_target=%s" % val, when="amdgpu_target=%s" % val)

    depends_on("roctracer-dev", when="+rocm +distconv")

    depends_on("cudnn", when="+cuda")
    depends_on("cub", when="^cuda@:10")

    # Note that #1712 forces us to enumerate the different blas variants
    depends_on("openblas", when="blas=openblas")
    depends_on("openblas +ilp64", when="blas=openblas +int64_blas")
    depends_on("openblas threads=openmp", when="blas=openblas +openmp_blas")

    depends_on("intel-mkl", when="blas=mkl")
    depends_on("intel-mkl +ilp64", when="blas=mkl +int64_blas")
    depends_on("intel-mkl threads=openmp", when="blas=mkl +openmp_blas")

    depends_on("veclibfort", when="blas=accelerate")
    conflicts("blas=accelerate +openmp_blas")

    depends_on("essl", when="blas=essl")
    depends_on("essl +ilp64", when="blas=essl +int64_blas")
    depends_on("essl threads=openmp", when="blas=essl +openmp_blas")
    depends_on("netlib-lapack +external-blas", when="blas=essl")

    depends_on("cray-libsci", when="blas=libsci")
    depends_on("cray-libsci +openmp", when="blas=libsci +openmp_blas")

    # Distconv builds require cuda or rocm
    conflicts("+distconv", when="~cuda ~rocm")

    conflicts("+distconv", when="+half")
    conflicts("+rocm", when="+half")

    depends_on("half", when="+half")

    generator = "Ninja"
    depends_on("ninja", type="build")
    depends_on("cmake@3.17.0:", type="build")

    depends_on("spdlog", when="@:0.1,0.2:")

    depends_on("llvm-openmp", when="%apple-clang +openmp")

    # TODO: Debug linker errors when NVSHMEM is built with UCX
    depends_on("nvshmem +nccl~ucx", when="+nvshmem")

    # Idenfity versions of cuda_arch that are too old
    # from lib/spack/spack/build_systems/cuda.py
    illegal_cuda_arch_values = ["10", "11", "12", "13", "20", "21"]
    for value in illegal_cuda_arch_values:
        conflicts("cuda_arch=" + value)

    @property
    def libs(self):
        shared = True if "+shared" in self.spec else False
        return find_libraries("libH2Core", root=self.prefix, shared=shared, recursive=True)

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DCMAKE_CXX_STANDARD=17",
            "-DCMAKE_INSTALL_MESSAGE:STRING=LAZY",
            "-DBUILD_SHARED_LIBS:BOOL=%s" % ("+shared" in spec),
            "-DH2_ENABLE_ALUMINUM=%s" % ("+al" in spec),
            "-DH2_ENABLE_CUDA=%s" % ("+cuda" in spec),
            "-DH2_ENABLE_DISTCONV_LEGACY=%s" % ("+distconv" in spec),
            "-DH2_ENABLE_OPENMP=%s" % ("+openmp" in spec),
            "-DH2_ENABLE_FP16=%s" % ("+half" in spec),
            "-DH2_DEVELOPER_BUILD=%s" % ("+developer" in spec),
        ]

        if spec.version < Version("0.3"):
            args.append("-DH2_ENABLE_HIP_ROCM=%s" % ("+rocm" in spec))
        else:
            args.append("-DH2_ENABLE_ROCM=%s" % ("+rocm" in spec))

        if not spec.satisfies("^cmake@3.23.0"):
            # There is a bug with using Ninja generator in this version
            # of CMake
            args.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=ON")

        if "+cuda" in spec:
            if self.spec.satisfies("%clang"):
                for flag in self.spec.compiler_flags["cxxflags"]:
                    if "gcc-toolchain" in flag:
                        args.append("-DCMAKE_CUDA_FLAGS=-Xcompiler={0}".format(flag))
            if spec.satisfies("^cuda@11.0:"):
                args.append("-DCMAKE_CUDA_STANDARD=17")
            else:
                args.append("-DCMAKE_CUDA_STANDARD=14")
            archs = spec.variants["cuda_arch"].value
            if archs != "none":
                arch_str = ";".join(archs)
                args.append("-DCMAKE_CUDA_ARCHITECTURES=%s" % arch_str)

            if spec.satisfies("%cce") and spec.satisfies("^cuda+allow-unsupported-compilers"):
                args.append("-DCMAKE_CUDA_FLAGS=-allow-unsupported-compiler")

        if "+cuda" in spec:
            args.append("-DcuDNN_DIR={0}".format(spec["cudnn"].prefix))

        if spec.satisfies("^cuda@:10"):
            if "+cuda" in spec or "+distconv" in spec:
                args.append("-DCUB_DIR={0}".format(spec["cub"].prefix))

        # Add support for OpenMP with external (Brew) clang
        if spec.satisfies("%clang +openmp platform=darwin"):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            args.extend(
                [
                    "-DOpenMP_CXX_FLAGS=-fopenmp=libomp",
                    "-DOpenMP_CXX_LIB_NAMES=libomp",
                    "-DOpenMP_libomp_LIBRARY={0}/lib/libomp.dylib".format(clang_root),
                ]
            )

        if "+rocm" in spec:
            args.extend(
                [
                    "-DCMAKE_CXX_FLAGS=-std=c++17",
                    "-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix),
                    "-DHIP_CXX_COMPILER={0}".format(self.spec["hip"].hipcc),
                ]
            )
            if "platform=cray" in spec:
                args.extend(["-DMPI_ASSUME_NO_BUILTIN_MPI=ON"])
            archs = self.spec.variants["amdgpu_target"].value
            if archs != "none":
                arch_str = ",".join(archs)
                args.append(
                    "-DHIP_HIPCC_FLAGS=--amdgpu-target={0}"
                    " -g -fsized-deallocation -fPIC -std=c++17".format(arch_str)
                )
                args.extend(
                    [
                        "-DCMAKE_HIP_ARCHITECTURES=%s" % arch_str,
                        "-DAMDGPU_TARGETS=%s" % arch_str,
                        "-DGPU_TARGETS=%s" % arch_str,
                    ]
                )

        if self.spec.satisfies("^essl"):
            # IF IBM ESSL is used it needs help finding the proper LAPACK libraries
            args.extend(
                [
                    "-DLAPACK_LIBRARIES=%s;-llapack;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                    "-DBLAS_LIBRARIES=%s;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                ]
            )

        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies("%apple-clang +openmp"):
            env.append_flags("CPPFLAGS", self.compiler.openmp_flag)
            env.append_flags("CFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("CXXFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["llvm-openmp"].libs.ld_flags)
