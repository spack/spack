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
import sys


class Pixman(Package):
    """The Pixman package contains a library that provides low-level
    pixel manipulation features such as image compositing and
    trapezoid rasterization."""

    homepage = "http://www.pixman.org"
    url      = "http://cairographics.org/releases/pixman-0.32.6.tar.gz"

    version('0.34.0', 'e80ebae4da01e77f68744319f01d52a3')
    version('0.32.6', '3a30859719a41bd0f5cccffbfefdd4c2')

    depends_on('pkg-config', type='build')
    depends_on('libpng')

    def install(self, spec, prefix):
        config_args = ["--prefix=" + prefix,
                       "--disable-gtk"]

        if sys.platform == "darwin":
            config_args.append("--disable-mmx")

        configure(*config_args)

        make()
        make('check')
        make('install')
