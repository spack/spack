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


class Rgb(AutotoolsPackage):
    """X color name database.

    This package includes both the list mapping X color names to RGB values
    (rgb.txt) and, if configured to use a database for color lookup, the
    rgb program to convert the text file into the binary database format.

    The "others" subdirectory contains some alternate color databases."""

    homepage = "http://cgit.freedesktop.org/xorg/app/rgb"
    url      = "https://www.x.org/archive/individual/app/rgb-1.0.6.tar.gz"

    version('1.0.6', '9759d058108f39066bbdf1d5d6de048c')

    depends_on('xorg-server')

    depends_on('xproto', type='build')
