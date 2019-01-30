# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xclock(AutotoolsPackage):
    """xclock is the classic X Window System clock utility.  It displays
    the time in analog or digital form, continuously updated at a
    frequency which may be specified by the user."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xclock"
    url      = "https://www.x.org/archive/individual/app/xclock-1.0.7.tar.gz"

    version('1.0.7', 'bbade10e6234d8db276212014e8c77fa')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libx11')
    depends_on('libxrender')
    depends_on('libxft')
    depends_on('libxkbfile')
    depends_on('libxt')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
