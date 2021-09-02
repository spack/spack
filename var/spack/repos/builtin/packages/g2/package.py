# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class G2(CMakePackage):
    """Utilities for coding/decoding GRIB2 messages. This library contains
    Fortran 90 decoder/encoder routines for GRIB edition 2, as well as
    indexing/searching utility routines."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-g2"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-g2/archive/refs/tags/v3.4.3.tar.gz"

    maintainers = ['t-brown']

    version('3.4.3', sha256='679ea99b225f08b168cbf10f4b29f529b5b011232f298a5442ce037ea84de17c')

    depends_on('jasper')
    depends_on('libpng')
