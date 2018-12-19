# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Editres(AutotoolsPackage):
    """Dynamic resource editor for X Toolkit applications."""

    homepage = "http://cgit.freedesktop.org/xorg/app/editres"
    url      = "https://www.x.org/archive/individual/app/editres-1.0.6.tar.gz"

    version('1.0.6', '310c504347ca499874593ac96e935353')

    depends_on('libxaw')
    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxmu')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
