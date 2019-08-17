# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxp(AutotoolsPackage):
    """libXp - X Print Client Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXp"
    url      = "https://www.x.org/archive/individual/lib/libXp-1.0.3.tar.gz"

    version('1.0.3', '1157da663b28e110f440ce64cede6e18')

    depends_on('libx11@1.6:')
    depends_on('libxext')
    depends_on('libxau')

    depends_on('xextproto', type='build')
    depends_on('printproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
