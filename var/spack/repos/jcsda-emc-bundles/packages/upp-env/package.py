# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UppEnv(BundlePackage):
    """Development environment for UPP"""

    homepage = "https://github.com/NOAA-EMC/UPP"
    git = "https://github.com/NOAA-EMC/UPP.git"

    maintainers = ["AlexanderRichert-NOAA"]

    version("1.0.0")

    depends_on("netcdf-fortran")
    depends_on("bacio")
    depends_on("crtm@2.4.0")
    depends_on("g2")
    depends_on("g2tmpl")
    depends_on("nemsio")
    depends_on("sfcio")
    depends_on("sigio")
    depends_on("sp")
    depends_on("w3nco")
    depends_on("w3emc")
    depends_on("wrf-io")

    # There is no need for install() since there is no code.
