# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvips(AutotoolsPackage):
    """libvips is a demand-driven, horizontally threaded image processing
    library. Compared to similar libraries, libvips runs quickly and uses
    little memory."""

    homepage = "https://libvips.github.io/libvips/"
    url      = "https://github.com/libvips/libvips/releases/download/v8.9.0/vips-8.9.0.tar.gz"
    git      = "https://github.com/libvips/libvips.git"

    version('develop', branch='master')
    version('8.9.0', sha256="97334a5e70aff343d2587f23cb8068fc846a58cd937c89a446142ccf00ea0349")
    version('8.7.4', sha256="ce7518a8f31b1d29a09b3d7c88e9852a5a2dcb3ee1501524ab477e433383f205")

    # Necessary dependencies
    depends_on('glib')
    depends_on('expat')

    # Optional, split into variants!
    depends_on('gobject-introspection')
    depends_on('swig',when='@develop')
    depends_on('libjpeg')
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

