# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xtrans(AutotoolsPackage):
    """xtrans is a library of code that is shared among various X packages to
    handle network protocol transport in a modular fashion, allowing a
    single place to add new transport types.  It is used by the X server,
    libX11, libICE, the X font server, and related components."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libxtrans"
    url      = "https://www.x.org/archive//individual/lib/xtrans-1.3.5.tar.gz"

    version('1.3.5', '6e4eac1b7c6591da0753052e1eccfb58')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
