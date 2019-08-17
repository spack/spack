# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XcbDemo(AutotoolsPackage):
    """xcb-demo: A collection of demo programs that use the XCB library."""

    homepage = "https://xcb.freedesktop.org/"
    url      = "https://xcb.freedesktop.org/dist/xcb-demo-0.1.tar.gz"

    version('0.1', '803c5c91d54e734e6f6fa3f04f2463ff')

    depends_on('libxcb')
    depends_on('xcb-util')
    depends_on('xcb-util-image')
    depends_on('xcb-util-wm')

    depends_on('pkgconfig', type='build')

    # FIXME: crashes with the following error message
    # X11/XCB/xcb.h: No such file or directory
