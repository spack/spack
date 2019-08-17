# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxkbui(AutotoolsPackage):
    """X.org libxkbui library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libxkbui/"
    url      = "https://www.x.org/archive/individual/lib/libxkbui-1.0.2.tar.gz"

    version('1.0.2', 'a6210171defde64d9e8bcf6a6f6074b0')

    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxkbfile')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
