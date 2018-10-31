# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xload(AutotoolsPackage):
    """xload displays a periodically updating histogram of the
    system load average."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xload"
    url      = "https://www.x.org/archive/individual/app/xload-1.1.2.tar.gz"

    version('1.1.2', '0af9a68193849b16f8168f096682efb4')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
