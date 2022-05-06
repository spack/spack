# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NceplibsBundleEnv(BundlePackage):
    """
    This is a collection of libraries commonly known as NCEPLIBS that are required 
    for several NCEP applications e.g. UFS, GSI, UPP, etc. 
    """

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS"
    # There is no URL since there is no code to download.

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA']

    version('1.0.0')

    depends_on('bacio')
    depends_on('bufr')
    depends_on('crtm')
    depends_on('g2')
    depends_on('g2c')
    depends_on('g2tmpl')
    depends_on('gfsio')
    depends_on('ip')
    depends_on('landsfcutil')
    depends_on('ncio')
    depends_on('nemsio')
    depends_on('sfcio')
    depends_on('sigio')
    depends_on('sp')
    depends_on('w3emc')
    depends_on('w3nco')
    depends_on('wrf-io')
    depends_on('wgrib2')

    # There is no need for install() since there is no code.
