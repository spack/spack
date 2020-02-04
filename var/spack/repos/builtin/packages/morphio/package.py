# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Morphio(CMakePackage):
    """Library for reading / writing morphology files"""

    homepage = "https://github.com/BlueBrain/MorphIO"
    url      = "https://github.com/BlueBrain/MorphIO.git"
    git      = "https://github.com/BlueBrain/MorphIO.git"

    version('develop', git=url, submodules=True)
    version('2.3.4', tag='v2.3.4', submodules=True)
    version('2.2.1', tag='v2.2.1', submodules=True)
    version('2.1.2', tag='v2.1.2', submodules=True)
    version('2.0.8', tag='v2.0.8', submodules=True)

    variant('mpi', default=True, description="Build with MPI support")

    depends_on('cmake@3.2:', type='build')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = ['-DBUILD_BINDINGS:BOOL=OFF']
        if self.spec.satisfies("+mpi"):
            args += ['-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
                     '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx)]
        return args
