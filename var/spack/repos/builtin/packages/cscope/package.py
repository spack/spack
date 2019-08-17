# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cscope(AutotoolsPackage):
    """Cscope is a developer's tool for browsing source code."""

    homepage = "http://cscope.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/cscope/cscope/15.8b/cscope-15.8b.tar.gz"

    version('15.8b', '8f9409a238ee313a96f9f87fe0f3b176')

    depends_on('ncurses')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')

    build_targets = ['CURSES_LIBS=-lncursesw']
