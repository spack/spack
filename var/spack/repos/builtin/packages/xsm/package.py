# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xsm(AutotoolsPackage):
    """X Session Manager."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xsm"
    url      = "https://www.x.org/archive/individual/app/xsm-1.0.3.tar.gz"

    version('1.0.3', '60a2e5987d8e49a568599ba8fe59c8db')

    depends_on('libx11')
    depends_on('libxt@1.1.0:')
    depends_on('libice')
    depends_on('libsm')
    depends_on('libxaw')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
