##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Latte(CMakePackage):
    """Open source density functional tight binding molecular dynamics."""

    homepage = "https://github.com/lanl/latte"
    url      = "https://github.com/lanl/latte/tarball/v1.2.1"
    git      = "https://github.com/lanl/latte.git"

    tags = ['ecp', 'ecp-apps']

    version('develop', branch='master')
    version('1.2.1', '56db44afaba2a89e6ca62ac565c3c012')
    version('1.2.0', 'b9bf8f84a0e0cf7b0e278a1bc7751b3d')
    version('1.1.1', 'ab11867ba6235189681cf6e50a50cc50')
    version('1.0.1', 'd0b99edbcf7a19abe0a68a192d6f6234')

    variant('mpi', default=True,
            description='Build with mpi')
    variant('progress', default=False,
            description='Use progress for fast')
    variant('shared', default=True, description='Build shared libs')

    depends_on("cmake@3.1:", type='build')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('qmd-progress', when='+progress')

    root_cmakelists_dir = 'cmake'

    def cmake_args(self):
        options = []
        if '+shared' in self.spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')
        if '+mpi' in self.spec:
            options.append('-DO_MPI=yes')
        if '+progress' in self.spec:
            options.append('-DPROGRESS=yes')

        blas_list = ';'.join(self.spec['blas'].libs)
        lapack_list = ';'.join(self.spec['lapack'].libs)
        options.append('-DBLAS_LIBRARIES={0}'.format(blas_list))
        options.append('-DLAPACK_LIBRARIES={0}'.format(lapack_list))

        return options
