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

import os
from spack import *


class Vtk(CMakePackage):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization. """

    homepage = "http://www.vtk.org"
    url      = "http://www.vtk.org/files/release/8.0/VTK-8.0.1.tar.gz"
    list_url = "http://www.vtk.org/download/"

    version('8.0.1', '692d09ae8fadc97b59d35cab429b261a')
    version('7.1.0', 'a7e814c1db503d896af72458c2d0228f')
    version('7.0.0', '5fe35312db5fb2341139b8e4955c367d')
    version('6.3.0', '0231ca4840408e9dd60af48b314c5b6d')
    version('6.1.0', '25e4dfb3bad778722dcaec80cd5dab7d')

    # VTK7 defaults to OpenGL2 rendering backend
    variant('opengl2', default=True, description='Enable OpenGL2 backend')
    variant('osmesa', default=False, description='Enable OSMesa support')
    variant('python', default=False, description='Enable Python support')
    variant('qt', default=False, description='Build with support for Qt')

    patch('gcc.patch', when='@6.1.0')

    # At the moment, we cannot build with both osmesa and qt, but as of
    # VTK 8.1, that should change
    conflicts('+osmesa', when='+qt')

    # The use of the OpenGL2 backend requires at least OpenGL Core Profile
    # version 3.2 or higher.
    depends_on('gl@3.2:', when='+opengl2')

    # If you didn't ask for osmesa, then hw rendering using vendor-specific
    # drivers is faster, but it must be done externally.
    depends_on('opengl', when='~osmesa')

    # mesa default is software rendering, make it faster with llvm
    depends_on('mesa+llvm', when='+osmesa')

    # VTK will need Qt5OpenGL, and qt needs '-opengl' for that
    depends_on('qt+opengl', when='+qt')

    depends_on('expat')
    depends_on('freetype')
    depends_on('glew')
    depends_on('hdf5')
    depends_on('libjpeg')
    depends_on('jsoncpp')
    depends_on('libharu')
    depends_on('libxml2')
    depends_on('lz4')
    depends_on('netcdf')
    depends_on('netcdf-cxx')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('zlib')

    extends('python', when='+python')

    def url_for_version(self, version):
        url = "http://www.vtk.org/files/release/{0}/VTK-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def setup_environment(self, spack_env, run_env):
        # VTK has some trouble finding freetype unless it is set in
        # the environment
        spack_env.set('FREETYPE_DIR', self.spec['freetype'].prefix)

    def cmake_args(self):
        spec = self.spec

        opengl_ver = 'OpenGL{0}'.format('2' if '+opengl2' in spec else '')

        cmake_args = [
            '-DBUILD_SHARED_LIBS=ON',
            '-DVTK_RENDERING_BACKEND:STRING={0}'.format(opengl_ver),

            # In general, we disable use of VTK "ThirdParty" libs, preferring
            # spack-built versions whenever possible
            '-DVTK_USE_SYSTEM_LIBRARIES=ON',

            # However, in a few cases we can't do without them yet
            '-DVTK_USE_SYSTEM_GL2PS=OFF',
            '-DVTK_USE_SYSTEM_LIBPROJ4=OFF',
            '-DVTK_USE_SYSTEM_OGGTHEORA=OFF',

            '-DNETCDF_DIR={0}'.format(spec['netcdf'].prefix),
            '-DNETCDF_C_ROOT={0}'.format(spec['netcdf'].prefix),
            '-DNETCDF_CXX_ROOT={0}'.format(spec['netcdf-cxx'].prefix),

            # Disable wrappers for other languages.
            '-DVTK_WRAP_JAVA=OFF',
            '-DVTK_WRAP_TCL=OFF',
        ]

        # Enable/Disable wrappers for Python.
        if '+python' in spec:
            cmake_args.extend([
                '-DVTK_WRAP_PYTHON=ON',
                '-DPYTHON_EXECUTABLE={0}'.format(spec['python'].command.path)
            ])
        else:
            cmake_args.append('-DVTK_WRAP_PYTHON=OFF')

        if 'darwin' in spec.architecture:
            cmake_args.extend([
                '-DCMAKE_MACOSX_RPATH=ON'
            ])

        if '+qt' in spec:
            qt_ver = spec['qt'].version.up_to(1)
            qt_bin = spec['qt'].prefix.bin
            qmake_exe = os.path.join(qt_bin, 'qmake')

            cmake_args.extend([
                # Enable Qt support here.
                '-DVTK_QT_VERSION:STRING={0}'.format(qt_ver),
                '-DQT_QMAKE_EXECUTABLE:PATH={0}'.format(qmake_exe),
                '-DVTK_Group_Qt:BOOL=ON',
            ])

            # NOTE: The following definitions are required in order to allow
            # VTK to build with qt~webkit versions (see the documentation for
            # more info: http://www.vtk.org/Wiki/VTK/Tutorials/QtSetup).
            if '~webkit' in spec['qt']:
                cmake_args.extend([
                    '-DVTK_Group_Qt:BOOL=OFF',
                    '-DModule_vtkGUISupportQt:BOOL=ON',
                    '-DModule_vtkGUISupportQtOpenGL:BOOL=ON',
                ])

        if '+osmesa' in spec:
            prefix = spec['mesa'].prefix
            osmesa_include_dir = prefix.include
            osmesa_library = os.path.join(prefix.lib, 'libOSMesa.so')

            use_param = 'VTK_USE_X'
            if 'darwin' in spec.architecture:
                use_param = 'VTK_USE_COCOA'

            cmake_args.extend([
                '-D{0}:BOOL=OFF'.format(use_param),
                '-DVTK_OPENGL_HAS_OSMESA:BOOL=ON',
                '-DOSMESA_INCLUDE_DIR:PATH={0}'.format(osmesa_include_dir),
                '-DOSMESA_LIBRARY:FILEPATH={0}'.format(osmesa_library),
            ])
        else:
            prefix = spec['opengl'].prefix

            opengl_include_dir = prefix.include
            opengl_library = os.path.join(prefix.lib, 'libGL.so')
            if 'darwin' in spec.architecture:
                opengl_include_dir = prefix
                opengl_library = prefix

            cmake_args.extend([
                '-DOPENGL_INCLUDE_DIR:PATH={0}'.format(opengl_include_dir),
                '-DOPENGL_gl_LIBRARY:FILEPATH={0}'.format(opengl_library)
            ])

        if spec.satisfies('@:6.1.0'):
            cmake_args.extend([
                '-DCMAKE_C_FLAGS=-DGLX_GLXEXT_LEGACY',
                '-DCMAKE_CXX_FLAGS=-DGLX_GLXEXT_LEGACY'
            ])

            # VTK 6.1.0 (and possibly earlier) does not use
            # NETCDF_CXX_ROOT to detect NetCDF C++ bindings, so
            # NETCDF_CXX_INCLUDE_DIR and NETCDF_CXX_LIBRARY must be
            # used instead to detect these bindings
            netcdf_cxx_lib = spec['netcdf-cxx'].libs.joined()
            cmake_args.extend([
                '-DNETCDF_CXX_INCLUDE_DIR={0}'.format(
                    spec['netcdf-cxx'].prefix.include),
                '-DNETCDF_CXX_LIBRARY={0}'.format(netcdf_cxx_lib),
            ])

            # Garbage collection is unsupported in Xcode starting with
            # version 5.1; if the Apple clang version of the compiler
            # is 5.1.0 or later, unset the required Objective-C flags
            # to remove the garbage collection flags.  Versions of VTK
            # after 6.1.0 set VTK_REQUIRED_OBJCXX_FLAGS to the empty
            # string. This fix was recommended on the VTK mailing list
            # in March 2014 (see
            # https://public.kitware.com/pipermail/vtkusers/2014-March/083368.html)
            if (self.compiler.is_apple and
                self.compiler.version >= Version('5.1.0')):
                cmake_args.extend(['-DVTK_REQUIRED_OBJCXX_FLAGS=""'])

        return cmake_args
