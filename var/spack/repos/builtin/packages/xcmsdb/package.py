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


class Xcmsdb(AutotoolsPackage):
    """xcmsdb is used to load, query, or remove Device Color Characterization
    data stored in properties on the root window of the screen as
    specified in section 7, Device Color Characterization, of the
    X11 Inter-Client Communication Conventions Manual (ICCCM)."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xcmsdb"
    url      = "https://www.x.org/archive/individual/app/xcmsdb-1.0.5.tar.gz"

    version('1.0.5', 'e7b1699c831b44d7005bff45977ed56a')

    depends_on('libx11')

    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
