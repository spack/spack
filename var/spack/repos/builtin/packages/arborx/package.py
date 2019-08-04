# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arborx(CMakePackage):
    """ArborX is a performance-portable library for geometric search"""

    homepage = "http://github.com/arborx/arborx"
    url      = "https://github.com/arborx/arborx/archive/v0.8-beta.tar.gz"
    git      = "https://github.com/arborx/arborx.git"

    version('master', branch='master')
    version('0.8-beta', sha256='d90254656df089b1321bf26d55f69d0db465fff12a972c446562ceaca5f090ad')

    variant('cuda', default=False, description='enable Cuda backend')
    variant('openmp', default=False, description='enable OpenMP backend')
    variant('serial', default=True, description='enable Serial backend (default)')
    variant('mpi', default=True, description='enable MPI')

    depends_on('cmake@3.12:', type='build')
    depends_on('cuda', when='+cuda')
    depends_on('mpi', when='+mpi')

    # ArborX relies on Kokkos to provide devices, thus having one-to-one match
    # The only way to disable those devices is to make sure Kokkos does not
    # provide them
    depends_on('kokkos@2.7.00:+cuda+enable_lambda', when='+cuda')
    depends_on('kokkos@2.7.00:+openmp', when='+openmp')
    depends_on('kokkos@2.7.00:+serial', when='+serial')

    def cmake_args(self):
        spec = self.spec

        options = [
            '-DCMAKE_PREFIX_PATH=%s' % spec['kokkos'].prefix,
            '-DArborX_ENABLE_TESTS=OFF',
            '-DArborX_ENABLE_EXAMPLES=OFF',
            '-DArborX_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF')
        ]

        if '+cuda' in spec:
            nvcc_wrapper_path = spec['kokkos'].prefix.bin.nvcc_wrapper
            options.append('-DCMAKE_CXX_COMPILER=%s' % nvcc_wrapper_path)

        return options
