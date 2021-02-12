# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xditview(AutotoolsPackage, XorgPackage):
    """xditview displays ditroff output on an X display."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xditview"
    xorg_mirror_path = "app/xditview-1.0.4.tar.gz"

    version('1.0.5', sha256='67c4522a24dd7e8762ae458fe216c5bddc12101af295e78c19ff7313fa8cbfad')
    version('1.0.4', sha256='73ad88cfc879edcc6ede65999c11d670da27575388126795d71f3ad60286d379')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
