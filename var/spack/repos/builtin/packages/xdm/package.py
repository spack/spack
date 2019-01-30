# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xdm(AutotoolsPackage):
    """X Display Manager / XDMCP server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xdm"
    url      = "https://www.x.org/archive/individual/app/xdm-1.1.11.tar.gz"

    version('1.1.11', 'aaf8c3d05d4a1e689d2d789c99a6023c')

    depends_on('libxmu')
    depends_on('libx11')
    depends_on('libxau')
    depends_on('libxinerama')
    depends_on('libxft')
    depends_on('libxpm')
    depends_on('libxaw')
    depends_on('libxdmcp')
    depends_on('libxt')
    depends_on('libxext')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
