# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wgrib2(CMakePackage):
    """The wgrib2 package functionality for interacting with, reading,
    writing, and manipulating GRIB2 files."""

    homepage = "https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-wgrib2/archive/refs/tags/v2.0.8-cmake-v6.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('2.0.8-cmake-v6', sha256='745cd008b4ce0245ea44247733e57e2b9ec6c5205d171d457e18d0ff8f87172d')

    depends_on('ip2')
    depends_on('jasper')
    depends_on('libpng')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    depends_on('sp')

    def cmake_args(self):
        args = ['-DUSE_IPOLATES=3', '-DUSE_SPECTRAL=BOOL:ON']
        return args
