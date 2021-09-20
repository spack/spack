# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ip2(CMakePackage):
    """The NCEP general interpolation library 2 (ip2lib) contains Fortran 90
    subprograms to be used for interpolating between nearly all grids used at
    NCEP."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-ip2"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-ip2/archive/refs/tags/v1.1.2.tar.gz"

    maintainers = ['t-brown']

    version('1.1.2', sha256='73c6beec8fd463ec7ccba3633d8c5d53d385c43d507367efde918c2db0af42ab')

    depends_on('sp')
