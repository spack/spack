# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Applewmproto(AutotoolsPackage):
    """Apple Rootless Window Management Extension.

    This extension defines a protcol that allows X window managers
    to better interact with the Mac OS X Aqua user interface when
    running X11 in a rootless mode."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/applewmproto"
    url      = "https://www.x.org/archive/individual/proto/applewmproto-1.4.2.tar.gz"

    version('1.4.2', 'ecc8a4424a893ce120f5652dba62e9e6')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
