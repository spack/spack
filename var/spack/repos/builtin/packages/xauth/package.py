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


class Xauth(AutotoolsPackage):
    """The xauth program is used to edit and display the authorization
    information used in connecting to the X server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xauth"
    url      = "https://www.x.org/archive/individual/app/xauth-1.0.9.tar.gz"

    version('1.0.9', 'def3b4588504ee3d8ec7be607826df02')

    depends_on('libx11')
    depends_on('libxau')
    depends_on('libxext')
    depends_on('libxmu')

    depends_on('xproto@7.0.17:')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')

    # TODO: add package for cmdtest test dependency
