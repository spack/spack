##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
