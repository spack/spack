# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Camp(CMakePackage, CudaPackage, ROCmPackage):
    """
    Compiler agnostic metaprogramming library providing concepts,
    type operations and tuples for C++ and cuda
    """

    homepage = "https://github.com/LLNL/camp"
    git = "https://github.com/LLNL/camp.git"
    url = "https://github.com/LLNL/camp/archive/v0.1.0.tar.gz"

    maintainers("trws")

    license("BSD-3-Clause")

    version("main", branch="main", submodules=False)
    version(
        "2024.02.0",
        tag="v2024.02.0",
        commit="03c80a6c6ab4f97e76a52639563daec71435a277",
        submodules=False,
    )
    version(
        "2023.06.0",
        tag="v2023.06.0",
        commit="ac34c25b722a06b138bc045d38bfa5e8fa3ec9c5",
        submodules=False,
    )
    version("2022.10.1", sha256="2d12f1a46f5a6d01880fc075cfbd332e2cf296816a7c1aa12d4ee5644d386f02")
    version("2022.10.0", sha256="3561c3ef00bbcb61fe3183c53d49b110e54910f47e7fc689ad9ccce57e55d6b8")
    version("2022.03.2", sha256="bc4aaeacfe8f2912e28f7a36fc731ab9e481bee15f2c6daf0cb208eed3f201eb")
    version("2022.03.0", sha256="e9090d5ee191ea3a8e36b47a8fe78f3ac95d51804f1d986d931e85b8f8dad721")
    version("0.3.0", sha256="129431a049ca5825443038ad5a37a86ba6d09b2618d5fe65d35f83136575afdb")
    version("0.2.3", sha256="58a0f3bd5eadb588d7dc83f3d050aff8c8db639fc89e8d6553f9ce34fc2421a7")
    version("0.2.2", sha256="194d38b57e50e3494482a7f94940b27f37a2bee8291f2574d64db342b981d819")
    version("0.1.0", sha256="fd4f0f2a60b82a12a1d9f943f8893dc6fe770db493f8fae5ef6f7d0c439bebcc")

    # TODO: figure out gtest dependency and then set this default True.
    variant("tests", default=False, description="Build tests")
    variant("openmp", default=False, description="Build with OpenMP support")

    depends_on("cub", when="+cuda")

    depends_on("blt", type="build")
    depends_on("blt@0.6.1:", type="build", when="@2024.02.0:")
    depends_on("blt@0.5.0:0.5.3", type="build", when="@2022.03.0:2023.06.0")

    patch("libstdc++-13-missing-header.patch", when="@:2022.10")

    conflicts("^blt@:0.3.6", when="+rocm")

    def cmake_args(self):
        spec = self.spec

        options = []

        options.append("-DBLT_SOURCE_DIR={0}".format(spec["blt"].prefix))

        options.append(self.define_from_variant("ENABLE_CUDA", "cuda"))
        if "+cuda" in spec:
            options.append("-DCUDA_TOOLKIT_ROOT_DIR={0}".format(spec["cuda"].prefix))

            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                options.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch[0]))
                options.append("-DCUDA_ARCH=sm_{0}".format(cuda_arch[0]))
                flag = "-arch sm_{0}".format(cuda_arch[0])
                options.append("-DCMAKE_CUDA_FLAGS:STRING={0}".format(flag))

        options.append(self.define_from_variant("ENABLE_HIP", "rocm"))
        if "+rocm" in spec:
            options.append("-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix))

            archs = self.spec.variants["amdgpu_target"].value
            options.append("-DCMAKE_HIP_ARCHITECTURES={0}".format(archs))
            options.append("-DGPU_TARGETS={0}".format(archs))
            options.append("-DAMDGPU_TARGETS={0}".format(archs))

        options.append(self.define_from_variant("ENABLE_OPENMP", "openmp"))
        options.append(self.define_from_variant("ENABLE_TESTS", "tests"))

        return options
