##############################################################################
# Copyright (c) 2018 Mark Olesen, OpenCFD Ltd.
#
# This file was authored by Mark Olesen <mark.olesen@esi-group.com>
# and is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for the LLNL notice and LGPL.
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


class Precice(CMakePackage):
    """preCICE (Precise Code Interaction Coupling Environment) is a
    coupling library for partitioned multi-physics simulations.
    Partitioned means that preCICE couples existing programs (solvers)
    capable of simulating a subpart of the complete physics involved in
    a simulation."""

    homepage = 'https://www.precice.org'
    git      = 'https://github.com/precice/precice.git'

    # Skip version 1.1.1 entirely, the cmake was lacking install.
    version('develop', branch='develop')

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
    depends_on('boost@1.60.0:')
    depends_on('eigen@3.2:')
    # Implicit via eigen, don't over-constrain: depends_on('libxml2')
    depends_on('mpi', when='+mpi')
    depends_on('petsc', when='+petsc')
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
