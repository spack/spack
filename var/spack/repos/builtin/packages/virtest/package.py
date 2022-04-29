# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.pkgkit import *


class Virtest(CMakePackage):
    """Header-only unit test framework, as easy as possible to use"""

    homepage    = 'https://github.com/mattkretz/virtest'
    git         = 'https://github.com/mattkretz/virtest.git'
    maintainers = ['bernhardkaindl']

    version('master', branch='master')

    def patch(self):
        script = FileFilter('tests/CMakeLists.txt')
        script.filter(r' *\${CMAKE_CTEST_COMMAND} -V -R \${target}',
                      '${CMAKE_CTEST_COMMAND} -V -R "^${target}$"')

    def setup_run_environment(self, env):
        env.prepend_path('CPATH', self.prefix.include.vir)

    @run_after('install')
    def rename_include_for_vc_package(self):
        with working_dir(self.prefix.include):
            os.rename('vir', 'virtest')
