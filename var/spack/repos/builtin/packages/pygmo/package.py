# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pygmo(CMakePackage):
    """Parallel Global Multiobjective Optimizer (and its Python alter ego
    PyGMO) is a C++ / Python platform to perform parallel computations of
    optimisation tasks (global and local) via the asynchronous generalized
    island model."""

    homepage = "https://esa.github.io/pygmo2/"
    url      = "https://github.com/esa/pygmo2/archive/v2.18.0.tar.gz"
    git      = "https://github.com/esa/pygmo2.git"

    version('master', branch='master')
    version('2.18.0', sha256='9f081cc973297894af09f713f889870ac452bfb32b471f9f7ba08a5e0bb9a125')

    depends_on('pagmo2')
    depends_on('mpi')
    depends_on('py-pybind11@2.6.0:2.6.2')
    depends_on('cmake@3.1:', type='build')

    patch('installdir.patch')

    variant('shared', default=True, description='Build shared libraries')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_INSTALL_PREFIX=%s' % self.prefix,
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
        ]

        return args
