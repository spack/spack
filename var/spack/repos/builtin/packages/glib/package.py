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

import os.path


class Glib(AutotoolsPackage):
    """GLib provides the core application building blocks for
    libraries and applications written in C.

    The GLib package contains a low-level libraries useful for
    providing data structure handling for C, portability wrappers
    and interfaces for such runtime functionality as an event loop,
    threads, dynamic loading and an object system.
    """

    homepage = "https://developer.gnome.org/glib/"
    url      = "https://ftp.gnome.org/pub/gnome/sources/glib/2.53/glib-2.53.1.tar.xz"

    version('2.56.2', 'd64abd16813501c956c4e123ae79f47f1b58de573df9fdd3b0795f1e2c1aa789')
    version('2.56.1', '40ef3f44f2c651c7a31aedee44259809b6f03d3d20be44545cd7d177221c0b8d')
    version('2.56.0', 'f2b59392f2fb514bbe7791dda0c36da5')
    version('2.55.1', '9cbb6b3c7e75ba75575588497c7707b6')
    version('2.53.1', '3362ef4da713f834ea26904caf3a75f5')
    version('2.49.7', '397ead3fcf325cb921d54e2c9e7dfd7a')
    version('2.49.4', 'e2c87c03017b0cd02c4c73274b92b148')
    version('2.48.1', '67bd3b75c9f6d5587b457dc01cdcd5bb')
    version('2.42.1', '89c4119e50e767d3532158605ee9121a')

    variant('libmount', default=False, description='Build with libmount support')
    variant(
        'tracing',
        default='',
        values=('dtrace', 'systemtap'),
        multi=True,
        description='Enable tracing support'
    )

    depends_on('pkgconfig', type='build')
    depends_on('libffi')
    depends_on('zlib')
    depends_on('gettext')
    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'), when='@2.53.4:')
    depends_on('pcre+utf', when='@2.48:')
    depends_on('util-linux', when='+libmount')

    # The following patch is needed for gcc-6.1
    patch('g_date_strftime.patch', when='@2.42.1')
    # Clang doesn't seem to acknowledge the pragma lines to disable the -Werror
    # around a legitimate usage.
    patch('no-Werror=format-security.patch')
    # Patch to prevent compiler errors in kernels older than 2.6.35
    patch('old-kernels.patch', when='@2.56.0:2.56.1 os=rhel6')
    patch('old-kernels.patch', when='@2.56.0:2.56.1 os=centos6')
    patch('old-kernels.patch', when='@2.56.0:2.56.1 os=scientific6')

    def url_for_version(self, version):
        """Handle glib's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/glib'
        return url + '/%s/glib-%s.tar.xz' % (version.up_to(2), version)

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable('libmount'))
        if self.spec.satisfies('@2.53.4:'):
            args.append('--with-python={0}'.format(
                os.path.basename(self.spec['python'].command.path))
            )
        args.extend(self.enable_or_disable('tracing'))
        return args

    @property
    def dtrace_copy_path(self):
        return join_path(self.stage.source_path, 'dtrace-copy')

    @run_before('configure')
    def fix_python_path(self):
        if not self.spec.satisfies('@2.53.4:'):
            return

        files = ['gobject/glib-genmarshal.in', 'gobject/glib-mkenums.in']

        filter_file('^#!/usr/bin/env @PYTHON@',
                    '#!/usr/bin/env python',
                    *files)

    @run_before('configure')
    def fix_dtrace_usr_bin_path(self):
        if 'tracing=dtrace' not in self.spec:
            return

        # dtrace may cause glib build to fail because it uses
        # '/usr/bin/python' in the shebang. To work around that
        # we copy the original script into a temporary folder, and
        # change the shebang to '/usr/bin/env python'
        dtrace = which('dtrace').path
        dtrace_copy = join_path(self.dtrace_copy_path, 'dtrace')

        with working_dir(self.dtrace_copy_path, create=True):
            copy(dtrace, dtrace_copy)
            filter_file(
                '^#!/usr/bin/python',
                '#!/usr/bin/env python',
                dtrace_copy
            )

        # To have our own copy of dtrace in PATH, we need to
        # prepend to PATH the temporary folder where it resides
        env['PATH'] = ':'.join(
            [self.dtrace_copy_path] + env['PATH'].split(':')
        )

    @run_after('install')
    def filter_sbang(self):
        # Revert sbang, so Spack's sbang hook can fix it up (we have to do
        # this after install because otherwise the install target will try
        # to rebuild files as filter_file updates the timestamps)
        if self.spec.satisfies('@2.53.4:'):
            pattern = '^#!/usr/bin/env python'
            repl = '#!{0}'.format(self.spec['python'].command.path)
            files = ['glib-genmarshal', 'glib-mkenums']
        else:
            pattern = '^#! /usr/bin/perl'
            repl = '#!{0}'.format(self.spec['perl'].command.path)
            files = ['glib-mkenums']

        files = [join_path(self.prefix.bin, file) for file in files]
        filter_file(pattern, repl, *files, backup=False)
