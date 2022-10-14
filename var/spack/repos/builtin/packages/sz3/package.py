# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sz3(CMakePackage):
    """SZ3 is the next generation of the SZ compressor framework"""

    homepage = "https://github.com/szcompressor/SZ3"
    git = "https://github.com/szcompressor/SZ3"

    maintainers = ["disheng222"]

    version("master")
    version("3.1.5.4", commit="08df24b566e6d2e419cb95553aebf4a4902a8015")
    version("3.1.5.1", commit="5736a63b917e439dd62248b4ff6234e96726af5d")
    version("3.1.3.1", commit="323cb17b412d657c4be681b52c34beaf933fe7af")
    version("3.1.3", commit="695dff8dc326f3b165f6676d810f46add088a585")

    depends_on("zstd")
    depends_on("gsl")
    depends_on("pkgconfig")

    def cmake_args(self):
        return [
            "-DSZ3_USE_BUNDLED_ZSTD=OFF",
            "-DSZ3_DEBUG_TIMINGS=OFF",
        ]
