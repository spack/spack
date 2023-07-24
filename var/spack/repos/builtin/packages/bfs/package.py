# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bfs(MakefilePackage):
    """A breadth-first version of the UNIX find command."""

    homepage = "https://github.com/tavianator/bfs"
    url = "https://github.com/tavianator/bfs/archive/refs/tags/3.0.1.tar.gz"

    maintainers("alecbcs")

    version("3.0.1", sha256="a38bb704201ed29f4e0b989fb2ab3791ca51c3eff90acfc31fff424579bbf962")

    depends_on("acl", when="platform=linux")
    depends_on("attr", when="platform=linux")
    depends_on("libcap", when="platform=linux")
    depends_on("oniguruma")

    def install(self, spec, prefix):
        make("install", f"PREFIX={prefix}")
