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
