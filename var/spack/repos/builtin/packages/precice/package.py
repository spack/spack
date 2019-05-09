# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Precice(CMakePackage):
    """preCICE (Precise Code Interaction Coupling Environment) is a
    coupling library for partitioned multi-physics simulations.
    Partitioned means that preCICE couples existing programs (solvers)
    capable of simulating a subpart of the complete physics involved in
    a simulation."""

    homepage = 'https://www.precice.org'
    git      = 'https://github.com/precice/precice.git'
    url      = 'https://github.com/precice/precice/archive/v1.2.0.tar.gz'
    maintainers = ['fsimonis', 'MakisH']

    version('develop', branch='develop')
    version('1.4.1', sha256='dde4882edde17882340f9f601941d110d5976340bd71af54c6e6ea22ae56f1a5')
    version('1.4.0', sha256='3499bfc0941fb9f004d5e32eb63d64f93e17b4057fab3ada1cde40c8311bd466')
    version('1.3.0', sha256='610322ba1b03df8e8f7d060d57a6a5afeabd5db4e8c4a638d04ba4060a3aec96')
    version('1.2.0', sha256='0784ecd002092949835151b90393beb6e9e7a3e9bd78ffd40d18302d6da4b05b')
    # Skip version 1.1.1 entirely, the cmake was lacking install.

    variant('mpi', default=True, description='Enable MPI support')
    variant('petsc', default=False, description='Enable PETSc support')
    variant('python', default=False, description='Enable Python support')
    variant('shared', default=True, description='Build shared libraries')

    # Not yet
#    variant(
#        'float', default=False,
#        description='Use single precision for field data exchange')
#    variant(
#        'int64',
#        default=False, description='Use 64-bit integers for indices')

    depends_on('cmake@3.5:', type='build')
    depends_on('cmake@3.9.6:', type='build', when='@1.4:')
    depends_on('boost@1.60.0:')
    depends_on('boost@1.65.1:', when='@1.4:')
    depends_on('eigen@3.2:')
    depends_on('libxml2')
    depends_on('mpi', when='+mpi')
    depends_on('petsc@3.6:', when='+petsc')
    depends_on('python@2.7', when='+python', type=('build', 'run'))

    def cmake_args(self):
        """Populate cmake arguments for precice."""
        spec = self.spec

        def variant_bool(feature, on='ON', off='OFF'):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off

        cmake_args = [
            '-DMPI:BOOL=%s' % variant_bool('+mpi'),
            '-DPETSC:BOOL=%s' % variant_bool('+petsc'),
            '-DPYTHON:BOOL=%s' % variant_bool('+python'),
            '-DBUILD_SHARED_LIBS:BOOL=%s' % variant_bool('+shared'),
        ]
        return cmake_args
