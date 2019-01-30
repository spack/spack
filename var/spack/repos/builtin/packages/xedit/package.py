# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xedit(AutotoolsPackage):
    """Xedit is a simple text editor for X."""

    homepage = "https://cgit.freedesktop.org/xorg/app/xedit"
    url      = "https://www.x.org/archive/individual/app/xedit-1.2.2.tar.gz"

    version('1.2.2', '9fb9d6f63b574e5a4937384fbe6579c1')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.0:')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
