# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack import *


class Vtk(CMakePackage):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization. """

    homepage = "http://www.vtk.org"
    url      = "http://www.vtk.org/files/release/8.0/VTK-8.0.1.tar.gz"
    list_url = "http://www.vtk.org/download/"

    version('8.1.2', sha256='0995fb36857dd76ccfb8bb07350c214d9f9099e80b1e66b4a8909311f24ff0db')
    version('8.1.1', sha256='71a09b4340f0a9c58559fe946dc745ab68a866cf20636a41d97b6046cb736324')
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
    variant('xdmf', default=False, description='Build XDMF file support')
    variant('ffmpeg', default=False, description='Build with FFMPEG support')
    variant('mpi', default=True, description='Enable MPI support')

    # Haru causes trouble on Fedora and Ubuntu in v8.1.1
    # See https://bugzilla.redhat.com/show_bug.cgi?id=1460059#c13
    variant('haru', default=True, description='Enable libharu')

    patch('gcc.patch', when='@6.1.0')

    # At the moment, we cannot build with both osmesa and qt, but as of
    # VTK 8.1, that should change
    conflicts('+osmesa', when='+qt')

    depends_on('python', when='+python')
    depends_on('py-mpi4py', when='+mpi +python', type='run')
    extends('python', when='+python')
    # python3.7 compatibility patch backported from upstream
    # https://gitlab.kitware.com/vtk/vtk/commit/706f1b397df09a27ab8981ab9464547028d0c322
    patch('python3.7-const-char.patch', when='@:8.1.1 ^python@3.7:')

    # The use of the OpenGL2 backend requires at least OpenGL Core Profile
    # version 3.2 or higher.
    depends_on('gl@3.2:', when='+opengl2')

    # If you didn't ask for osmesa, then hw rendering using vendor-specific
    # drivers is faster, but it must be done externally.
    depends_on('opengl', when='~osmesa')

    # Note: it is recommended to use mesa+llvm, if possible.
    # mesa default is software rendering, llvm makes it faster
    depends_on('mesa', when='+osmesa')

    # VTK will need Qt5OpenGL, and qt needs '-opengl' for that
    depends_on('qt+opengl', when='+qt')

    depends_on('mpi', when='+mpi')

    depends_on('libharu', when='+haru')

    depends_on('boost', when='+xdmf')
    depends_on('boost+mpi', when='+xdmf +mpi')

    depends_on('mpi', when='+mpi')

    depends_on('ffmpeg', when='+ffmpeg')

    depends_on('expat')
    depends_on('freetype')
    depends_on('glew')
    depends_on('hdf5')
    depends_on('libjpeg')
    depends_on('jsoncpp')
    depends_on('libxml2')
    depends_on('lz4')
    depends_on('netcdf')
    depends_on('netcdf-cxx')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('zlib')

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

            '-DVTK_USE_SYSTEM_LIBHARU=%s' % (
                'ON' if '+haru' in spec else 'OFF'),

            # In general, we disable use of VTK "ThirdParty" libs, preferring
            # spack-built versions whenever possible
            '-DVTK_USE_SYSTEM_LIBRARIES:BOOL=ON',

            # However, in a few cases we can't do without them yet
            '-DVTK_USE_SYSTEM_GL2PS:BOOL=OFF',
            '-DVTK_USE_SYSTEM_LIBPROJ4:BOOL=OFF',
            '-DVTK_USE_SYSTEM_OGGTHEORA:BOOL=OFF',

            '-DNETCDF_DIR={0}'.format(spec['netcdf'].prefix),
            '-DNETCDF_C_ROOT={0}'.format(spec['netcdf'].prefix),
            '-DNETCDF_CXX_ROOT={0}'.format(spec['netcdf-cxx'].prefix),

            # Disable wrappers for other languages.
            '-DVTK_WRAP_JAVA=OFF',
            '-DVTK_WRAP_TCL=OFF',
        ]

        if '+mpi' in spec:
            cmake_args.extend([
                '-DVTK_Group_MPI:BOOL=ON',
                '-DVTK_USE_SYSTEM_DIY2:BOOL=OFF',
            ])

        if '+ffmpeg' in spec:
            cmake_args.extend(['-DModule_vtkIOFFMPEG:BOOL=ON'])

        # Enable/Disable wrappers for Python.
        if '+python' in spec:
            cmake_args.extend([
                '-DVTK_WRAP_PYTHON=ON',
                '-DPYTHON_EXECUTABLE={0}'.format(spec['python'].command.path),
                '-DVTK_USE_SYSTEM_MPI4PY:BOOL=ON'
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

        if '+xdmf' in spec:
            if spec.satisfies('^cmake@3.12:'):
                # This policy exists only for CMake >= 3.12
                cmake_args.extend(["-DCMAKE_POLICY_DEFAULT_CMP0074=NEW"])

            cmake_args.extend([
                # Enable XDMF Support here
                "-DModule_vtkIOXdmf2:BOOL=ON",
                "-DModule_vtkIOXdmf3:BOOL=ON",
                "-DBOOST_ROOT={0}".format(spec['boost'].prefix),
                "-DBOOST_LIBRARY_DIR={0}".format(spec['boost'].prefix.lib),
                "-DBOOST_INCLUDE_DIR={0}".format(spec['boost'].prefix.include),
                "-DBOOST_NO_SYSTEM_PATHS:BOOL=ON",
                # This is needed because VTK has multiple FindBoost
                # and they stick to system boost if there's a system boost
                # installed with CMake
                "-DBoost_NO_BOOST_CMAKE:BOOL=ON",
                "-DHDF5_ROOT={0}".format(spec['hdf5'].prefix),
                # The xdmf project does not export any CMake file...
                "-DVTK_USE_SYSTEM_XDMF3:BOOL=OFF",
                "-DVTK_USE_SYSTEM_XDMF2:BOOL=OFF"
            ])

            if '+mpi' in spec:
                cmake_args.extend(["-DModule_vtkIOParallelXdmf3:BOOL=ON"])

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
            if (self.spec.satisfies('%clang') and
                self.compiler.is_apple and
                self.compiler.version >= Version('5.1.0')):
                cmake_args.extend(['-DVTK_REQUIRED_OBJCXX_FLAGS=""'])

        return cmake_args
