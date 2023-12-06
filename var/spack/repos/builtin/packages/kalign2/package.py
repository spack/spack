# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack.package import *


class Kalign2(AutotoolsPackage):
    """A fast and accurate multiple sequence alignment algorithm"""

    homepage = "https://msa.sbc.su.se"
    version(
        "2.0.3",
        sha256="8cf20ac4e1807dc642e7ffba8f42a117313beccaee4f87c5555d53a2eeac4cbb",
        url="file://{0}/kalign_2.0.3.tar.gz".format(
            os.getcwd()
        ),
    )
    manual_download = True

    def patch(self):
        """Change hard-coded prefix path"""
        filter_file("/usr/local/bin", self.prefix.bin, "Makefile.in")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("kalign", prefix.bin)
