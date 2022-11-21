# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobalWorkflowEnv(BundlePackage):
    """Development environment for NOAA's Global Workflow"""

    homepage = "https://github.com/NOAA-EMC/global-workflow"
    git = "https://github.com/NOAA-EMC/global-workflow.git"

    maintainers = ["AlexanderRichert-NOAA"]

    version("1.0.0")
    variant("python", default=True, description="Build Python dependencies")

    depends_on("ufs-pyenv", when="+python")
    depends_on("prod-util")
    depends_on("nco")
    depends_on("cdo")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("esmf")
    depends_on("bacio")
    depends_on("g2")
    depends_on("w3nco")
    depends_on("w3emc")
    depends_on("sp")
    depends_on("ip")
    depends_on("nemsio")
    depends_on("nemsiogfs")
    depends_on("ncio")
    depends_on("landsfcutil")
    depends_on("sigio")
    depends_on("bufr")
    depends_on("wgrib2")
    depends_on("met")
    depends_on("metplus")

    # There is no need for install() since there is no code.
