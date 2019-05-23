# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url      = "http://ceres-solver.org/ceres-solver-1.12.0.tar.gz"

    version('1.12.0', '278a7b366881cc45e258da71464114d9')

    depends_on('eigen@3:')
    depends_on('lapack')
    depends_on('glog')

    def cmake_args(self):
        args = [
            '-DSUITESPARSE=OFF',
            '-DCXSPARSE=OFF',
            '-DEIGENSPARSE=ON',
            '-DLAPACK=ON',
            '-DBUILD_SHARED_LIBS=ON',
            '-DSCHUR_SPECIALIZATIONS=OFF'
        ]
        return args
