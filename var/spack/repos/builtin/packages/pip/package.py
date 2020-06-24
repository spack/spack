# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pip(Package):
    """Process-in-Process"""

    homepage = "https://github.com/RIKEN-SysSoft/PiP"
    git      = "https://github.com/RIKEN-SysSoft/PiP.git"

    version('1', branch='pip-1')

    depends_on('pip-glibc', type=('build'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check(self):
        make('check')  # TODO: replace with 'install-test'

        args = []
        return args

    def install(self, spec, prefix):
        bash = which('bash')
        configure('--prefix=%s' % prefix,
                  '--with-glibc-libdir=%s' % spec['pip-glibc'].prefix.lib)
        make()
        make('install')
        make('doxygen-install')  # installing already-doxygen-ed man pages
        bash('%s/bin/piplnlibs' % prefix)
