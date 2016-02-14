##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import sys

# FIXME : lot of code is duplicated from packages/metis/package.py . Inheriting from there may reduce
# FIXME : the installation rules to just a few lines


class Parmetis(Package):
    """
    ParMETIS is an MPI-based parallel library that implements a variety of algorithms for partitioning unstructured
    graphs, meshes, and for computing fill-reducing orderings of sparse matrices.
    """
    homepage = 'http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overview'
    url = 'http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/parmetis-4.0.3.tar.gz'

    version('4.0.3', 'f69c479586bf6bb7aff6a9bc0c739628')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds the library in debug mode')
    variant('gdb', default=False, description='Enables gdb support')

    variant('idx64', default=False, description='Use int64_t as default index type')
    variant('double', default=False, description='Use double precision floating point types')

    depends_on('cmake @2.8:')  # build dependency
    depends_on('mpi')

    # FIXME : this should conflict with metis as it builds its own version internally

    depends_on('gdb', when='+gdb')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        metis_source = join_path(source_directory, 'metis')

        # FIXME : Once a contract is defined, MPI compilers should be retrieved indirectly via spec['mpi'] in case
        # FIXME : they use a non-standard name
        options.extend(['-DGKLIB_PATH:PATH={metis_source}/GKlib'.format(metis_source=metis_source),
                        '-DMETIS_PATH:PATH={metis_source}'.format(metis_source=metis_source),
                        '-DCMAKE_C_COMPILER:STRING=mpicc',
                        '-DCMAKE_CXX_COMPILER:STRING=mpicxx'])

        if '+shared' in spec:
            options.append('-DSHARED:BOOL=ON')

        if '+debug' in spec:
            options.extend(['-DDEBUG:BOOL=ON',
                            '-DCMAKE_BUILD_TYPE:STRING=Debug'])

        if '+gdb' in spec:
            options.append('-DGDB:BOOL=ON')

        metis_header = join_path(metis_source, 'include', 'metis.h')

        if '+idx64' in spec:
            filter_file('IDXTYPEWIDTH 32', 'IDXTYPEWIDTH 64', metis_header)

        if '+double' in spec:
            filter_file('REALTYPEWIDTH 32', 'REALTYPEWIDTH 64', metis_header)

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")
            # Parmetis build system doesn't allow for an external metis to be used, but doesn't copy the required
            # metis header either
            install(metis_header, self.prefix.include)

        # The shared library is not installed correctly on Darwin; correct this
        if sys.platform == 'darwin':
            install_name_tool = which('install_name_tool')
            install_name_tool('-id', join_path(prefix.lib, 'libparmetis.dylib'),
                join_path(prefix.lib, 'libparmetis.dylib'))
