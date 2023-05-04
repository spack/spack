# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GribUtil(CMakePackage):
    """This is a collection of NCEP GRIB related utilities.

    This is related to NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util/archive/refs/tags/v1.2.3.tar.gz"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("1.2.4", sha256="f021d6df3186890b0b1781616dabf953581d71db63e7c2913360336985ccaec7")
    version("1.2.3", sha256="b17b08e12360bb8ad01298e615f1b4198e304b0443b6db35fe990a817e648ad5")

    variant("openmp", default=False, description="Use OpenMP multithreading")

    depends_on("jasper")
    depends_on("libpng")
    depends_on("zlib")
    depends_on("w3emc", when="@1.2.4:")
    depends_on("w3nco", when="@:1.2.3")
    depends_on("g2")
    depends_on("bacio")
    depends_on("ip@:3.3.3")
    depends_on("sp")

    def cmake_args(self):
        args = [self.define_from_variant("OPENMP", "openmp")]
        return args
