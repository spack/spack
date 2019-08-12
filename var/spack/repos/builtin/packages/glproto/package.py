# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glproto(AutotoolsPackage):
    """OpenGL Extension to the X Window System.

    This extension defines a protocol for the client to send 3D rendering
    commands to the X server."""

    homepage = "https://www.x.org/wiki/"
    url      = "https://www.x.org/archive/individual/proto/glproto-1.4.17.tar.gz"

    version('1.4.17', 'd69554c1b51a83f2c6976a640819911b')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
