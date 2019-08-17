# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
