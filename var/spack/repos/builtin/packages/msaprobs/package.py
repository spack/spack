# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Msaprobs(MakefilePackage):
    """MSAProbs is a well-established state-of-the-art multiple sequence alignment algorithm
    for protein sequences"""

    homepage = "https://msaprobs.sourceforge.net/homepage.htm#latest"
    url = "https://downloads.sourceforge.net/project/msaprobs/MSAProbs-0.9.7.tar.gz"

    license("GPL-3.0-only", checked_by="A-N-Other")

    version("0.9.7", sha256="a14c59d714a5020c091ba9dd64d57d4d4aa5e39fefec06ba2f3d29e9ab38dad0")

    depends_on("mpi")

    build_directory = "MSAProbs"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file("CXX = .*", f"CXX = {spack_cxx}", "Makefile")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("all")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("msaprobs", prefix.bin)
