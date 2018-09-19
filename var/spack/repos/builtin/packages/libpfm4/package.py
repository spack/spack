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

    version('4.8.0', '730383896db92e12fb2cc10f2d41dd43')

    # Fails to build libpfm4 with intel compiler version 16 and 17
    conflicts('%intel@16:17')

    @property
    def install_targets(self):
        return ['DESTDIR={0}'.format(self.prefix),
                'LIBDIR=/lib',
                'INCDIR=/include',
                'MANDIR=/man',
                'LDCONFIG=true',
                'install']
