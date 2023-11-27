# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.paths

from spack.package import *


class MsvcCompilerWrapper(NMakePackage):
    """Package to represent Spack """

    homepage = "https://github.com/spack/msvc-wrapper"
    git = "https://github.com/spack/msvc-wrapper"

    tags = ["windows"]

    maintainers("johnwparent")

    version("main", branch="main")


    build_targets = ["cl.exe"]

    def nmake_install_args(self, spec, prefix):
            return [f"PREFIX={spack.paths.build_env_path}\\msvc"]
