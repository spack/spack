# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qcat(CMakePackage):
    """Quick data compression quality analysis tool"""

    homepage = "https://github.com/szcompressor/qcat"
    git = "https://github.com/robertu94/qcat"

    maintainers = ["disheng222", "robertu94"]

    version("master", branch="master")

    depends_on("zstd")

    def cmake_args(self):
        args = ["-DQCAT_USE_BUNDLES=OFF"]
        return args
