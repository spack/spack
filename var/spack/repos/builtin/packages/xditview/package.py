# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xditview(AutotoolsPackage):
    """xditview displays ditroff output on an X display."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xditview"
    url      = "https://www.x.org/archive/individual/app/xditview-1.0.4.tar.gz"

    version('1.0.4', '46dffbbc4de3039fdecabb73d10d6a4f')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
