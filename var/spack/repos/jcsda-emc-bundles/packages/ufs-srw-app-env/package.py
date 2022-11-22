# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfsSrwAppEnv(BundlePackage):
    """
    Development environment for the UFS Short-Range Weather Application
    """

    homepage = "https://github.com/ufs-community/ufs-srweather-app"
    git = "https://github.com/ufs-community/ufs-srweather-app.git"
    # There is no URL since there is no code to download.

    maintainers = ["AlexanderRichert-NOAA", "Hang-Lei-NOAA"]

    variant("python", default=True, description="Build Python dependencies")

    version("1.0.0")

    depends_on("ufs-pyenv", when="+python")
    depends_on("netcdf-fortran")
    depends_on("parallelio")
    depends_on("esmf")
    depends_on("fms@2022.01")
    depends_on("bacio")
    depends_on("crtm@2.4.0")
    depends_on("g2")
    depends_on("g2tmpl")
    depends_on("ip")
    depends_on("sp")
    depends_on("w3nco")
    depends_on("upp")
    depends_on("gfsio")
    depends_on("landsfcutil")
    depends_on("nemsio")
    depends_on("nemsiogfs")
    depends_on("sfcio")
    depends_on("sigio")
    depends_on("w3emc")
    depends_on("wgrib2")

    # There is no need for install() since there is no code.
