# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from spack import *


class Lbann(CMakePackage):
    """LBANN: Livermore Big Artificial Neural Network Toolkit.  A distributed
    memory, HPC-optimized, model and data parallel training toolkit for deep
    neural networks."""

    homepage = "http://software.llnl.gov/lbann/"
    url      = "https://github.com/LLNL/lbann/archive/v0.91.tar.gz"
    git      = "https://github.com/LLNL/lbann.git"

    version('develop', branch='develop')
    version('0.96', sha256='97af78e9d3c405e963361d0db96ee5425ee0766fa52b43c75b8a5670d48e4b4a')
    version('0.95', sha256='d310b986948b5ee2bedec36383a7fe79403721c8dc2663a280676b4e431f83c2')
    version('0.94', sha256='567e99b488ebe6294933c98a212281bffd5220fc13a0a5cd8441f9a3761ceccf')
    version('0.93', '1913a25a53d4025fa04c16f14afdaa55')
    version('0.92', 'c0eb1595a7c74640e96f280beb497564')
    version('0.91', '83b0ec9cd0b7625d41dfb06d2abd4134')

    variant('gpu', default=False, description='Builds with support for GPUs via CUDA and cuDNN')
    variant('nccl', default=False, description='Builds with support for NCCL communication lib')
    variant('opencv', default=True, description='Builds with support for image processing routines with OpenCV')
    variant('seq_init', default=False, description='Force serial initialization of weight matrices.')
    variant('dtype', default='float',
            description='Type for floating point representation of weights',
            values=('float', 'double'))
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('al', default=False, description='Builds with support for Aluminum Library')
    variant('conduit', default=False, description='Builds with support for Conduit Library')
    variant('vtune', default=False, description='Builds with support for Intel VTune')

    # It seems that there is a need for one statement per version bounds
    depends_on('hydrogen +openmp_blas +shared +int64', when='@:0.90,0.95: ~al')
    depends_on('hydrogen +openmp_blas +shared +int64 +al', when='@:0.90,0.95: +al')

    depends_on('hydrogen +openmp_blas +shared +int64 build_type=Debug',
               when='build_type=Debug @:0.90,0.95: ~al')
    depends_on('hydrogen +openmp_blas +shared +int64 build_type=Debug +al',
               when='build_type=Debug @:0.90,0.95: +al')

    depends_on('hydrogen +openmp_blas +shared +int64 +cuda',
               when='+gpu @:0.90,0.95: ~al')
    depends_on('hydrogen +openmp_blas +shared +int64 +cuda +al',
               when='+gpu @:0.90,0.95: +al')

    depends_on('hydrogen +openmp_blas +shared +int64 +cuda build_type=Debug',
               when='build_type=Debug @:0.90,0.95: +gpu')
    depends_on('hydrogen +openmp_blas +shared +int64 +cuda build_type=Debug +al',
               when='build_type=Debug @:0.90,0.95: +gpu +al')

    # Older versions depended on Elemental not Hydrogen
    depends_on('elemental +openmp_blas +shared +int64', when='@0.91:0.94')
    depends_on('elemental +openmp_blas +shared +int64 build_type=Debug',
               when='build_type=Debug @0.91:0.94')

    depends_on('aluminum@master', when='@:0.90,0.95: +al ~gpu')
    depends_on('aluminum@master +gpu +mpi-cuda', when='@:0.90,0.95: +al +gpu ~nccl')
    depends_on('aluminum@master +gpu +nccl +mpi_cuda', when='@:0.90,0.95: +al +gpu +nccl')

    depends_on('cuda', when='+gpu')
    depends_on('cudnn', when='+gpu')
    depends_on('cub', when='+gpu')
    depends_on('mpi', when='~gpu')
    depends_on('mpi +cuda', when='+gpu')
    depends_on('hwloc')

    # LBANN wraps OpenCV calls in OpenMP parallel loops, build without OpenMP
    # Additionally disable video related options, they incorrectly link in a
    # bad OpenMP library when building with clang or Intel compilers
    depends_on('opencv@3.2.0: +core +highgui +imgproc +jpeg +png +tiff +zlib '
               '+fast-math +powerpc +vsx ~calib3d ~cuda ~dnn ~eigen'
               '~features2d ~flann ~gtk ~ipp ~ipp_iw ~jasper ~java ~lapack ~ml'
               '~openmp ~opencl ~opencl_svm ~openclamdblas ~openclamdfft'
               '~pthreads_pf ~python ~qt ~stitching ~superres ~ts ~video'
               '~videostab ~videoio ~vtk', when='+opencv')

    depends_on('protobuf@3.0.2: build_type=Release')
    depends_on('cnpy')
    depends_on('nccl', when='+gpu +nccl')

    depends_on('conduit@master +hdf5', when='+conduit')

    generator = 'Ninja'
    depends_on('ninja', type='build')

    @property
    def common_config_args(self):
        spec = self.spec
        # Environment variables
        cppflags = []
        cppflags.append('-DLBANN_SET_EL_RNG -ldl')

        return [
            '-DCMAKE_INSTALL_MESSAGE=LAZY',
            '-DCMAKE_CXX_FLAGS=%s' % ' '.join(cppflags),
            '-DLBANN_VERSION=spack',
            '-DCNPY_DIR={0}'.format(spec['cnpy'].prefix),
        ]

    # Get any recent versions or non-numeric version
    # Note that develop > numeric and non-develop < numeric
    @when('@:0.90,0.94:')
    def cmake_args(self):
        spec = self.spec
        args = self.common_config_args
        args.extend([
            '-DLBANN_WITH_TOPO_AWARE:BOOL=%s' % ('+gpu +nccl' in spec),
            '-DLBANN_WITH_ALUMINUM:BOOL=%s' % ('+al' in spec),
            '-DLBANN_WITH_CONDUIT:BOOL=%s' % ('+conduit' in spec),
            '-DLBANN_WITH_CUDA:BOOL=%s' % ('+gpu' in spec),
            '-DLBANN_WITH_CUDNN:BOOL=%s' % ('+gpu' in spec),
            '-DLBANN_WITH_NCCL:BOOL=%s' % ('+gpu +nccl' in spec),
            '-DLBANN_WITH_SOFTMAX_CUDA:BOOL=%s' % ('+gpu' in spec),
            '-DLBANN_SEQUENTIAL_INITIALIZATION:BOOL=%s' %
            ('+seq_init' in spec),
            '-DLBANN_WITH_TBINF=OFF',
            '-DLBANN_WITH_VTUNE:BOOL=%s' % ('+vtune' in spec),
            '-DLBANN_DATATYPE={0}'.format(spec.variants['dtype'].value),
            '-DLBANN_VERBOSE=0'])

        if self.spec.satisfies('@:0.90') or self.spec.satisfies('@0.95:'):
            args.extend([
                '-DHydrogen_DIR={0}/CMake/hydrogen'.format(
                    spec['hydrogen'].prefix)])
        elif self.spec.satisfies('@0.94'):
            args.extend([
                '-DElemental_DIR={0}/CMake/elemental'.format(
                    spec['elemental'].prefix)])

        if '+vtune' in spec:
            args.extend(['-DVTUNE_DIR={0}'.format(spec['vtune'].prefix)])

        if '+al' in spec:
            args.extend(['-DAluminum_DIR={0}'.format(spec['aluminum'].prefix)])

        if '+conduit' in spec:
            args.extend(['-DLBANN_CONDUIT_DIR={0}'.format(
                spec['conduit'].prefix)])

        # Add support for OpenMP
        if (self.spec.satisfies('%clang')):
            if (sys.platform == 'darwin'):
                clang = self.compiler.cc
                clang_bin = os.path.dirname(clang)
                clang_root = os.path.dirname(clang_bin)
                args.extend([
                    '-DOpenMP_CXX_FLAGS=-fopenmp=libomp',
                    '-DOpenMP_CXX_LIB_NAMES=libomp',
                    '-DOpenMP_libomp_LIBRARY={0}/lib/libomp.dylib'.format(
                        clang_root)])

        if '+opencv' in spec:
            args.extend(['-DOpenCV_DIR:STRING={0}'.format(
                spec['opencv'].prefix)])

        if '+gpu' in spec:
            args.extend([
                '-DCUDA_TOOLKIT_ROOT_DIR={0}'.format(
                    spec['cuda'].prefix)])
            args.extend([
                '-DcuDNN_DIR={0}'.format(
                    spec['cudnn'].prefix)])
            args.extend(['-DCUB_DIR={0}'.format(
                spec['cub'].prefix)])
            if '+nccl' in spec:
                args.extend([
                    '-DNCCL_DIR={0}'.format(
                        spec['nccl'].prefix)])

        return args

    @when('@0.91:0.93')
    def cmake_args(self):
        spec = self.spec
        args = self.common_config_args
        args.extend([
            '-DWITH_CUDA:BOOL=%s' % ('+gpu' in spec),
            '-DWITH_CUDNN:BOOL=%s' % ('+gpu' in spec),
            '-DELEMENTAL_USE_CUBLAS:BOOL=%s' % (
                '+cublas' in spec['elemental']),
            '-DWITH_TBINF=OFF',
            '-DWITH_VTUNE=OFF',
            '-DElemental_DIR={0}'.format(spec['elemental'].prefix),
            '-DELEMENTAL_MATH_LIBS={0}'.format(
                spec['elemental'].libs),
            '-DSEQ_INIT:BOOL=%s' % ('+seq_init' in spec),
            '-DVERBOSE=0',
            '-DLBANN_HOME=.'])

        if spec.variants['dtype'].value == 'float':
            args.extend(['-DDATATYPE=4'])
        elif spec.variants['dtype'].value == 'double':
            args.extend(['-DDATATYPE=8'])

        if '+opencv' in spec:
            args.extend(['-DOpenCV_DIR:STRING={0}'.format(
                spec['opencv'].prefix)])

        if '+cudnn' in spec:
            args.extend(['-DcuDNN_DIR={0}'.format(
                spec['cudnn'].prefix)])

        if '+cub' in spec:
            args.extend(['-DCUB_DIR={0}'.format(
                spec['cub'].prefix)])

        return args
