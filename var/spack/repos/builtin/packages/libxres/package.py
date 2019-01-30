# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxres(AutotoolsPackage):
    """libXRes - X-Resource extension client library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXRes"
    url      = "https://www.x.org/archive/individual/lib/libXres-1.0.7.tar.gz"

    version('1.0.7', '7fad9ab34201bb4adffcbf0cd7e87a89')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('resourceproto@1.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
