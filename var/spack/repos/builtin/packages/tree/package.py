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
