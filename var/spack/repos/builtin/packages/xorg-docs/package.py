# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XorgDocs(AutotoolsPackage):
    """This package provides miscellaneous documentation for the X Window
    System that doesn't better fit into other packages.

    The preferred documentation format for these documents is DocBook XML."""

    homepage = "http://cgit.freedesktop.org/xorg/doc/xorg-docs"
    url      = "https://www.x.org/archive/individual/doc/xorg-docs-1.7.1.tar.gz"

    version('1.7.1', 'ca689ccbf8ebc362afbe5cc5792a4abd')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('xorg-sgml-doctools@1.8:', type='build')
    depends_on('xmlto', type='build')
