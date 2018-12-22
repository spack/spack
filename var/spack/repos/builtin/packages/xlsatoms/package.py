# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xlsatoms(AutotoolsPackage):
    """xlsatoms lists the interned atoms defined on an X11 server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xlsatoms"
    url      = "https://www.x.org/archive/individual/app/xlsatoms-1.1.2.tar.gz"

    version('1.1.2', '1f32e2b8c2135b5867291517848cb396')

    depends_on('libxcb', when='@1.1:')
    depends_on('libx11', when='@:1.0')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
