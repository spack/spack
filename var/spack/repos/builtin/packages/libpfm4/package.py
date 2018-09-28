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


class Libpfm4(MakefilePackage):
    """libpfm4 is a userspace library to help
     setup performance events for use with
     the perf_events Linux kernel interface."""

    homepage = "http://perfmon2.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/perfmon2/libpfm4/libpfm-4.8.0.tar.gz"

    version('4.10.1', 'd8f66cb9bfa7e1434434e0de6409db5b')
    version('4.9.0', '42ad4a2e5b8e1f015310db8535739c73')
    version('4.8.0', '730383896db92e12fb2cc10f2d41dd43')

    # Fails to build libpfm4 with intel compiler version 16 and 17
    conflicts('%intel@16:17')

    # Set default optimization level (-O2) if not specified.
    def flag_handler(self, name, flags):
        if name == 'cflags':
            for flag in flags:
                if flag.startswith('-O'):
                    break
            else:
                flags.append('-O2')

        return (flags, None, None)

    # Remove -Werror from CFLAGS.  Given the large space of platform,
    # compiler, version, we don't want to fail the build over a stray
    # warning.
    def patch(self):
        filter_file('-Werror', '', 'config.mk')

    @property
    def install_targets(self):
        return ['DESTDIR={0}'.format(self.prefix),
                'LIBDIR=/lib',
                'INCDIR=/include',
                'MANDIR=/man',
                'LDCONFIG=true',
                'install']
