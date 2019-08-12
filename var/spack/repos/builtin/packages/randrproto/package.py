# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Randrproto(AutotoolsPackage):
    """X Resize and Rotate Extension (RandR).

    This extension defines a protocol for clients to dynamically change X
    screens, so as to resize, rotate and reflect the root window of a screen.
    """

    homepage = "http://cgit.freedesktop.org/xorg/proto/randrproto"
    url      = "https://www.x.org/archive/individual/proto/randrproto-1.5.0.tar.gz"

    version('1.5.0', '863d6ee3e0b2708f75d968470ed31eb9')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
