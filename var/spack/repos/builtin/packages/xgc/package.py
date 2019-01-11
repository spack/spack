# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xgc(AutotoolsPackage):
    """xgc is an X11 graphics demo that shows various features of the X11
    core protocol graphics primitives."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xgc"
    url      = "https://www.x.org/archive/individual/app/xgc-1.0.5.tar.gz"

    version('1.0.5', '605557a9c138f6dc848c87a21bc7c7fc')

    depends_on('libxaw')
    depends_on('libxt')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
