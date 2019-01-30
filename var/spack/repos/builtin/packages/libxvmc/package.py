# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxvmc(AutotoolsPackage):
    """X.org libXvMC library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXvMC"
    url      = "https://www.x.org/archive/individual/lib/libXvMC-1.0.9.tar.gz"

    version('1.0.9', 'a28c0780373537f4774565309b31a69e')

    depends_on('libx11@1.6:')
    depends_on('libxext')
    depends_on('libxv')

    depends_on('xextproto', type='build')
    depends_on('videoproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
