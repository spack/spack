# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xf86vidmodeproto(AutotoolsPackage):
    """XFree86 Video Mode Extension.

    This extension defines a protocol for dynamically configuring modelines
    and gamma."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/xf86vidmodeproto"
    url      = "https://www.x.org/archive/individual/proto/xf86vidmodeproto-2.3.1.tar.gz"

    version('2.3.1', '99016d0fe355bae0bb23ce00fb4d4a2c')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
