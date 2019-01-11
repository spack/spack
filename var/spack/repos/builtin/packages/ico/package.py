# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ico(AutotoolsPackage):
    """ico is a simple animation program that may be used for testing various
    X11 operations and extensions.  It displays a wire-frame rotating
    polyhedron, with hidden lines removed, or a solid-fill polyhedron with
    hidden faces removed."""

    homepage = "http://cgit.freedesktop.org/xorg/app/ico"
    url      = "https://www.x.org/archive/individual/app/ico-1.0.4.tar.gz"

    version('1.0.4', '8833b2da01a7f919b0db8e5a49184c0f')

    depends_on('libx11@0.99.1:')

    depends_on('xproto@7.0.22:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
