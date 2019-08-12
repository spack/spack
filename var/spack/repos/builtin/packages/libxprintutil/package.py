# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxprintutil(AutotoolsPackage):
    """Xprint application utility routines."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXprintUtil/"
    url      = "https://www.x.org/archive/individual/lib/libXprintUtil-1.0.1.tar.gz"

    version('1.0.1', '2f02e812f3e419534ced6fcb5860825f')

    depends_on('libx11')
    depends_on('libxp')
    depends_on('libxt')
    depends_on('libxau')

    depends_on('printproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
