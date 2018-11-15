# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xbacklight(AutotoolsPackage):
    """Xbacklight is used to adjust the backlight brightness where supported.
    It uses the RandR extension to find all outputs on the X server
    supporting backlight brightness control and changes them all in the
    same way."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xbacklight"
    url      = "https://www.x.org/archive/individual/app/xbacklight-1.2.1.tar.gz"

    version('1.2.1', 'e8e4c86b0f867e23aa3532618a697609')

    depends_on('libxcb')
    depends_on('xcb-util')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
