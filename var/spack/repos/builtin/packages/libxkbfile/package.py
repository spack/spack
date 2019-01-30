# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxkbfile(AutotoolsPackage):
    """XKB file handling routines."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libxkbfile"
    url      = "https://www.x.org/archive/individual/lib/libxkbfile-1.0.9.tar.gz"

    version('1.0.9', '5aab87eba67f37dd910a19be5c1129ee')

    depends_on('libx11')

    depends_on('kbproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
