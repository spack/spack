# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioErrorinjector(CMakePackage):
    """LibPressioErrorInjector injects errors into data for sensitivity studies"""

    homepage = "https://github.com/robertu94/libpressio-errorinjector"
    git = "git@github.com:robertu94/libpressio-errorinjector.git"

    maintainers = ["robertu94"]

    version("master", branch="master")

    depends_on("libpressio")

    def cmake_args(self):
        args = []
        return args
