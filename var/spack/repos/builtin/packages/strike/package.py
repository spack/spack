# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Strike(MakefilePackage):
    """STRIKE (Single sTRucture Induced Evaluation) is a program to evaluate protein multiple
    sequence alignments using a single protein structure"""

    homepage = "https://tcoffee.org/Projects/strike/index.html"
    url = "https://s3.eu-central-1.amazonaws.com/tcoffee-packages/strike/download/strike_v1.2.tar.bz2"

    version("1.2", sha256="4e0974c57a18b10faff635f60d2d4c5e253a67e43e525aec98545f45884e7295")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("CC = .*", f"CC = {spack_cc}")

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
