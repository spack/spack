# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bufr(CMakePackage):
    """The NOAA bufr library contains subroutines, functions and other utilities
    that can be used to read (decode) and write (encode) data in BUFR, which
    is a WMO standard format for the exchange of meteorological data."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bufr"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-bufr/archive/refs/tags/bufr_v11.5.0.tar.gz"

    maintainers = ['t-brown']

    version('11.5.0', sha256='d154839e29ef1fe82e58cf20232e9f8a4f0610f0e8b6a394b7ca052e58f97f43')
