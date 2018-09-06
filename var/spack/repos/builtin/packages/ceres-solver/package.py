##############################################################################
# Copyright (c) 2018, The VOTCA Development Team (http://www.votca.org)
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
