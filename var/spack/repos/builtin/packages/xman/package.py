# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xman(AutotoolsPackage):
    """xman is a graphical manual page browser using the Athena Widgets (Xaw)
    toolkit."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xman"
    url      = "https://www.x.org/archive/individual/app/xman-1.1.4.tar.gz"

    version('1.1.4', 'f4238c79ee7227ea193898fc159f31e5')

    depends_on('libxaw')
    depends_on('libxt')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
