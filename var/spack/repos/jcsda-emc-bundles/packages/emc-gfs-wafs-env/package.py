# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import sys

from spack import *


class EmcGfsWafsEnv(BundlePackage):
    """Development environment for EMC GFS WAFS"""

    homepage = "https://github.com/NOAA-EMC/EMC_gfs_wafs"
    git      = "https://github.com/NOAA-EMC/EMC_gfs_wafs.git"

    maintainers = ['kgerheiser']

    version('1.0.0')

    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
    depends_on('bacio')
    depends_on('w3emc')
    depends_on('w3nco')
    depends_on('sp')
    depends_on('ip')
    depends_on('g2')
    depends_on('bufr')
