# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    homepage = "https://visit-dav.github.io/visit-website/"
    git      = "https://github.com/visit-dav/visit.git"
    url = "https://github.com/visit-dav/visit/releases/download/v3.2.1/visit3.2.1.tar.gz"

    tags = ['radiuss']

    maintainers = ['cyrush']

    extendable = True

    executables = ['^visit$']

    version('develop', branch='develop')
    version('3.2.1', sha256='779d59564c63f31fcbfeff24b14ddd6ac941b3bb7d671d31765a770d193f02e8')

    variant('gui',    default=True, description='Enable VisIt\'s GUI')
    variant('adios2', default=False, description='Enable ADIOS2 file format')
    variant('hdf5',   default=True, description='Enable HDF5 file format')
    variant('silo',   default=True, description='Enable Silo file format')
    variant('python', default=True, description='Enable Python support')
    variant('mpi',    default=False, description='Enable parallel engine')

    patch('spack-changes-3.1.patch', when="@3.1.0:,develop")
    patch('spack-changes-3.0.1.patch', when="@3.0.1")
    patch('nonframework-qwt.patch', when='^qt~framework platform=darwin')
    patch('parallel-hdf5.patch', when='+hdf5+mpi')

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

    depends_on('cmake@3.14.7', type='build')
    # https://github.com/visit-dav/visit/issues/3498
    depends_on('vtk@8.1.0+opengl2+osmesa~python',
               patches=[patch('vtk_compiler_visibility.patch'),
                        patch('vtk_rendering_opengl2_x11.patch'),
                        patch('vtk_wrapping_python_x11.patch'),
                       ],
               when='~python @3.2:,develop')
    depends_on('vtk@8.1.0+opengl2+osmesa+python',
               patches=[patch('vtk_compiler_visibility.patch'),
                        patch('vtk_rendering_opengl2_x11.patch'),
                        patch('vtk_wrapping_python_x11.patch'),
                       ],
               when='+python @3.2:,develop')
    depends_on('glu', when='platform=linux')
    depends_on('vtk+python', when='+python @3.2:,develop')
    depends_on('vtk~mpi', when='~mpi')
    depends_on('vtk+qt', when='+gui')
    depends_on('qt+gui@5.14.2:', when='+gui @3.2:,develop')
    depends_on('qwt@6.1.6', when='+gui')
    depends_on('python@3.7.7', when='+python')
    depends_on('llvm@6.0.1', when='^mesa')
    depends_on('mesa+glx@20.2.1', when='^mesa')
    depends_on('mesa-glu@9.0.1', when='^mesa')
    depends_on('hdf5@1.8.14', when='+hdf5')
    # VisIt uses Silo's 'ghost zone' data structures, which are only available
    # in v4.10+ releases: https://wci.llnl.gov/simulation/computer-codes/silo/releases/release-notes-4.10
    depends_on('silo@4.10:+shared', when='+silo')
    depends_on('silo~mpi', when='+silo~mpi')
    depends_on('silo+mpi', when='+silo+mpi')
    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('adios2', when='+adios2')

    root_cmakelists_dir = 'src'

    @when('@3.0.0:,develop')
    def patch(self):
        # Some of VTK's targets don't create explicit libraries, so there is no
        # 'vtktiff'. Instead, replace with the library variable defined from
        # VTK's module flies (e.g. lib/cmake/vtk-8.1/Modules/vtktiff.cmake)
        for filename in find('src', 'CMakeLists.txt'):
            filter_file(r'\bvtk(tiff|jpeg|png)', r'${vtk\1_LIBRARIES}',
                        filename)

    def cmake_args(self):
        spec = self.spec

        cxx_flags = [self.compiler.cxx_pic_flag]
        cc_flags = [self.compiler.cc_pic_flag]

        # NOTE: This is necessary in order to allow VisIt to compile a couple
        # of lines of code with 'const char*' to/from 'char*' conversions.
        if spec.satisfies('@3:%gcc'):
            cxx_flags.append('-fpermissive')
            cc_flags.append('-fpermissive')

        args = [
            '-DVTK_MAJOR_VERSION=' + str(spec['vtk'].version[0]),
            '-DVTK_MINOR_VERSION=' + str(spec['vtk'].version[1]),
            '-DVISIT_VTK_DIR:PATH=' + spec['vtk'].prefix,
            '-DVISIT_ZLIB_DIR:PATH=' + spec['zlib'].prefix,
            '-DVISIT_USE_GLEW=OFF',
            '-DCMAKE_CXX_FLAGS=' + ' '.join(cxx_flags),
            '-DCMAKE_C_FLAGS=' + ' '.join(cc_flags),
            '-DVISIT_CONFIG_SITE=NONE',
        ]

        # Provide the plugin compilation environment so as to extend VisIt
        args.append('-DVISIT_INSTALL_THIRD_PARTY=ON')

        if spec.satisfies('@3.1:'):
            args.append('-DFIXUP_OSX=OFF')

        if '+python' in spec:
            args.append('-DVISIT_PYTHON_SCRIPTING=ON')
            # keep this off, we have an openssl + python linking issue
            # that appears in spack
            args.append('-DVISIT_PYTHON_FILTERS=OFF')
            args.append('-DPYTHON_DIR:PATH={0}'.format(spec['python'].home))
        else:
            args.append('-DVISIT_PYTHON_SCRIPTING=OFF')
            # keep this off, we have an openssl + python linking issue
            # that appears in spack
            args.append('-DVISIT_PYTHON_FILTERS=OFF')

        if '+gui' in spec:
            qt_bin = spec['qt'].prefix.bin
            args.extend([
                '-DVISIT_LOC_QMAKE_EXE:FILEPATH={0}/qmake'.format(qt_bin),
                '-DVISIT_QT_DIR:PATH=' + spec['qt'].prefix,
                '-DVISIT_QWT_DIR:PATH=' + spec['qwt'].prefix
            ])
        else:
            args.append('-DVISIT_SERVER_COMPONENTS_ONLY=ON')
            args.append('-DVISIT_ENGINE_ONLY=ON')

        if '^mesa' in spec:
            args.append(
                '-DVISIT_LLVM_DIR:PATH={0}'.format(spec['llvm'].prefix))
            args.append(
                '-DVISIT_MESAGL_DIR:PATH={0}'.format(spec['mesa'].prefix))

        if '+hdf5' in spec:
            args.append(
                '-DVISIT_HDF5_DIR:PATH={0}'.format(spec['hdf5'].prefix))
            if '+mpi' in spec:
                args.append('-DVISIT_HDF5_MPI_DIR:PATH={0}'.format(
                    spec['hdf5'].prefix))

        if '+silo' in spec:
            args.append(
                '-DVISIT_SILO_DIR:PATH={0}'.format(spec['silo'].prefix))

        if '+mpi' in spec:
            args.append('-DVISIT_PARALLEL=ON')
            args.append('-DVISIT_C_COMPILER={0}'.format(spec['mpi'].mpicc))
            args.append('-DVISIT_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx))
            args.append('-DVISIT_MPI_COMPILER={0}'.format(spec['mpi'].mpicxx))

        return args

    # https://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=executables#making-a-package-discoverable-with-spack-external-find
    # Here we are only able to determine the latest version
    # despite VisIt may have multiple versions
    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('-version', output=str, error=str)
        match = re.search(r'\s*(\d[\d\.]+)\.', output)
        return match.group(1) if match else None
