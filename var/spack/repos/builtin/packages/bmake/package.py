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
import re


class Bmake(Package):
    """bmake: portable BSD make

       bmake is the BSD make(1) utility ported to several non-BSD
       systems. It supports GNU's autoconf."""

    homepage = "http://www.crufty.net/FreeWare/"
    url      = "ftp://ftp.netbsd.org/pub/NetBSD/misc/sjg/bmake-20171207.tar.gz"

    version('20171207', '5d7f2f85f16c4a6ba34ceea68957447f')

    def install(self, spec, prefix):
        # Do not pre-roff cat pages
        mk_file = FileFilter('mk/man.mk')
        mk_file.filter(re.escape(r'MANTARGET?'), 'MANTARGET')

        # -DWITHOUT_PROG_LINK does not symlink bmake as
        # -"bmake-VERSION"
        sh = which('sh')
        sh('boot-strap', '--prefix={0}'.format(prefix),
           '-DWITHOUT_PROG_LINK', '--install')
        mkdirp(prefix.man1)
        install('bmake.1', join_path(prefix.man1, 'bmake.1'))
