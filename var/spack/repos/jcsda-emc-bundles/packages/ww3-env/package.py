# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ww3Env(BundlePackage):
    """
    Development environment for Wave Watch III
    """

    homepage = "https://github.com/NOAA-EMC/WW3"
    # There is no URL since there is no code to download.

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA")

    version("1.0.0")

    variant("grib2", default=True, description="Build with g2 library for GRIB2 I/O.")
    variant("netcdf", default=True, description="Build with NetCDF I/O.")
    variant("esmf", default=False, description="Build with ESMF support.")
    variant("parmetis", default=True, description="Build with ParMETIS support.")

    depends_on("bacio", when="+grib2")
    depends_on("g2", when="+grib2")
    depends_on("w3emc", when="+grib2")
    depends_on("w3nco", when="+grib2")

    depends_on("netcdf-fortran", when="+netcdf")

    depends_on("metis", when="+parmetis")
    depends_on("parmetis", when="+parmetis")
    depends_on("esmf", when="+esmf")

    # There is no need for install() since there is no code.
