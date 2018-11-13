# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Imake(AutotoolsPackage):
    """The imake build system."""

    homepage = "http://www.snake.net/software/imake-stuff/"
    url      = "https://www.x.org/archive/individual/util/imake-1.0.7.tar.gz"

    version('1.0.7', '186ca7b8ff0de8752f2a2d0426542363')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
