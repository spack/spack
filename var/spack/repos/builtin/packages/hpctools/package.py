##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Hpctools(CMakePackage):
    """Tools from the BBP HPC team
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/hpc/HPCTools"
    url      = "ssh://bbpcode.epfl.ch/hpc/HPCTools"

    version('develop', git=url)
    version('3.5.2', tag='v3.5.2', git=url, preferred=True)
    version('3.5.1', tag='3.5.1', git=url)
    version('3.1.0', tag='3.1.0', git=url)

    variant('openmp', default=True, description='Enables OpenMP support')

    depends_on('boost@1.50:')
    depends_on('cmake', type='build')
    depends_on('libxml2')
    depends_on('mpi')

    def cmake_args(self):
        args = [
            '-DUSE_OPENMP:BOOL={}'.format('+openmp' in self.spec),
            '-DMPI_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
            '-DMPI_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx),
        ]
        return args
