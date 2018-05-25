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


class Mosh(AutotoolsPackage):
    """Remote terminal application that allows roaming, supports intermittent
    connectivity, and provides intelligent local echo and line editing of user
    keystrokes. Mosh is a replacement for SSH. It's more robust and responsive,
    especially over Wi-Fi, cellular, and long-distance links.
    """

    homepage = "https://mosh.org/"
    url      = "https://mosh.org/mosh-1.2.6.tar.gz"

    version('1.3.2', '5122f4d2b973ab7c38dcdac8c35cb61e')
    version('1.3.0', 'd961276995936953bf2d5a794068b076')
    version('1.2.6', 'bb4e24795bb135a754558176a981ee9e')

    depends_on('protobuf')
    depends_on('ncurses')
    depends_on('zlib')
    depends_on('openssl')

    depends_on('pkgconfig', type='build')
    depends_on('perl', type='run')

    build_directory = 'spack-build'
