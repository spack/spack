# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libx11(AutotoolsPackage):
    """libX11 - Core X11 protocol client library."""

    homepage = "https://www.x.org/"
    url      = "https://www.x.org/archive/individual/lib/libX11-1.6.7.tar.gz"

    version('1.6.7', sha256='f62ab88c2a87b55e1dc338726a55bb6ed8048084fe6a3294a7ae324ca45159d1')
    version('1.6.5', sha256='3abce972ba62620611fab5b404dafb852da3da54e7c287831c30863011d28fb3')
    version('1.6.3', sha256='0b03b9d22f4c9e59b4ba498f294e297f013cae27050dfa0f3496640200db5376')

    depends_on('libxcb@1.1.92:')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('xextproto', type=('build', 'link'))
    depends_on('xtrans', type='build')
    depends_on('kbproto', type=('build', 'link'))
    depends_on('inputproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('perl', type='build')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XLOCALEDIR', self.prefix.share.X11.locale)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XLOCALEDIR', self.prefix.share.X11.locale)

    @property
    def libs(self):
        for dir in ['lib64', 'lib']:
            libs = find_libraries('libX11', join_path(self.prefix, dir),
                                  shared=True, recursive=False)
            if libs:
                return libs
        return None
