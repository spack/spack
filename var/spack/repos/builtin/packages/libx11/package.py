# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libx11(AutotoolsPackage):
    """libX11 - Core X11 protocol client library."""

    homepage = "https://www.x.org/"
    url      = "https://www.x.org/archive/individual/lib/libX11-1.6.7.tar.gz"

    version('1.6.7', sha256='f62ab88c2a87b55e1dc338726a55bb6ed8048084fe6a3294a7ae324ca45159d1')
    version('1.6.5', '300b5831916ffcc375468431d856917e')
    version('1.6.3', '7d16653fe7c36209799175bb3dc1ae46')

    depends_on('libxcb@1.1.92:')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('xextproto', type=('build', 'link'))
    depends_on('xtrans', type='build')
    depends_on('kbproto', type=('build', 'link'))
    depends_on('inputproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('perl', type='build')

    @property
    def libs(self):
        for dir in ['lib64', 'lib']:
            libs = find_libraries('libX11', join_path(self.prefix, dir),
                                  shared=True, recursive=False)
            if libs:
                return libs
        return None
