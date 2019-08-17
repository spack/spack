# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxext(AutotoolsPackage):
    """libXext - library for common extensions to the X11 protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXext"
    url      = "https://www.x.org/archive/individual/lib/libXext-1.3.3.tar.gz"

    version('1.3.3', '93f5ec084c998efbfb0befed22f9b57f')

    depends_on('libx11@1.6:')

    depends_on('xproto@7.0.13:', type='build')
    depends_on('xextproto@7.1.99:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
