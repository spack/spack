# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvips(AutotoolsPackage):
    """A fast image processing library with low memory needs."""

    homepage = "https://libvips.github.io/libvips/"
    url      = "https://github.com/libvips/libvips/releases/download/v8.7.4/vips-8.7.4.tar.gz"
    git      = "https://github.com/libvips/libvips.git"

    version('develop', branch='master')
    version('8.7.4',sha256 = 'ce7518a8f31b1d29a09b3d7c88e9852a5a2dcb3ee1501524ab477e433383f205')

    depends_on('glib')
    depends_on('gobject-introspection')
    depends_on('expat')
    depends_on('swig',when='@develop')
    depends_on('libjpeg')
    #depends_on('giflib')
    depends_on('libtiff')
    depends_on('poppler')
    depends_on('libtiff')
    depends_on('fftw')
    depends_on('lcms')
    depends_on('libpng')

    def configure_args(self):
        args = []
        args.append('--enable-gtk-doc=no')
        return args

