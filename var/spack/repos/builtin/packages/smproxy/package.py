# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Smproxy(AutotoolsPackage):
    """smproxy allows X applications that do not support X11R6 session
    management to participate in an X11R6 session."""

    homepage = "http://cgit.freedesktop.org/xorg/app/smproxy"
    url      = "https://www.x.org/archive/individual/app/smproxy-1.0.6.tar.gz"

    version('1.0.6', '012c259f5a89e5c636037446d44eb354')

    depends_on('libsm')
    depends_on('libice')
    depends_on('libxt')
    depends_on('libxmu')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
