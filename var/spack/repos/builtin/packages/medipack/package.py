# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Medipack(CMakePackage):
    """MeDiPack (Message Differentiation Package) is a tool that handles the MPI communication
    of Algorithmic Differentiation (AD) tools like CoDiPack."""

    homepage = "https://github.com/SciCompKL/MeDiPack"
    url = "https://github.com/SciCompKL/MeDiPack/archive/refs/tags/v1.2.2.tar.gz"

    version("1.2.2", sha256="8937fa1025c6fb12f516cacf38a7f776221e7e818b30f17ce334c63f78513aa7")
    version("1.2.1", sha256="c746196b98cfe24a212584cdb88bd12ebb14f4a54728070d605e0c6d0e75db8a")

    depends_on("cmake@3.12:", type="build", when="@1.2.2:")

    build_system(
        conditional("cmake", when="@1.2.2:"),
        conditional("generic", when="@:1.2.1"),
        default="cmake",
    )

    def install(self, spec, prefix):
        mkdirp(join_path(prefix, "include"))
        install_tree(join_path(self.stage.source_path, "include"), join_path(prefix, "include"))
        mkdirp(join_path(prefix, "src"))
        install_tree(join_path(self.stage.source_path, "src"), join_path(prefix, "src"))
