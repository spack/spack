##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Pnmpi(CMakePackage):
    """PnMPI is a dynamic MPI tool infrastructure that builds on top of
       the standardized PMPI interface. """

    homepage = "https://github.com/LLNL/PnMPI"
    url      = "https://github.com/LLNL/PnMPI/releases/download/v1.7/PnMPI-v1.7-full.tar.gz"

    version('1.7', '8040c1558c0deaa3d964c35d1760f3a8')

    variant('fortran', default=False,
            description='Configure PnMPI with Fortran support')
    variant('tests', default=False,
            description='Build test cases and enable "test" makefile target')

    depends_on('cmake', type='build')
    depends_on('argp-standalone', when='platform=darwin')
    depends_on('binutils')
    depends_on('help2man')
    depends_on('doxygen')
    depends_on('mpi')

    @run_before('cmake')
    def check_fortran(self):
        is_no_fortran_compiler = not self.compiler.f77 and not self.compiler.fc
        if self.spec.satisfies('+fortran'):
            if is_no_fortran_compiler:
                raise InstallError('pnmpi+fortran requires Fortran compiler '
                                   'but no Fortran compiler found!')

    def cmake_args(self):
        args = []
        spec = self.spec
        on_off = {True: 'ON', False: 'OFF'}

        has_fortran = spec.satisfies('+fortran')
        has_tests = spec.satisfies('+tests')

        args.append('-DENABLE_FORTRAN:BOOL={0}'.format(on_off[has_fortran]))
        args.append('-DENABLE_TESTING:BOOL={0}'.format(on_off[has_tests]))
        return args
