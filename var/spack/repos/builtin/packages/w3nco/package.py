# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *
from spack.operating_systems.mac_os import macos_version


class W3nco(CMakePackage):
    """This library contains Fortran 90 decoder/encoder routines for GRIB
    edition 1 with NCO changes. This library is deprecated; all
    functionality has been moved to the w3emc library.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS/NCEPLIBS-w3nco/"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-w3nco/archive/refs/tags/v2.4.1.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('2.4.1', sha256='48b06e0ea21d3d0fd5d5c4e7eb50b081402567c1bff6c4abf4fd4f3669070139')

    if sys.platform == 'darwin' and macos_version() >= Version('12.0'):
        patch('darwin/apple-clang-13.0.0-times.patch')
