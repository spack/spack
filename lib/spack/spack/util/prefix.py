##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
"""
This file contains utilities to help with installing packages.
"""
from llnl.util.filesystem import join_path


class Prefix(str):
    """This class represents an installation prefix, but provides useful
       attributes for referring to directories inside the prefix.

       For example, you can do something like this::

           prefix = Prefix('/usr')
           print(prefix.lib)
           print(prefix.lib64)
           print(prefix.bin)
           print(prefix.share)
           print(prefix.man4)

       This program would print:

           /usr/lib
           /usr/lib64
           /usr/bin
           /usr/share
           /usr/share/man/man4

       Prefix objects behave identically to strings.  In fact, they
       subclass str.  So operators like + are legal:

           print("foobar " + prefix)

       This prints 'foobar /usr". All of this is meant to make custom
       installs easy.
    """

    def __new__(cls, path):
        s = super(Prefix, cls).__new__(cls, path)
        s.bin     = join_path(s, 'bin')
        s.sbin    = join_path(s, 'sbin')
        s.etc     = join_path(s, 'etc')
        s.include = join_path(s, 'include')
        s.lib     = join_path(s, 'lib')
        s.lib64   = join_path(s, 'lib64')
        s.libexec = join_path(s, 'libexec')
        s.share   = join_path(s, 'share')
        s.doc     = join_path(s.share, 'doc')
        s.info    = join_path(s.share, 'info')

        s.man  = join_path(s, 'man')
        s.man1 = join_path(s.man, 'man1')
        s.man2 = join_path(s.man, 'man2')
        s.man3 = join_path(s.man, 'man3')
        s.man4 = join_path(s.man, 'man4')
        s.man5 = join_path(s.man, 'man5')
        s.man6 = join_path(s.man, 'man6')
        s.man7 = join_path(s.man, 'man7')
        s.man8 = join_path(s.man, 'man8')

        s.share_man  = join_path(s.share, 'man')
        s.share_man1 = join_path(s.share_man, 'man1')
        s.share_man2 = join_path(s.share_man, 'man2')
        s.share_man3 = join_path(s.share_man, 'man3')
        s.share_man4 = join_path(s.share_man, 'man4')
        s.share_man5 = join_path(s.share_man, 'man5')
        s.share_man6 = join_path(s.share_man, 'man6')
        s.share_man7 = join_path(s.share_man, 'man7')
        s.share_man8 = join_path(s.share_man, 'man8')

        return s
