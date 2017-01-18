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


class Gmsh(CMakePackage):
    """Gmsh is a free 3D finite element grid generator with a built-in CAD engine
    and post-processor. Its design goal is to provide a fast, light and
    user-friendly meshing tool with parametric input and advanced visualization
    capabilities. Gmsh is built around four modules: geometry, mesh, solver and
    post-processing. The specification of any input to these modules is done
    either interactively using the graphical user interface or in ASCII text
    files using Gmsh's own scripting language.
    """

    homepage = 'http://gmsh.info'
    url = 'http://gmsh.info/src/gmsh-2.11.0-source.tgz'

    version('2.16.0', 'e829eaf32ea02350a385202cc749341f2a3217c464719384b18f653edd028eea')
    version('2.15.0', '992a4b580454105f719f5bc05441d3d392ab0b4b80d4ea07b61ca3bdc974070a')
    version('2.12.0', '7fbd2ec8071e79725266e72744d21e902d4fe6fa9e7c52340ad5f4be5c159d09')
    version('2.11.0', 'f15b6e7ac9ca649c9a74440e1259d0db')

    variant('shared',      default=True,
            description='Enables the build of shared libraries')
    variant('debug',       default=False,
            description='Builds the library in debug mode')
    variant('mpi',         default=True,
            description='Builds MPI support for parser and solver')
    variant('fltk',        default=False,
            description='Enables the build of the FLTK GUI')
    variant('hdf5',        default=False, description='Enables HDF5 support')
    variant('compression', default=True,
            description='Enables IO compression through zlib')
    variant('oce',         default=False, description='Build with OCE')
    variant('petsc',       default=False, description='Build with PETSc')
    variant('slepc',       default=False,
            description='Build with SLEPc (only when PETSc is enabled)')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cmake@2.8:', type='build')
    depends_on('gmp')
    depends_on('mpi',  when='+mpi')
    # Assumes OpenGL with GLU is already provided by the system:
    depends_on('fltk', when='+fltk')
    depends_on('hdf5', when='+hdf5')
    depends_on('oce',  when='+oce')
    depends_on('petsc+mpi', when='+petsc+mpi')
    depends_on('petsc', when='+petsc~mpi')
    depends_on('slepc', when='+slepc+petsc')
    depends_on('zlib',  when='+compression')

    def cmake_args(self):
        spec = self.spec
        prefix = self.prefix

        options = []

        # Make sure native file dialogs are used
        options.extend(['-DENABLE_NATIVE_FILE_CHOOSER=ON'])

        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        # Prevent GMsh from using its own strange directory structure on OSX
        options.append('-DENABLE_OS_SPECIFIC_INSTALL=OFF')

        # Make sure GMSH picks up correct BlasLapack by providing linker flags
        blas_lapack = spec['lapack'].lapack_libs + spec['blas'].blas_libs
        options.append(
            '-DBLAS_LAPACK_LIBRARIES={0}'.format(blas_lapack.ld_flags))

        # Gmsh does not have an option to compile against external metis.
        # Its own Metis, however, fails to build
        options.append('-DENABLE_METIS=OFF')

        if '+fltk' in spec:
            options.append('-DENABLE_FLTK=ON')
        else:
            options.append('-DENABLE_FLTK=OFF')

        if '+oce' in spec:
            env['CASROOT'] = self.spec['oce'].prefix
            options.extend(['-DENABLE_OCC=ON'])
        else:
            options.extend(['-DENABLE_OCC=OFF'])

        if '+petsc' in spec:
            env['PETSC_DIR'] = self.spec['petsc'].prefix
            options.extend(['-DENABLE_PETSC=ON'])
        else:
            options.extend(['-DENABLE_PETSC=OFF'])

        if '+slepc' in spec:
            env['SLEPC_DIR'] = self.spec['slepc'].prefix
            options.extend(['-DENABLE_SLEPC=ON'])
        else:
            options.extend(['-DENABLE_SLEPC=OFF'])

        if '+shared' in spec:
            # Builds dynamic executable and installs shared library
            options.extend(['-DENABLE_BUILD_SHARED:BOOL=ON',
                            '-DENABLE_BUILD_DYNAMIC:BOOL=ON'])
        else:
            # Builds and installs static library
            options.append('-DENABLE_BUILD_LIB:BOOL=ON')

        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')

        if '+mpi' in spec:
            options.append('-DENABLE_MPI:BOOL=ON')

        if '+compression' in spec:
            options.append('-DENABLE_COMPRESSED_IO:BOOL=ON')

        return options
