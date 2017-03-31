##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

# TODO: Add support for a C++11 enabled installation that filters out the
# TODO: "C++11-Disabled" flag (but only if the spec compiler supports C++11).

# TODO: Use variant forwarding to forward the 'mpi' variant to the direct
# TODO: dependencies 'hdf5' and 'netcdf'.


class Exodusii(Package):
    """Exodus II is a C++/Fortran library developed to store and retrieve
       data for finite element analyses. It's used for preprocessing
       (problem definition), postprocessing (results visualization), and
       data transfer between codes.  An Exodus II data file is a random
       access, machine independent, binary file that is written and read
       via C, C++, or Fortran API routines.

    """

    homepage = "https://github.com/gsjaardema/seacas"
    url      = "https://github.com/gsjaardema/seacas/archive/master.zip"

    version('2016-08-09', git='https://github.com/gsjaardema/seacas.git', commit='2ffeb1b')

    variant('mpi', default=True, description='Enables MPI parallelism.')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('mpi', when='+mpi')

    # https://github.com/gsjaardema/seacas/blob/master/NetCDF-Mapping.md
    depends_on('netcdf maxdims=65536 maxvars=524288')
    depends_on('hdf5+shared')

    patch('cmake-exodus.patch')

    def install(self, spec, prefix):
        cc_path = spec['mpi'].mpicc if '+mpi' in spec else self.compiler.cc
        cxx_path = spec['mpi'].mpicxx if '+mpi' in spec else self.compiler.cxx

        config_args = std_cmake_args[:]
        config_args.extend([
            # General Flags #
            '-DSEACASProj_ENABLE_CXX11:BOOL=OFF',
            '-DSEACASProj_ENABLE_Zoltan:BOOL=OFF',
            '-DHDF5_ROOT:PATH={0}'.format(spec['hdf5'].prefix),
            '-DNetCDF_DIR:PATH={0}'.format(spec['netcdf'].prefix),

            # MPI Flags #
            '-DTPL_ENABLE_MPI={0}'.format('ON' if '+mpi' in spec else 'OFF'),
            '-DCMAKE_C_COMPILER={0}'.format(cc_path),
            '-DCMAKE_CXX_COMPILER={0}'.format(cxx_path),
        ])

        build_directory = join_path(self.stage.source_path, 'spack-build')
        source_directory = self.stage.source_path

        with working_dir(build_directory, create=True):
            mcmake = Executable(join_path(source_directory, 'cmake-exodus'))
            mcmake(*config_args)

            make()
            make('install')
