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

class Metis(Package):
    """
    METIS is a set of serial programs for partitioning graphs, partitioning finite element meshes, and producing fill
    reducing orderings for sparse matrices. The algorithms implemented in METIS are based on the multilevel
    recursive-bisection, multilevel k-way, and multi-constraint partitioning schemes.
    """

    homepage = 'http://glaros.dtc.umn.edu/gkhome/metis/metis/overview'
    url = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz"

    version('5.1.0', '5465e67079419a69e0116de24fce58fe')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds the library in debug mode')
    variant('gdb', default=False, description='Enables gdb support')

    variant('idx64', default=False, description='Use int64_t as default index type')
    variant('double', default=False, description='Use double precision floating point types')

    depends_on('cmake @2.8:')  # build-time dependency

    depends_on('gdb', when='+gdb')

    def install(self, spec, prefix):

        options = []
        options.extend(std_cmake_args)

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        options.append('-DGKLIB_PATH:PATH={metis_source}/GKlib'.format(metis_source=source_directory))

        if '+shared' in spec:
            options.append('-DSHARED:BOOL=ON')

        if '+debug' in spec:
            options.extend(['-DDEBUG:BOOL=ON',
                            '-DCMAKE_BUILD_TYPE:STRING=Debug'])

        if '+gdb' in spec:
            options.append('-DGDB:BOOL=ON')

        metis_header = join_path(source_directory, 'include', 'metis.h')

        if '+idx64' in spec:
            filter_file('IDXTYPEWIDTH 32', 'IDXTYPEWIDTH 64', metis_header)

        if '+double' in spec:
            filter_file('REALTYPEWIDTH 32', 'REALTYPEWIDTH 64', metis_header)

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")

        # The shared library is not installed correctly on Darwin; correct this
        if sys.platform == 'darwin':
            install_name_tool = which('install_name_tool')
            install_name_tool('-id', join_path(prefix.lib, 'libmetis.dylib'),
                join_path(prefix.lib, 'libmetis.dylib'))
