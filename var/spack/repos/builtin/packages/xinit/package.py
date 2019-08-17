# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xinit(AutotoolsPackage):
    """The xinit program is used to start the X Window System server and a
    first client program on systems that are not using a display manager
    such as xdm."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xinit"
    url      = "https://www.x.org/archive/individual/app/xinit-1.3.4.tar.gz"

    version('1.3.4', '91c5697345016ec7841f5e5fccbe7a4c')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
