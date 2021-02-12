# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gearshifft(CMakePackage):
    """Benchmark Suite for Heterogenuous FFT Implementations"""

    homepage = "https://github.com/mpicbg-scicomp/gearshifft"
    url      = "https://github.com/mpicbg-scicomp/gearshifft/archive/v0.2.1-lw.tar.gz"

    maintainers = ['ax3l']

    version('0.4.0', sha256='15b9e4bfa1d9b4fe4ae316f289c67b7be0774cdada5bd7310df4d0e026d9d227')
    version('0.3.0', sha256='254332ef99819d3b21e3cb4fc4c5b0ff1937fc43110dcc7763c7b2b4caa91ec1')
    version('0.2.1-lw', sha256='04ba7401615ab29a37089c0dce8580270c0c4aa1ba328c9d438d6e4f163899c5')

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
