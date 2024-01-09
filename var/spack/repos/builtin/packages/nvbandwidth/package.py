# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvbandwidth(CMakePackage, CudaPackage):
    """
    nvbandwidth: A tool for bandwidth measurements on NVIDIA GPUs.
    """

    git = "https://github.com/NVIDIA/nvbandwidth"

    license("Apache-2.0")

    version("main", branch="main")

    depends_on("boost@1.66.0 +program_options")

    def install(self, spec, prefix):
        # We have no `make install` target, so move the files over explicitly
        mkdirp(prefix.bin)
        install(join_path(self.build_directory, "nvbandwidth"), join_path(prefix.bin))
