# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dri3proto(AutotoolsPackage):
    """Direct Rendering Infrastructure 3 Extension.

    This extension defines a protocol to securely allow user applications to
    access the video hardware without requiring data to be passed through the
    X server."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/dri3proto/"
    url      = "https://www.x.org/releases/individual/proto/dri3proto-1.0.tar.gz"

    version('1.0', '25e84a49a076862277ee12aebd49ff5f')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
