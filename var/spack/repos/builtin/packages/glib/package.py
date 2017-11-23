##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Glib(AutotoolsPackage):
    """The GLib package contains a low-level libraries useful for
       providing data structure handling for C, portability wrappers
       and interfaces for such runtime functionality as an event loop,
       threads, dynamic loading and an object system."""

    homepage = "https://developer.gnome.org/glib/"
    url      = "https://ftp.gnome.org/pub/gnome/sources/glib/2.53/glib-2.53.1.tar.xz"

    version('2.53.1', '3362ef4da713f834ea26904caf3a75f5')
    version('2.49.7', '397ead3fcf325cb921d54e2c9e7dfd7a')
    version('2.49.4', 'e2c87c03017b0cd02c4c73274b92b148')
    version('2.48.1', '67bd3b75c9f6d5587b457dc01cdcd5bb')
    version('2.42.1', '89c4119e50e767d3532158605ee9121a')

    variant('libmount', default=False, description='Build with libmount support')

    depends_on('pkgconfig', type='build')
    depends_on('libffi')
    depends_on('zlib')
    depends_on('gettext')
    depends_on('perl', type=('build', 'run'))
    depends_on('pcre+utf', when='@2.48:')
    depends_on('util-linux', when='+libmount')

    # The following patch is needed for gcc-6.1
    patch('g_date_strftime.patch', when='@2.42.1')
    # Clang doesn't seem to acknowledge the pragma lines to disable the -Werror
    # around a legitimate usage.
    patch('no-Werror=format-security.patch')

    def url_for_version(self, version):
        """Handle glib's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/glib'
        return url + '/%s/glib-%s.tar.xz' % (version.up_to(2), version)

    def configure_args(self):
        spec = self.spec
        args = []

        if '+libmount' in spec:
            args.append('--enable-libmount')
        else:
            args.append('--disable-libmount')

        return args

    @run_before('install')
    def filter_sbang(self):
        # Filter sbang before install so Spack's sbang hook can fix it up
        perl = join_path(self.spec['perl'].prefix.bin, 'perl')
        files = ['gobject/glib-mkenums']

        filter_file('^#! /usr/bin/perl', '#!{0}'.format(perl), *files)
