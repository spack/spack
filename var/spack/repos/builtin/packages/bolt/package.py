# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Bolt(CMakePackage):
    """BOLT targets a high-performing OpenMP implementation,
    especially specialized for fine-grain parallelism. Unlike other
    OpenMP implementations, BOLT utilizes a lightweight threading
    model for its underlying threading mechanism. It currently adopts
    Argobots, a new holistic, low-level threading and tasking runtime,
    in order to overcome shortcomings of conventional OS-level
    threads. The current BOLT implementation is based on the OpenMP
    runtime in LLVM, and thus it can be used with LLVM/Clang, Intel
    OpenMP compiler, and GCC."""

    homepage = "https://www.bolt-omp.org/"
    url      = "https://github.com/pmodels/bolt/releases/download/v1.0b1/bolt-1.0b1.tar.gz"
    git      = "https://github.com/pmodels/bolt.git"
    maintainers = ['shintaro-iwasaki']

    version("main", branch="main")
    version("2.0", sha256="f84b6a525953edbaa5d28748ef3ab172a3b6f6899b07092065ba7d1ccc6eb5ac")
    version("1.0.1", sha256="769e30dfc4042cee7ebbdadd23cf08796c03bcd8b335f516dc8cbc3f8adfa597")
    version("1.0", sha256="1c0d2f75597485ca36335d313a73736594e75c8a36123c5a6f54d01b5ba5c384")

    test_requires_compiler = True

    depends_on('argobots')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DLIBOMP_USE_ARGOBOTS=on',
            '-DLIBOMP_ARGOBOTS_INSTALL_DIR=' + spec['argobots'].prefix
        ]

        return options

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(['examples'])

    def run_sample_nested_example(self):
        """Run stand alone test: sample_nested"""

        test_dir = join_path(self.test_suite.current_test_cache_dir, 'examples')

        if not os.path.exists(test_dir):
            print('Skipping bolt test')
            return

        exe = 'sample_nested'

        # TODO: Either change to use self.compiler.cc (so using the build-time compiler)
        #  or add test parts that compile with the different supported compilers.
        self.run_test('gcc',
                      options=['-lomp', '-o', exe,
                               '-L{0}'.format(join_path(self.prefix, 'lib')),
                               '{0}'.format(join_path(test_dir, 'sample_nested.c'))],
                      purpose='test: compile {0} example'.format(exe),
                      work_dir=test_dir)

        self.run_test(exe,
                      purpose='test: run {0} example'.format(exe),
                      work_dir=test_dir)

    def test(self):
        print("Running bolt test")
        self.run_sample_nested_example()
