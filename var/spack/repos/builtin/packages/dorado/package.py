# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dorado(Package):
    """
    Dorado is a high-performance, easy-to-use, open source basecaller for Oxford Nanopore reads.
    """

    homepage = "https://github.com/nanoporetech/dorado"
    url = "https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.5.1-linux-x64.tar.gz"

    version("0.5.1", sha256="7d95f4d47e0024db8ca275a5c591ebcaf2e17bfbff714fa824b212fb58a98802")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bin/dorado", prefix.bin)
        mkdirp(prefix.lib)
        install_tree("lib/.", prefix.lib)
