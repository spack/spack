# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfsUtilsEnv(BundlePackage):
    """
    Development environment for UFS_UTILS
    """

    homepage = "https://github.com/ufs-community/UFS_UTILS"
    git = "https://github.com/ufs-community/UFS_UTILS.git"
    # There is no URL since there is no code to download.

    maintainers = ["AlexanderRichert-NOAA", "Hang-Lei-NOAA"]

    version("1.0.0")

    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("esmf")
    depends_on("bacio")
    depends_on("g2")
    depends_on("ip")
    depends_on("nemsio")
    depends_on("sp")
    depends_on("w3nco")
    depends_on("w3emc")
    depends_on("sfcio")
    depends_on("sigio")
    depends_on("nccmp")
    depends_on("wgrib2")

    # There is no need for install() since there is no code.
