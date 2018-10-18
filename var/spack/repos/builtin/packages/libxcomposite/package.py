# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxcomposite(AutotoolsPackage):
    """libXcomposite - client library for the Composite extension to the
    X11 protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXcomposite"
    url      = "https://www.x.org/archive/individual/lib/libXcomposite-0.4.4.tar.gz"

    version('0.4.4', 'af860b1554a423735d831e6f29ac1ef5')

    depends_on('libx11')
    depends_on('libxfixes')
    depends_on('fixesproto@0.4:', type='build')
    depends_on('compositeproto@0.4:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
