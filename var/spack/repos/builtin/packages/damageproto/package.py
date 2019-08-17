# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Damageproto(AutotoolsPackage):
    """X Damage Extension.

    This package contains header files and documentation for the X Damage
    extension.  Library and server implementations are separate."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/damageproto"
    url      = "https://www.x.org/releases/individual/proto/damageproto-1.2.1.tar.gz"

    version('1.2.1', 'bf8c47b7f48625230cff155180f8ddce')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
