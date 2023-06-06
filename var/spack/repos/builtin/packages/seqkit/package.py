# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.filesystem import join_path, set_executable

from spack.util.executable import which
from spack.package import *


class Seqkit(Package):
    """seqkit: a cross-platform and ultrafast toolkit for FASTA/Q file manipulation"""

    homepage = "https://bioinf.shenwei.me/seqkit/"
    url = "https://github.com/shenwei356/seqkit/archive/refs/tags/v2.4.0.tar.gz"

    version("2.4.0", sha256="c319f3d5feb7c99309e654042432959f01bbc5f7e4c71f55dc9854df46c73c7f")
    version(
        "0.10.1",
        sha256="82f1c86dc4bd196403a56c2bf3ec063e5674a71777e68d940c4cc3d8411d2e9d",
        url="https://github.com/shenwei356/seqkit/releases/download/v0.10.1/seqkit_linux_amd64.tar.gz",
        deprecated=True,
    )

    depends_on("go@1.17:", type="build", when="@2.0.0:")
    depends_on("go@1.16:", type="build", when="@0.15.0:0.16.1")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        """Build using `go build`"""

        if self.spec.satisfies("@0.15.0:"):
            go_exec = which("go")
            go_exec("build", "-C", "seqkit")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if self.spec.satisfies("@0.15.0:"):
            install(join_path("seqkit", "seqkit"), prefix.bin)
        else:
            install("seqkit", prefix.bin)
        set_executable(join_path(prefix.bin, "seqkit"))
