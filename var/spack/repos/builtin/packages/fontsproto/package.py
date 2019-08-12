# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fontsproto(AutotoolsPackage):
    """X Fonts Extension."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/fontsproto"
    url      = "https://www.x.org/archive/individual/proto/fontsproto-2.1.3.tar.gz"

    version('2.1.3', '0415f0360e33f3202af67c6c46782251')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
