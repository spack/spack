# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arbor(CMakePackage):
    """Arbor is a high-performance library for computational neuroscience
    simulations."""

    homepage = "https://github.com/arbor-sim/arbor/"
    url      = "https://github.com/arbor-sim/arbor/archive/v0.2.tar.gz"

    version('0.2', git='https://github.com/arbor-sim/arbor.git',
            commit='6f70bfee22415fc8cca5f12ab7f3917a043bddb3',
            submodules=True)

    variant('vectorize', default=False,
            description='Enable vectorization of computational kernels')
    variant('gpu', default=False, description='Enable GPU support')
    variant('mpi', default=False, description='Enable MPI support')
    variant('python', default=False,
            description='Enable python frontend support')
    variant('unwind', default=False,
            description='Enable libunwind for pretty stack traces')

    depends_on('cuda', when='+gpu')
    depends_on('mpi', when='+mpi')
    depends_on('libunwind', when='+unwind')

    extends('python@3.6:', when='+python')
    depends_on('py-mpi4py', when='+mpi+python', type=('build', 'run'))

    # when building documentation
    # depends_on('py-sphinx')

    def patch(self):
        filter_file(
            r'find_library\(_unwind_library_target unwind-\${libunwind_arch}',
            r'find_library(_unwind_library_target unwind-${_libunwind_arch}',
            'cmake/FindUnwind.cmake'
        )
        filter_file(
            r'target_compile_definitions\(arbor-private-deps ARB_WITH_UNWIND\)',      # noqa
            r'target_compile_definitions(arbor-private-deps INTERFACE WITH_UNWIND)',  # noqa
            'CMakeLists.txt'
        )

    def cmake_args(self):
        args = []
        args.extend([
            '-DARB_VECTORIZE=' + ('ON' if '+vectorize' in self.spec else 'OFF'),      # noqa
            '-DARB_WITH_GPU=' + ('ON' if '+gpu' in self.spec else 'OFF'),
            '-DARB_WITH_PYTHON=' + ('ON' if '+python' in self.spec else 'OFF'),
        ])

        if '+unwind' in self.spec:
            args.append('-DUnwind_ROOT_DIR={}'.format(self.spec['libunwind'].prefix))  # noqa

        return args
