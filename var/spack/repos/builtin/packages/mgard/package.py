# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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

    maintainers = ["robertu94"]

    version("2021-11-12", commit="3c05c80a45a51bb6cc5fb5fffe7b1b16787d3366")
    version("2020-10-01", commit="b67a0ac963587f190e106cc3c0b30773a9455f7a")

    depends_on("zlib")
    depends_on("zstd")
    depends_on("libarchive", when="@2021-11-12:")
    depends_on("tclap", when="@2021-11-12:")
    depends_on("yaml-cpp", when="@2021-11-12:")
    depends_on("cmake@3.19:")
    depends_on("nvcomp@2.0.2", when="+cuda")
    conflicts("cuda_arch=none", when="+cuda")
    conflicts("~cuda", when="@2021-11-12")

    def cmake_args(self):
        args = ["-DBUILD_TESTING=OFF"]
        if "+cuda" in self.spec:
            args.append("-DMGARD_ENABLE_CUDA=ON")
            cuda_arch = self.spec.variants["cuda_arch"].value
            args.append("-DCUDA_ARCH_STRING={}".format(";".join(cuda_arch)))
            if "75" in cuda_arch:
                args.append("-DMGARD_ENABLE_CUDA_OPTIMIZE_TURING=ON")
            if "70" in cuda_arch:
                args.append("-DMGARD_ENABLE_CUDA_OPTIMIZE_VOLTA=ON")

        return args
