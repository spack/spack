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


class Ncdu(Package):
    """Ncdu is a disk usage analyzer with an ncurses interface. It is designed
    to find space hogs on a remote server where you don't have an entire
    gaphical setup available, but it is a useful tool even on regular desktop
    systems. Ncdu aims to be fast, simple and easy to use, and should be able
    to run in any minimal POSIX-like environment with ncurses installed.
    """

    homepage = "http://dev.yorhel.nl/ncdu"
    url      = "http://dev.yorhel.nl/download/ncdu-1.11.tar.gz"

    version('1.11', '9e44240a5356b029f05f0e70a63c4d12')
    version('1.10', '7535decc8d54eca811493e82d4bfab2d')
    version('1.9', '93258079db897d28bb8890e2db89b1fb')
    version('1.8', '94d7a821f8a0d7ba8ef3dd926226f7d5')
    version('1.7', '172047c29d232724cc62e773e82e592a')

    depends_on("ncurses")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-ncurses=%s' % spec['ncurses'])

        make()
        make("install")
