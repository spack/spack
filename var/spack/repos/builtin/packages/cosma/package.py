# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cosma(CMakePackage):
    """
    Distributed Communication-Optimal Matrix-Matrix Multiplication Library
    """

    maintainers("haampie", "kabicm", "teonnik")
    homepage = "https://github.com/eth-cscs/COSMA"
    url = "https://github.com/eth-cscs/COSMA/releases/download/v2.5.1/COSMA-v2.5.1.tar.gz"
    git = "https://github.com/eth-cscs/COSMA.git"

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version("master", branch="master", submodules=True)
    version("2.5.1", sha256="085b7787597374244bbb1eb89bc69bf58c35f6c85be805e881e1c0b25166c3ce")
    version("2.5.0", sha256="7f68bb0ee5c80f9b8df858afcbd017ad4ed87ac09439d13d7d890844dbdd3d54")
    version("2.4.0", sha256="5714315ce06d48037f86cfee2d7f19340643fee95e9d7f1e92dc1b623b67e395")
    version("2.3.0", sha256="0c01c2deb5a0cd177952178350188a62c42ce55e604d7948ac472f55bf0d4815")
    version("2.2.0", sha256="1eb92a98110df595070a12193b9221eecf9d103ced8836c960f6c79a2bd553ca")
    version("2.0.7", sha256="8d70bfcbda6239b6a8fbeaca138790bbe58c0c3aa576879480d2632d4936cf7e")
    version("2.0.2", sha256="4f3354828bc718f3eef2f0098c3bdca3499297497a220da32db1acd57920c68d")

    # We just need the libraries of cuda and rocm, so no need to extend
    # CudaPackage or ROCmPackage.
    variant("cuda", default=False, description="Build with cuBLAS support")
    variant("rocm", default=False, description="Build with rocBLAS support")
    variant("scalapack", default=False, description="Build with ScaLAPACK API")
    variant("shared", default=False, description="Build the shared library version")

    depends_on("cmake@3.12:", type="build")
    depends_on("mpi@3:")
    depends_on("blas", when="~cuda ~rocm")
    depends_on("scalapack", when="+scalapack")
    depends_on("cuda", when="+cuda")
    depends_on("rocblas", when="+rocm")

    def url_for_version(self, version):
        if version <= Version("2.3.0"):
            return "https://github.com/eth-cscs/COSMA/releases/download/v{0}/cosma.tar.gz".format(
                version
            )

        return "https://github.com/eth-cscs/COSMA/releases/download/v{0}/COSMA-v{1}.tar.gz".format(
            version, version
        )

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("CUDA_PATH", self.spec["cuda"].prefix)

    def cosma_blas_cmake_arg(self):
        query_to_cmake_arg = [
            ("^intel-mkl", "MKL"),
            ("^intel-oneapi-mkl", "MKL"),
            ("^cray-libsci", "CRAY_LIBSCI"),
            ("^netlib-lapack", "CUSTOM"),
            ("^openblas", "OPENBLAS"),
            ("+cuda", "CUDA"),
            ("+rocm", "ROCM"),
        ]

        if self.version >= Version("2.4.0"):
            query_to_cmake_arg.extend(
                [("^blis", "BLIS"), ("^amdblis", "BLIS"), ("^atlas", "ATLAS")]
            )

        for query, cmake_arg in query_to_cmake_arg:
            if query in self.spec:
                return cmake_arg

        return "CUSTOM"

    def cosma_scalapack_cmake_arg(self):
        spec = self.spec

        if "~scalapack" in spec:
            return "OFF"
        elif "^intel-mkl" in spec or "^intel-oneapi-mkl" in spec:
            return "MKL"
        elif "^cray-libsci" in spec:
            return "CRAY_LIBSCI"

        return "CUSTOM"

    def cmake_args(self):
        return [
            self.define("COSMA_WITH_TESTS", False),
            self.define("COSMA_WITH_APPS", False),
            self.define("COSMA_WITH_PROFILING", False),
            self.define("COSMA_WITH_BENCHMARKS", False),
            self.define("COSMA_BLAS", self.cosma_blas_cmake_arg()),
            self.define("COSMA_SCALAPACK", self.cosma_scalapack_cmake_arg()),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
