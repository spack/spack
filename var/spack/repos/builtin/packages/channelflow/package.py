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


class Channelflow(CMakePackage):
    """Channelflow is a software system for numerical analysis of the
    incompressible fluid flow in channel geometries, written in C++.
    """

    homepage = 'https://github.com/epfl-ecps/channelflow'
    url = 'https://github.com/epfl-ecps/channelflow.git'

    version(
        'develop',
        git='https://github.com/epfl-ecps/channelflow.git',
        branch='master'
    )

    variant('shared', default=True, description='Build shared libs')
    variant('mpi', default=True, description='Enable MPI parallelism')
    variant('hdf5', default=True, description='Enable support for HDF5 I/O')
    variant(
        'netcdf', default='serial', values=('none', 'serial', 'parallel'),
        multi=False, description='Level of support for NetCDF I/O'
    )
    variant('python', default=False, description='Build python bindings')

    depends_on('eigen')
    depends_on('fftw')

    # MPI related constraints
    depends_on('mpi', when='+mpi')
    depends_on('fftw+mpi', when='+mpi')

    # Support for different I/O formats
    depends_on('hdf5+cxx', when='+hdf5')
    depends_on('netcdf', when='netcdf=serial')
    depends_on('netcdf+mpi', when='netcdf=parallel')

    # Python bindings
    depends_on('boost+python', when='+python')

    conflicts('~mpi', when='netcdf=parallel', msg='Parallel NetCDF requires MPI')
    conflicts(
        '+mpi', when='+python',
        msg='Building python bindings is possible only for the serial code'
    )
    conflicts('~mpi', when='^mpi',
              msg='There should be no MPI in the DAG when ~mpi is active')

    def cmake_args(self):
        spec = self.spec

        on_or_off = lambda predicate: 'ON' if predicate else 'OFF'

        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                on_or_off('+shared' in spec)
            ),
            '-DUSE_MPI:BOOL={0}'.format(on_or_off('+mpi' in spec)),
            '-DWITH_HDF5CXX:BOOL={0}'.format(on_or_off('+hdf5' in spec)),
            '-DWITH_PYTHON:BOOL={0}'.format(on_or_off('+python' in spec))
        ]

        netcdf_str = {
            'none': 'OFF',
            'serial': 'Serial',
            'parallel': 'Parallel'
        }

        args.append('-DWITH_NETCDF:STRING={0}'.format(
            netcdf_str[spec.variants['netcdf'].value]
        ))

        # Set an MPI compiler for parallel builds
        if '+mpi' in spec:
            args.append(
                '-DCMAKE_CXX_COMPILER:PATH={0}'.format(spec['mpi'].mpicxx)
            )

        return args
