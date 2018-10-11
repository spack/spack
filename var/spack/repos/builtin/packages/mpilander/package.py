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


class Mpilander(CMakePackage):
    """There can only be one (MPI process)!"""

    homepage = "https://github.com/MPILander/MPILander"
    git      = "https://github.com/MPILander/MPILander.git"

    maintainers = ['ax3l']

    version('develop', branch='master')

    # variant('cuda', default=False, description='Enable CUDA support')
    # variant(
    #     'schedulers',
    #     description='List of supported schedulers',
    #     values=('alps', 'lsf', 'tm', 'slurm', 'sge', 'loadleveler'),
    #     multi=True
    # )

    depends_on('cmake@3.9.2:', type='build')

    provides('mpi@:3.1')

    # compiler support
    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.8')
    conflicts('%intel@:16')

    def cmake_args(self):
        args = [
            # tests and examples
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
            '-DBUILD_EXAMPLES:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
        ]

        return args
