# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kbproto(AutotoolsPackage):
    """X Keyboard Extension.

    This extension defines a protcol to provide a number of new capabilities
    and controls for text keyboards."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/kbproto"
    url      = "https://www.x.org/archive/individual/proto/kbproto-1.0.7.tar.gz"

    version('1.0.7', '19acc5f02ae80381e216f443134e0bbb')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
