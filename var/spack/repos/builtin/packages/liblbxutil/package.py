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


class Liblbxutil(AutotoolsPackage):
    """liblbxutil - Low Bandwith X extension (LBX) utility routines."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/liblbxutil"
    url      = "https://www.x.org/archive/individual/lib/liblbxutil-1.1.0.tar.gz"

    version('1.1.0', '2735cd23625d4cc870ec4eb7ca272788')

    depends_on('xextproto@7.0.99.1:', type='build')
    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    # There is a bug in the library that causes the following messages:
    # undefined symbol: Xfree
    # undefined symbol: Xalloc
    # See https://bugs.freedesktop.org/show_bug.cgi?id=8421
    # Adding a dependency on libxdmcp and adding LIBS=-lXdmcp did not fix it
