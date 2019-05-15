# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arborx(CMakePackage):
    """ArborX is a performance-portable library for geometric search"""

    homepage = "http://github.com/arborx/arborx"
    git      = "https://github.com/arborx/arborx.git"

    version('master', branch='master')

    variant('cuda', default=False, description='enable Cuda backend')
    variant('openmp', default=False, description='enable OpenMP backend')
    variant('serial', default=True, description='enable Serial backend (default)')
    variant('mpi', default=True, description='enable MPI')

    depends_on('cmake@3.12:')
    depends_on('cuda', when='+cuda')
    depends_on('mpi', when='+mpi')

    # ArborX relies on Kokkos to provide devices, thus having one-to-one match
    # The only way to disable those devices is to make sure Kokkos does not
    # provide them
    depends_on('kokkos@2.7.00:+cuda+enable_lambda', when='+cuda')
    depends_on('kokkos@2.7.00:~cuda', when='~cuda')
    depends_on('kokkos@2.7.00:+openmp', when='+openmp')
    depends_on('kokkos@2.7.00:~openmp', when='~openmp')
    depends_on('kokkos@2.7.00:+serial', when='+serial')
    depends_on('kokkos@2.7.00:~serial', when='~serial')

    def cmake_args(self):
        spec = self.spec

        options = [
            '-DCMAKE_PREFIX_PATH=%s' % (spec['kokkos'].prefix),
            '-DArborX_ENABLE_TESTS=OFF',
            '-DArborX_ENABLE_EXAMPLES=OFF',
            '-DArborX_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF')
        ]

        if '+cuda' in spec:
            options.extend([
                '-DCMAKE_CXX_COMPILER=%s' % (
                    spec['kokkos'].prefix.bin + "/nvcc_wrapper"
                )
            ])

        return options
