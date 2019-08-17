# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tasmanian(CMakePackage):
    """The Toolkit for Adaptive Stochastic Modeling and Non-Intrusive
    ApproximatioN is a robust library for high dimensional integration and
    interpolation as well as parameter calibration."""

    homepage = 'http://tasmanian.ornl.gov'
    url      = 'https://github.com/ORNL/TASMANIAN/archive/v6.0.tar.gz'
    git      = 'https://github.com/ORNL/TASMANIAN.git'

    maintainers = ['mkstoyanov']

    version('develop', branch='master')

    version('6.0', '43dcb1d2bcb2f2c829ad046d0e91e83d')  # use for xsdk-0.4.0
    version('5.1', '5d904029a24470a6acf4a87d3339846e')

    version('5.0', '4bf131841d786033863d271739be0f7a',
            url='http://tasmanian.ornl.gov/documents/Tasmanian_v5.0.zip')

    variant('xsdkflags', default=False,
            description='enable XSDK defaults for Tasmanian')

    variant('openmp', default=True,
            description='add OpenMP support to Tasmanian')
    # tested with OpenMP 3.1 (clang4) through 4.0-4.5 (gcc 5 - 8)

    variant('blas', default=False,
            description='add BLAS support to Tasmanian')

    variant('mpi', default=False,
            description='add MPI support to Tasmanian')

    variant('cuda', default=False,
            description='add CUDA support to Tasmanian')

    variant('magma', default=False,
            description='add UTK MAGMA support to Tasmanian')

    variant('python', default=False,
            description='add Python binding for Tasmanian')

    variant('fortran', default=False,
            description='add Fortran 90/95 interface to Tasmanian')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release'))

    depends_on('cmake@3.5.1:', type='build')

    depends_on('python@2.7:', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))

    extends('python', when='+python', type=('build', 'run'))

    depends_on('mpi', when="+mpi", type=('build', 'run'))  # openmpi 2 and 3 tested

    depends_on('blas', when="+blas", type=('build', 'run'))  # openblas 0.2.18 or newer

    depends_on('cuda@8.0.61:', when='+cuda', type=('build', 'run'))
    depends_on('cuda@8.0.61:', when='+magma', type=('build', 'run'))

    depends_on('magma@2.4.0:', when='+magma', type=('build', 'run'))

    conflicts('-cuda', when='+magma')  # currently MAGMA only works with CUDA

    # old versions
    conflicts('+magma', when='@:5.1')  # magma does not work prior to 6.0
    conflicts('+mpi', when='@:5.1')    # MPI is broken prior to 6.0
    conflicts('+xsdkflags', when='@:5.1')  # 6.0 is the first version included in xSDK

    def cmake_args(self):
        spec = self.spec

        if '+xsdkflags' in spec:
            args = [
                '-DUSE_XSDK_DEFAULTS:BOOL=ON',
                '-DXSDK_ENABLE_PYTHON:BOOL={0}'.format(
                    'ON' if '+python' in spec else 'OFF'),
                '-DTasmanian_ENABLE_MPI:BOOL={0}'.format(
                    'ON' if '+mpi' in spec else 'OFF'),
                '-DXSDK_ENABLE_OPENMP:BOOL={0}'.format(
                    'ON' if '+openmp' in spec else 'OFF'),
                '-DTPL_ENABLE_BLAS:BOOL={0}'.format(
                    'ON' if '+blas' in spec else 'OFF'),
                '-DXSDK_ENABLE_CUDA:BOOL={0}'.format(
                    'ON' if '+cuda' in spec else 'OFF'),
                '-DTPL_ENABLE_MAGMA:BOOL={0}'.format(
                    'ON' if '+magma' in spec else 'OFF'),
                '-DXSDK_ENABLE_FORTRAN:BOOL={0}'.format(
                    'ON' if '+fortran' in spec else 'OFF'), ]
        else:
            args = [
                '-DTasmanian_ENABLE_OPENMP:BOOL={0}'.format(
                    'ON' if '+openmp' in spec else 'OFF'),
                '-DTasmanian_ENABLE_BLAS:BOOL={0}'.format(
                    'ON' if '+blas' in spec else 'OFF'),
                '-DTasmanian_ENABLE_PYTHON:BOOL={0}'.format(
                    'ON' if '+python' in spec else 'OFF'),
                '-DTasmanian_ENABLE_MPI:BOOL={0}'.format(
                    'ON' if '+mpi' in spec else 'OFF'),
                '-DTasmanian_ENABLE_CUDA:BOOL={0}'.format(
                    'ON' if '+cuda' in spec else 'OFF'),
                '-DTasmanian_ENABLE_MAGMA:BOOL={0}'.format(
                    'ON' if '+magma' in spec else 'OFF'),
                '-DTasmanian_ENABLE_FORTRAN:BOOL={0}'.format(
                    'ON' if '+fortran' in spec else 'OFF'), ]

        if spec.satisfies('+python'):
            args.append('-DPYTHON_EXECUTABLE:FILEPATH={0}'.format(
                self.spec['python'].command.path))

        # _CUBLAS and _CUDA were separate options prior to 6.0
        # skipping _CUBLAS leads to peformance regression
        if spec.satisfies('@:5.1'):
            args.append('-DTasmanian_ENABLE_CUBLAS={0}'.format(
                        'ON' if '+cuda' in spec else 'OFF'))

        return args
