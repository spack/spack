# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxrandr(AutotoolsPackage):
    """libXrandr - X Resize, Rotate and Reflection extension library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXrandr"
    url      = "https://www.x.org/archive/individual/lib/libXrandr-1.5.0.tar.gz"

    version('1.5.0', 'e2fafff575b94ba0b15983eb4df93656')

    depends_on('libx11@1.6:')
    depends_on('libxext')
    depends_on('libxrender')

    depends_on('randrproto@1.5:', type='build')
    depends_on('xextproto', type='build')
    depends_on('renderproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
