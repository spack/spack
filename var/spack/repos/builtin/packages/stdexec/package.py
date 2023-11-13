# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stdexec(CMakePackage):
    """The proposed C++ framework for asynchronous and parallel programming."""

    homepage = "https://github.com/NVIDIA/stdexec"
    url = "https://github.com/NVIDIA/stdexec/archive/nvhpc-0.0.tar.gz"
    git = "https://github.com/NVIDIA/stdexec.git"
    maintainers("msimberg", "aurianer")

    license("Apache-2.0")

    version("23.03", sha256="2c9dfb6e56a190543049d2300ccccd1b626f4bb82af5b607869c626886fadd15")
    version("main", branch="main")

    depends_on("cmake@3.23.1:", type="build")

    conflicts("%gcc@:10")
    conflicts("%clang@:13")

    def build(self, spec, prefix):
        pass
