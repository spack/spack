# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Probconsrna(MakefilePackage):
    """Experimental version of PROBCONS with parameters estimated via unsupervised training
    on BRAliBASE"""

    homepage = "http://probcons.stanford.edu/"
    url = "http://probcons.stanford.edu/probconsRNA.tar.gz"

    version("1.10", sha256="7fe4494bd423db1d5f33f5ece2c70f9f66a0d9112e28d3eaa7dfdfe7fa66eba8")

    # update includes to bring inline with modern C++
    # (from patch file in the bioconda recipe)
    patch("probconsrna.patch")

    def edit(self, spec, prefix):
        filter_file("CXX = .*", f"CXX = {spack_cxx}", "Makefile")

    def build(self, spec, prefix):
        make("probcons", "compare", "project")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("probcons", prefix.bin.probconsRNA)
        install("compare", prefix.bin)
        install("project", prefix.bin)
