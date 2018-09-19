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


class Dmxproto(AutotoolsPackage):
    """Distributed Multihead X (DMX) Extension.

    This extension defines a protocol for clients to access a front-end proxy
    X server that controls multiple back-end X servers making up a large
    display."""

    homepage = "http://dmx.sourceforge.net/"
    url      = "https://www.x.org/archive/individual/proto/dmxproto-2.3.1.tar.gz"

    version('2.3.1', '7c52af95aac192e8de31bd9a588ce121')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
