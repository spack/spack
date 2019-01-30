# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxdmcp(AutotoolsPackage):
    """libXdmcp - X Display Manager Control Protocol library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXdmcp"
    url      = "https://www.x.org/archive/individual/lib/libXdmcp-1.1.2.tar.gz"

    version('1.1.2', 'ab0d6a38f0344a05d698ec7d48cfa5a8')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
