# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dri2proto(AutotoolsPackage):
    """Direct Rendering Infrastructure 2 Extension.

    This extension defines a protocol to securely allow user applications to
    access the video hardware without requiring data to be passed through the
    X server."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/dri2proto/"
    url      = "https://www.x.org/releases/individual/proto/dri2proto-2.8.tar.gz"

    version('2.8', '19ea18f63d8ae8053c9fa84b60365b77')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
