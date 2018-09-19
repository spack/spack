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


class Cairo(AutotoolsPackage):
    """Cairo is a 2D graphics library with support for multiple output
    devices."""
    homepage = "http://cairographics.org"
    url      = "http://cairographics.org/releases/cairo-1.14.8.tar.xz"

    version('1.14.12', '490025a0ba0622a853010f49fb6343f29fb70b9b')
    version('1.14.8', 'c6f7b99986f93c9df78653c3e6a3b5043f65145e')
    version('1.14.0', '53cf589b983412ea7f78feee2e1ba9cea6e3ebae')

    variant('X', default=False, description="Build with X11 support")

    depends_on('libx11', when='+X')
    depends_on('libxext', when='+X')
    depends_on('libxrender', when='+X')
    depends_on('libxcb', when='+X')
    depends_on('python', when='+X', type='build')
    depends_on("libpng")
    depends_on("glib")
    depends_on("pixman")
    depends_on("freetype")
    depends_on("pkgconfig", type="build")
    depends_on("fontconfig@2.10.91:")  # Require newer version of fontconfig.

    def configure_args(self):
        args = ["--disable-trace",  # can cause problems with libiberty
                "--enable-tee"]
        if '+X' in self.spec:
            args.extend(["--enable-xlib", "--enable-xcb"])
        else:
            args.extend(["--disable-xlib", "--disable-xcb"])
        return args
