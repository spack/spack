# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Restic(Package):
    """Fast, secure, efficient backup program."""

    homepage = "https://restic.net"
    url = "https://github.com/restic/restic/releases/download/v0.12.1/restic-0.12.1.tar.gz"

    maintainers("alecbcs")

    version("0.15.1", sha256="fce382fdcdac0158a35daa640766d5e8a6e7b342ae2b0b84f2aacdff13990c52")
    version("0.15.0", sha256="85a6408cfb0798dab52335bcb00ac32066376c32daaa75461d43081499bc7de8")
    version("0.14.0", sha256="78cdd8994908ebe7923188395734bb3cdc9101477e4163c67e7cc3b8fd3b4bd6")
    version("0.12.1", sha256="a9c88d5288ce04a6cc78afcda7590d3124966dab3daa9908de9b3e492e2925fb")

    depends_on("go@1.18:", type="build", when="@0.15.0:")
    depends_on("go@1.15:", type="build", when="@0.14.0:")
    depends_on("go", type="build")

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.stage.path)

    def install(self, spec, prefix):
        go("run", "build.go")
        mkdirp(prefix.bin)
        install("restic", prefix.bin)
