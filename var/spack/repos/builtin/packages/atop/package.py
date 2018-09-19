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


class Atop(Package):
    """Atop is an ASCII full-screen performance monitor for Linux"""
    homepage = "http://www.atoptool.nl/index.php"
    url      = "http://www.atoptool.nl/download/atop-2.2-3.tar.gz"

    version('2.2-3', '034dc1544f2ec4e4d2c739d320dc326d')

    depends_on('zlib')
    depends_on('ncurses')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install("atop", join_path(prefix.bin, "atop"))
        mkdirp(join_path(prefix.man, "man1"))
        install(join_path("man", "atop.1"),
                join_path(prefix.man, "man1", "atop.1"))
