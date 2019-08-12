# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xkbevd(AutotoolsPackage):
    """XKB event daemon demo."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xkbevd"
    url      = "https://www.x.org/archive/individual/app/xkbevd-1.1.4.tar.gz"

    version('1.1.4', '0e9e05761551b1e58bd541231f90ae87')

    depends_on('libxkbfile')
    depends_on('libx11')

    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
