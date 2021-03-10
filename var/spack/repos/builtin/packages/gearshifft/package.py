# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gearshifft(CMakePackage):
    """Benchmark Suite for Heterogenuous FFT Implementations"""

    homepage = "https://github.com/mpicbg-scicomp/gearshifft"
    url      = "https://github.com/mpicbg-scicomp/gearshifft/archive/v0.2.1-lw.tar.gz"

    maintainers = ['zyzzyxdonta']

    version('0.4.0', sha256='15b9e4bfa1d9b4fe4ae316f289c67b7be0774cdada5bd7310df4d0e026d9d227')

    # gearshifft used the variable name `CMAKE_DEFAULT_BUILD_TYPE` which was
    # later introduced by CMake leading to an error in newer CMake versions.
    # This patch renames the variable to `GEARSHIFFT_DEFAULT_BUILD_TYPE`.
    patch('gearshifft-v0.4.0-cmake-variable-name.patch', when='@0.4.0')

    variant('cufft', default=True,
            description='Compile gearshifft_cufft')
    variant('clfft', default=True,
            description='Compile gearshifft_clfft')
    variant('fftw', default=True,
            description='Compile gearshifft_fftw')
    variant('openmp', default=True,
            description='use OpenMP parallel fftw libraries')
    # variant('hcfft', default=True,
    #         description='Not implemented yet')
    variant('mkl', default=True,
            description='Compile gearshifft_fftwwrappers')
    variant('rocfft', default=True,
            description='Compile gearshifft_rocfft')

    # depends_on C++14 compiler, e.g. GCC 5.0+
    depends_on('cmake@2.8.0:', type='build')
    depends_on('boost@1.59.0:')
    depends_on('cuda@8.0:', when='+cufft')
    depends_on('opencl@1.2:', when='+clfft')
    depends_on('clfft@2.12.0:', when='+clfft')
    depends_on('fftw@3.3.4:~mpi~openmp', when='+fftw~openmp')
    depends_on('fftw@3.3.4:~mpi+openmp', when='+fftw+openmp')
    depends_on('intel-mkl threads=openmp', when='+mkl')
    depends_on('rocfft', when='+rocfft')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DGEARSHIFFT_FLOAT16_SUPPORT:BOOL=OFF',
            '-DGEARSHIFFT_BACKEND_HCFFT:BOOL=OFF',
        ]
        args.extend([
            '-DGEARSHIFFT_BACKEND_FFTW:BOOL={0}'.format(
                'ON' if '+fftw' in spec else 'OFF'),
            '-DGEARSHIFFT_BACKEND_FFTW_PTHREADS:BOOL={0}'.format(
                'ON' if '~openmp' in spec else 'OFF'),
            '-DGEARSHIFFT_BACKEND_FFTW_OPENMP:BOOL={0}'.format(
                'ON' if '+openmp' in spec else 'OFF'),
            '-DGEARSHIFFT_BACKEND_CUFFT:BOOL={0}'.format(
                'ON' if '+cufft' in spec else 'OFF'),
            '-DGEARSHIFFT_BACKEND_CLFFT:BOOL={0}'.format(
                'ON' if '+clfft' in spec else 'OFF'),
            '-DGEARSHIFFT_BACKEND_FFTWWRAPPERS:BOOL={0}'.format(
                'ON' if '+mkl' in spec else 'OFF'),
            '-DGEARSHIFFT_BACKEND_ROCFFT:BOOL={0}'.format(
                'ON' if '+rocfft' in spec else 'OFF')
        ])
        return args
