# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xf86dga(AutotoolsPackage):
    """dga is a simple test client for the XFree86-DGA extension."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xf86dga"
    url      = "https://www.x.org/archive/individual/app/xf86dga-1.0.3.tar.gz"

    version('1.0.3', '3b87bb916c9df68cf5e4e969307b25b5')

    depends_on('libx11')
    depends_on('libxxf86dga@1.1:')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
