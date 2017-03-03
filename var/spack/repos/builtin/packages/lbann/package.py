##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Lbann(CMakePackage):
    """LBANN: Livermore Big Artificial Neural Network Toolkit.  A distributed
    memory, HPC-optimized, model and data parallel training toolkit for deep
    neural networks."""

    homepage = "http://software.llnl.gov/lbann/"
    url      = "https://github.com/LLNL/lbann/archive/v0.91.tar.gz"

    version('develop', git='https://github.com/LLNL/lbann.git', branch="develop")
    version('0.91', '83b0ec9cd0b7625d41dfb06d2abd4134')

    variant('debug', default=False, description='Builds a debug version of the libraries')
    variant('gpu', default=False, description='Builds with support for GPUs via CUDA and cuDNN')
    variant('opencv', default=True, description='Builds with support for image processing routines with OpenCV')
    variant('seq_init', default=False, description='Force serial initialization of weight matrices.')

    depends_on('elemental +openmp_blas +scalapack +shared +int64')
    depends_on('elemental +openmp_blas +scalapack +shared +int64 +debug', when='+debug')
    depends_on('cuda', when='+gpu')
    depends_on('mpi')
    depends_on('opencv@2.4.13', when='+opencv')
    depends_on('protobuf@3.0.2')

    def build_type(self):
        if '+debug' in self.spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        spec = self.spec
        # Environment variables
        CPPFLAGS = []
        CPPFLAGS.append('-DLBANN_SET_EL_RNG')
        if '~seq_init' in spec:
            CPPFLAGS.append('-DLBANN_PARALLEL_RANDOM_MATRICES')

        args = [
            '-DCMAKE_INSTALL_MESSAGE=LAZY',
            '-DCMAKE_CXX_FLAGS=%s' % ' '.join(CPPFLAGS),
            '-DWITH_CUDA:BOOL=%s' % ('+gpu' in spec),
            '-DWITH_CUDNN:BOOL=%s' % ('+gpu' in spec),
            '-DWITH_TBINF=OFF',
            '-DWITH_VTUNE=OFF',
            '-DElemental_DIR={0}'.format(self.spec['elemental'].prefix),
            '-DELEMENTAL_MATH_LIBS={0}'.format(
                self.spec['elemental'].elemental_libs),
            '-DVERBOSE=0',
            '-DLBANN_HOME=.',
            '-DLBANN_VER=spack']

        if '+opencv' in self.spec:
            args.extend(['-DOpenCV_DIR:STRING={0}'.format(
                self.spec['opencv'].prefix)])

        return args
