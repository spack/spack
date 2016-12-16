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


class Pngwriter(Package):
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

    version('dev', branch='dev',
            git='https://github.com/pngwriter/pngwriter.git')
    version('master', branch='master',
            git='https://github.com/pngwriter/pngwriter.git')
    version('0.5.6', 'c13bd1fdc0e331a246e6127b5f262136')

    depends_on('cmake', type='build')
    depends_on('libpng')
    depends_on('zlib')
    depends_on('freetype')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('-DCMAKE_INSTALL_PREFIX=%s' % prefix,
                  '..', *std_cmake_args)

            make()
            make('install')
