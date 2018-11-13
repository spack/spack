# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libdmx(AutotoolsPackage):
    """libdmx - X Window System DMX (Distributed Multihead X) extension
    library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libdmx"
    url      = "https://www.x.org/archive/individual/lib/libdmx-1.1.3.tar.gz"

    version('1.1.3', 'eed755e7cdb161e05f70e955f2b0ef4d')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('dmxproto@2.2.99.1:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
