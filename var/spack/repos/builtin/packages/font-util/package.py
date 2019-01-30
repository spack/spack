# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontUtil(AutotoolsPackage):
    """X.Org font package creation/installation utilities."""

    homepage = "http://cgit.freedesktop.org/xorg/font/util"
    url      = "https://www.x.org/archive/individual/font/font-util-1.3.1.tar.gz"

    version('1.3.1', 'd153a9af216e4498fa171faea2c82514')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
