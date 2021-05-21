# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NceplibsIp(CMakePackage):
    """The NCEP general interpolation library (iplib) contains Fortran
    90 subprograms to be used for interpolating between nearly all
    (rectilinear) grids used at NCEP."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-ip"
    git      = "git@github.com:NOAA-EMC/NCEPLIBS-ip"

    version('v3.3.3')

    depends_on('NCEPLIBS-sp')

