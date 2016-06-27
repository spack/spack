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


class Gmsh(Package):
    """
    Gmsh is a free 3D finite element grid generator with a built-in CAD engine and post-processor. Its design goal is
    to provide a fast, light and user-friendly meshing tool with parametric input and advanced visualization
    capabilities. Gmsh is built around four modules: geometry, mesh, solver and post-processing. The specification of
    any input to these modules is done either interactively using the graphical user interface or in ASCII text files
    using Gmsh's own scripting language.
    """
    homepage = 'http://gmsh.info'
    url = 'http://gmsh.info/src/gmsh-2.11.0-source.tgz'

    version('2.11.0', 'f15b6e7ac9ca649c9a74440e1259d0db')

    # FIXME : Misses dependencies on gmm, PetsC, TetGen

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds the library in debug mode')
    variant('mpi', default=False, description='Builds MPI support for parser and solver')
    variant('fltk', default=False, description='Enables the build of the FLTK GUI')
    variant('hdf5', default=False, description='Enables HDF5 support')
    variant('compression', default=True, description='Enables IO compression through zlib')

    depends_on('blas')
    depends_on('lapack')
    depends_on('gmp')
    depends_on('mpi', when='+mpi')
    depends_on('fltk', when='+fltk')  # Assumes OpenGL with GLU is already provided by the system
    depends_on('hdf5', when='+hdf5')
    depends_on('zlib', when='+compression')

    def install(self, spec, prefix):

        options = []
        options.extend(std_cmake_args)

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        # Prevent GMsh from using its own strange directory structure on OSX
        options.append('-DENABLE_OS_SPECIFIC_INSTALL=OFF')

        if '+shared' in spec:
            options.extend(['-DENABLE_BUILD_SHARED:BOOL=ON',
                            '-DENABLE_BUILD_DYNAMIC:BOOL=ON'])  # Builds dynamic executable and installs shared library
        else:
            options.append('-DENABLE_BUILD_LIB:BOOL=ON')  # Builds and installs static library

        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')

        if '+mpi' in spec:
            options.append('-DENABLE_MPI:BOOL=ON')

        if '+compression' in spec:
            options.append('-DENABLE_COMPRESSED_IO:BOOL=ON')

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make('install')
