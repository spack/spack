# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pkgconf(AutotoolsPackage):
    """pkgconf is a program which helps to configure compiler and linker
    flags for development frameworks. It is similar to pkg-config from
    freedesktop.org, providing additional functionality while also
    maintaining compatibility."""

    homepage = "http://pkgconf.org/"
    url      = "http://distfiles.alpinelinux.org/distfiles/pkgconf-1.4.2.tar.xz"

    version('1.4.2',  '678d242b4eef1754bba6a58642af10bb')
    version('1.4.0',  'c509c0dad5a70aa4bc3210557b7eafce')
    version('1.3.10', '9b63707bf6f8da6efb3868101d7525fe')
    version('1.3.8',  '484ba3360d983ce07416843d5bc916a8')

    provides('pkgconfig')

    # TODO: Add a package for the kyua testing framework
    # depends_on('kyua', type='test')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        spack_env.append_path('ACLOCAL_PATH',
                              join_path(self.prefix.share, 'aclocal'))

    @run_after('install')
    def link_pkg_config(self):
        symlink('pkgconf', '{0}/pkg-config'.format(self.prefix.bin))
        symlink('pkgconf.1',
                '{0}/pkg-config.1'.format(self.prefix.share.man.man1))
