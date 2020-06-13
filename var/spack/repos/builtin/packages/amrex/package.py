# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Amrex(CMakePackage):
    """AMReX is a publicly available software framework designed
    for building massively parallel block- structured adaptive
    mesh refinement (AMR) applications."""

    homepage = "https://amrex-codes.github.io/amrex/"
    url      = "https://github.com/AMReX-Codes/amrex/releases/download/20.05/amrex-20.05.tar.gz"
    git      = "https://github.com/AMReX-Codes/amrex.git"

    maintainers = ['mic84', 'asalmgren']

    version('develop', branch='development')
    version('20.06', sha256='be2f2a5107111fcb8b3928b76024b370c7cb01a9e5dd79484cf7fcf59d0b4858')
    version('20.05', sha256='97d753bb75e845a0a959ec1a044a48e6adb86dd008b5e29ce7a01d49ed276338')
    version('20.04', sha256='a7ece54d5d89cc00fd555551902a0d4d0fb50db15d2600f441353eed0dddd83b')
    version('20.03', sha256='9728f20c0d7297c935fe5cbc63c1ee60f983b833a735c797340ee2765d626165')
    version('20.02', sha256='2eda858b43e7455718ccb96c18f678da1778ec61031e90effdcb9c3e7e6f9bb5')
    version('20.01', sha256='957e7a7fe90a0a9f4ae10bf9e46dba68d72448d0bec69a4a4e66a544930caca3')
    version('19.10', sha256='9f30a2b3ec13711dfc6a1b59af59bd7df78449b5846ac6457b5dbbdecb20c576')
    version('19.08', sha256='94b1e9a9dcfb8c5b52aef91a2ed373aef504d766dd7d0aba6731ceb94e48e940')
    version('18.10.1', sha256='e648465c9c3b7ff4c696dfa8b6d079b4f61c80d96c51e27af210951c9367c201')
    version('18.10', sha256='298eba03ef03d617c346079433af1089d38076d6fab2c34476c687740c1f4234')
    version('18.09.1', sha256='a065ee4d1d98324b6c492ae20ea63ba12a4a4e23432bf5b3fe9788d44aa4398e')

    # Config options
    variant('dimensions', default='3',
            description='Dimensionality', values=('2', '3'))
    variant('shared',  default=False,
            description='Build shared library')
    variant('mpi',          default=True,
            description='Build with MPI support')
    variant('openmp',       default=False,
            description='Build with OpenMP support')
    variant('precision',  default='double',
            description='Real precision (double/single)',
            values=('single', 'double'))
    variant('eb',  default=False,
            description='Build Embedded Boundary classes')
    variant('fortran',  default=False,
            description='Build Fortran API')
    variant('linear_solvers', default=True,
            description='Build linear solvers')
    variant('amrdata',    default=False,
            description='Build data services')
    variant('particles',  default=False,
            description='Build particle classes')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('sundials', default=False,
            description='Build AMReX with SUNDIALS support')

    # Build dependencies
    depends_on('mpi', when='+mpi')
    depends_on('sundials@4.0.0:4.1.0 +ARKODE +CVODE', when='@19.08: +sundials')
    depends_on('python@2.7:', type='build', when='@:20.04')
    depends_on('cmake@3.5:',  type='build', when='@:18.10.99')
    depends_on('cmake@3.13:', type='build', when='@18.11:')
    depends_on('cmake@3.14:', type='build', when='@19.04:')
    conflicts('%clang')

    def url_for_version(self, version):
        if version >= Version('20.05'):
            url = "https://github.com/AMReX-Codes/amrex/releases/download/{0}/amrex-{0}.tar.gz"
        else:
            url = "https://github.com/AMReX-Codes/amrex/archive/{0}.tar.gz"
        return url.format(version.dotted)

    def cmake_is_on(self, option):
        return 'ON' if option in self.spec else 'OFF'

    def cmake_args(self):
        args = [
            '-DUSE_XSDK_DEFAULTS=ON',
            '-DDIM:STRING=%s' % self.spec.variants['dimensions'].value,
            '-DBUILD_SHARED_LIBS:BOOL=%s' % self.cmake_is_on('+shared'),
            '-DENABLE_MPI:BOOL=%s' % self.cmake_is_on('+mpi'),
            '-DENABLE_OMP:BOOL=%s' % self.cmake_is_on('+openmp'),
            '-DXSDK_PRECISION:STRING=%s' %
            self.spec.variants['precision'].value.upper(),
            '-DENABLE_EB:BOOL=%s' % self.cmake_is_on('+eb'),
            '-DXSDK_ENABLE_Fortran:BOOL=%s' % self.cmake_is_on('+fortran'),
            '-DENABLE_LINEAR_SOLVERS:BOOL=%s' %
            self.cmake_is_on('+linear_solvers'),
            '-DENABLE_AMRDATA:BOOL=%s' % self.cmake_is_on('+amrdata'),
            '-DENABLE_PARTICLES:BOOL=%s' % self.cmake_is_on('+particles'),
            '-DENABLE_SUNDIALS:BOOL=%s' % self.cmake_is_on('+sundials')
        ]
        if self.spec.satisfies('%fj'):
            args.append('-DCMAKE_Fortran_MODDIR_FLAG=-M')

        return args
