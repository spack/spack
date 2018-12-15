# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Tree(Package):
    """Tree is a recursive directory listing command that produces a depth
       indented listing of files, which is colorized ala dircolors if
       the LS_COLORS environment variable is set and output is to
       tty. Tree has been ported and reported to work under the
       following operating systems: Linux, FreeBSD, OS X, Solaris,
       HP/UX, Cygwin, HP Nonstop and OS/2."""

    homepage = "http://mama.indstate.edu/users/ice/tree/"
    url      = "http://mama.indstate.edu/users/ice/tree/src/tree-1.7.0.tgz"

    version('1.7.0', 'abe3e03e469c542d8e157cdd93f4d8a6')

    def install(self, spec, prefix):
        objs = [
            'tree.o',
            'unix.o',
            'html.o',
            'xml.o',
            'json.o',
            'hash.o',
            'color.o'
        ]
        if (sys.platform == 'darwin'):
            objs.append('strverscmp.o')

        args = [
            'prefix=%s' % prefix,
            'CC=%s' % spack_cc,
            'CFLAGS=',
            'OBJS=%s' % ' '.join(objs),
            'install'
        ]

        make(*args)
