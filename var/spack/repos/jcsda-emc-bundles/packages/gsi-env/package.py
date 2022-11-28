# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GsiEnv(BundlePackage):
    """Development environment for GSI"""

    homepage = "https://github.com/NOAA-EMC/GSI"
    git = "https://github.com/NOAA-EMC/GSI.git"

    maintainers = ["AlexanderRichert-NOAA"]

    version("1.0.0")

    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("bufr")
    depends_on("bacio")
    depends_on("w3emc")
    depends_on("sp")
    depends_on("ip")
    depends_on("sigio")
    depends_on("sfcio")
    depends_on("nemsio")
    depends_on("wrf-io")
    depends_on("crtm@2.4.0")
    depends_on("ncio")
    depends_on("gsi-ncdiag")

    # There is no need for install() since there is no code.
