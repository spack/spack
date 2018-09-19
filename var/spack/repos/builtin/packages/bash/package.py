##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Bash(AutotoolsPackage):
    """The GNU Project's Bourne Again SHell."""

    homepage = "https://www.gnu.org/software/bash/"
    url      = "https://ftpmirror.gnu.org/bash/bash-4.4.tar.gz"

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
