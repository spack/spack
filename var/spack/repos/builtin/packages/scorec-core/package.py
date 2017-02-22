##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class ScorecCore(CMakePackage):
    """The SCOREC Core is a set of C/C++ libraries for unstructured mesh
    simulations on supercomputers.
    """

    homepage = 'https://www.scorec.rpi.edu/'
    url = 'https://github.com/SCOREC/core.git'

    version('develop', git=url)

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
