##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Gdb(Package):
    """
    GDB, the GNU Project debugger, allows you to see what is going on `inside' another program while it executes
    -- or what another program was doing at the moment it crashed.
    """
    homepage = "https://www.gnu.org/software/gdb"
    url = "http://ftp.gnu.org/gnu/gdb/gdb-7.10.tar.xz"

    version('7.10.1', '39e654460c9cdd80200a29ac020cfe11')
    version('7.10', '2a35bac41fa8e10bf04f3a0dd7f7f363')
    version('7.9.1', '35374c77a70884eb430c97061053a36e')
    version('7.9', 'e6279f26559d839f0b4218a482bcb43e')
    version('7.8.2', 'a80cf252ed2e775d4e4533341bbf2459')

    depends_on('texinfo')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
