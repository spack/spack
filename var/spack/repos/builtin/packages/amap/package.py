# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amap(MakefilePackage):
    """AMAP is a multiple sequence alignment program based on sequence annealing. This
    approach consists of building up the multiple alignment one match at a time, thereby
    circumventing many of the problems of progressive alignment"""

    homepage = "https://github.com/mes5k/amap-align"
    git = "https://github.com/mes5k/amap-align.git"

    version("2.2", commit="600fc29fb9d0e8a6abf797c173c7a416ab99c541")

    build_directory = "align"

    # update includes to bring inline with modern C++
    # (combines relevant patches from the `amap` and `probcons` bioconda recipes)
    patch("amap.patch")

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file("CXX = .*", f"CXX = {spack_cxx}", "Makefile")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("amap", prefix.bin)
