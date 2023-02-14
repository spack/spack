# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Xgboost(CMakePackage, CudaPackage):
    """XGBoost is an optimized distributed gradient boosting library designed to be
    highly efficient, flexible and portable. It implements machine learning algorithms
    under the Gradient Boosting framework. XGBoost provides a parallel tree boosting
    (also known as GBDT, GBM) that solve many data science problems in a fast and
    accurate way. The same code runs on major distributed environment (Hadoop, SGE, MPI)
    and can solve problems beyond billions of examples."""

    homepage = "https://xgboost.ai/"
    git = "https://github.com/dmlc/xgboost.git"

    maintainers("adamjstewart")

    version("master", branch="master", submodules=True)
    version("1.6.2", tag="v1.6.2", submodules=True)
    version("1.6.1", tag="v1.6.1", submodules=True)
    version("1.5.2", tag="v1.5.2", submodules=True)
    version("1.3.3", tag="v1.3.3", submodules=True)

    variant("nccl", default=False, description="Build with NCCL to enable distributed GPU support")
    variant("openmp", default=True, description="Build with OpenMP support")

    depends_on("cmake@3.13:", type="build")
    depends_on("cmake@3.16:", when="platform=darwin", type="build")
    depends_on("ninja", type="build")
    depends_on("cuda@10:", when="+cuda")
    # https://github.com/dmlc/xgboost/pull/7379
    depends_on("cuda@10:11.4", when="@:1.5.0+cuda")
    depends_on("nccl", when="+nccl")
    depends_on("llvm-openmp", when="%apple-clang +openmp")
    depends_on("hwloc", when="%clang")

    # https://github.com/dmlc/xgboost/issues/6972
    conflicts("%gcc@:7", when="+cuda")
    conflicts("%gcc@:4", msg="GCC version must be at least 5.0!")
    conflicts("+nccl", when="~cuda", msg="NCCL requires CUDA")
    conflicts("+cuda", when="~openmp", msg="CUDA requires OpenMP")
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    generator = "Ninja"

    def cmake_args(self):
        # https://xgboost.readthedocs.io/en/latest/build.html
        args = [
            self.define_from_variant("USE_CUDA", "cuda"),
            self.define_from_variant("USE_NCCL", "nccl"),
            self.define_from_variant("USE_OPENMP", "openmp"),
        ]

        if "+cuda" in self.spec:
            args.append(self.define("GPU_COMPUTE_VER", self.spec.variants["cuda_arch"].value))

        if "@1.5: ^cuda@11.4:" in self.spec:
            args.append(self.define("BUILD_WITH_CUDA_CUB", True))

        if self.spec.satisfies("+openmp%clang"):
            OpenMP_C_FLAGS = "-fopenmp=libomp"
            OpenMP_C_LIB_NAMES = "libomp"
            args += [
                self.define("OpenMP_C_FLAGS", OpenMP_C_FLAGS),
                self.define("OpenMP_C_LIB_NAMES", OpenMP_C_LIB_NAMES),
                self.define("OpenMP_CXX_FLAGS", OpenMP_C_FLAGS),
                self.define("OpenMP_CXX_LIB_NAMES", OpenMP_C_LIB_NAMES),
            ]
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            args += [
                self.define(
                    "OpenMP_libomp_LIBRARY",
                    find_libraries("libomp", root=clang_root, shared=True, recursive=True),
                )
            ]

        return args
