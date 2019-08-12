# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxprintapputil(AutotoolsPackage):
    """Xprint application utility routines."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXprintAppUtil/"
    url      = "https://www.x.org/archive/individual/lib/libXprintAppUtil-1.0.1.tar.gz"

    version('1.0.1', '3adb71fa34a2d4e75d8b840310318f76')

    depends_on('libx11')
    depends_on('libxp')
    depends_on('libxprintutil')
    depends_on('libxau')

    depends_on('printproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
