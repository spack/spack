# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fontsproto(AutotoolsPackage):
    """X Fonts Extension."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/fontsproto"
    url      = "https://www.x.org/archive/individual/proto/fontsproto-2.1.3.tar.gz"

    version('2.1.3', sha256='72c44e63044b2b66f6fa112921621ecc20c71193982de4f198d9a29cda385c5e')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
