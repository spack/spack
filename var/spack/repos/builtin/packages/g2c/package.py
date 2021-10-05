# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class G2c(CMakePackage):
    """This library contains C decoder/encoder routines for GRIB edition 2.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-g2c"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-g2c/archive/refs/tags/v1.6.4.tar.gz"

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    variant('png', default=True)
    variant('jasper', default=True)
    variant('openjpeg', default=False)

    version('1.6.4', sha256='5129a772572a358296b05fbe846bd390c6a501254588c6a223623649aefacb9d')
    version('1.6.2', sha256='b5384b48e108293d7f764cdad458ac8ce436f26be330b02c69c2a75bb7eb9a2c')

    depends_on('libpng', when='+png')
    depends_on('jasper', when='+jasper')
    depends_on('openjpeg', when='+openjpeg')
