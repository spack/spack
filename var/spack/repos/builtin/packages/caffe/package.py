# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Caffe(CMakePackage):
    """Caffe is a deep learning framework made with expression, speed, and
       modularity in mind. It is developed by the Berkeley Vision and Learning
       Center (BVLC) and by community contributors."""

    homepage = "http://caffe.berkeleyvision.org"
    url      = "https://github.com/BVLC/caffe/archive/1.0.tar.gz"

    version('1.0', '5fbb0e32e7cd8de3de46e6fe6e4cd2b5')
    version('rc5', '692bd3580b7576485cde6b1e03eb5a6d')
    version('rc4', 'd86eeb38b1400097d32ffcabdec75b55')
    version('rc3', '84e39223115753b48312a8bf48c31f59')
    version('rc2', 'c331932e34b5e2f5022fcc34c419080f')

    variant('cuda', default=False,
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
    depends_on('cuda', when='+cuda')
    depends_on('blas')
    depends_on('protobuf')
    depends_on('glog')
    depends_on('gflags')
    depends_on('hdf5')

    # Optional dependencies
    depends_on('opencv@3.2.0+core+highgui+imgproc', when='+opencv')
    depends_on('leveldb', when='+leveldb')
    depends_on('lmdb', when='+lmdb')
    depends_on('python@2.7:', when='+python')
    depends_on('py-numpy@1.7:', when='+python', type=('build', 'run'))
    depends_on('matlab', when='+matlab')

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec
        args = ['-DBLAS={0}'.format('open' if spec['blas'].name == 'openblas'
                else spec['blas'].name),
                '-DCPU_ONLY=%s' % ('~cuda' in spec),
                '-DUSE_CUDNN=%s' % ('+cuda' in spec),
                '-DBUILD_python=%s' % ('+python' in spec),
                '-DBUILD_python_layer=%s' % ('+python' in spec),
                '-DBUILD_matlab=%s' % ('+matlab' in spec),
                '-DUSE_OPENCV=%s' % ('+opencv' in spec),
                '-DUSE_LEVELDB=%s' % ('+leveldb' in spec),
                '-DUSE_LMDB=%s' % ('+lmdb' in spec),
                '-DGFLAGS_ROOT_DIR=%s' % spec['gflags'].prefix,
                '-DGLOG_ROOT_DIR=%s' % spec['glog'].prefix,
                ]

        if spec.satisfies('^openblas'):
            env['OpenBLAS_HOME'] = spec['openblas'].prefix

        if spec.satisfies('+lmdb'):
            env['LMDB_DIR'] = spec['lmdb'].prefix

        if spec.satisfies('+leveldb'):
            env['LEVELDB_ROOT'] = spec['leveldb'].prefix

        if spec.satisfies('+python'):
            version = spec['python'].version.up_to(1)
            args.append('-Dpython_version=%s' % version)

        return args
