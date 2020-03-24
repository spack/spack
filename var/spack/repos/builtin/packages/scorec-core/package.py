# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ScorecCore(CMakePackage):
    """The SCOREC Core is a set of C/C++ libraries for unstructured mesh
    simulations on supercomputers.
    """

    homepage = 'https://www.scorec.rpi.edu/'
    git      = 'https://github.com/SCOREC/core.git'

    version('develop')

    depends_on('mpi')
    depends_on('zoltan')
    depends_on('cmake@3.0:', type='build')

    @property
    def std_cmake_args(self):
        # Default cmake RPATH options causes build failure on bg-q
        if self.spec.satisfies('platform=bgq'):
            return ['-DCMAKE_INSTALL_PREFIX:PATH={0}'.format(self.prefix)]
        else:
            return self._std_args(self)

    def cmake_args(self):
        options = []
        options.append('-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc)
        options.append('-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx)
        options.append('-DENABLE_ZOLTAN=ON')

        if self.compiler.name == 'xl':
            options.append('-DSCOREC_EXTRA_CXX_FLAGS=%s' % '-qminimaltoc')

        return options
