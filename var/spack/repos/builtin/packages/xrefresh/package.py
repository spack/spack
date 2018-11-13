# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xrefresh(AutotoolsPackage):
    """xrefresh - refresh all or part of an X screen."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xrefresh"
    url      = "https://www.x.org/archive/individual/app/xrefresh-1.0.5.tar.gz"

    version('1.0.5', 'e41c5148d894406484af59887257c465')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
