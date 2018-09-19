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


class Libxkbcommon(AutotoolsPackage):
    """xkbcommon is a library to handle keyboard descriptions, including
    loading them from disk, parsing them and handling their state. It's mainly
    meant for client toolkits, window systems, and other system
    applications."""

    homepage = "https://xkbcommon.org/"
    url      = "https://github.com/xkbcommon/libxkbcommon/archive/xkbcommon-0.8.0.tar.gz"

    version('0.8.0', '0d9738fb2ed2dcc6e2c6920d94e135ce')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('bison',    type='build')
    depends_on('xkbdata')

    def configure_args(self):
        spec = self.spec
        args = []
        args.append('--with-xkb-config-root={0}'
                    .format(spec['xkbdata'].prefix))
        return args
