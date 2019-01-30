# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xhost(AutotoolsPackage):
    """xhost is used to manage the list of host names or user names
    allowed to make connections to the X server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xhost"
    url      = "https://www.x.org/archive/individual/app/xhost-1.0.7.tar.gz"

    version('1.0.7', 'de34b4ba5194634dbeb29a1f008f495a')

    depends_on('libx11')
    depends_on('libxmu')
    depends_on('libxau')

    depends_on('xproto@7.0.22:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
