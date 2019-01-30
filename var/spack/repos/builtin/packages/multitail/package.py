# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Multitail(MakefilePackage):
    """MultiTail allows you to monitor logfiles and command output
       in multiple windows in a terminal, colorize, filter and merge."""

    homepage = "https://www.vanheusden.com/multitail/index.php"
    url      = "https://www.vanheusden.com/multitail/multitail-6.4.2.tgz"

    version('6.4.2', 'a0959f7b2385061080712afd8ae6e33d')

    depends_on('ncurses')

    # It's counterintuitive, but use DESTDIR for the install because
    # the Makefile doesn't consistently use PREFIX with the things
    # it's installing...
    @property
    def install_targets(self):
        targets = []
        targets.append('PREFIX=')
        targets.append('DESTDIR={0}'.format(self.prefix))
        targets.append('install')
        return targets

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')

        nc_include_flags = spec['ncurses'].headers.include_flags
        nc_ld_flags = spec['ncurses'].libs.ld_flags
        makefile.filter('CFLAGS\+=', 'CFLAGS+={0} '.format(nc_include_flags))
        makefile.filter('LDFLAGS\+=', 'LDFLAGS+={0} '.format(nc_ld_flags))

        # Copy the conf file directly into place (don't worry about
        # overwriting an existing file...)
        kwargs = {'ignore_absent': False, 'backup': False, 'string': True}
        makefile.filter('cp multitail.conf $(CONFIG_FILE).new',
                        'cp multitail.conf $(CONFIG_FILE)', **kwargs)
