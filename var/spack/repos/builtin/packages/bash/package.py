# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bash(AutotoolsPackage):
    """The GNU Project's Bourne Again SHell."""

    homepage = "https://www.gnu.org/software/bash/"
    url      = "https://ftpmirror.gnu.org/bash/bash-4.4.tar.gz"

    version('5.0', sha256='b4a80f2ac66170b2913efbfb9f2594f1f76c7b1afd11f799e22035d63077fb4d')
    version('4.4.12', '7c112970cbdcadfc331e10eeb5f6aa41')
    version('4.4', '148888a7c95ac23705559b6f477dfe25')
    version('4.3', '81348932d5da294953e15d4814c74dd1')

    depends_on('ncurses')
    depends_on('readline@5.0:')

    def configure_args(self):
        spec = self.spec

        return [
            'LIBS=-lncursesw',
            '--with-curses',
            '--enable-readline',
            '--with-installed-readline={0}'.format(spec['readline'].prefix),
        ]

    def check(self):
        make('tests')

    @property
    def install_targets(self):
        args = ['install']

        if self.spec.satisfies('@4.4:'):
            args.append('install-headers')

        return args
