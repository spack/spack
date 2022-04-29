# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Flecsi(CMakePackage, CudaPackage):
    '''FleCSI is a compile-time configurable framework designed to support
       multi-physics application development. As such, FleCSI attempts to
       provide a very general set of infrastructure design patterns that can
       be specialized and extended to suit the needs of a broad variety of
       solver and data requirements. Current support includes multi-dimensional
       mesh topology, mesh geometry, and mesh adjacency information,
       n-dimensional hashed-tree data structures, graph partitioning
       interfaces,and dependency closures.
    '''
    homepage = 'http://flecsi.org/'
    git      = 'https://github.com/flecsi/flecsi.git'
    maintainers = ['rspavel', 'ktsai7']

    tags = ['e4s']

    version('develop', branch='develop', submodules=False)
    version('1.4.develop', git="https://github.com/laristra/flecsi.git",  branch='1.4', submodules=False, preferred=False)
    version('1.4.2', git="https://github.com/laristra/flecsi.git",  tag='v1.4.2', submodules=False, preferred=True)
    version('2.1.0', tag='v2.1.0', submodules=False, preferred=False)
    version('flecsph', git="https://github.com/laristra/flecsi.git", branch="stable/flecsph", submodules=True, preferred=False)

    variant('backend', default='mpi', values=('serial', 'mpi', 'legion', 'hpx', 'charmpp'),
            description='Backend to use for distributed memory', multi=False)
    variant('debug_backend', default=False,
            description='Build Backend with Debug Mode')
    variant('disable_metis', default=False,
            description='Disable FindPackageMetis')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('flog', default=False,
            description='Enable flog testing')
    variant('doxygen', default=False,
            description='Enable doxygen')
    variant('doc', default=False,
            description='Enable documentation')
    variant('coverage', default=False,
            description='Enable coverage build')
    variant('hdf5', default=True,
            description='Enable HDF5 Support')
    variant('caliper_detail', default='none',
            values=('none', 'low', 'medium', 'high'),
            description='Set Caliper Profiling Detail', multi=False)
    variant('graphviz', default=False,
            description='Enable GraphViz Support')
    variant('tutorial', default=False,
            description='Build FleCSI Tutorials')
    variant('flecstan', default=False,
            description='Build FleCSI Static Analyzer')
    variant('external_cinch', default=True,
            description='Enable External Cinch')
    variant('kokkos', default=False,
            description='Enable Kokkos Support')
    variant('unit_tests', default=False,
            description='Build with Unit Tests Enabled')
    variant('openmp', default=False,
            description='Enable OpenMP Support')

    # All Current FleCSI Releases
    for level in ('low', 'medium', 'high'):
        depends_on('caliper@2.0.1~adiak~libdw', when='@:1.9 caliper_detail=%s' % level)
        depends_on('caliper@2.4.0~libdw', when='@2.0: caliper_detail=%s' % level)
    depends_on('graphviz', when='+graphviz')
    depends_on('hdf5+hl+mpi', when='+hdf5')
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')
    depends_on('boost@1.70.0: cxxstd=17 +program_options')
    depends_on('openmpi+legacylaunchers', when='+unit_tests ^openmpi')
    depends_on('legion network=gasnet', when='backend=legion')

    # FleCSI@1.x
    depends_on('cmake@3.12:', when='@:1.9')
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on('cinch@1.01:', type='build', when='+external_cinch @:1.9')
    depends_on('mpi', when='backend=mpi @:1.9')
    depends_on('mpi', when='backend=legion @:1.9')
    depends_on('mpi', when='backend=hpx @:1.9')
    depends_on('legion+shared', when='backend=legion @:1.9')
    depends_on('legion+hdf5', when='backend=legion +hdf5 @:1.9')
    depends_on('legion build_type=Debug', when='backend=legion +debug_backend @:1.9')
    depends_on('legion@cr', when='backend=legion @:1.9')
    depends_on('hpx@1.4.1 cxxstd=17 malloc=system max_cpu_count=128', when='backend=hpx @:1.9')
    depends_on('hpx build_type=Debug', when='backend=hpx +debug_backend @:1.9')
    depends_on('googletest@1.8.1+gmock', when='@:1.9')
    depends_on('python@3.0:', when='+tutorial @:1.9')
    depends_on('doxygen', when='+doxygen @:1.9')
    depends_on('llvm', when='+flecstan @:1.9')
    depends_on('pfunit@3.0:3', when='@:1.9')
    depends_on('py-gcovr', when='+coverage @:1.9')

    # FleCSI@2.x
    depends_on('cmake@3.15:', when='@2.0:')
    depends_on('boost +atomic +filesystem +regex +system', when='@2.0:')
    depends_on('kokkos@3.2.00:', when='+kokkos @2.0:')
    depends_on('legion@cr', when='backend=legion @2.0:')
    depends_on('legion+hdf5', when='backend=legion +hdf5 @2.0:')
    depends_on('hdf5@1.10.7:', when='backend=legion +hdf5 @2.0:')
    depends_on('hpx@1.3.0 cxxstd=17 malloc=system', when='backend=hpx @2.0:')
    depends_on('kokkos@3.2.00:', when='+kokkos @2.0:')
    depends_on('mpich@3.4.1:', when='@2.0: ^mpich')
    depends_on('openmpi@4.1.0:', when='@2.0: ^openmpi')
    depends_on('lanl-cmake-modules', when='@2.1.1:')

    conflicts('%gcc@:8', when='@2.1:')

    conflicts('+tutorial', when='backend=hpx')
    # FleCSI@2: no longer supports serial or charmpp backends
    conflicts('backend=serial', when='@2.0:')
    conflicts('backend=charmpp', when='@2.0:')
    # FleCSI@2: no longer expects to control how backend is built
    conflicts('+debug_backend', when='@2.0:')
    # FleCSI@2: No longer supports previous TPL related flags
    conflicts('+disable_metis', when='@2.0:')
    # FleCSI@2: no longer provides documentation variants
    conflicts('+doxygen', when='@2.0:')
    conflicts('+doc', when='@2.0:')
    # FleCSI@2: no longer provides coverage variants
    conflicts('+coverage', when='@2.0:')
    # FleCSI@2: no longer provides tutorial variants
    conflicts('+tutorial', when='@2.0:')
    # FleCSI@2: no longer supports flecstan
    conflicts('+flecstan', when='@2.0:')
    # FleCSI@2: integrates cinch and no longer depends on external installs
    #   Except for lanl-cmake-modules as of 2.1.1: but that has no submodule
    conflicts('+external_cinch', when='@2.0:')
    # Current FleCSI@:1.4 releases do not support kokkos, omp, or cuda
    conflicts('+kokkos', when='@:1.4.99')
    conflicts('+openmp', when='@:1.4.99')
    conflicts('+cuda', when='@:1.4.99')
    # Unit tests require flog support
    conflicts('+unit_tests', when='~flog')
    # Disallow conduit=none when using legion as a backend
    conflicts('^legion conduit=none', when='backend=legion')
    # Due to overhauls of Legion and Gasnet spackages
    #   flecsi@:1.4 can no longer be built with a usable legion
    conflicts('backend=legion', when='@:1.4.99')

    def cmake_args(self):
        spec = self.spec
        options = []

        if '+external_cinch' in spec:
            options.append('-DCINCH_SOURCE_DIR=' + spec['cinch'].prefix)

        backend_flag = ''
        if spec.satisfies('@2.1.1:'):
            backend_flag = 'FLECSI_BACKEND'
        else:
            backend_flag = 'FLECSI_RUNTIME_MODEL'

        if spec.variants['backend'].value == 'legion':
            options.append('-D' + backend_flag + '=legion')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'mpi':
            options.append('-D' + backend_flag + '=mpi')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'hpx':
            options.append('-D' + backend_flag + '=hpx')
            options.append('-DENABLE_MPI=ON')
            options.append('-DHPX_IGNORE_CMAKE_BUILD_TYPE_COMPATIBILITY=ON')
        elif spec.variants['backend'].value == 'charmpp':
            options.append('-D' + backend_flag + '=charmpp')
            options.append('-DENABLE_MPI=ON')
        else:
            options.append('-D' + backend_flag + '=serial')
            options.append('-DENABLE_MPI=OFF')

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        options.append('-DCALIPER_DETAIL=%s' %
                       spec.variants['caliper_detail'].value)
        if spec.satisfies('@:1.9'):
            if spec.variants['caliper_detail'].value == 'none':
                options.append('-DENABLE_CALIPER=OFF')
            else:
                options.append('-DENABLE_CALIPER=ON')

        if self.run_tests or '+unit' in spec:
            options.append('-DENABLE_UNIT_TESTS=ON')
        else:
            options.append('-DENABLE_UNIT_TESTS=OFF')

        if ('+flog' in spec):
            options.append('-DENABLE_FLOG=ON')
        else:
            options.append('-DENABLE_FLOG=OFF')

        if '+hdf5' in spec and spec.variants['backend'].value != 'hpx':
            options.append('-DENABLE_HDF5=ON')
        else:
            options.append('-DENABLE_HDF5=OFF')

        if '+graphviz' in spec:
            options.append('-DENABLE_GRAPHVIZ=ON')
        else:
            options.append('-DENABLE_GRAPHVIZ=OFF')

        if '+kokkos' in spec:
            options.append('-DENABLE_KOKKOS=ON')
        else:
            options.append('-DENABLE_KOKKOS=OFF')
        if '+openmp' in spec:
            options.append('-DENABLE_OPENMP=ON')
        else:
            options.append('-DENABLE_OPENMP=OFF')

        if '+disable_metis' in spec:
            options.append('-DCMAKE_DISABLE_FIND_PACKAGE_METIS=ON')
        else:
            options.append('-DCMAKE_DISABLE_FIND_PACKAGE_METIS=OFF')

        if '+tutorial' in spec:
            options.append('-DENABLE_FLECSIT=ON')
            options.append('-DENABLE_FLECSI_TUTORIAL=ON')
        else:
            options.append('-DENABLE_FLECSIT=OFF')
            options.append('-DENABLE_FLECSI_TUTORIAL=OFF')

        if '+flecstan' in spec:
            options.append('-DENABLE_FLECSTAN=ON')
        else:
            options.append('-DENABLE_FLECSTAN=OFF')

        if '+doxygen' in spec:
            options.append('-DENABLE_DOXYGEN=ON')
        else:
            options.append('-DENABLE_DOXYGEN=OFF')
        if '+doc' in spec:
            options.append('-DENABLE_DOCUMENTATION=ON')
        else:
            options.append('-DENABLE_DOCUMENTATION=OFF')
        if '+coverage' in spec:
            options.append('-DENABLE_COVERAGE_BUILD=ON')
        else:
            options.append('-DENABLE_COVERAGE_BUILD=OFF')

        return options
