# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pngwriter(CMakePackage):
    """PNGwriter is a very easy to use open source graphics library that uses
    PNG as its output format. The interface has been designed to be as simple
    and intuitive as possible. It supports plotting and reading pixels in the
    RGB (red, green, blue), HSV (hue, saturation, value/brightness) and CMYK
    (cyan, magenta, yellow, black) colour spaces, basic shapes, scaling,
    bilinear interpolation, full TrueType antialiased and rotated text support,
    bezier curves, opening existing PNG images and more.
    """

    homepage = "http://pngwriter.sourceforge.net/"
    url      = "https://github.com/pngwriter/pngwriter/archive/0.5.6.tar.gz"
    git      = "https://github.com/pngwriter/pngwriter.git"

    maintainers = ['ax3l']

    version('develop', branch='dev')
    version('master', branch='master')
    version('0.7.0', 'a68aa0889f120f5bb07848afce278a95')
    version('0.6.0', '0a19bc55c5f6379fea7343752fd3ffae')
    version('0.5.6', 'c13bd1fdc0e331a246e6127b5f262136')

    depends_on('libpng')
    depends_on('zlib')
    depends_on('freetype')

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('@0.7.0:'):
            args += ['-DPNGwriter_USE_FREETYPE:BOOL=ON']

        return args
