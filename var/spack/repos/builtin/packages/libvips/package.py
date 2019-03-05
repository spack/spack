# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvips(AutotoolsPackage):
    """A fast image processing library with low memory needs."""

    homepage = "https://libvips.github.io/libvips/"
    url      = "https://github.com/libvips/libvips/archive/v8.7.4.tar.gz"
    git      = "https://github.com/libvips/libvips.git"

    version('8.7.4', tag='v8.7.4')

    depends_on('glib')
    depends_on('expat')
    depends_on('libjpeg')
    depends_on('giflib')
    depends_on('libtiff')
    depends_on('poppler')
    depends_on('libtiff')
    depends_on('fftw')
    depends_on('lcms')
    depends_on('libpng')
