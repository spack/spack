##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os


class Nrnh5(CMakePackage):

    """Neuron HDF5 library developed by Blue Brain Project, EPFL"""

    homepage = "https://bbpcode.epfl.ch/sim/nrnh5"
    url      = "ssh://bbpcode.epfl.ch/sim/nrnh5"

    version('develop', git=url, preferred=True)

    variant('tests', default=False, description="Build unit tests")

    depends_on('cmake@3.5:', type='build')
    depends_on('boost', when='+tests')
    depends_on('hdf5')
    depends_on('mpi')

    def cmake_args(self):
        spec   = self.spec
        options = []

        if spec.satisfies('~tests'):
            options.append('-DUNIT_TESTS=OFF')
        
        options.extend([
            '-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx)
        ])

        return options
