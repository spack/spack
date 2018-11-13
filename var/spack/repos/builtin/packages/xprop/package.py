# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xprop(AutotoolsPackage):
    """xprop is a command line tool to display and/or set window and font
    properties of an X server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xprop"
    url      = "https://www.x.org/archive/individual/app/xprop-1.2.2.tar.gz"

    version('1.2.2', 'db03a6bcf7b0d0c2e691ea3083277cbc')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
