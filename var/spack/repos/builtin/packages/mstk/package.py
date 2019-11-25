# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mstk(CMakePackage):
    """MSTK is a mesh framework that allows users to represent,
    manipulate and query unstructured 3D arbitrary topology meshes
    in a general manner without the need to code their own data
    structures. MSTK is a flexible framework in that it allows a
    variety of underlying representations for the mesh while
    maintaining a common interface. It allows users to choose from
    different mesh representations either at initialization (implemented)
    or during the program execution (not yet implemented) so that the
    optimal data structures are used for the particular algorithm.
    The interaction of users and applications with MSTK is through a
    functional interface that acts as though the mesh always contains
    vertices, edges, faces and regions and maintains connectivity between
    all these entities."""

    homepage = "https://github.com/MeshToolkit/MSTK"
    git      = "https://github.com/MeshToolkit/MSTK"

    maintainers = ['raovgarimella','julienloiseau']

    version('master', branch='master')

    variant('exodusii', default=False, description='Enable ExodusII')
    variant('use_markers', default=True, description='Enable use of markers')
    variant('enable_tests', default=False, description='Enable unit testing')
    variant('parallel', default=False, description='Enable Parallel Support')
    variant('partitioner', default='none',
            values=('none', 'metis', 'zoltan','all'),
            multi=False, description='Choose partitioner')
    conflicts('partitioner=none', when='+parallel')
    conflicts('partitioner=all', when='-parallel')
    conflicts('partitioner=zoltan', when='-parallel')

    # MSTK turns on METIS only for parallel buildsu
    conflicts('partitioner=metis', when='-parallel')

    # dependencies
    depends_on('cmake@3.11:', type='build')

    #
    depends_on('mpi', when='+parallel')

    depends_on('zoltan -fortran', when='partitioner=zoltan')
    depends_on('zoltan -fortran', when='partitioner=all')
    depends_on('metis', when='partitioner=metis')
    depends_on('metis', when='partitioner=all')


    # Exodusii variant
    # The default exodusii build with mpi support
    depends_on('exodusii', when='+exodusii')

    # Unit testing variant
    depends_on('unittest-cpp', when='+enable_tests')

    def cmake_args(self):
        options = []
        if '+use_markers' in self.spec:
            options.append('-DMSTK_USE_MARKERS=ON')
        else:
            options.append('-DMSTK_USE_MARKERS=OFF')

        # Parallel variant
        if '+parallel' in self.spec:
            options.append('-DENABLE_PARALLEL=ON')
        else:
            options.append('-DENABLE_PARALLEL=OFF')

        if 'partitioner=none' in self.spec:
            options.append('-DENABLE_METIS=OFF')
            options.append('-DENABLE_ZOLTAN=OFF')
        else:
            if 'zoltan' or 'all' in self.spec:
                options.append('-DENABLE_ZOLTAN=ON')
            else:
                options.append('-DENABLE_ZOLTAN=OFF')
            if 'metis' or 'all' in self.spec:
                options.append('-DENABLE_METIS=ON')
            else:
                options.append('-DENABLE_METIS=OFF')


        # ExodusII variant
        if '+exodusii' in self.spec:
            options.append('-DENABLE_ExodusII=ON')
        else:
            options.append('-DENABLE_ExodusII=OFF')

        # Unit test variant
        if '+enable_tests' in self.spec:
            options.append('-DENABLE_Tests=ON')
        else:
            options.append('-DENABLE_Tests=OFF')

        return options
