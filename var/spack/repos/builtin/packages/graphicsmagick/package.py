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


class Graphicsmagick(AutotoolsPackage):
    """GraphicsMagick is the swiss army knife of image processing.

    Provides a robust and efficient collection of tools and libraries which
    support reading, writing, and manipulating an image in over 88 major
    formats including important formats like DPX, GIF, JPEG, JPEG-2000, PNG,
    PDF, PNM, and TIFF.
    """

    homepage = "http://www.graphicsmagick.org/"
    url      = "https://sourceforge.net/projects/graphicsmagick/files/graphicsmagick/1.3.29/GraphicsMagick-1.3.29.tar.xz/download"

    version('1.3.29', 'ddde0dd239592db50c5378472355c03c')

    depends_on('bzip2')
    depends_on('ghostscript')
    depends_on('ghostscript-fonts')
    depends_on('graphviz')
    depends_on('jasper')
    depends_on('jpeg')
    depends_on('lcms')
    depends_on('libice')
    depends_on('libpng')
    depends_on('libsm')
    depends_on('libtiff')
    depends_on('libtool')
    depends_on('libxml2')
    depends_on('xz')
    depends_on('zlib')

    def configure_args(self):
        args = ['--enable-shared']
        return args
