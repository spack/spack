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


class Xfsinfo(AutotoolsPackage):
    """xfsinfo is a utility for displaying information about an X font
    server.  It is used to examine the capabilities of a server, the
    predefined values for various parameters used in communicating between
    clients and the server, and the font catalogues and alternate servers
    that are available."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfsinfo"
    url      = "https://www.x.org/archive/individual/app/xfsinfo-1.0.5.tar.gz"

    version('1.0.5', '36b64a3f37b87c759c5d17634e129fb9')

    depends_on('libfs')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
