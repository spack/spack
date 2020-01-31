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
    homepage = 'http://flecsi.lanl.gov/'
    git      = 'https://github.com/laristra/flecsi.git'

    version('develop', branch='master', submodules=False, preferred=True)

    variant('backend', default='mpi', values=('serial', 'mpi', 'legion'),
            description='Backend to use for distributed memory')
    variant('caliper', default=False,
            description='Enable Caliper Support')
    variant('graphviz', default=False,
            description='Enable GraphViz Support')
    variant('tutorial', default=False,
            description='Build FleCSI Tutorials')
    variant('flecstan', default=False,
            description='Build FleCSI Static Analyzer')

    depends_on('cmake@3.1:',  type='build')
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on('cinch@1.01:', type='build')
    depends_on('mpi', when='backend=mpi')
    depends_on('mpi', when='backend=legion')
    depends_on('gasnet@2019.3.0 ~pshm', when='backend=legion')
    depends_on('legion@ctrl-rep +shared +mpi', when='backend=legion')
    depends_on('boost@1.59.0: cxxstd=11 +program_options')
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')
    depends_on('caliper', when='+caliper')
    depends_on('graphviz', when='+graphviz')
    depends_on('python@3.0:', when='+tutorial')
    depends_on('llvm', when='+flecstan')

    def cmake_args(self):
        options = ['-DCMAKE_BUILD_TYPE=debug']
        options.append('-DCINCH_SOURCE_DIR=' + self.spec['cinch'].prefix)

        if self.spec.variants['backend'].value == 'legion':
            options.append('-DFLECSI_RUNTIME_MODEL=legion')
        elif self.spec.variants['backend'].value == 'mpi':
            options.append('-DFLECSI_RUNTIME_MODEL=mpi')
        else:
            options.append('-DFLECSI_RUNTIME_MODEL=serial')
            options.append(
                '-DENABLE_MPI=OFF',
            )

        if '+tutorial' in self.spec:
            options.append('-DENABLE_FLECSIT=ON')
            options.append('-DENABLE_FLECSI_TUTORIAL=ON')
        else:
            options.append('-DENABLE_FLECSIT=OFF')
            options.append('-DENABLE_FLECSI_TUTORIAL=OFF')

        if '+caliper' in self.spec:
            options.append('-DENABLE_CALIPER=ON')
        else:
            options.append('-DENABLE_CALIPER=OFF')

        if '+flecstan' in self.spec:
            options.append('-DENABLE_FLECSTAN=ON')
        else:
            options.append('-DENABLE_FLECSTAN=OFF')

        return options
