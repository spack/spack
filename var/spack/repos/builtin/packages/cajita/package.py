# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cajita(CMakePackage):
    """An MPI+Kokkos library for logically rectilinear grids"""

    homepage = "https://github.com/ECP-copa/Cajita"
    git      = "https://github.com/ECP-copa/Cajita.git"

    version('master', branch='master')
    version('0.1', tag='0.1.0')

    variant('shared', default=True, description='Build shared libraries')

    depends_on('mpi')
    depends_on('kokkos@3.0:')

    def cmake_args(self):
        options = [
            '-DBUILD_SHARED_LIBS=%s' % (
                'On' if '+shared'  in self.spec else 'Off')
        ]

        return options
