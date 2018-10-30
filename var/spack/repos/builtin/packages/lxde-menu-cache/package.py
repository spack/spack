# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LxdeMenuCache(AutotoolsPackage):
    """LXDE PCManFM menucache component"""

    homepage = "https://wiki.lxde.org/en/PCManFM"
    url      = "https://downloads.sourceforge.net/project/lxde/menu-cache/1.0/menu-cache-1.0.1.tar.xz"

    version('1.0.1', 'a856ba860b16fdc8c69ee784bc4ade36')

    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('glib')
    depends_on('lxde-libfm+extraonly')
