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
