# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack import *


class Archer(CMakePackage):
    """ARCHER, a data race detection tool for large OpenMP applications."""

    homepage = "https://github.com/PRUNERS/ARCHER"
    url      = "https://github.com/PRUNERS/archer/archive/v1.0.0.tar.gz"

    test_requires_compiler = True

    version('2.0.0', sha256='3241cadb0078403368b69166b27f815e12c350486d4ceb3fb33147895b9ebde8')
    version('1.0.0', sha256='df814a475606b83c659932caa30a68bed1c62e713386b375c1b78eb8d60e0d15')

    depends_on('cmake@3.4.3:', type='build')
    depends_on('llvm@:8.0.0')
    depends_on('ninja@1.5:', type='build')
    depends_on('llvm-openmp-ompt@tr6_forwards')

    generator = 'Ninja'

    def patch(self):
        if self.spec.satisfies('^llvm@8.0.0:'):
            filter_file(r'add_llvm_loadable_module\(LLVMArcher',
                        'add_llvm_library(LLVMArcher MODULE',
                        'lib/CMakeLists.txt')

    def cmake_args(self):
        return [
            '-DCMAKE_C_COMPILER=clang',
            '-DCMAKE_CXX_COMPILER=clang++',
            '-DOMP_PREFIX:PATH=%s' % self.spec['llvm-openmp-ompt'].prefix,
        ]

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(['test'])

    def run_parallel_example_test(self):
        """Run stand alone test: parallel-simple"""

        test_dir = join_path(self.test_suite.current_test_cache_dir, 'test', 'parallel')

        if not os.path.exists(test_dir):
            print('Skipping archer test')
            return

        exe = 'parallel-simple'

        self.run_test('clang-archer',
                      options=['-o', exe,
                               '{0}'.format(join_path(test_dir, 'parallel-simple.c'))],
                      purpose='test: compile {0} example'.format(exe),
                      work_dir=test_dir)

        self.run_test(exe,
                      purpose='test: run {0} example'.format(exe),
                      work_dir=test_dir)

    def test(self):
        self.run_parallel_example_test()
