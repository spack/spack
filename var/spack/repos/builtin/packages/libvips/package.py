# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvips(AutotoolsPackage):
    """A fast image processing library with low memory needs."""

    homepage = "https://libvips.github.io/libvips/"
    git      = "https://github.com/libvips/libvips.git"

    version('8.7,4', sha256='ce7518a8f31b1d29a09b3d7c88e9852a5a2dcb3ee1501524ab477e433383f205')

    depends_on('swig')
    depends_on('gobject-introspection')
    #depends_on('gtk-doc')

