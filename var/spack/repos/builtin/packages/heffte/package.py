# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Heffte(CMakePackage):
    """Highly Efficient FFT for Exascale"""

    homepage = "https://bitbucket.org/icl/heffte"
    url      = "https://bitbucket.org/icl/heffte/get/v1.0.tar.gz"
    git      = "https://bitbucket.org/icl/heffte.git"

    maintainers = ['mkstoyanov']

    version('develop', branch='master')
    version('1.0', sha256='0902479fb5b1bad01438ca0a72efd577a3529c3d8bad0028f3c18d3a4935ca74')
    version('0.2', sha256='4e76ae60982b316c2e873b2e5735669b22620fefa1fc82f325cdb6989bec78d1')
    version('0.1', sha256='d279a03298d2dc76574b1ae1031acb4ea964348cf359273d1afa4668b5bfe748')

    patch('threads10.patch', when='@1.0')

    variant('shared', default=True, description='Builds with shared libraries')
    variant('fftw', default=False, description='Builds with support for FFTW backend')
    variant('mkl',  default=False, description='Builds with support for MKL backend')
    variant('cuda', default=False, description='Builds with support for GPUs via CUDA')

    conflicts('~fftw', when='~mkl~cuda')  # requires at least one backend
    conflicts('+fftw', when='+mkl')  # old API supports at most one CPU backend
    conflicts('openmpi~cuda', when='+cuda')  # +cuda requires CUDA enabled OpenMPI

    depends_on('mpi', type=('build', 'run'))

    depends_on('fftw@3.3.8:', when="+fftw", type=('build', 'run'))
    depends_on('intel@16.0:', when="+mkl", type=('build', 'run'))
    depends_on('cuda@8.0:', when="+cuda", type=('build', 'run'))

    def cmake_args(self):
        return [
            '-DBUILD_SHARED_LIBS={0:1s}'.format(
                'ON' if '+shared' in self.spec else 'OFF'),
            '-DBUILD_GPU={0:1s}'.format(
                'ON' if ('+cuda' in self.spec and
                         '+fftw' in self.spec) else 'OFF'),
            '-DHeffte_ENABLE_CUDA={0:1s}'.format(
                'ON' if '+cuda' in self.spec else 'OFF'),
            '-DHeffte_ENABLE_FFTW={0:1s}'.format(
                'ON' if '+fftw' in self.spec else 'OFF'),
            '-DHeffte_ENABLE_MKL={0:1s}'.format(
                'ON' if '+mkl' in self.spec else 'OFF'), ]
