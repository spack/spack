# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glab(Package):
    """GitLab's official command line tool."""

    homepage = "https://gitlab.com/gitlab-org/cli"
    url = "https://gitlab.com/gitlab-org/cli/-/archive/v1.22.0/cli-v1.22.0.tar.gz"

    version("1.22.0", sha256="4d9bceb6818c8bf9f681119dae3a65f1c895fa21e9da6b38e8f88d245f524e10")
    version("1.21.1", sha256="8bb35c5cf6b011ff14d1eaa9ab70ec052d296978792984250e9063b006ee4d50")
    version("1.20.0", sha256="6beb0186fa50d0dea3b05fcfe6e4bc1f9be0c07aa5fa15b37ca2047b16980412")

    depends_on("go@1.13:", type="build")

    def install(self, spec, prefix):
        make()
        make("install", "prefix=" + prefix)
