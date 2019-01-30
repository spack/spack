# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Liboldx(AutotoolsPackage):
    """X version 10 backwards compatibility."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/liboldX/"
    url      = "https://www.x.org/archive/individual/lib/liboldX-1.0.1.tar.gz"

    version('1.0.1', 'ea7c4b6a19bf2d04100e2580abf83fae')

    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
