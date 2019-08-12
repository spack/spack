# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libfs(AutotoolsPackage):
    """libFS - X Font Service client library.

    This library is used by clients of X Font Servers (xfs), such as
    xfsinfo, fslsfonts, and the X servers themselves."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libFS"
    url      = "https://www.x.org/archive/individual/lib/libFS-1.0.7.tar.gz"

    version('1.0.7', 'd8c1246f5b3d0e7ccf2190d3bf2ecb73')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('fontsproto', type='build')
    depends_on('xtrans', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
