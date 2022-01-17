# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack import *


class HpxLocal(CMakePackage, CudaPackage, ROCmPackage):
    """C++ runtime system for parallel and distributed applications (on-node)."""

    homepage = "https://hpx.stellar-group.org/"
    url = "https://github.com/STEllAR-GROUP/hpx-local/archive/0.0.0.tar.gz"
    maintainers = ['msimberg', 'albestro', 'teonnik']

    version('master', git='https://github.com/STEllAR-GROUP/hpx-local.git', branch='master')

    generator = 'Ninja'

    map_cxxstd = lambda cxxstd: '2a' if cxxstd == '20' else cxxstd
    cxxstds = ('17', '20')
    variant('cxxstd',
            default='17',
            values=cxxstds,
            description='Use the specified C++ standard when building.')

    variant(
        'malloc', default='tcmalloc',
        description='Define which allocator will be linked in',
        values=('system', 'tcmalloc', 'jemalloc', 'tbbmalloc')
    )

    default_generic_coroutines = True
    if sys.platform.startswith('linux') or sys.platform == 'win32':
        default_generic_coroutines = False
    variant(
        "generic_coroutines", default=default_generic_coroutines,
        description='Use Boost.Context as the underlying coroutines'
                    ' context switch implementation.')

    variant('examples', default=False, description='Build examples')
    variant('mpi', default=False, description='Enable MPI support')

    # Build dependencies
    depends_on('git', type='build')
    depends_on('ninja', type='build')
    depends_on('cmake@3.18:', type='build')

    conflicts('%gcc@:6')
    conflicts('%clang@:6')

    # Other dependecies
    depends_on('hwloc@1.11.5:')
    depends_on('boost@1.71:')
    depends_on('asio@1.12:')

    depends_on('gperftools', when='malloc=tcmalloc')
    depends_on('jemalloc', when='malloc=jemalloc')
    depends_on('tbb', when='malloc=tbbmalloc')

    depends_on('mpi', when='+mpi')
    depends_on('cuda@11:', when='+cuda')

    for cxxstd in cxxstds:
        depends_on(
            "boost cxxstd={0}".format(map_cxxstd(cxxstd)),
            when="cxxstd={0}".format(cxxstd)
        )
    for cxxstd in cxxstds:
        depends_on(
            "asio cxxstd={0}".format(map_cxxstd(cxxstd)),
            when="cxxstd={0} ^asio".format(cxxstd),
        )

    # COROUTINES
    # ~generic_coroutines conflict is not fully implemented
    # for additional information see:
    # https://github.com/spack/spack/pull/17654
    # https://github.com/STEllAR-GROUP/hpx/issues/4829
    depends_on('boost+context', when='+generic_coroutines')
    _msg_generic_coroutines = 'This platform requires +generic_coroutines'
    conflicts('~generic_coroutines', when='platform=darwin', msg=_msg_generic_coroutines)

    def cmake_args(self):
        spec, args = self.spec, []

        args += [
            self.define('HPXLocal_WITH_CXX_STANDARD', spec.variants['cxxstd'].value),
            self.define_from_variant('HPXLocal_WITH_EXAMPLES', 'examples'),
            self.define_from_variant('HPXLocal_WITH_MALLOC', 'malloc'),
            self.define_from_variant('HPXLocal_WITH_CUDA', 'cuda'),
            self.define_from_variant('HPXLocal_WITH_HIP', 'rocm'),
            self.define_from_variant('HPXLocal_WITH_ASYNC_MPI', 'mpi'),
            self.define('HPXLocal_WITH_TESTS', self.run_tests),
            self.define_from_variant(
                'HPXLocal_WITH_GENERIC_CONTEXT_COROUTINES', 'generic_coroutines'),

            self.define('ASIO_ROOT', spec['asio'].prefix),
            self.define('BOOST_ROOT', spec['boost'].prefix),
            self.define('HWLOC_ROOT', spec['hwloc'].prefix),

            self.define('HPXLocal_DATASTRUCTURES_WITH_ADAPT_STD_TUPLE', False),
            self.define('HPXLocal_WITH_UNITY_BUILD', True),
            self.define('HPXLocal_WITH_PRECOMPILED_HEADERS', True),
        ]

        # HIP support requires compiling with hipcc
        if '+rocm' in self.spec:
            args += [self.define('CMAKE_CXX_COMPILER', self.spec['hip'].hipcc)]
            if self.spec.satisfies('^cmake@3.21:'):
                args += [self.define('__skip_rocmclang', True)]

        return args
