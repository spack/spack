# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xcursorgen(AutotoolsPackage):
    """xcursorgen prepares X11 cursor sets for use with libXcursor."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xcursorgen"
    url      = "https://www.x.org/archive/individual/app/xcursorgen-1.0.6.tar.gz"

    version('1.0.6', '669df84fc30d89c12ce64b95aba26677')

    depends_on('libx11')
    depends_on('libxcursor')
    depends_on('libpng@1.2.0:')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
