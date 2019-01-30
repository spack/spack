# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xlogo(AutotoolsPackage):
    """The xlogo program simply displays the X Window System logo."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xlogo"
    url      = "https://www.x.org/archive/individual/app/xlogo-1.0.4.tar.gz"

    version('1.0.4', '4c4f82c196a55a90800a77906f4353fb')

    depends_on('libsm')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.0:')
    depends_on('libxext')
    depends_on('libx11')
    depends_on('libxft')
    depends_on('libxrender')
    depends_on('libxt')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
