# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools

from spack.package import *


class Rocwmma(CMakePackage):
    """AMD's C++ library for accelerating mixed precision matrix multiplication
    and accumulation (MFMA) operations leveraging specialized GPU matrix cores.
    rocWMMA provides a C++ API to facilitate breaking down matrix multiply-accumulate
    problems into fragments and using them in block-wise operations that are
    distributed in parallel across GPU wavefronts. The API is a header library
    of GPU device code meaning that matrix core acceleration may be compiled directly
    into your kernel device code. This can benefit from compiler optimization in the
    generation of kernel assembly, and does not incur additional overhead costs of
    linking to external runtime libraries or having to launch separate kernels."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocWMMA"
    git = "https://github.com/ROCmSoftwarePlatform/rocWMMA.git"
    url = "https://github.com/ROCmSoftwarePlatform/rocWMMA/archive/refs/tags/rocm-5.2.0.tar.gz"
    tags = ["rocm"]

    maintainers = ["srekolam"]

    version("5.2.0", sha256="257ccd1cf2bc1d8064e72e78d276ef7446b2cb7e2dec05ff8331bb44eff2b7cb")

    # gfx908:xnack-;gfx90a:xnack-;gfx90a:xnack+
    # are only targets currently supported for @5.2.0
    # releases

    amdgpu_targets = ("gfx908:xnack-", "gfx90a", "gfx90a:xnack-", "gfx90a:xnack+")
    variant("amdgpu_target", values=auto_or_any_combination_of(*amdgpu_targets))
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.16:", type="build", when="@5.2.0:")
    depends_on("cmake@3.5:", type="build")

    depends_on("googletest@1.10.0:", type="test")

    for ver in ["5.2.0"]:
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, type="build", when="@" + ver)
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocblas@" + ver, type="build", when="@" + ver)

        depends_on("rocm-openmp-extras@" + ver, type="build", when="@" + ver)

    for tgt in itertools.chain(["auto"], amdgpu_targets):
        depends_on("rocblas amdgpu_target={0}".format(tgt), when="amdgpu_target={0}".format(tgt))

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("ROCWMMA_BUILD_TESTS", "ON"),
            self.define("ROCWMMA_BUILD_VALIDATION_TESTS", "ON"),
            self.define("ROCWMMA_BUILD_BENCHMARK_TESTS", "ON"),
            self.define("ROCWMMA_BUILD_SAMPLES", "ON"),
            self.define("ROCWMMA_BUILD_DOCS", "OFF"),
            self.define("ROCWMMA_BUILD_ASSEMBLY", "OFF"),
        ]
        args.extend(
            [
                "-DOpenMP_CXX_FLAGS=-fopenmp=libomp",
                "-DOpenMP_CXX_LIB_NAMES=libomp",
                "-DOpenMP_libomp_LIBRARY={0}/lib/libomp.so".format(
                    self.spec["rocm-openmp-extras"].prefix
                ),
            ]
        )
        tgt = self.spec.variants["amdgpu_target"]
        if "auto" not in tgt:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        return args
