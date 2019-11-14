# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Flecsi(CMakePackage):
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
    git      = 'https://github.com/laristra/flecsi.git'

    version('develop', branch='master', submodules=False, preferred=True)

    variant('build_type', default='Release', values=('Debug', 'Release'),
            description='The build type to build', multi=False)
    variant('backend', default='mpi', values=('serial', 'mpi', 'legion','hpx'),
            description='Backend to use for distributed memory', multi=False)
    variant('minimal', default=False,
            description='Disable FindPackageMetis')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('unittest', default=False,
            description='Enable unit testing')
    variant('flog', default=False,
            description='Enable flog testing')
    variant('doxygen', default=False,
            description='Enable doxygen')
    variant('doc', default=False,
            description='Enable documentation')
    variant('coverage', default=False,
            description='Enable coverage build')
    variant('openmpi', default=False,
            description='Use OpenMPI package')
    variant('mpich', default=False,
            description='Use MPICH package')
    variant('hdf5', default=False,
            description='Enable HDF5 Support')
    variant('caliper', default=False,
            description='Enable Caliper Support')
    variant('graphviz', default=False,
            description='Enable GraphViz Support')
    variant('tutorial', default=False,
            description='Build FleCSI Tutorials')
    variant('flecstan', default=False,
            description='Build FleCSI Static Analyzer')

    depends_on('cmake@3.12:',  type='build')
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on('cinch@1.01:', type='build')
    depends_on('mpi', when='backend=mpi')
    depends_on('mpi', when='backend=legion')
    depends_on('mpi', when='backend=hpx')
    depends_on('openmpi@3.1.3:3.1.4', when='+openmpi')
    depends_on('mpich@3.2.1', when='+mpich')
    depends_on('legion@ctrl-rep +shared +mpi +hdf5', when='backend=legion +hdf5')
    depends_on('legion@ctrl-rep +shared +mpi', when='backend=legion ~hdf5')
    depends_on('hpx@1.3.0 cxxstd=14', when='backend=hpx')
    depends_on('boost@1.70.0: cxxstd=14 +program_options')
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')
    depends_on('hdf5', when='+hdf5')
    depends_on('caliper', when='+caliper')
    depends_on('graphviz', when='+graphviz')
    depends_on('python@3.0:', when='+tutorial')
    depends_on('llvm', when='+flecstan')

    conflicts('+tutorial', when='backend=hpx')
#    conflicts('+hdf5', when='backend=hpx')
#    conflicts('+hdf5', when='backend=mpi')

    def cmake_args(self):
        spec = self.spec
        options = ['-DENABLE_MPI=ON',
                   '-DENABLE_OPENMP=ON',
                   '-DCXX_CONFORMANCE_STANDARD=c++17',
                   '-DENABLE_METIS=ON',
                   '-DENABLE_PARMETIS=ON',
                   '-DENABLE_COLORING=ON',
                   '-DENABLE_DEVEL_TARGETS=ON',
                   '-DCMAKE_DISABLE_FIND_PACKAGE_METIS=%s'%('ON' if '+minimal' in spec else 'OFF'),
                   '-DBUILD_SHARED_LIBS=%s'%('ON' if '+shared' in spec else 'OFF'),
                   '-DENABLE_UNIT_TESTS=%s'%('ON' if '+unittest' in spec else 'OFF'),
                   '-DENABLE_CALIPER=%s'%('ON' if '+caliper' in spec else 'OFF'),
                   '-DENABLE_FLECSTAN=%s'%('ON' if '+flecstan' in spec else 'OFF'),
                   '-DENABLE_DOXYGEN=%s'%('ON' if '+doxygen' in spec else 'OFF'),
                   '-DENABLE_DOCUMENTATION=%s'%('ON' if '+doc' in spec else 'OFF'),
                   '-DENABLE_COVERAGE_BUILD=%s'%('ON' if '+coverage' in spec else 'OFF')]
        options.append('-DCINCH_SOURCE_DIR=' + spec['cinch'].prefix)

        if spec.variants['build_type'].value == 'Debug':
            options.append('-DCMAKE_BUILD_TYPE=Debug')
        elif spec.variants['build_type'].value == 'Release':
            options.append('-DCMAKE_BUILD_TYPE=Release')

        if spec.variants['backend'].value == 'legion':
            options.append('-DFLECSI_RUNTIME_MODEL=legion')
        elif spec.variants['backend'].value == 'mpi':
            options.append('-DFLECSI_RUNTIME_MODEL=mpi')
        elif spec.variants['backend'].value == 'hpx':
            options.append('-DFLECSI_RUNTIME_MODEL=hpx')
        else:
            options.append('-DFLECSI_RUNTIME_MODEL=serial')
            options.append('-DENABLE_MPI=OFF')

        if '+hdf5' in spec and spec.variants['backend'].value == 'legion':
            options.append('-DENABLE_HDF5=ON')
        else:
            options.append('-DENABLE_HDF5=OFF')

        if '+tutorial' in self.spec:
            options.append('-DENABLE_FLECSIT=ON')
            options.append('-DENABLE_FLECSI_TUTORIAL=ON')
        else:
            options.append('-DENABLE_FLECSIT=OFF')
            options.append('-DENABLE_FLECSI_TUTORIAL=OFF')

        return options
