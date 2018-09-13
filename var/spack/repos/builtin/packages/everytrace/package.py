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


class Everytrace(CMakePackage):
    """Get stack trace EVERY time a program exits."""

    homepage = "https://github.com/citibeth/everytrace"
    url      = "https://github.com/citibeth/everytrace/archive/0.2.2.tar.gz"
    git      = "https://github.com/citibeth/everytrace.git"

    maintainers = ['citibeth']

    version('develop', branch='develop')
    version('0.2.2', 'dd60b8bf68cbf3dc2be305a040f2fe3e')

    variant('mpi', default=True, description='Enables MPI parallelism')
    variant('fortran', default=True,
            description='Enable use with Fortran programs')
    variant('cxx', default=True, description='Enable C++ Exception-based features')

    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DUSE_MPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
            '-DUSE_FORTRAN=%s' % ('YES' if '+fortran' in spec else 'NO'),
            '-DUSE_CXX=%s' % ('YES' if '+cxx' in spec else 'NO')]

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', join_path(self.prefix, 'bin'))
