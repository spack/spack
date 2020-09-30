# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import llnl.util.lang as lang
import llnl.util.tty as tty

from spack import *


class Umpire(CMakePackage, CudaPackage):
    """An application-focused API for memory management on NUMA & GPU
    architectures"""

    homepage = 'https://github.com/LLNL/Umpire'
    git      = 'https://github.com/LLNL/Umpire.git'

    version('develop', branch='develop', submodules='True')
    version('main', branch='main', submodules='True')
    version('4.0.1', tag='v4.0.1', submodules='True')
    version('4.0.0', tag='v4.0.0', submodules='True')
    version('3.0.0', tag='v3.0.0', submodules='True')
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

    patch('camp_target_umpire_3.0.0.patch', when='@3.0.0')

    variant('fortran', default=False, description='Build C/Fortran API')
    variant('c', default=True, description='Build C API')
    variant('numa', default=False, description='Enable NUMA support')
    variant('shared', default=True, description='Enable Shared libs')
    variant('openmp', default=False, description='Build with OpenMP support')
    variant('deviceconst', default=False,
            description='Enables support for constant device memory')
    variant('examples', default=True, description='Build Umpire Examples')
    variant('tests', default='none', values=('none', 'basic', 'benchmarks'),
            multi=False, description='Tests to run')

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
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
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

        options.append('-DBUILD_SHARED_LIBS={0}'.format(
            'On' if '+shared' in spec else 'Off'))

        options.append('-DENABLE_BENCHMARKS={0}'.format(
            'On' if 'tests=benchmarks' in spec else 'Off'))

        options.append('-DENABLE_EXAMPLES={0}'.format(
            'On' if '+examples' in spec else 'Off'))

        options.append('-DENABLE_TESTS={0}'.format(
            'Off' if 'tests=none' in spec else 'On'))

        return options

    extra_install_tests = '../spack-build/bin'

    @run_after('install')
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(self.extra_install_tests)

    @property
    @lang.memoized
    def _extra_tests_path(self):
        return os.path.join(self.install_test_root, self.extra_install_tests)

    @property
    @lang.memoized
    def _has_bad_strategy(self):
        return self.spec.satisfies('@0.2.0:0.2.3')

    def _run_checks(self, dirs, checks):
        """Run the specified checks in the provided directories."""

        if not dirs or not checks:
            return

        for exe in checks:
            if exe == 'strategy_example' and self._has_bad_strategy:
                # Skip this test until install testing can properly capture
                # the abort associated with this version.
                # (An umpire::util::Exception is thrown; status value is -6.)
                tty.warn('Skipping {0} test until Spack can handle core dump'
                         .format(exe))
                continue

            expected, status = checks[exe]
            for work_dir in dirs:
                src = 'from build ' if 'spack-build' in work_dir else ''
                reason = 'test {0} {1}output'.format(exe, src)
                self.run_test(exe, [], expected, status, installed=False,
                              purpose=reason, skip_missing=True,
                              work_dir=work_dir)

    def _run_bench_checks(self):
        """Run the benchmark smoke test checks."""
        tty.info('Running benchmark checks')

        dirs = []
        if self.spec.satisfies('@0.3.3:1.0.1'):
            dirs.append(os.path.join(self._extra_tests_path, 'benchmarks'))
        elif self.spec.satisfies('@1.1.0:'):
            dirs.append(self.prefix.bin)

        checks = {
            # Versions 0.3.3:1.0.1  (spack-build/bin/benchmarks)
            # Versions 1.1.0:2.1.0  (spack-build/bin)
            'allocator_benchmarks': (
                ['Malloc/malloc', 'Malloc/free', 'ns',
                 'Host/allocate', 'Host/deallocate',
                 'FixedPoolHost/allocate',
                 'FixedPoolHost/deallocate'], 0),
            'copy_benchmarks': (['benchmark_copy/host_host', 'ns'], 0),
            'debuglog_benchmarks': (['benchmark_DebugLogger', 'ns'], 0),
        }
        self._run_checks(dirs, checks)

    def _run_cookbook_checks(self):
        """Run the cookbook smoke test checks."""
        tty.info('Running cookbook checks')

        dirs = []
        cb_subdir = os.path.join('examples', 'cookbook')
        if self.spec.satisfies('@0.3.3:1.0.1'):
            dirs.append(os.path.join(self._extra_tests_path, cb_subdir))
        elif self.spec.satisfies('@1.1.0'):
            dirs.append(os.path.join(self.prefix.bin, cb_subdir))
        elif self.spec.satisfies('@2.0.0:'):
            dirs.append(self.prefix.bin)

        checks = {
            # Versions 0.3.3:1.0.1  (spack-build/bin/examples/cookbook)
            # Versions 2.0.0:2.1.0  (spack-build/bin)
            # Versions 1.1.0        (prefix.bin/examples/cookbook)
            # Versions 2.0.0:2.1.0  (prefix.bin)
            'recipe_dynamic_pool_heuristic': (['in the pool', 'releas'], 0),
            'recipe_no_introspection': (['has allocated', 'used'], 0),
        }
        self._run_checks(dirs, checks)

    def _run_example_checks(self):
        """Run the example smoke test checks."""
        tty.info('Running example checks')

        dirs = []
        if self.spec.satisfies('@0.1.3:0.3.1'):
            dirs.append(self._extra_tests_path)
        elif self.spec.satisfies('@0.3.3:1.0.1'):
            dirs.append(os.path.join(self._extra_tests_path, 'examples'))
        elif self.spec.satisfies('@1.1.0'):
            dirs.append(os.path.join(self.prefix.bin, 'examples'))
        elif self.spec.satisfies('@2.0.0:'):
            dirs.append(self.prefix.bin)

        # Check the results from a subset of the (potentially) available
        # executables
        checks = {
            # Versions 0.1.3:0.3.1  (spack-build/bin)
            # Versions 0.3.3:1.0.1  (spack-build/bin/examples)
            # Versions 2.0.0:2.1.0  (spack-build/bin)
            # Version  1.1.0        (prefix.bin/examples)
            # Versions 2.0.0:2.1.0  (prefix.bin)
            'malloc': (['99 should be 99'], 0),
            'strategy_example': (['Available allocators', 'HOST'], 0),
            'vector_allocator': ([''], 0),
        }
        self._run_checks(dirs, checks)

    def _run_plots_checks(self):
        """Run the plots smoke test checks."""
        tty.info('Running plots checks')

        dirs = [self.prefix.bin] if self.spec.satisfies('@0.3.3:0.3.5') else []
        checks = {
            # Versions 0.3.3:0.3.5  (prefix.bin)
            'plot_allocations': ([''], 0),
        }
        self._run_checks(dirs, checks)

    def _run_tools_checks(self):
        """Run the tools smoke test checks."""
        tty.info('Running tools checks')

        dirs = [self.prefix.bin] if self.spec.satisfies('@0.3.3:0.3.5') else []
        checks = {
            # Versions 0.3.3:0.3.5  (spack-build/bin/tools)
            'replay': (['No input file'], 0),
        }
        self._run_checks(dirs, checks)

    def _run_tut_checks(self):
        """Run the tutorial smoke test checks."""
        tty.info('Running tutorials checks')

        dirs = []
        tut_subdir = os.path.join('examples', 'tutorial')
        if self.spec.satisfies('@0.2.4:0.3.1'):
            dirs.append(self._extra_tests_path)
        elif self.spec.satisfies('@0.3.3:1.0.1'):
            dirs.append(os.path.join(self._extra_tests_path, tut_subdir))
        elif self.spec.satisfies('@1.1.0'):
            dirs.append(os.path.join(self.prefix.bin, tut_subdir))
        elif self.spec.satisfies('@2.0.0:'):
            dirs.append(self.prefix.bin)

        checks = {
            # Versions 0.2.4:0.3.1  (spack-build/bin)
            # Versions 0.3.3:1.0.1  (spack-build/bin/examples/tutorial)
            # Versions 2.0.0:2.1.0  (spack-build/bin)
            # Version  1.1.0        (prefix.bin/examples/tutorial)
            # Versions 2.0.0:2.1.0  (prefix.bin)
            'tut_copy': (['Copied source data'], 0),
            'tut_introspection': (
                ['Allocator used is HOST', 'size of the allocation'], 0),
            'tut_memset': (['Set data from HOST'], 0),
            'tut_move': (['Moved source data', 'HOST'], 0),
            'tut_reallocate': (['Reallocated data'], 0),
        }
        self._run_checks(dirs, checks)

    def test(self):
        """Perform smoke tests on the installed package."""
        self._run_bench_checks()
        self._run_cookbook_checks()
        self._run_example_checks()
        self._run_plots_checks()
        self._run_tools_checks()
        self._run_tut_checks()
