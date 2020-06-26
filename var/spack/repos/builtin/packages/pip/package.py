# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pip(AutotoolsPackage):
    """Process-in-Process"""

    homepage = "https://github.com/RIKEN-SysSoft/PiP"
    git      = "https://github.com/RIKEN-SysSoft/PiP.git"

    version('1', branch='pip-1')

    depends_on('pip-glibc', type=('build', 'link', 'run'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check(self):
        make('check')  # TODO: replace with 'install-test'

    def configure_args(self):
        spec = self.spec
        glibc_prefix = spec['pip-glibc'].prefix
        glibc_dir = join_path(join_path(glibc_prefix, 'pip-glibc'), 'lib')
        args = ['--with-glibc-libdir=%s' % glibc_dir]
        return args

    def install(self, spec, prefix):
        bash = which('bash')
        make('install')
        make('doxygen-install')  # installing already-doxygen-ed man pages
        bash('%s/bin/piplnlibs' % prefix)
