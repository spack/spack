# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Liblbxutil(AutotoolsPackage):
    """liblbxutil - Low Bandwith X extension (LBX) utility routines."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/liblbxutil"
    url      = "https://www.x.org/archive/individual/lib/liblbxutil-1.1.0.tar.gz"

    version('1.1.0', '2735cd23625d4cc870ec4eb7ca272788')

    depends_on('xextproto@7.0.99.1:', type='build')
    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    # There is a bug in the library that causes the following messages:
    # undefined symbol: Xfree
    # undefined symbol: Xalloc
    # See https://bugs.freedesktop.org/show_bug.cgi?id=8421
    # Adding a dependency on libxdmcp and adding LIBS=-lXdmcp did not fix it
