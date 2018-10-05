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


class SuperluDist(CMakePackage):
    """A general purpose library for the direct solution of large, sparse,
    nonsymmetric systems of linear equations on high performance machines."""

    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "https://github.com/xiaoyeli/superlu_dist/archive/v6.0.0.tar.gz"
    git      = "https://github.com/xiaoyeli/superlu_dist.git"

    version('develop', branch='master')
    version('xsdk-0.2.0', tag='xsdk-0.2.0')
    version('6.0.0', '2e3ce927fa5786470dacbdf8c41afb08')
    version('5.4.0', 'e64645c5be352ae2c88327af2cac66e1')
    version('5.3.0', '35d5aa8e0a246efaf327988b20106714')
    version('5.2.2', 'a685ef7fb7859b24c8c9d5d5f121a8a5')
    version('5.2.1', 'af857778ffeb04aea02aa4843e6e8e1d')
    version('5.1.3', '3a9e88a8469aa7f319f0364364b8da35')
    version('5.1.1', '12638c631733a27dcbd87110e9f9cb1e')
    version('5.1.0', '6bb86e630bd4bd8650243aed8fd92eb9')
    version('5.0.0', '2b53baf1b0ddbd9fcf724992577f0670')
    version('4.3', 'ee66c84e37b4f7cc557771ccc3dc43ae')
    version('4.2', 'ae9fafae161f775fbac6eba11e530a65')
    version('4.1', '4edee38cc29f687bd0c8eb361096a455')
    version('4.0', 'c0b98b611df227ae050bc1635c6940e0')
    version('3.3', 'f4805659157d93a962500902c219046b')

    variant('int64', default=False, description='Build with 64 bit integers')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('parmetis')
    depends_on('metis@5:')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DTPL_PARMETIS_LIBRARIES=%s' % spec['parmetis'].libs.ld_flags +
            ';' + spec['metis'].libs.ld_flags,
            '-DTPL_PARMETIS_INCLUDE_DIRS=%s' % spec['parmetis'].prefix.include
        ]

        if '+int64' in spec:
            args.append('-DXSDK_INDEX_SIZE=64')
        else:
            args.append('-DXSDK_INDEX_SIZE=32')

        if '+shared' in spec:
            args.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS:BOOL=OFF')
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        if name == 'cflags' and '%pgi' not in self.spec:
            flags.append('-std=c99')
        return (None, None, flags)
