# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qoz(CMakePackage):
    """Quality optimized version of SZ3 is the next generation of the SZ compressor framework"""

    git = "https://github.com/robertu94/QoZ"
    homepage = git

    version("2022.04.26", commit="d28a7a8c9f703075441b700202b8a1ee185ded00")

    maintainers("disheng222")

    depends_on("zstd")
    depends_on("gsl")
    depends_on("pkgconfig")

    def cmake_args(self):
        args = ["-DQoZ_USE_BUNDLED_ZSTD=OFF", "-DQoZ_DEBUG_TIMINGS=OFF"]
        return args
