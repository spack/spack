# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Generax(CMakePackage):
    """GeneRax is a parallel tool for species tree-aware maximum likelihood
    based gene family tree inference under gene duplication, transfer,
    and loss.
    """

    homepage = "https://github.com/BenoitMorel/GeneRax"
    git = "https://github.com/BenoitMorel/GeneRax.git"

    maintainers("snehring")

    version("2.0.4", commit="e4fab40f407bdd3b588d3d69a449f8c1be56f9fa", submodules=True)

    depends_on("cmake@3.0.1:", type="build")
    depends_on("mpi")
    depends_on("bison")
    depends_on("flex")

    build_directory = "build"

    @when("@:2.0.4")
    def patch(self):
        filter_file(
            r"(^#include <memory>.*$)", "\\1\n#include <stdexcept>", "src/core/IO/Model.hpp"
        )

    def install(self, spec, prefix):
        install_tree("build/bin", prefix.bin)
