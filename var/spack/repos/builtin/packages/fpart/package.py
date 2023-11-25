# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fpart(AutotoolsPackage):
    """Fpart is a filesystem partitioner. It helps you sort file trees and pack them
    into bags (called "partitions"). Fpsync wraps fpart and rsync, tar, or cpio
    to launch several synchronization jobs in parallel."""

    homepage = "https://www.fpart.org"
    url = "https://github.com/martymac/fpart/archive/refs/tags/fpart-1.5.1.tar.gz"
    git = "https://github.com/martymac/fpart.git"

    maintainers("drkrynstrng")

    license("BSD-2-Clause")

    version("master", branch="master")
    version("1.5.1", sha256="c353a28f48e4c08f597304cb4ebb88b382f66b7fabfc8d0328ccbb0ceae9220c")

    variant("embfts", default=False, description="Build with embedded fts functions")
    variant("static", default=False, description="Build static binary")
    variant("debug", default=False, description="Build with debugging support")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    # fpsync has the following run dependencies
    depends_on("rsync", type="run")
    depends_on("tar", type="run")
    depends_on("cpio", type="run")

    def configure_args(self):
        config_args = []
        config_args.extend(self.enable_or_disable("embfts"))
        config_args.extend(self.enable_or_disable("static"))
        config_args.extend(self.enable_or_disable("debug"))
        return config_args
