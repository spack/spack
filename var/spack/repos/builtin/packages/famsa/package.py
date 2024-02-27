# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Famsa(MakefilePackage):
    """Progressive algorithm for large-scale multiple sequence alignments"""

    homepage = "https://github.com/refresh-bio/FAMSA"
    url = "https://github.com/refresh-bio/FAMSA/archive/refs/tags/v2.2.2.tar.gz"

    license("GPL-3.0-only", checked_by="A-N-Other")

    version("2.2.2", sha256="9e1d96b80ff0010852dcab24f8691bf2deb7415838c001f0362ec72fd0ac2d44")

    # patching to correct barrier implementation
    patch("famsa.patch")

    def build(self, spec, prefix):
        if spec.satisfies("target=m1:"):
            arch = "m1"
        elif spec.satisfies("target=aarch64:"):
            arch = "arm8"
        elif "avx2" in spec.target:
            arch = "avx2"
        elif "avx" in spec.target:
            arch = "avx"
        elif "sse4" in spec.target:
            arch = "sse4"
        else:
            arch = "none"
        make(f"PLATFORM={arch}")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("famsa", prefix.bin)
