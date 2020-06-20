# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import llnl.util.tty as tty

from spack import *


class Umpire(CMakePackage, CudaPackage):
    """An application-focused API for memory management on NUMA & GPU
    architectures"""

    homepage = 'https://github.com/LLNL/Umpire'
    git      = 'https://github.com/LLNL/Umpire.git'

    version('develop', branch='develop', submodules='True')
    version('master', branch='master', submodules='True')
    version('2.1.0', tag='v2.1.0', submodules='True')
    version('2.0.0', tag='v2.0.0', submodules='True')
    version('1.1.0', tag='v1.1.0', submodules='True')
    version('1.0.1', tag='v1.0.1', submodules='True')
    version('1.0.0', tag='v1.0.0', submodules='True')
    version('0.3.5', tag='v0.3.5', submodules='True')
    version('0.3.4', tag='v0.3.4', submodules='True')
    version('0.3.3', tag='v0.3.3', submodules='True')
    version('0.3.2', tag='v0.3.2', submodules='True')
    version('0.3.1', tag='v0.3.1', submodules='True')
    version('0.3.0', tag='v0.3.0', submodules='True')
    version('0.2.4', tag='v0.2.4', submodules='True')
    version('0.2.3', tag='v0.2.3', submodules='True')
    version('0.2.2', tag='v0.2.2', submodules='True')
    version('0.2.1', tag='v0.2.1', submodules='True')
    version('0.2.0', tag='v0.2.0', submodules='True')
    version('0.1.4', tag='v0.1.4', submodules='True')
    version('0.1.3', tag='v0.1.3', submodules='True')

    variant('fortran', default=False, description='Build C/Fortran API')
    variant('c', default=True, description='Build C API')
    variant('numa', default=False, description='Enable NUMA support')
    variant('openmp', default=False, description='Build with OpenMP support')
    variant('deviceconst', default=False,
            description='Enables support for constant device memory')

    depends_on('cmake@3.8:', type='build')
    depends_on('cmake@3.9:', when='+cuda', type='build')

    conflicts('+numa', when='@:0.3.2')
    conflicts('~c', when='+fortran', msg='Fortran API requires C API')

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=On',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                options.append('-DCMAKE_CUDA_FLAGS:STRING={0}'.format(flag))

            if '+deviceconst' in spec:
                options.append('-DENABLE_DEVICE_CONST=On')
        else:
            options.append('-DENABLE_CUDA=Off')

        options.append('-DENABLE_C={0}'.format(
            'On' if '+c' in spec else 'Off'))

        options.append('-DENABLE_FORTRAN={0}'.format(
            'On' if '+fortran' in spec else 'Off'))

        options.append('-DENABLE_NUMA={0}'.format(
            'On' if '+numa' in spec else 'Off'))

        options.append('-DENABLE_OPENMP={0}'.format(
            'On' if '+openmp' in spec else 'Off'))

        options.append('-DENABLE_TESTS={0}'.format(
            'On' if self.run_tests else 'Off'))

        return options

    extra_install_tests = '../spack-build/bin'

    @run_after('install')
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(self.extra_install_tests)

    def _run_build_smoke_tests(self):
        """Run the build tests pulled from the install process."""
        work_dir = os.path.join(self.install_test_root,
                                self.extra_install_tests)

        allocator_benchmarks = (['Malloc/malloc', 'Malloc/free', 'ns',
                                 'Host/allocate', 'Host/deallocate',
                                 'FixedPoolHost/allocate',
                                 'FixedPoolHost/deallocate'], None)
        blt_openmp_smoke = (
            ['My thread id is', 'Num threads is', 'Max threads is'], None)
        copy_benchmarks = (['benchmark_copy/host_host', 'ns'], None)
        debuglog_benchmarks = (['benchmark_DebugLogger', 'ns'], None)
        malloc = (['99 should be 99'], None)
        strategy_example = (['Available allocators', 'HOST'], None)
        tut_copy = (['Copied source data'], None)
        tut_introspection = (
            ['Allocator used is HOST', 'size of the allocation'], None)
        tut_memset = (['Set data from HOST'], None)
        tut_move = (['Moved source data', 'HOST'], None)
        tut_reallocate = (['Reallocated data'], None)
        vector_allocator = ([''], None)

        checks = {
            # Versions 0.1.3:0.3.1 and 2.0.0:
            'malloc': malloc,
            'strategy_example': strategy_example,
            'vector_allocator': vector_allocator,

            # Versions 0.2.4:0.3.1 and 2.0.0:
            'tut_copy': tut_copy,
            'tut_introspection': tut_introspection,
            'tut_memset': tut_memset,
            'tut_move': tut_move,
            'tut_reallocate': tut_reallocate,

            # Version 0.3.3:1.0.1
            'benchmarks/allocator_benchmarks': allocator_benchmarks,
            'benchmarks/copy_benchmarks': copy_benchmarks,
            'benchmarks/debuglog_benchmarks': debuglog_benchmarks,
            'benchmarks/blt_openmp_smoke': blt_openmp_smoke,

            # Versions 0.3.3:1.1.0
            'examples/malloc': malloc,
            'examples/strategy_example': strategy_example,
            'examples/vector_allocator': vector_allocator,

            'examples/tutorial/tut_copy': tut_copy,
            'examples/tutorial/tut_introspection': tut_introspection,
            'examples/tutorial/tut_memset': tut_memset,
            'examples/tutorial/tut_move': tut_move,
            'examples/tutorial/tut_reallocate': tut_reallocate,

            # Versions 1.1.0:
            'allocator_benchmarks': allocator_benchmarks,
            'copy_benchmarks': copy_benchmarks,
            'debuglog_benchmarks': debuglog_benchmarks,
            'blt_openmp_smoke': blt_openmp_smoke,
        }

        has_bad_strategy = self.spec.satisfies('@0.2.0:0.2.3')
        for exe in checks:
            if exe == 'strategy_example' and has_bad_strategy:
                # Skip this test until install testing can properly capture
                # the abort associated with this version.
                # (An umpire::util::Exception is thrown; status value is -6.)
                tty.warn('Skipping {0} test until Spack can handle core dump'
                         .format(exe))
                continue

            expected, status = checks[exe]
            reason = 'test {0} output'.format(exe)
            self.run_test(exe, [], expected, status, installed=False,
                          purpose=reason, skip_missing=True, work_dir=work_dir)

    def test(self):
        """Perform smoke tests on the installed package."""
        tty.warn('Expected results currently based on simple {0} builds'
                 .format(self.name))

        if not self.spec.satisfies('@0.1.3:2.1.0'):
            tty.warn('Expected results have not been confirmed for {0} {1}'
                     .format(self.name, self.spec.version))

        # Run tests pulled from the build
        self._run_build_smoke_tests()
