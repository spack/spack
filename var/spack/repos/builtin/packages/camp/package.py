# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


def hip_repair_options(options, spec):
    # there is only one dir like this, but the version component is unknown
    options.append(
        "-DHIP_CLANG_INCLUDE_PATH="
        + glob.glob("{}/lib/clang/*/include".format(spec["llvm-amdgpu"].prefix))[0]
    )


def hip_repair_cache(options, spec):
    # there is only one dir like this, but the version component is unknown
    options.append(
        cmake_cache_path(
            "HIP_CLANG_INCLUDE_PATH",
            glob.glob("{}/lib/clang/*/include".format(spec["llvm-amdgpu"].prefix))[0],
        )
    )


class Camp(CMakePackage, CudaPackage, ROCmPackage):
    """
    Compiler agnostic metaprogramming library providing concepts,
    type operations and tuples for C++ and cuda
    """

    homepage = "https://github.com/LLNL/camp"
    git = "https://github.com/LLNL/camp.git"
    url = "https://github.com/LLNL/camp/archive/v0.1.0.tar.gz"

    maintainers("trws")

    version("main", branch="main", submodules="True")
    version("2022.10.1", sha256="2d12f1a46f5a6d01880fc075cfbd332e2cf296816a7c1aa12d4ee5644d386f02")
    version("2022.03.2", sha256="bc4aaeacfe8f2912e28f7a36fc731ab9e481bee15f2c6daf0cb208eed3f201eb")
    version("2022.03.0", sha256="e9090d5ee191ea3a8e36b47a8fe78f3ac95d51804f1d986d931e85b8f8dad721")
    version("0.3.0", sha256="129431a049ca5825443038ad5a37a86ba6d09b2618d5fe65d35f83136575afdb")
    version("0.2.3", sha256="58a0f3bd5eadb588d7dc83f3d050aff8c8db639fc89e8d6553f9ce34fc2421a7")
    version("0.2.2", sha256="194d38b57e50e3494482a7f94940b27f37a2bee8291f2574d64db342b981d819")
    version("0.1.0", sha256="fd4f0f2a60b82a12a1d9f943f8893dc6fe770db493f8fae5ef6f7d0c439bebcc")

    # TODO: figure out gtest dependency and then set this default True.
    variant("tests", default=False, description="Build tests")
    variant("openmp", default=False, description="Build OpenMP support")

    depends_on("cub", when="+cuda")

    depends_on("blt", type="build")

    conflicts("^blt@:0.3.6", when="+rocm")

    def cmake_args(self):
        spec = self.spec

        options = []

        options.append("-DBLT_SOURCE_DIR={0}".format(spec["blt"].prefix))

        options.append("-DENABLE_OPENMP=" + ("On" if "+openmp" in spec else "Off"))
        if "+cuda" in spec:
            options.extend(
                ["-DENABLE_CUDA=ON", "-DCUDA_TOOLKIT_ROOT_DIR=%s" % (spec["cuda"].prefix)]
            )

            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                options.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch[0]))
                options.append("-DCUDA_ARCH=sm_{0}".format(cuda_arch[0]))
                flag = "-arch sm_{0}".format(cuda_arch[0])
                options.append("-DCMAKE_CUDA_FLAGS:STRING={0}".format(flag))
        else:
            options.append("-DENABLE_CUDA=OFF")

        if "+rocm" in spec:
            options.extend(["-DENABLE_HIP=ON", "-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix)])

            hip_repair_options(options, spec)

            archs = self.spec.variants["amdgpu_target"].value
            if archs != "none":
                arch_str = ",".join(archs)
                options.append("-DHIP_HIPCC_FLAGS=--amdgpu-target={0}".format(arch_str))
        else:
            options.append("-DENABLE_HIP=OFF")

        options.append(self.define_from_variant("ENABLE_TESTS", "tests"))

        return options
