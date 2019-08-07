# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bml(CMakePackage):
    """The basic matrix library (bml) is a collection of various matrix data
    formats (in dense and sparse) and their associated algorithms for basic
    matrix operations."""

    homepage = "http://lanl.github.io/bml/"
    url      = "https://github.com/lanl/bml/tarball/v1.2.2"
    git      = "https://github.com/lanl/bml.git"

    version('develop', branch='master')
    version('1.3.1', sha256='17145eda96aa5e550dcbff1ee7ce62b45723af8210b1ab70c5975ec792fa3d13')
    version('1.3.0', '2bf8546b27a89666dab3e8f4873cd117')
    version('1.2.3', '8133137fb56a27fade44d1588449c2ac')
    version('1.2.2', 'c86959cb0188e9d0a9a2cbad03b2782d')
    version('1.1.0', '271adecee08aee678be9eeceee06b6fb')

    variant('shared', default=True, description='Build shared libs')
    variant('mpi', default=True, description='Build with MPI Support')

    conflicts('+mpi', when='@:1.2.2')

    depends_on("blas")
    depends_on("lapack")
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS={0}'.format(
                'ON' if '+shared' in self.spec else 'OFF')
        ]
        spec = self.spec
        if '+mpi' in spec:
            args.append('-DBML_MPI=True')
            args.append('-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx)
            args.append('-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc)
        else:
            args.append('-DBML_MPI=False')
        return args
