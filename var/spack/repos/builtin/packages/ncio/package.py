# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ncio(CMakePackage):
    """This is a library used by NCEP GSI system to read the GFS forecast
    files for use in data assimilation.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-ncio"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-ncio/archive/refs/tags/v1.0.0.tar.gz"

    maintainers = ['edwardhartnett', 'kgerheiser', 'Hang-Lei-NOAA']

    version('1.0.0', sha256='2e2630b26513bf7b0665619c6c3475fe171a9d8b930e9242f5546ddf54749bd4')

    depends_on('mpi')
    depends_on('netcdf-fortran')
