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
    variant('magma', default=False, description='Use helper methods from the UTK MAGMA library')

    conflicts('~fftw', when='~mkl~cuda')  # requires at least one backend
    conflicts('+fftw', when='+mkl@:1.0')  # old API supports at most one CPU backend
    conflicts('openmpi~cuda', when='+cuda')  # +cuda requires CUDA enabled OpenMPI
    conflicts('~cuda', when='+magma')  # magma requires CUDA or HIP
    conflicts('+magma', when="@:1.0")  # magma support was added post v1.0

    depends_on('mpi', type=('build', 'run'))

    depends_on('fftw@3.3.8:', when="+fftw", type=('build', 'run'))
    depends_on('intel@16.0:', when="+mkl", type=('build', 'run'))
    depends_on('cuda@8.0:', when="+cuda", type=('build', 'run'))
    depends_on('magma@2.5.3:', when="+cuda+magma", type=('build', 'run'))

    def cmake_args(self):
        return [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('Heffte_ENABLE_CUDA', 'cuda'),
            self.define_from_variant('Heffte_ENABLE_FFTW', 'fftw'),
            self.define_from_variant('Heffte_ENABLE_MKL', 'mkl'),
            self.define_from_variant('Heffte_ENABLE_MAGMA', 'magma'),
            '-DBUILD_GPU={0:1s}'.format(
                'ON' if ('+cuda' in self.spec and
                         '+fftw' in self.spec) else 'OFF'), ]
