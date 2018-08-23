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
import sys


class Veclibfort(Package):
    """Lightweight but flexible shim designed to rectify the incompatibilities
    between the Accelerate/vecLib BLAS and LAPACK libraries shipped with macOS
    and FORTRAN code compiled with modern compilers such as GNU Fortran."""

    homepage = "https://github.com/mcg1969/vecLibFort"
    url      = "https://github.com/mcg1969/vecLibFort/archive/0.4.2.tar.gz"
    git      = "https://github.com/mcg1969/vecLibFort.git"

    version('develop', branch='master')
    version('0.4.2', '83395ffcbe8a2122c3f726a5c3a7cf93')

    variant('shared', default=True,
            description="Build shared libraries as well as static libs.")

    # virtual dependency
    provides('blas')
    provides('lapack')

    @property
    def libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libvecLibFort', root=self.prefix, shared=shared, recursive=True
        )

    def install(self, spec, prefix):
        if sys.platform != 'darwin':
            raise InstallError('vecLibFort can be installed on macOS only')

        filter_file(r'^PREFIX=.*', '', 'Makefile')

        make_args = []

        if spec.satisfies('%gcc@6:'):
            make_args += ['CFLAGS=-flax-vector-conversions']

        make_args += ['PREFIX=%s' % prefix, 'install']

        make(*make_args)

        # test
        fc = which('fc')
        flags = ['-o', 'tester', '-O', 'tester.f90']
        flags.extend(spec['veclibfort'].libs.ld_flags.split())
        fc(*flags)
        Executable('./tester')()
