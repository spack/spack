# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xsetmode(AutotoolsPackage):
    """Set the mode for an X Input device."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xsetmode"
    url      = "https://www.x.org/archive/individual/app/xsetmode-1.0.0.tar.gz"

    version('1.0.0', '0dc2a917138d0345c00e016ac720e085')

    depends_on('libxi')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
