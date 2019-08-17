# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxmu(AutotoolsPackage):
    """This library contains miscellaneous utilities and is not part of the
    Xlib standard.  It contains routines which only use public interfaces so
    that it may be layered on top of any proprietary implementation of Xlib
    or Xt."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXmu"
    url      = "https://www.x.org/archive/individual/lib/libXmu-1.1.2.tar.gz"

    version('1.1.2', 'd5be323b02e6851607205c8e941b4e61')

    depends_on('libxt')
    depends_on('libxext')
    depends_on('libx11')

    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
