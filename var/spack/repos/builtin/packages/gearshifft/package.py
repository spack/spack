# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gearshifft(CMakePackage):
    """Benchmark Suite for Heterogenuous FFT Implementations"""

    homepage = "https://github.com/mpicbg-scicomp/gearshifft"
    url      = "https://github.com/mpicbg-scicomp/gearshifft/archive/v0.2.1-lw.tar.gz"

    maintainers = ['ax3l']

    version('0.2.1-lw', 'c3208b767b24255b488a83e5d9e517ea')

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

    # depends_on C++14 compiler, e.g. GCC 5.0+
    depends_on('cmake@2.8.0:', type='build')
    depends_on('boost@1.56.0:')
    depends_on('cuda@8.0:', when='+cufft')
    depends_on('opencl@1.2:', when='+clfft')
    depends_on('clfft@2.12.0:', when='+clfft')
    depends_on('fftw@3.3.4:~mpi~openmp', when='+fftw~openmp')
    depends_on('fftw@3.3.4:~mpi+openmp', when='+fftw+openmp')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DGEARSHIFFT_HCFFT:BOOL=OFF',
            '-DGEARSHIFFT_FFTW_PTHREADS:BOOL=ON',
            '-DGEARSHIFFT_CLFFT:BOOL=OFF'
        ]
        args.extend([
            '-DGEARSHIFFT_FFTW:BOOL={0}'.format(
                'ON' if '+fftw' in spec else 'OFF'),
            '-DGEARSHIFFT_FFTW_OPENMP:BOOL={0}'.format(
                'ON' if '+openmp' in spec else 'OFF'),
            '-DGEARSHIFFT_CUFFT:BOOL={0}'.format(
                'ON' if '+cufft' in spec else 'OFF'),
            '-DGEARSHIFFT_CLFFT:BOOL={0}'.format(
                'ON' if '+clfft' in spec else 'OFF')
        ])
        return args
