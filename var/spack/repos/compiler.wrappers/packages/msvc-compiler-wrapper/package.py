# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MsvcCompilerWrapper(Package):
    """Package to represent Spack """

    homepage = "https://github.com/spack/msvc-wrapper"
    git = "https://github.com/spack/msvc-wrapper"

    tags = ["windows"]

    maintainers("johnwparent")

    version("main", branch="main")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        with working_dir(spec.stage.source_path):
            Executable("cl.exe")("/EHsc cl.cxx")

    def install(self, spec, prefix):
        with working_dir(spec.stage.source_path):
            copy(".\\cl.exe", prefix.bin)
