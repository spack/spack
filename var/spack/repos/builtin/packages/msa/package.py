# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Msa(MakefilePackage):
    """MSA is a program to perform multiple sequence alignment under the sum-of-pairs criterion"""

    homepage = "https://www.ncbi.nlm.nih.gov/research/staff/schaffer/msa/"
    url = "https://ftp.ncbi.nih.gov/pub/msa/msa.tar.Z"

    version(
        "2.1",
        sha256="b162b206bb6f47971cb6f1b6b7093eac19d96f45ed1d6268bf57fe983ce61976",
        url="https://ftp.ncbi.nih.gov/pub/msa/msa.tar.Z",
    )

    def edit(self, spec, prefix):
        filter_file("CC = .*", f"CC = {spack_cc}", "makefile")

    def build(self, spec, prefix):
        make("msa")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("msa", prefix.bin)
