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

    version('develop', branch='develop')

    depends_on('nco')
    # depends_on('gempak')
    # depends_on('ncl')
    depends_on('prod_util')
    # Also Python dependencies in ufswm Python
    depends_on('grib-util')

    #depends_on('crtm-fix')
    depends_on('sigio')
    depends_on('zlib')
    depends_on('sfcio')
    depends_on('nemsio')
    depends_on('bacio')
    depends_on('gfsio')
    depends_on('g2')
    depends_on('ip')
    depends_on('sp')
    depends_on('w3emc')
    depends_on('w3nco')
    depends_on('crtm')
    depends_on('g2tmpl')
    depends_on('wrf-io')
    depends_on('netcdf-fortran')
    depends_on('bufr')
    depends_on('met')
    depends_on('metplus')
    depends_on('wgrib2')
    depends_on('fms')
    depends_on('parallelio')
