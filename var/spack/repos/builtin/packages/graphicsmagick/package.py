# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
