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


class Readline(AutotoolsPackage):
    """The GNU Readline library provides a set of functions for use by
    applications that allow users to edit command lines as they are typed in.
    Both Emacs and vi editing modes are available. The Readline library
    includes additional functions to maintain a list of previously-entered
    command lines, to recall and perhaps reedit those lines, and perform
    csh-like history expansion on previous commands."""

    homepage = "http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html"
    url      = "https://ftpmirror.gnu.org/readline/readline-7.0.tar.gz"

    version('7.0', '205b03a87fc83dab653b628c59b9fc91')
    version('6.3', '33c8fb279e981274f485fd91da77e94a')

    depends_on('ncurses')
    # from url=http://www.linuxfromscratch.org/patches/downloads/readline/readline-6.3-upstream_fixes-1.patch
    # this fixes a bug that could lead to seg faults in ipython
    patch('readline-6.3-upstream_fixes-1.patch', when='@6.3')

    def build(self, spec, prefix):
        options = [
            'SHLIB_LIBS=-L{0} -lncursesw'.format(spec['ncurses'].prefix.lib)
        ]

        make(*options)
