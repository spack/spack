# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsm(AutotoolsPackage):
    """libSM - X Session Management Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libSM"
    url      = "https://www.x.org/archive/individual/lib/libSM-1.2.2.tar.gz"

    version('1.2.2', sha256='14bb7c669ce2b8ff712fbdbf48120e3742a77edcd5e025d6b3325ed30cf120f4')

    depends_on('libice@1.0.5:')

    depends_on('xproto', type='build')
    depends_on('xtrans', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
