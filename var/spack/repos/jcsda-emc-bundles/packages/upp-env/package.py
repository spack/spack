# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import sys

from spack import *


class UppEnv(BundlePackage):
    """Development environment for UPP"""

    homepage = "https://github.com/NOAA-EMC/UPP"
    git      = "https://github.com/NOAA-EMC/UPP.git"

    maintainers = ['kgerheiser']

    version('develop', branch='develop')

    depends_on('netcdf-fortran')
    depends_on('bacio')
    depends_on('crtm')
    depends_on('g2')
    depends_on('g2tmpl')
    depends_on('nemsio')
    depends_on('sfcio')
    depends_on('sigio')
    depends_on('sp')
    depends_on('w3nco')
    depends_on('w3emc')
    depends_on('wrf-io')
