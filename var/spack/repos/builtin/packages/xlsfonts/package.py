# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xlsfonts(AutotoolsPackage):
    """xlsfonts lists fonts available from an X server via the X11
    core protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xlsfonts"
    url      = "https://www.x.org/archive/individual/app/xlsfonts-1.0.5.tar.gz"

    version('1.0.5', '074cc44e5238c6a501523ef06caba517')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
