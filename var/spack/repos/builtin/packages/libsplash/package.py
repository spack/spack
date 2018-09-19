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


class Libsplash(CMakePackage):
    """libSplash aims at developing a HDF5-based I/O library for HPC
    simulations. It is created as an easy-to-use frontend for the standard HDF5
    library with support for MPI processes in a cluster environment. While the
    standard HDF5 library provides detailed low-level control, libSplash
    simplifies tasks commonly found in large-scale HPC simulations, such as
    iterative computations and MPI distributed processes.
    """

    homepage = "https://github.com/ComputationalRadiationPhysics/libSplash"
    url      = "https://github.com/ComputationalRadiationPhysics/libSplash/archive/v1.4.0.tar.gz"
    git      = "https://github.com/ComputationalRadiationPhysics/libSplash.git"
    maintainers = ['ax3l']

    version('develop', branch='dev')
    version('master', branch='master')
    version('1.7.0', '22dea94734fe4f4c5f4e875ce70900d3')
    version('1.6.0', 'c05bce95abfe1ae4cd9d9817acf58d94')
    version('1.5.0', 'c1efec4c20334242c8a3b6bfdc0207e3')
    version('1.4.0', '2de37bcef6fafa1960391bf44b1b50e0')
    version('1.3.1', '524580ba088d97253d03b4611772f37c')
    version('1.2.4', '3fccb314293d22966beb7afd83b746d0')

    variant('mpi', default=True,
            description='Enable parallel I/O (one-file aggregation) support')

    depends_on('cmake@3.10.0:', type='build', when='@1.7.0:')
    depends_on('hdf5@1.8.6: ~mpi', when='~mpi')
    depends_on('hdf5@1.8.6: +mpi', when='+mpi')
    depends_on('mpi', when='+mpi')

    patch('root_cmake_1.7.0.patch', when='@1.7.0')

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('@1.7.0:'):
            args += [
                '-DSplash_USE_MPI:BOOL={0}'.format(
                    'ON' if '+mpi' in spec else 'OFF'),
                '-DSplash_USE_PARALLEL:BOOL={0}'.format(
                    'ON' if '+mpi' in spec else 'OFF')
            ]

        return args
