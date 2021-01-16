# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CeresSolver(CMakePackage):
    """Ceres Solver is an open source C++ library for modeling and solving
    large, complicated optimization problems. It can be used to solve
    Non-linear Least Squares problems with bounds constraints and general
    unconstrained optimization problems. It is a mature, feature rich, and
    performant library that has been used in production at Google since 2010.
    """

    homepage = "http://ceres-solver.org"
    url      = "https://github.com/ceres-solver/ceres-solver/archive/2.0.0.tar.gz"

    version('2.0.0',  sha256='2ab0348e0f65fdf43bebcd325a1c73f7e8999691ee75e2a2981281931c42e9fa')
    version('1.14.0', sha256='1296330fcf1e09e6c2f926301916f64d4a4c5c0ff12d460a9bc5d4c48411518f')
    version('1.12.0', sha256='7433c1e0518108bb3e4b9d8a2a481da43cd490e839f234feb828b4a6b2b07a23')

    variant('suitesparse', default=False, description='Build with SuiteSparse')
    variant('shared', default=True, description='Build shared libraries')
    variant('examples', default=False, description='Build examples')

    depends_on('eigen@3:')
    depends_on('lapack')
    depends_on('glog')

    def cmake_args(self):
        args = [
            '-DCXSPARSE=OFF',
            '-DEIGENSPARSE=ON',
            '-DLAPACK=ON',
            '-DSCHUR_SPECIALIZATIONS=OFF'
        ]

        if '+suitesparse' in self.spec:
            args.append('-DSUITESPARSE=ON')
        else:
            args.append('-DSUITESPARSE=OFF')

        if '+shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        if '+examples' in self.spec:
            args.append('-DBUILD_EXAMPLES=ON')
        else:
            args.append('-DBUILD_EXAMPLES=OFF')

        return args
