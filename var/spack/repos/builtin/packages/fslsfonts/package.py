# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fslsfonts(AutotoolsPackage):
    """fslsfonts produces a list of fonts served by an X font server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/fslsfonts"
    url      = "https://www.x.org/archive/individual/app/fslsfonts-1.0.5.tar.gz"

    version('1.0.5', 'ef781bd6a7b529d3ed7a256055715730')

    depends_on('libfs')

    depends_on('xproto@7.0.25:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
