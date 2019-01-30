# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xprehashprinterlist(AutotoolsPackage):
    """Rehash list of Xprint printers."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xprehashprinterlist"
    url      = "https://www.x.org/archive/individual/app/xprehashprinterlist-1.0.1.tar.gz"

    version('1.0.1', '395578955634e4b2daa5b78f6fa9222c')

    depends_on('libxp')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
