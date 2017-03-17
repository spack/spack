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
import sys


class Libdrm(Package):
    """A userspace  library for  accessing the  DRM, direct
    rendering  manager, on  Linux,  BSD and  other  operating
    systems that support the  ioctl interface."""

    homepage = "http://dri.freedesktop.org/libdrm/"
    url      = "http://dri.freedesktop.org/libdrm/libdrm-2.4.59.tar.gz"

    version('2.4.70', 'a8c275bce5f3d71a5ca25e8fb60df084')
    version('2.4.59', '105ac7af1afcd742d402ca7b4eb168b6')
    version('2.4.33', '86e4e3debe7087d5404461e0032231c8')

    depends_on('libpciaccess@0.10:', when=(sys.platform != 'darwin'))
    depends_on('libpthread-stubs')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix),
                  '--enable-static',
                  'LIBS=-lrt')  # This fixes a bug with `make check`

        make()
        make('check')
        make('install')
