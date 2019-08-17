# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xtrap(AutotoolsPackage):
    """XTrap sample clients."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xtrap"
    url      = "https://www.x.org/archive/individual/app/xtrap-1.0.2.tar.gz"

    version('1.0.2', '601e4945535d2d25eb1bc640332e2363')

    depends_on('libx11')
    depends_on('libxtrap')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
