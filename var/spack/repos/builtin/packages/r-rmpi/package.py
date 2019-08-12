# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRmpi(RPackage):
    """An interface (wrapper) to MPI APIs. It also provides interactive R
       manager and worker environment."""

    homepage = "http://www.stats.uwo.ca/faculty/yu/Rmpi"
    url      = "https://cran.r-project.org/src/contrib/Rmpi_0.6-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Rmpi"

    version('0.6-6', 'a6fa2ff5e1cd513334b4e9e9e7a2286f')
    depends_on('mpi')
    depends_on('r@2.15.1:')

    # The following MPI types are not supported
    conflicts('^intel-mpi')
    conflicts('^intel-parallel-studio')
    conflicts('^mvapich2')
    conflicts('^spectrum-mpi')

    def configure_args(self):
        spec = self.spec

        mpi_name = spec['mpi'].name

        # The type of MPI. Supported values are:
        # OPENMPI, LAM, MPICH, MPICH2, or CRAY
        if mpi_name == 'openmpi':
            rmpi_type = 'OPENMPI'
        elif mpi_name == 'mpich':
            rmpi_type = 'MPICH2'
        else:
            raise InstallError('Unsupported MPI type')

        return [
            '--with-Rmpi-type={0}'.format(rmpi_type),
            '--with-mpi={0}'.format(spec['mpi'].prefix),
        ]
