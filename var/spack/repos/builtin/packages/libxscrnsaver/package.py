# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxscrnsaver(AutotoolsPackage):
    """XScreenSaver - X11 Screen Saver extension client library"""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXScrnSaver"
    url      = "https://www.x.org/archive/individual/lib/libXScrnSaver-1.2.2.tar.gz"

    version('1.2.2', '79227e7d8c0dad27654c526de3d6fef3')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('scrnsaverproto@1.2:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
