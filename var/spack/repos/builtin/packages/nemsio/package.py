# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nemsio(CMakePackage):
    """The NOAA Environmental Modeling System I/O (NEMSIO) library. The
    basic functions it provides are to read and write data sets for all the
    NEMS applications."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-nemsio"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-nemsio/archive/refs/tags/v2.5.2.tar.gz"

    maintainers = ['t-brown']

    version('2.5.2', sha256='c59e9379969690de8d030cbf4bbbbe3726faf13c304f3b88b0f6aec1496d2c08')

    depends_on('bacio')
    depends_on('mpi')
    depends_on('w3nco')

    def cmake_args(self):
        return ['-DMPI_Fortran_COMPILER=%s' % self.spec['mpi'].mpifc]
