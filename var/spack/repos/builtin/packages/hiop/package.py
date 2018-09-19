##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
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


class Hiop(CMakePackage):
    """HiOp is an optimization solver for solving certain mathematical
    optimization problems expressed as nonlinear programming problems.
    HiOp is a lightweight HPC solver that leverages application's existing
    data parallelism to parallelize the optimization iterations by using
    specialized linear algebra kernels."""

    homepage = "https://github.com/LLNL/hiop"
    git      = "https://github.com/LLNL/hiop.git"

    version('0.1', tag='v0.1')

    variant('mpi', default=True,
            description='Enable/Disable MPI')

    variant('deepchecking', default=True,
            description='Ultra safety checks - \
            used for increased robustness and self-diagnostics')

    depends_on('mpi', when='+mpi')
    depends_on('lapack')
    depends_on('blas')

    flag_handler = CMakePackage.build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        if '+mpi' in spec:
            args.append("-DWITH_MPI=ON")
        else:
            args.append("-DWITH_MPI=OFF")

        if '+deepchecking' in spec:
            args.append("-DDEEP_CHECKING=ON")
        else:
            args.append("-DDEEP_CHECKING=OFF")

        lapack_blas_libs = (
            spec['lapack'].libs + spec['blas'].libs).joined(';')
        args.extend([
            '-DLAPACK_FOUND=TRUE',
            '-DLAPACK_LIBRARIES={0}'.format(lapack_blas_libs)
        ])

        return args
