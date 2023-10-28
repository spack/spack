# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mgard(CMakePackage, CudaPackage):
    """MGARD error bounded lossy compressor
    forked from https://github.com/CODARcode/MGARD with patches to support Spack"""

    # This is a research compressor with a fast evolving API.  The fork is updated
    # when releases are made with minimal changes to support spack

    homepage = "https://github.com/CODARcode/MGARD"
    git = "https://github.com/robertu94/MGARD"

    maintainers("robertu94")

    tags = ["e4s"]

    version("2023-03-31", commit="a8a04a86ff30f91d0b430a7c52960a12fa119589", preferred=True)
    version("2023-01-10", commit="3808bd8889a0f8e6647fc0251a3189bc4dfc920f")
    version("2022-11-18", commit="72dd230ed1af88f62ed3c0f662e2387a6e587748")
    version("2021-11-12", commit="3c05c80a45a51bb6cc5fb5fffe7b1b16787d3366")
    version("2020-10-01", commit="b67a0ac963587f190e106cc3c0b30773a9455f7a")

    variant(
        "serial",
        when="@2022-11-18:",
        default=True,
        description="Enable the classic non-parallel implmementation",
    )
    variant("openmp", when="@2022-11-18:", default=True, description="Enable OpenMP support")
    variant("timing", when="@2022-11-18:", default=False, description="Enable profile timings")
    variant(
        "unstructured",
        when="@2022-11-18:",
        default=False,
        description="Enable experimental unstructured mesh support",
    )

    depends_on("python", type=("build",), when="@2022-11-18:")
    depends_on("sed", type=("build",), when="@2022-11-18:")
    depends_on("zlib-api")
    depends_on("pkgconfig", type=("build",), when="@2022-11-18:")
    depends_on("zstd")
    depends_on("protobuf@:3.21.12", when="@2022-11-18:")
    depends_on("libarchive", when="@2021-11-12:")
    depends_on("tclap", when="@2021-11-12")
    depends_on("yaml-cpp", when="@2021-11-12:")
    depends_on("cmake@3.19:", type="build")
    depends_on("nvcomp@2.2.0:", when="@2022-11-18:+cuda")
    depends_on("nvcomp@2.0.2", when="@:2021-11-12+cuda")
    conflicts("cuda_arch=none", when="+cuda")
    conflicts(
        "~cuda", when="@2021-11-12", msg="without cuda MGARD@2021-11-12 has undefined symbols"
    )
    conflicts("%gcc@:7", when="@2022-11-18:", msg="requires std::optional and other c++17 things")

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            if self.spec.satisfies("@2020-10-01 %oneapi@2023:"):
                flags.append("-Wno-error=c++11-narrowing")
        return (flags, None, None)

    def cmake_args(self):
        spec = self.spec
        args = ["-DBUILD_TESTING=OFF"]
        args.append(self.define_from_variant("MGARD_ENABLE_CUDA", "cuda"))
        if "+cuda" in spec:
            cuda_arch_list = spec.variants["cuda_arch"].value
            arch_str = ";".join(cuda_arch_list)
            if cuda_arch_list[0] != "none":
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", arch_str))
        if self.spec.satisfies("@:2021-11-12"):
            if "+cuda" in self.spec:
                if "75" in cuda_arch:
                    args.append("-DMGARD_ENABLE_CUDA_OPTIMIZE_TURING=ON")
                if "70" in cuda_arch:
                    args.append("-DMGARD_ENABLE_CUDA_OPTIMIZE_VOLTA=ON")
        elif self.spec.satisfies("@2022-11-18:"):
            args.append("-DMAXIMUM_DIMENSION=4")  # how do we do variants with arbitrary values
            args.append("-DMGARD_ENABLE_CLI=OFF")  # the CLI is busted
            args.append(self.define_from_variant("MGARD_ENABLE_OPENMP", "openmp"))
            args.append(self.define_from_variant("MGARD_ENABLE_TIMING", "timing"))
            args.append(self.define_from_variant("MGARD_ENABLE_SERIAL", "serial"))
            args.append(self.define_from_variant("MGARD_ENABLE_UNSTRUCTURED", "unstructured"))
        return args
