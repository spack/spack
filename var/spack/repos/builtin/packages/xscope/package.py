# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xscope(AutotoolsPackage):
    """XSCOPE -- a program to monitor X11/Client conversations."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xscope"
    url      = "https://www.x.org/archive/individual/app/xscope-1.4.1.tar.gz"

    version('1.4.1', 'c476fb73b354f4a5c388f3814052ce0d')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('xtrans', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
