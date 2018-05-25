##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Mxnet(MakefilePackage):
    """MXNet is a deep learning framework
    designed for both efficiency and flexibility."""

    homepage = "http://mxnet.io"
    url      = "https://github.com/apache/incubator-mxnet/archive/0.10.0.post2.tar.gz"

    version('0.10.0.post2',  '7819d511cf4a6efad681e6662fa966e4',
            url="https://github.com/apache/incubator-mxnet/archive/0.10.0.post2.tar.gz")
    version('0.10.0.post1',  '16d540f407cd22285555b3ab22040032',
            url="https://github.com/apache/incubator-mxnet/archive/v0.10.0.post1.tar.gz")
    version('0.10.0', '2d0c83c33eda729932d620cca3078826',
            url="https://github.com/apache/incubator-mxnet/archive/v0.10.0.tar.gz")

    variant('cuda', default=False, description='Enable CUDA support')
    variant('opencv', default=True, description='Enable OpenCV support')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('profiler', default=False, description='Enable Profiler (for verification and debug only).')

    depends_on('dmlc-core@20170508')
    depends_on('dmlc-core+openmp', when='+openmp')
    depends_on('dmlc-core~openmp', when='~openmp')
    depends_on('mshadow@20170721')
    depends_on('ps-lite@20170328')
    depends_on('nnvm~shared@20170418')
    depends_on('openblas')
    depends_on('cudnn', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('cub', when='+cuda')
    depends_on('opencv+core+imgproc+highgui+jpeg+png+tiff~eigen~ipp@3.0:', when='+opencv')

    patch('makefile.patch', when='@0.10:0.11')

    def build(self, spec, prefix):
        filter_file('export CC = gcc', '', 'make/config.mk', string=True)
        filter_file('export CXX = g++', '', 'make/config.mk', string=True)

        args = [
            'CC=%s' % self.compiler.cc,
            'CXX=%s' % self.compiler.cxx,
            'DMLC_CORE=%s' % spec['dmlc-core'].prefix,
            'MSHADOW_PATH=%s' % spec['mshadow'].prefix,
            'PS_PATH=%s' % spec['ps-lite'].prefix,
            'NNVM_PATH=%s' % spec['nnvm'].prefix,
            'USE_OPENMP=%s' % ('1' if '+openmp' in spec else '0'),
            'USE_CUDA=%s' % ('1' if '+cuda' in spec else '0'),
            'USE_CUDNN=%s' % ('1' if '+cuda' in spec else '0'),
            'CUB_INCLUDE=%s' % spec['cub'].prefix.include,
            'USE_OPENCV=%s' % ('1' if '+opencv' in spec else '0'),
            'USE_PROFILER=%s' % ('1' if '+profiler' in spec else '0'),
        ]

        if '+opencv' in spec:
            filter_file('$(shell pkg-config --cflags opencv)',
                        '-I%s' % spec['opencv'].prefix.include,
                        'Makefile', string=True)
            filter_file('$(filter-out -lopencv_ts, '
                        '$(shell pkg-config --libs opencv))',
                        '-lopencv_core -lopencv_imgproc -lopencv_imgcodecs',
                        'Makefile', string=True)

        # TODO: Add more BLAS support
        args.append('USE_BLAS=openblas')

        if '+cuda' in spec:
            args.extend(['USE_CUDA_PATH=%s' % spec['cuda'].prefix,
                         'CUDNN_PATH=%s' % spec['cudnn'].prefix])

        make(*args)

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
        install_tree('lib', prefix.lib)
        install_tree('bin', prefix.bin)
