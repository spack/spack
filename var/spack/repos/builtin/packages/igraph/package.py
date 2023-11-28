# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Igraph(CMakePackage, AutotoolsPackage):
    """igraph is a library for creating and manipulating graphs."""

    homepage = "https://igraph.org/"
    url = "https://github.com/igraph/igraph/releases/download/0.7.1/igraph-0.7.1.tar.gz"

    version("0.10.6", sha256="99bf91ee90febeeb9a201f3e0c1d323c09214f0b5f37a4290dc3b63f52839d6d")
    version("0.7.1", sha256="d978030e27369bf698f3816ab70aa9141e9baf81c56cc4f55efbe5489b46b0df")

    variant("shared", default=False, description="Enable shared build")

    build_system(
        conditional("cmake", when="@0.9:"), conditional("autotools", when="@:0.8"), default="cmake"
    )

    with when("build_system=cmake"):
        depends_on("arpack-ng")
        depends_on("blas")
        depends_on("glpk+gmp@4.57:")
        depends_on("gmp")
        depends_on("lapack")

    depends_on("libxml2")

    def cmake_args(self):
        args = [
            "-DIGRAPH_ENABLE_LTO=AUTO",
            "-DIGRAPH_GLPK_SUPPORT=ON",
            "-DIGRAPH_GRAPHML_SUPPORT=ON",
            "-DIGRAPH_USE_INTERNAL_ARPACK=OFF",
            "-DIGRAPH_USE_INTERNAL_BLAS=OFF",
            "-DIGRAPH_USE_INTERNAL_GLPK=OFF",
            "-DIGRAPH_USE_INTERNAL_GMP=OFF",
            "-DIGRAPH_USE_INTERNAL_LAPACK=OFF",
            "-DIGRAPH_USE_INTERNAL_PLFIT=ON",
            "-DBLA_VENDOR=OpenBLAS",
        ]

        if "+shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")

        return args
