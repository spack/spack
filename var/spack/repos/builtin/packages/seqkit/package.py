# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Seqkit(Package):
    """seqkit: a cross-platform and ultrafast toolkit for FASTA/Q file manipulation"""

    homepage = "https://bioinf.shenwei.me/seqkit/"
    url = "https://github.com/shenwei356/seqkit/archive/refs/tags/v2.4.0.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version("2.6.1", sha256="d88249bd3b630c908ebd308abaa9cd7acb7a781c12bab877d3daaab56f43c443")
    version("2.5.1", sha256="76d105921f918be20e616fbb607fe0fb2db603535a254ec0f853cb36bef817da")
    version("2.4.0", sha256="c319f3d5feb7c99309e654042432959f01bbc5f7e4c71f55dc9854df46c73c7f")

    depends_on("go@1.17:", type="build")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        # Build using `go build`
        go("build", "-C", "seqkit")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path("seqkit", "seqkit"), prefix.bin)
