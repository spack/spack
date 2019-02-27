# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvips(AutotoolsPackage):
    """A fast image processing library with low memory needs."""

    homepage = "https://libvips.github.io/libvips/"
    git      = "https://github.com/libvips/libvips.git"

    version('8.7,4', tag='v8.7.4')

    depends_on('swig')
    depends_on('gobject-introspection')
    #depends_on('gtk-doc')

