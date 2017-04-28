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


class Xf86miscproto(AutotoolsPackage):
    """This package includes the protocol definitions of the "XFree86-Misc"
    extension to the X11 protocol.  The "XFree86-Misc" extension is
    supported by the XFree86 X server and versions of the Xorg X server
    prior to Xorg 1.6."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/xf86miscproto"
    url      = "https://www.x.org/archive/individual/proto/xf86miscproto-0.9.3.tar.gz"

    version('0.9.3', 'c6432f04f84929c94fa05b3a466c489d')
