# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xfs(AutotoolsPackage):
    """X Font Server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfs"
    url      = "https://www.x.org/archive/individual/app/xfs-1.1.4.tar.gz"

    version('1.1.4', '0818a2e0317e0f0a1e8a15ca811827e2')

    depends_on('libxfont@1.4.5:')
    depends_on('font-util')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('fontsproto', type='build')
    depends_on('xtrans', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
