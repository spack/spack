# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcroco(AutotoolsPackage):
    """Libcroco is a standalone css2 parsing and manipulation library."""

    homepage = "https://developer.gnome.org/libcroco"
    url      = "http://ftp.gnome.org/pub/gnome/sources/libcroco/0.6/libcroco-0.6.12.tar.xz"

    version('0.6.12', 'bc0984fce078ba2ce29f9500c6b9ddce')

    depends_on('glib')
    depends_on('libxml2')
