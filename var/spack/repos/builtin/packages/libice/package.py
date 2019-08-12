# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libice(AutotoolsPackage):
    """libICE - Inter-Client Exchange Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libICE"
    url      = "https://www.x.org/archive/individual/lib/libICE-1.0.9.tar.gz"

    version('1.0.9', '95812d61df8139c7cacc1325a26d5e37')

    depends_on('xproto', type='build')
    depends_on('xtrans', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
