# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class PressioLog(Package):
    """
    pressio-log is a header-only logging library designed
    for use with Pressio repositories.
    """

    homepage = "https://github.com/Pressio/pressio-log/blob/main/README.md"
    git = "https://github.com/pressio/pressio-log.git"

    license("BSD-3-Clause")

    maintainers("fnrizzi", "cwschilly")

    version("main", branch="main")
    version("0.15.0", branch="0.15.0")

    def install(self, spec, prefix):
        install_tree("include", prefix.include)
