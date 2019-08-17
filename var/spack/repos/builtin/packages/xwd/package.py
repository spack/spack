# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xwd(AutotoolsPackage):
    """xwd - dump an image of an X window."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xwd"
    url      = "https://www.x.org/archive/individual/app/xwd-1.0.6.tar.gz"

    version('1.0.6', 'd6c132f5f00188ce2a1393f12bd34ad4')

    depends_on('libx11')
    depends_on('libxkbfile')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
