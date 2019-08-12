# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xsetpointer(AutotoolsPackage):
    """Set an X Input device as the main pointer."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xsetpointer"
    url      = "https://www.x.org/archive/individual/app/xsetpointer-1.0.1.tar.gz"

    version('1.0.1', 'bb206b6875f2428c2281e1165b6c7f88')

    depends_on('libxi')
    depends_on('libx11')

    depends_on('inputproto@1.4:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
