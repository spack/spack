# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XorgSgmlDoctools(AutotoolsPackage):
    """This package provides a common set of SGML entities and XML/CSS style
    sheets used in building/formatting the documentation provided in other
    X.Org packages."""

    homepage = "http://cgit.freedesktop.org/xorg/doc/xorg-sgml-doctools"
    url      = "https://www.x.org/archive/individual/doc/xorg-sgml-doctools-1.11.tar.gz"

    version('1.11', '51cf4c6b476e2b98a068fea6975b9b21')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
