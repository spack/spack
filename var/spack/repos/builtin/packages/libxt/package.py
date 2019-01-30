# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxt(AutotoolsPackage):
    """libXt - X Toolkit Intrinsics library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXt"
    url      = "https://www.x.org/archive/individual/lib/libXt-1.1.5.tar.gz"

    version('1.1.5', '77d317fbc508dd6adefb59d57a663032')

    depends_on('libsm')
    depends_on('libice')
    depends_on('libx11')

    depends_on('xproto', type='build')
    depends_on('kbproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    @property
    def libs(self):
        return find_libraries(
            'libXt', root=self.prefix, shared=True, recursive=True
        )
