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

from spack import *


class Gdb(Package):
    """
    GDB, the GNU Project debugger, allows you to see what is going on `inside' another program while it executes
    -- or what another program was doing at the moment it crashed.
    """
    homepage = "https://www.gnu.org/software/gdb"
    url = "http://ftp.gnu.org/gnu/gdb/gdb-7.10.tar.gz"

    version('7.11', 'f585059252836a981ea5db9a5f8ce97f')
    version('7.10.1', 'b93a2721393e5fa226375b42d567d90b')
    version('7.10', 'fa6827ad0fd2be1daa418abb11a54d86')
    version('7.9.1', 'f3b97de919a9dba84490b2e076ec4cb0')
    version('7.9', '8f8ced422fe462a00e0135a643544f17')
    version('7.8.2', '8b0ea8b3559d3d90b3ff4952f0aeafbc')

    depends_on('texinfo')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
