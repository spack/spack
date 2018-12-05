# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Argobots(AutotoolsPackage):
    """Argobots, which was developed as a part of the Argo project, is
    a lightweight runtime system that supports integrated computation
    and data movement with massive concurrency. It will directly
    leverage the lowest-level constructs in the hardware and OS:
    lightweight notification mechanisms, data movement engines, memory
    mapping, and data placement strategies. It consists of an
    execution model and a memory model."""

    homepage = "http://www.argobots.org/"
    url      = "https://github.com/pmodels/argobots/releases/download/v1.0b1/argobots-1.0b1.tar.gz"
    git      = "https://github.com/pmodels/argobots.git"

    version("develop", branch="master")
    version("1.0b1", "5eeab7b2c639d08bbea22db3026cdf39")
    version("1.0a1", "9d29d57d14d718f93b505178f6ba3e08")

    variant("valgrind", default=False, description="Enable Valgrind")

    depends_on("m4", type=("build"), when="@develop")
    depends_on("autoconf", type=("build"), when="@develop")
    depends_on("automake", type=("build"), when="@develop")
    depends_on("libtool", type=("build"), when="@develop")
    depends_on("valgrind", when="+valgrind")

    def configure_args(self):
        args = ["--enable-perf-opt"]
        if '+valgrind' in self.spec:
            args.append('--enable-valgrind')
        else:
            args.append('--disable-valgrind')

        return args
