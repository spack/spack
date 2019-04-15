# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hpx(CMakePackage):
    """C++ runtime system for parallel and distributed applications."""

    homepage = "http://stellar.cct.lsu.edu/tag/hpx/"
    url = "https://github.com/STEllAR-GROUP/hpx/archive/1.2.1.tar.gz"

    version('1.2.1', sha256='8cba9b48e919035176d3b7bbfc2c110df6f07803256626f1dad8d9dde16ab77a')
    version('1.2.0', sha256='20942314bd90064d9775f63b0e58a8ea146af5260a4c84d0854f9f968077c170')
    version('1.1.0', sha256='1f28bbe58d8f0da600d60c3a74a644d75ac777b20a018a5c1c6030a470e8a1c9')

    version('1.0.0', '4983e7c6402417ec794d40343e36e417', url='http://stellar.cct.lsu.edu/files/hpx_1.0.0')

    variant(
        'malloc', default='tcmalloc',
        description='Define which allocator will be linked in',
        values=('system', 'tcmalloc', 'jemalloc', 'tbbmalloc')
    )

    variant('instrumentation', values=any_combination_of(
        'apex', 'google_perftools', 'papi', 'valgrind'
    ), description='Add support for various kind of instrumentation')

    depends_on('boost@1.55.0:')
    depends_on('hwloc@1.6:')
    depends_on('python')
    depends_on('pkgconfig', type='build')
    depends_on('git', type='build')

    # Malloc
    depends_on('gperftools', when='malloc=tcmalloc')
    depends_on('jemalloc', when='malloc=jemalloc')
    depends_on('tbb', when='malloc=tbbmalloc')

    # Instrumentation
    depends_on('apex', when='instrumentation=apex')
    depends_on('gperftools', when='instrumentation=google_perftools')
    depends_on('papi', when='instrumentation=papi')
    depends_on('valgrind', when='instrumentation=valgrind')

    # TODO: hpx can build perfectly fine in parallel, except that each
    # TODO: process might need more than 2GB to compile. This is just the
    # TODO: most conservative approach to ensure a sane build.
    parallel = False

    def instrumentation_args(self):
        for value in self.variants['instrumentation'].values:
            if value == 'none':
                continue

            condition = 'instrumentation={0}'.format(value)
            yield '-DHPX_WITH_{0}={1}'.format(
                str(value).upper(), 'ON' if condition in self.spec else 'OFF'
            )

    def cmake_args(self):
        spec, args = self.spec, []

        # Malloc
        selected_malloc = spec.variants['malloc'].value
        args.append('-DHPX_WITH_MALLOC={0}'.format(selected_malloc))

        # Instrumentation
        args.extend(self.instrumentation_args())

        return args
