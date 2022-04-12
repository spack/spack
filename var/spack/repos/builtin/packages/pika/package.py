# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack import *


class Pika(CMakePackage, CudaPackage, ROCmPackage):
    """C++ runtime system for parallellism and concurrency."""

    homepage = "https://github.com/pika-org/pika/"
    url = "https://github.com/pika-org/pika/archive/0.0.0.tar.gz"
    maintainers = ['msimberg', 'albestro', 'teonnik', 'aurianer']

    version('0.3.0', sha256='bbb89f9824c58154ed59e2e14276c0ad132fd7b90b2be64ddd0e284f3b57cc0f')
    version('0.2.0', sha256='712bb519f22bdc9d5ee4ac374d251a54a0af4c9e4e7f62760b8ab9a177613d12')
    version('0.1.0', sha256='aa0ae2396cd264d821a73c4c7ecb118729bb3de042920c9248909d33755e7327')
    version('main', git='https://github.com/pika-org/pika.git', branch='main')

    generator = 'Ninja'

    map_cxxstd = lambda cxxstd: '2a' if cxxstd == '20' else cxxstd
    cxxstds = ('17', '20')
    variant('cxxstd',
            default='17',
            values=cxxstds,
            description='Use the specified C++ standard when building')

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
                    ' context switch implementation')

    variant('examples', default=False, description='Build and install examples')
    variant('mpi', default=False, description='Enable MPI support')
    variant('apex', default=False, description='Enable APEX support', when='@0.2:')

    # Build dependencies
    depends_on('git', type='build')
    depends_on('ninja', type='build')
    depends_on('cmake@3.18:', type='build')

    conflicts('%gcc@:6')
    conflicts('%clang@:6')
    # Pika is requiring the std::filesystem support starting from version 0.2.0
    conflicts('%gcc@:8', when='@0.2:')
    conflicts('%clang@:8', when='@0.2:')

    # Other dependecies
    depends_on('hwloc@1.11.5:')
    depends_on('boost@1.71:')

    depends_on('gperftools', when='malloc=tcmalloc')
    depends_on('jemalloc', when='malloc=jemalloc')
    depends_on('tbb', when='malloc=tbbmalloc')

    depends_on('mpi', when='+mpi')
    depends_on('cuda@11:', when='+cuda')
    depends_on('apex', when='+apex')
    depends_on('hipblas', when='+rocm')

    for cxxstd in cxxstds:
        depends_on(
            "boost cxxstd={0}".format(map_cxxstd(cxxstd)),
            when="cxxstd={0}".format(cxxstd)
        )

    # COROUTINES
    # ~generic_coroutines conflict is not fully implemented
    # for additional information see:
    # https://github.com/spack/spack/pull/17654
    # https://github.com/STEllAR-GROUP/hpx/issues/4829
    depends_on('boost+context', when='+generic_coroutines')
    depends_on('boost+atomic+chrono+thread', when='@:0.3.0+generic_coroutines')
    _msg_generic_coroutines = 'This platform requires +generic_coroutines'
    conflicts('~generic_coroutines', when='platform=darwin', msg=_msg_generic_coroutines)

    # Patches
    patch('transform_mpi_includes.patch', when="@0.3.0 +mpi")

    def cmake_args(self):
        spec, args = self.spec, []

        args += [
            self.define('PIKA_WITH_CXX_STANDARD', spec.variants['cxxstd'].value),
            self.define_from_variant('PIKA_WITH_EXAMPLES', 'examples'),
            self.define_from_variant('PIKA_WITH_MALLOC', 'malloc'),
            self.define_from_variant('PIKA_WITH_CUDA', 'cuda'),
            self.define_from_variant('PIKA_WITH_HIP', 'rocm'),
            self.define_from_variant('PIKA_WITH_MPI', 'mpi'),
            self.define_from_variant('PIKA_WITH_APEX', 'apex'),
            self.define('PIKA_WITH_TESTS', self.run_tests),
            self.define_from_variant(
                'PIKA_WITH_GENERIC_CONTEXT_COROUTINES', 'generic_coroutines'),

            self.define('BOOST_ROOT', spec['boost'].prefix),
            self.define('HWLOC_ROOT', spec['hwloc'].prefix),
        ]

        # HIP support requires compiling with hipcc
        if '+rocm' in self.spec:
            args += [self.define('CMAKE_CXX_COMPILER', self.spec['hip'].hipcc)]
            if self.spec.satisfies('^cmake@3.21:'):
                args += [self.define('__skip_rocmclang', True)]

        return args
