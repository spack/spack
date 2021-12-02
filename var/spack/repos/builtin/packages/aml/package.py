# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Aml(AutotoolsPackage):
    """AML: Building Blocks for Memory Management."""

    homepage = "https://argo-aml.readthedocs.io/"
    url = "https://www.mcs.anl.gov/research/projects/argo/downloads/aml-0.1.0.tar.gz"
    git = "https://github.com/anlsys/aml.git"
    maintainers = ['perarnau']

    test_requires_compiler = True

    tags = ['e4s']

    version('0.1.0', sha256='cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b')
    version('master', branch='master', submodules=True)

    depends_on('numactl')

    with when('@master'):
        depends_on('m4', type='build')
        depends_on('autoconf', type='build')
        depends_on('automake', type='build')
        depends_on('libtool', type='build')

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(['tests', join_path('include', 'config.h')])

    def run_area_test(self):
        """Run stand alone test: test_area"""

        test_dir = join_path(self.test_suite.current_test_cache_dir, 'tests', 'area')

        if not os.path.exists(test_dir):
            print('Skipping aml test')
            return

        exe = 'test_area'

        self.run_test('gcc',
                      options=['-o', exe, join_path(test_dir, 'test_area.c'),
                               '-I{0}'.format(join_path(
                                   self.test_suite.current_test_cache_dir,
                                   'include')),
                               '-I{0}'.format(self.prefix.include),
                               '-I{0}'.format(self.spec['numactl'].prefix.include),
                               '-L{0}'.format(self.prefix.lib),
                               '-laml', '-lexcit', '-lpthread'],
                      purpose='test: compile {0} example'.format(exe),
                      work_dir=test_dir)

        self.run_test(exe,
                      purpose='test: run {0} example'.format(exe),
                      work_dir=test_dir)

    def test(self):
        self.run_area_test()
