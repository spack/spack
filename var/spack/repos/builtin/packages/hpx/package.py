# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hpx(CMakePackage, CudaPackage):
    """C++ runtime system for parallel and distributed applications."""

    homepage = "http://stellar.cct.lsu.edu/tag/hpx/"
    url = "https://github.com/STEllAR-GROUP/hpx/archive/1.2.1.tar.gz"
    maintainers = ['msimberg', 'albestro']

    version('master', git='https://github.com/STEllAR-GROUP/hpx.git', branch='master')
    version('stable', git='https://github.com/STEllAR-GROUP/hpx.git', tag='stable')
    version('1.4.1', sha256='965dabe44d17480e326d92da4eec56722d98b33943c53d2b0f8f4655cb208023')
    version('1.4.0', sha256='241a1c47fafba751848fac12446e7bf4ad3d342d5eb2fa1ef94dd904acc329ed')
    version('1.3.0', sha256='cd34da674064c4cc4a331402edbd65c5a1f8058fb46003314ca18fa08423c5ad')
    version('1.2.1', sha256='8cba9b48e919035176d3b7bbfc2c110df6f07803256626f1dad8d9dde16ab77a')
    version('1.2.0', sha256='20942314bd90064d9775f63b0e58a8ea146af5260a4c84d0854f9f968077c170')
    version('1.1.0', sha256='1f28bbe58d8f0da600d60c3a74a644d75ac777b20a018a5c1c6030a470e8a1c9')

    variant('cxxstd',
            default='17',
            values=('11', '14', '17'),
            description='Use the specified C++ standard when building.')

    variant(
        'malloc', default='tcmalloc',
        description='Define which allocator will be linked in',
        values=('system', 'tcmalloc', 'jemalloc', 'tbbmalloc')
    )

    variant('max_cpu_count', default='64',
            description='Max number of OS-threads for HPX applications',
            values=lambda x: isinstance(x, str) and x.isdigit())

    variant('instrumentation', values=any_combination_of(
        'apex', 'google_perftools', 'papi', 'valgrind'
    ), description='Add support for various kind of instrumentation')

    variant(
        "networking",
        values=any_combination_of("tcp", "mpi").with_default("tcp"),
        description="Support for networking through parcelports",
    )

    variant('tools', default=False, description='Build HPX tools')
    variant('examples', default=False, description='Build examples')

    depends_on('hwloc')
    depends_on('python', type=('build', 'test', 'run'))
    depends_on('pkgconfig', type='build')
    depends_on('git', type='build')

    # Recommended dependency versions for 1.2.X
    depends_on('cmake@3.9.0:', when='@:1.2.1', type='build')
    depends_on('boost@1.62.0:', when='@:1.2.1')
    depends_on('hwloc@1.11:', when='@:1.2.1')

    # Recommended dependency versions before 1.2
    depends_on('boost@1.55.0:', when='@:1.1.0')
    depends_on('hwloc@1.6:', when='@:1.1.0')

    # CXX Standard
    depends_on('boost cxxstd=11', when='cxxstd=11')
    depends_on('boost cxxstd=14', when='cxxstd=14')
    depends_on('boost cxxstd=17', when='cxxstd=17')
    depends_on('boost cxxstd=17', when='@stable')

    # Malloc
    depends_on('gperftools', when='malloc=tcmalloc')
    depends_on('jemalloc', when='malloc=jemalloc')
    depends_on('tbb', when='malloc=tbbmalloc')

    # MPI
    depends_on('mpi', when='networking=mpi')

    # Instrumentation
    depends_on('otf2', when='instrumentation=apex')
    depends_on('gperftools', when='instrumentation=google_perftools')
    depends_on('papi', when='instrumentation=papi')
    depends_on('valgrind', when='instrumentation=valgrind')

    # Patches APEX
    patch('git_external.patch', when='@1.3.0 instrumentation=apex')

    def cxx_standard(self):
        value = self.spec.variants['cxxstd'].value
        return '-DHPX_WITH_CXX{0}=ON'.format(value)

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

        # CXX Standard
        args.append(self.cxx_standard())

        # Malloc
        selected_malloc = spec.variants['malloc'].value
        args.append('-DHPX_WITH_MALLOC={0}'.format(selected_malloc))

        # Instrumentation
        args.extend(self.instrumentation_args())

        if 'instrumentation=apex' in spec:
            args += ['-DAPEX_WITH_OTF2=ON'
                     '-DOTF2_ROOT={0}'.format(spec['otf2'].prefix)]

        # Networking
        args.append('-DHPX_WITH_NETWORKING={0}'.format(
            'OFF' if 'networking=none' in spec else 'ON'
        ))
        args.append('-DHPX_WITH_PARCELPORT_TCP={0}'.format(
            'ON' if 'networking=tcp' in spec else 'OFF'
        ))
        args.append('-DHPX_WITH_PARCELPORT_MPI={0}'.format(
            'ON' if 'networking=mpi' in spec else 'OFF'
        ))

        # Cuda support
        args.append('-DHPX_WITH_CUDA={0}'.format(
            'ON' if '+cuda' in spec else 'OFF'
        ))

        # Tests
        args.append('-DHPX_WITH_TESTS={0}'.format(
            'ON' if self.run_tests else 'OFF'
        ))

        # Tools
        args.append('-DHPX_WITH_TOOLS={0}'.format(
            'ON' if '+tools' in spec else 'OFF'
        ))

        # MAX_CPU_COUNT
        args.append('-DHPX_WITH_MAX_CPU_COUNT={0}'.format(
            spec.variants['max_cpu_count'].value
        ))

        # Examples
        args.append('-DHPX_WITH_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'
        ))

        args.extend([
            '-DBOOST_ROOT={0}'.format(spec['boost'].prefix),
            '-DHWLOC_ROOT={0}'.format(spec['hwloc'].prefix),
            '-DHPX_WITH_BOOST_ALL_DYNAMIC_LINK=ON',
            '-DBUILD_SHARED_LIBS=ON',
            '-DHPX_DATASTRUCTURES_WITH_ADAPT_STD_TUPLE=OFF'
        ])

        return args
