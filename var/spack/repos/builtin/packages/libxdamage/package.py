# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxdamage(AutotoolsPackage):
    """This package contains the library for the X Damage extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXdamage"
    url      = "https://www.x.org/archive/individual/lib/libXdamage-1.1.4.tar.gz"

    version('1.1.4', '95867778da012623815214769007c0d7')

    depends_on('libxfixes')
    depends_on('libx11')

    depends_on('damageproto@1.1:', type='build')
    depends_on('fixesproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
