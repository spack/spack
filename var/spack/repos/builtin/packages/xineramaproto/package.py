# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xineramaproto(AutotoolsPackage):
    """X Xinerama Extension.

    This is an X extension that allows multiple physical screens controlled
    by a single X server to appear as a single screen."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/xineramaproto"
    url      = "https://www.x.org/archive/individual/proto/xineramaproto-1.2.1.tar.gz"

    version('1.2.1', 'e0e148b11739e144a546b8a051b17dde')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
