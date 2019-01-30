# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxau(AutotoolsPackage):
    """The libXau package contains a library implementing the X11
    Authorization Protocol. This is useful for restricting client
    access to the display."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXau/"
    url      = "https://www.x.org/archive/individual/lib/libXau-1.0.8.tar.gz"

    version('1.0.8', 'a85cd601d82bc79c0daa280917572e20')

    depends_on('xproto', type=('build', 'link'))
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
