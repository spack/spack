# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PressioOps(Package):
    """
    pressio-ops is a header-only library containing
    essential operations for the Pressio ecosystem.
    """

    homepage = "https://pressio.github.io/pressio-ops"
    git = "https://github.com/pressio/pressio-ops.git"

    license("BSD-3-Clause")

    maintainers("fnrizzi", "cwschilly")

    version("main", branch="main")
    version("0.15.0", branch="0.15.0")

    def install(self, spec, prefix):
        install_tree("include", prefix.include)
