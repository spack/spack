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


class Globalarrays(AutotoolsPackage):
    """Global Arrays (GA) is a Partitioned Global Address Space (PGAS)
    programming model. It provides primitives for one-sided communication
    (Get, Put, Accumulate) and Atomic Operations (read increment).
    It supports blocking and non-blocking primtives, and supports location
    consistency."""

    homepage = "http://hpc.pnl.gov/globalarrays/"
    url = "https://github.com/GlobalArrays/ga/releases/download/v5.7/ga-5.7.tar.gz"

    version('5.7',   'bb9a441a6b4fbb8b52b58c2d3f4cd07f')
    version('5.6.5', '90da628dc72048deeda3f0cd095cb5b3')
    version('5.6.4', '051901b316c9766b8ba54306bff7f6b3')
    version('5.6.3', 'df3cf6cc8288d9f202b7fd0ea82f5491')
    version('5.6.2', '901e4612203bac45059be524fc1abfb7')
    version('5.6.1', '674c0ea9bf413840b1ff1e669de73fca')
    version('5.6',   '49d7e997daed094eeb9565423879ba36')

    variant('int64', default=False, description='Compile with 64 bit indices support')
    variant('blas', default=False, description='Enable BLAS')
    variant('lapack', default=False, description='Enable LAPACK')
    variant('scalapack', default=False, description='Enable SCALAPACK')
    variant('armci', values=('mpi-ts', 'mpi-pr', 'mpi3', 'openib', 'ofi'), 
        default='mpi-ts', description='ARMCI runtime')

    depends_on('mpi')
    depends_on('blas', when='+blas')
    depends_on('lapack', when='+lapack')
    depends_on('scalapack', when='+scalapack')

    conflicts('+lapack', when='~blas')
    conflicts('+scalapack', when='~blas')
    conflicts('+scalapack', when='~lapack')

    def configure_args(self):
        args = ['--with-mpi']

        if '+blas' in self.spec:
            if '+int64' in self.spec:
                args.append('--with-blas8')
            else:
                args.append('--with-blas')

        if '+lapack' in self.spec:
            args.append('--with-lapack')

        if '+scalapack' in self.spec:
            if '+int64' in self.spec:
                args.append('--with-scalapack8')
            else:
                args.append('--with-scalapack')

        args.append('--with-' + self.spec.variants['armci'].value)

        return args
