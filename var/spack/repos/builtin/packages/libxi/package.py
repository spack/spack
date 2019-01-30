# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxi(AutotoolsPackage):
    """libXi - library for the X Input Extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXi"
    url      = "https://www.x.org/archive/individual/lib/libXi-1.7.6.tar.gz"

    version('1.7.6', 'f3828f9d7893068f6f6f10fe15b31afa')

    depends_on('pkgconfig', type='build')
    depends_on('libx11@1.6:')
    depends_on('libxext@1.0.99.1:')
    depends_on('libxfixes@5:')

    # transient build dependency (from libxfixes), i.e. shouldn't be needed?
    depends_on('fixesproto@5.0:', type='build')

    depends_on('xproto@7.0.13:', type='build')
    depends_on('xextproto@7.0.3:', type='build')
    depends_on('inputproto@2.2.99.1:', type='build')
