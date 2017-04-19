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


class Caffe(CMakePackage):
    """Caffe is a deep learning framework made with expression, speed, and
       modularity in mind. It is developed by the Berkeley Vision and Learning
       Center (BVLC) and by community contributors."""

    homepage = "http://caffe.berkeleyvision.org"
    url      = "https://github.com/BVLC/caffe/archive/rc5.tar.gz"

    version('rc5', '692bd3580b7576485cde6b1e03eb5a6d')

    variant('gpu', default=False,
            description='Builds with support for GPUs via CUDA and cuDNN')
    variant('opencv', default=True,
            description='Build with OpenCV support')
    variant('leveldb', default=True,
            description="Build with levelDB")
    variant('lmdb', default=True,
            description="Build with lmdb")
    variant('python', default=False,
            description='Build python wrapper and caffe python layer')
    variant('matlab', default=False,
            description='Build Matlab wrapper')

    depends_on('boost')
    depends_on('boost +python', when='+python')
    depends_on('cuda', when='+gpu')
    depends_on('blas')
    depends_on('protobuf')
    depends_on('glog')
    depends_on('gflags')
    depends_on('hdf5')

    # Optional dependencies
    depends_on('opencv@3.2.0', when='+opencv')
    depends_on('leveldb', when='+leveldb')
    depends_on('lmdb', when='+lmdb')
    depends_on('python@2.7:', when='+python')
    depends_on('py-numpy@1.7:', when='+python', type=('build', 'run'))
    depends_on('matlab', when='+matlab')

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec
        args = ['-DBLAS={0}'.format(spec['blas'].name),
                '-DCPU_ONLY=%s' % ('~gpu' in spec),
                '-DUSE_CUDNN=%s' % ('+gpu' in spec),
                '-DBUILD_python=%s' % ('+python' in spec),
                '-DBUILD_python_layer=%s' % ('+python' in spec),
                '-DBUILD_matlab=%s' % ('+matlab' in spec),
                '-DUSE_OPENCV=%s' % ('+opencv' in spec),
                '-DUSE_LEVELDB=%s' % ('+leveldb' in spec),
                '-DUSE_LMDB=%s' % ('+lmdb' in spec)]

        return args
