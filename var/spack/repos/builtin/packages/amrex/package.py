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
    url      = "https://github.com/AMReX-Codes/amrex/archive/20.01.tar.gz"
    git      = "https://github.com/AMReX-Codes/amrex.git"

    maintainers = ['mic84', 'asalmgren']

    version('develop', branch='development')
    version('20.03', sha256='a535dcc016f0d38b55d0ab8e9067c1c53e3686961f6a1fb471cb18a0ebc909e6')
    version('20.02', sha256='33529a23694283d12eb37d4682aa86c9cc1240bd50124efcf4464747a7554147')
    version('20.01', sha256='f7026d267ca5de79ec7e740264d54230f419776d40feae705e939be0b1d8e0d3')
    version('19.10', commit='52844b32b7da11e9733b9a7f4a782e51de7f5e1e')  # tag:19.10
    version('19.08', commit='bdd1146139e8727a513d451075f900c172eb81fd')  # tag:19.08
    version('18.10.1', commit='260b53169badaa760b91dfc60ea6b2ea3d9ccf06')  # tag:18.10.1
    version('18.10', commit='d37a266c38092e1174096e245326e9eead1f4e03')  # tag:18.10
    version('18.09.1', commit='88120db4736c325a2d3d2c291adacaffd3bf224b')  # tag:18.09.1

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
    depends_on('python@2.7:', type='build')
    depends_on('cmake@3.5:',  type='build', when='@:18.10.99')
    depends_on('cmake@3.13:',  type='build', when='@18.11:')
    conflicts('%clang')

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
