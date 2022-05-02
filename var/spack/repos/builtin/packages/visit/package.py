# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Visit(CMakePackage):
    """VisIt is an Open Source, interactive, scalable, visualization,
       animation and analysis tool. See comments in VisIt's package.py
       for tips about building VisIt with spack. Building VisIt with
       Spack is still experimental and many standard features are likely
       disabled
       LINUX-------------------------------------------------------------------
       spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0
       LINUX-W/O-OPENGL--------------------------------------------------------
       spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \\
       ^mesa+opengl
       MACOS-------------------------------------------------------------------
       spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \\
       ^qt~framework

    """
    ############################
    # Suggestions for building:
    ############################
    # cyrush note:
    #
    # Out of the box, VisIt's python 2 requirement will cause
    # spack spec constraint errors due Qt + Mesa build
    # dependencies.
    #
    # You can avoid this using:
    #
    # linux:
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0
    #
    # linux w/o opengl: (add mesa as opengl if system lacks system opengl )
    #
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \
    #                      ^mesa+opengl
    #
    # macOS:
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \
    #                      ^qt~framework
    #
    # Rpath issues undermine qwt (not qt) when a build as a framework
    # VisIt's osxfixup resolves this for us in other cases,
    # but we can't use osxfixup with spack b/c it will undermine other libs.
    #
    # Even with these changes, VisIt's Python CLI does not work on macOS,
    # there is a linking issue related to OpenSSL.
    # (dyld: Symbol not found: _GENERAL_NAME_free - which comes from OpenSSL)
    #
    ############################
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    git      = "https://github.com/visit-dav/visit.git"
    url = "https://github.com/visit-dav/visit/releases/download/v3.2.1/visit3.2.1.tar.gz"

    tags = ['radiuss']

    maintainers = ['cyrush']

    extendable = True

    executables = ['^visit$']

    version('develop', branch='develop')
    version('3.2.2', sha256='d19ac24c622a3bc0a71bc9cd6e5c9860e43f39e3279672129278b6ebce8d0ead')
    version('3.2.1', sha256='779d59564c63f31fcbfeff24b14ddd6ac941b3bb7d671d31765a770d193f02e8')
    version('3.1.1', sha256='0b60ac52fd00aff3cf212a310e36e32e13ae3ca0ddd1ea3f54f75e4d9b6c6cf0')
    version('3.0.1', sha256='a506d4d83b8973829e68787d8d721199523ce7ec73e7594e93333c214c2c12bd')

    root_cmakelists_dir = 'src'
    generator = "Ninja"

    variant('gui',    default=True, description='Enable VisIt\'s GUI')
    variant('osmesa', default=False, description='Use OSMesa for off-screen CPU rendering')
    variant('adios2', default=True, description='Enable ADIOS2 file format')
    variant('hdf5',   default=True, description='Enable HDF5 file format')
    variant('silo',   default=True, description='Enable Silo file format')
    variant('python', default=True, description='Enable Python support')
    variant('mpi',    default=True, description='Enable parallel engine')

    patch('spack-changes-3.1.patch', when="@3.1.0:,develop")
    patch('spack-changes-3.0.1.patch', when="@3.0.1")
    patch('nonframework-qwt.patch', when='^qt~framework platform=darwin')
    patch('parallel-hdf5.patch', when='+hdf5+mpi')

    # Exactly one of 'gui' or 'osmesa' has to be enabled
    conflicts('+gui', when='+osmesa')
    conflicts('~gui', when='~osmesa')

    #############################################
    # Full List of dependencies from build_visit
    #############################################
    # cyrush note:
    #  I added these here to give folks details
    #  to help eventually build up to full
    #  support for visit
    #############################################
    # =====================================
    # core:
    # =====================================
    #  cmake (build)
    #  vtk
    #  qt
    #  qwt
    #  python
    #  mpi
    #
    # =====================================
    # rendering (optional):
    # =====================================
    # icet
    # vtk-m
    # vtk-h
    # llvm
    # mesagl
    # osmesa
    # tbb
    # embree
    # ispc
    # ospray
    #
    # =====================================
    # python modules:
    # =====================================
    # numpy
    # pillow
    # mpi4py
    # seedme
    # sphinx (build, docs)
    # sphinx rtd theme (build, docs)
    # pyqt (visit support deprecated)
    # pyside (note: we want pyside 2)
    #
    # =====================================
    # testing related:
    # =====================================
    # p7zip (build, test)
    #
    # =====================================
    # io libs:
    # =====================================
    # adios
    # adios2
    # advio
    # boost
    # boxlib
    # cfitsio
    # cgns
    # conduit
    # damaris
    # fastbit
    # fastquery
    # gdal
    # h5part
    # hdf4
    # hdf5
    # mdsplus
    # mfem
    # mili
    # moab
    # mxml
    # nektarpp
    # netcdf
    # openexr
    # pidx
    # silo
    # stripack
    # szip
    # tbb
    # uintah
    # xdmf
    # xercesc
    # xsd
    # zlib
    #
    # =====================================

    depends_on('cmake@3.14.7:', type='build')
    depends_on('ninja', type='build')

    depends_on('mpi', when='+mpi')

    # VTK flavors
    depends_on('vtk@8.1:8 +opengl2')
    depends_on('vtk +osmesa', when='+osmesa')
    depends_on('vtk +qt', when='+gui')
    depends_on('vtk +python', when='+python')
    depends_on('vtk +mpi', when='+mpi')
    depends_on('vtk ~mpi', when='~mpi')

    # Necessary VTK patches
    depends_on('vtk', patches=[patch('vtk_compiler_visibility.patch')])
    depends_on('vtk', patches=[patch('vtk_rendering_opengl2_x11.patch')],
               when='~osmesa platform=linux')
    depends_on('vtk', patches=[patch('vtk_wrapping_python_x11.patch')],
               when='+python')

    depends_on('glu', when='~osmesa')
    depends_on('mesa-glu+osmesa', when='+osmesa')

    # VisIt doesn't work with later versions of qt.
    depends_on('qt+gui+opengl@5:5.14', when='+gui')
    depends_on('qwt', when='+gui')

    # python@3.8 doesn't work with VisIt.
    depends_on('python@3.2:3.7', when='+python')
    extends('python', when='+python')

    # VisIt uses the hdf5 1.8 api
    # set the API version later on down in setup_build_environment
    depends_on('hdf5@1.8:', when='+hdf5')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('hdf5~mpi', when='+hdf5~mpi')

    # VisIt uses Silo's 'ghost zone' data structures, which are only available
    # in v4.10+ releases: https://wci.llnl.gov/simulation/computer-codes/silo/releases/release-notes-4.10
    depends_on('silo@4.10: +shared', when='+silo')
    depends_on('silo+hdf5', when='+silo+hdf5')
    depends_on('silo~hdf5', when='+silo~hdf5')
    depends_on('silo+mpi', when='+silo+mpi')
    depends_on('silo~mpi', when='+silo~mpi')

    depends_on('adios2@2.6:', when='+adios2')
    depends_on('adios2+hdf5', when='+adios2+hdf5')
    depends_on('adios2~hdf5', when='+adios2~hdf5')
    depends_on('adios2+mpi', when='+adios2+mpi')
    depends_on('adios2~mpi', when='+adios2~mpi')
    depends_on('adios2+python', when='+adios2+python')
    depends_on('adios2~python', when='+adios2~python')

    depends_on('zlib')

    @when('@3:,develop')
    def patch(self):
        # Some of VTK's targets don't create explicit libraries, so there is no
        # 'vtktiff'. Instead, replace with the library variable defined from
        # VTK's module flies (e.g. lib/cmake/vtk-8.1/Modules/vtktiff.cmake)
        for filename in find('src', 'CMakeLists.txt'):
            filter_file(r'\bvtk(tiff|jpeg|png)', r'${vtk\1_LIBRARIES}',
                        filename)

    def flag_handler(self, name, flags):
        if name in ('cflags', 'cxxflags'):
            # NOTE: This is necessary in order to allow VisIt to compile a couple
            # of lines of code with 'const char*' to/from 'char*' conversions.
            if '@3:%gcc' in self.spec:
                flags.append('-fpermissive')

            # VisIt still uses the hdf5 1.8 api
            if '+hdf5' in self.spec and '@1.10:' in self.spec['hdf5']:
                flags.append('-DH5_USE_18_API')

        return (flags, None, None)

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define('CMAKE_POSITION_INDEPENDENT_CODE', True),
            self.define('VTK_MAJOR_VERSION', spec['vtk'].version[0]),
            self.define('VTK_MINOR_VERSION', spec['vtk'].version[1]),
            self.define('VISIT_VTK_DIR', spec['vtk'].prefix),
            self.define('VISIT_ZLIB_DIR', spec['zlib'].prefix),
            self.define('VISIT_USE_GLEW', False),
            self.define('VISIT_CONFIG_SITE', 'NONE'),
            self.define('VISIT_INSTALL_THIRD_PARTY', True),
        ]

        if '@3.1: platform=darwin' in spec:
            args.append(self.define('FIXUP_OSX', False))

        if '+python' in spec:
            args.extend([
                self.define('VISIT_PYTHON_FILTERS', True),
                self.define('VISIT_PYTHON_SCRIPTING', True),
                self.define('PYTHON_DIR', spec['python'].home),
            ])
        else:
            args.extend([
                self.define('VISIT_PYTHON_FILTERS', False),
                self.define('VISIT_PYTHON_SCRIPTING', False),
            ])

        if '+gui' in spec:
            qt_bin = spec['qt'].prefix.bin
            qmake_exe = os.path.join(qt_bin, 'qmake')
            args.extend([
                self.define('VISIT_SERVER_COMPONENTS_ONLY', False),
                self.define('VISIT_ENGINE_ONLY', False),
                self.define('VISIT_LOC_QMAKE_EXE', qmake_exe),
                self.define('VISIT_QT_DIR', spec['qt'].prefix),
                self.define('VISIT_QWT_DIR', spec['qwt'].prefix),
            ])
        else:
            args.extend([
                self.define('VISIT_SERVER_COMPONENTS_ONLY', True),
                self.define('VISIT_ENGINE_ONLY', True),
            ])

        # No idea why this is actually needed
        if '^mesa' in spec:
            args.append(self.define('VISIT_MESAGL_DIR', spec['mesa'].prefix))
            if '+llvm' in spec['mesa']:
                args.append(self.define('VISIT_LLVM_DIR', spec['libllvm'].prefix))

        if '+hdf5' in spec:
            args.append(self.define('VISIT_HDF5_DIR', spec['hdf5'].prefix))
            if '+mpi' in spec and '+mpi' in spec['hdf5']:
                args.append(self.define('VISIT_HDF5_MPI_DIR', spec['hdf5'].prefix))

        if '+silo' in spec:
            args.append(self.define('VISIT_SILO_DIR', spec['silo'].prefix))

        if '+mpi' in spec:
            args.extend([
                self.define('VISIT_PARALLEL', True),
                self.define('VISIT_MPI_COMPILER', spec['mpi'].mpicxx),
            ])
        else:
            args.append(self.define('VISIT_PARALLEL', False))

        return args

    # https://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=executables#making-a-package-discoverable-with-spack-external-find
    # Here we are only able to determine the latest version
    # despite VisIt may have multiple versions
    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('-version', output=str, error=str)
        match = re.search(r'\s*(\d[\d\.]+)\.', output)
        return match.group(1) if match else None
