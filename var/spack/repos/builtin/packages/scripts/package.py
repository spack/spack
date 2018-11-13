# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scripts(AutotoolsPackage):
    """Various X related scripts."""

    homepage = "http://cgit.freedesktop.org/xorg/app/scripts"
    url      = "https://www.x.org/archive/individual/app/scripts-1.0.1.tar.gz"

    version('1.0.1', '1e8294a126a2a7556b21025a8d933e8b')

    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
