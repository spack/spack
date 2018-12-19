# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxaw(AutotoolsPackage):
    """Xaw is the X Athena Widget Set.
    Xaw is a widget set based on the X Toolkit Intrinsics (Xt) Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXaw"
    url      = "https://www.x.org/archive/individual/lib/libXaw-1.0.13.tar.gz"

    version('1.0.13', '6c522476024df5872cddc5f1562fb656')

    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libxpm')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
