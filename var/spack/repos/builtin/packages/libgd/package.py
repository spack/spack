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


class Libgd(AutotoolsPackage):
    """GD is an open source code library for the dynamic creation of images
       by programmers. GD is written in C, and "wrappers" are available
       for Perl, PHP and other languages. GD creates PNG, JPEG, GIF,
       WebP, XPM, BMP images, among other formats. GD is commonly used to
       generate charts, graphics, thumbnails, and most anything else, on
       the fly. While not restricted to use on the web, the most common
       applications of GD involve website development.

    """

    homepage = "https://github.com/libgd/libgd"
    url      = 'https://github.com/libgd/libgd/releases/download/gd-2.2.4/libgd-2.2.4.tar.gz'

    version('2.2.4', '0a3c307b5075edbe1883543dd1153c02')
    version('2.2.3', 'a67bd15fa33d4aac0a1c7904aed19f49')
    version('2.1.1', 'e91a1a99903e460e7ba00a794e72cc1e')

    # Build dependencies
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('gettext', type='build')
    depends_on('pkg-config', type='build')

    depends_on('libpng')
    depends_on('libtiff')
    depends_on('fontconfig')
