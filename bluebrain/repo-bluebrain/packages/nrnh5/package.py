##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Nrnh5(CMakePackage):

    """Neuron HDF5 library developed by Blue Brain Project, EPFL"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/archive/nrnh5"
    url      = "git@bbpgitlab.epfl.ch:hpc/archive/nrnh5.git"

    version('develop', git=url, preferred=True)

    variant('tests', default=False, description="Build unit tests")

    depends_on('cmake@3.2:', type='build')
    depends_on('boost', when='+tests')
    depends_on('hdf5')
    depends_on('mpi')

    def cmake_args(self):
        spec   = self.spec
        options = []

        if spec.satisfies('~tests'):
            options.append('-DUNIT_TESTS=OFF')

        options.extend([
            '-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx)
        ])

        return options
