# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fixesproto(AutotoolsPackage):
    """X Fixes Extension.

    The extension makes changes to many areas of the protocol to resolve
    issues raised by application interaction with core protocol mechanisms
    that cannot be adequately worked around on the client side of the wire."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/fixesproto"
    url      = "https://www.x.org/archive/individual/proto/fixesproto-5.0.tar.gz"

    version('5.0', '1b3115574cadd4cbea1f197faa7c1de4')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
