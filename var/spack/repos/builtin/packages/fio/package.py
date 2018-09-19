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


class Fio(AutotoolsPackage):
    """Flexible I/O Tester."""

    homepage = "https://github.com/axboe/fio"
    url      = "https://github.com/axboe/fio/archive/fio-2.19.tar.gz"

    version('2.19', '67125b60210a4daa689a4626fc66c612')

    variant('gui', default=False, description='Enable building of gtk gfio')
    variant('doc', default=False, description='Generate documentation')

    depends_on('gtkplus@2.18:', when='+gui')
    depends_on('cairo',         when='+gui')

    depends_on('py-sphinx', type='build', when='+doc')

    def configure_args(self):
        config_args = []

        if '+gui' in self.spec:
            config_args.append('--enable-gfio')

        return config_args

    @run_after('build')
    def build_docs(self):
        if '+doc' in self.spec:
            make('-C', 'doc', 'html')
            make('-C', 'doc', 'man')
