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
    """LBANN: Livermore Big Artificial Neural Network Toolkit.  A distributed memory, HPC-optimized, model and data parallel training toolkit for deep neural networks."""

    homepage = "http://software.llnl.gov/lbann/"
    url      = "https://github.com/LLNL/lbann/archive/v0.91.tar.gz"

    version('develop', git='https://github.com/LLNL/lbann.git', branch="develop")
    version('0.91', '83b0ec9cd0b7625d41dfb06d2abd4134')

    variant('debug', default=False,
            description='Builds a debug version of the libraries')
    variant('gpu', default=False,
            description='Builds with support for GPUs via CUDA and cuDNN')
    variant('opencv', default=True,
            description='Builds with support for image processing routines with OpenCV')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('int64', default=False,
            description='Elemental: use 64bit integers')
    variant('int64_blas', default=False,
            description='Elemental: use 64bit integers for BLAS')

    depends_on('cmake', type='build')
    depends_on('elemental +openmp_blas +scalapack')
    depends_on('elemental +openmp_blas +scalapack +debug', when='+debug')
    depends_on('cuda', when='+gpu')
    depends_on('mpi')
    depends_on('opencv', when='+opencv')
    depends_on('protobuf@3.0.2')

    def build_type(self):
        """Returns the correct value for the ``CMAKE_BUILD_TYPE`` variable                                                                                                                                
        :return: value for ``CMAKE_BUILD_TYPE``                                                                                                                                                           
        """
        if '+debug' in self.spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        spec = self.spec

#        include_flags = ["-I%s" % join_path(self.stage.source_path, "spack-build/include")]
#        include_flags = ["-I%s" % join_path(spec.prefix, "include")]
#        link_flags = self.lapack_libs.ld_flags.split()

#/g/g19/vanessen/spack.git/opt/spack/linux-rhel7-x86_64/gcc-4.9.3/lbann-develop-ioboloaiznrunp4da4xjgodobsxdihe6/include
        args = ['-DCMAKE_INSTALL_MESSAGE=LAZY',
#                '-D GFORTRAN_LIB=/usr/tce/packages/gcc/gcc-4.9.3/lib64/libgfortran.so',
                '-DCMAKE_CXX_FLAGS=-DLBANN_SET_EL_RNG -I{0}/spack-build/include'.format((
                    self.stage.source_path)),
                '-DWITH_CUDA:BOOL={0}'.format((
                    'ON' if '+gpu' in self.spec else 'OFF')),
                '-DWITH_CUDNN:BOOL={0}'.format((
                    'ON' if '+gpu' in self.spec else 'OFF')),
                '-DWITH_TBINF=OFF',
                '-DWITH_VTUNE=OFF',
                '-DElemental_DIR={0}'.format(self.spec['elemental'].prefix),
                '-DELEMENTAL_MATH_LIBS={0}'.format(self.spec['elemental'].elemental_libs),
                '-DVERBOSE=0',
                '-DLBANN_HOME=.',
                '-DLBANN_VERSION=spack']

        if '+opencv' in self.spec:
            args.extend(['-DOpenCV_DIR:STRING={0}'.format(
                self.spec['opencv'].prefix)])

        return args
