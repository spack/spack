# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxshmfence(AutotoolsPackage):
    """libxshmfence - Shared memory 'SyncFence' synchronization primitive.

    This library offers a CPU-based synchronization primitive compatible
    with the X SyncFence objects that can be shared between processes
    using file descriptor passing."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libxshmfence/"
    url      = "https://www.x.org/archive/individual/lib/libxshmfence-1.3.tar.bz2"

    version('1.3', '42dda8016943dc12aff2c03a036e0937')
    version('1.2', '66662e76899112c0f99e22f2fc775a7e')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
