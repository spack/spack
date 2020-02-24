# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cscope(AutotoolsPackage):
    """Cscope is a developer's tool for browsing source code."""

    homepage = "http://cscope.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/cscope/cscope/15.8b/cscope-15.8b.tar.gz"

    version('15.8b', sha256='4889d091f05aa0845384b1e4965aa31d2b20911fb2c001b2cdcffbcb7212d3af')

    depends_on('ncurses')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')

    build_targets = ['CURSES_LIBS=-lncursesw']
