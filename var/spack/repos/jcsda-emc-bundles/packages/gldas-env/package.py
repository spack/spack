# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GldasEnv(BundlePackage):
    """Development environment for GLDAS"""

    homepage = "https://github.com/NOAA-EMC/GLDAS"
    git = "https://github.com/NOAA-EMC/GLDAS.git"

    maintainers("AlexanderRichert-NOAA")

    version("1.0.0")

    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("esmf")
    depends_on("w3nco")
    depends_on("w3emc")
    depends_on("nemsio")
    depends_on("bacio")
    depends_on("sp")

    # There is no need for install() since there is no code.
