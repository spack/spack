# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xset(AutotoolsPackage):
    """User preference utility for X."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xset"
    url      = "https://www.x.org/archive/individual/app/xset-1.2.3.tar.gz"

    version('1.2.3', '1a76965ed0e8cb51d3fa04d458cb3d8f')

    depends_on('libxmu')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
