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

    def url_for_version(self, version):
        url = 'https://github.com/MeshToolkit/MSTK/archive/{0}.tar.gz'
        return url.format(version)
    
    version('master', branch='master')
    version('v3_2_1', sha256='430bdf06826d47bd025dffe70165113505d2c6fbc6b3fd0d019a39c1a4e6ee5a')
    version('v3_2_0', sha256='76a3bcdff132e586fddb39c60855c9201eaa587a6736b8b8bc762f66a4d0cb82')
    version('v3_1_3', sha256='ce0a13e1c32ddf50787afbcab79b581e1f858d4fb6013846a4b3434ba613759c')
    version('v3_1_2', sha256='f068e6d535122b5820a8a4563a2aab73d6a25c8d2db1a788cd1f3bb510de3574')
    version('v3_1_1', sha256='1c161d2e1bfef4ac2ceb95d0e82265f0a32b654c9fd5ae117e2ce3aee0252393')
    version('v3_1_0', sha256='975f9b8218675c80e7fe0691efe342cd0480cd90e9d3e8c78fe2e17a7ea992b9')
    version('v3_0_4', sha256='ce9a5ccd60833ad2b74791a41e18a3bf200bfd4604baa3b284384a363873db8f')
    version('v3_0_3', sha256='9cf5398e4beac587457c8a7d1fe146d2c126793fac9b46d76da5994dd10163b1')
    version('v3_0_2', sha256='1cdae8cad0cb65991854bb7667f5a08e6c9ea23f41e2dca7f3484c4c0b8f9a90')
    version('v3_0_1', sha256='ac63063c861e605ef9060f726568600f9ad367d6b7e2a5664bc97e766d188f4d')
    version('v3_0_0', sha256='7f1b3ad68b397d5487de87122c642b48fb76f656ac68a733bf8a0195fddbaeac')

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
