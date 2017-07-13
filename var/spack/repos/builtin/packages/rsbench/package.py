##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Rsbench(MakefilePackage):
    """A mini-app to represent the multipole resonance representation lookup
       cross section algorithm."""

    homepage = "https://github.com/ANL-CESAR/RSBench"
    url = "https://github.com/ANL-CESAR/RSBench/archive/v2.tar.gz"

    variant('pgi', default=False, description='Build with PGI.')

    depends_on('pgi', when='+pgi')

    version('2', '15a3ac5ea72529ac1ed9ed016ee68b4f')
    version('0', '3427634dc5e7cd904d88f9955b371757')


    @property
    def build_targets(self):

        targets = [
            '--directory=src'
        ]

        if '%intel' in self.spec:
            targets.append('COMPILER=intel')

        if '%pgi' in self.spec:
            targets.append('COMPILER=pgi')
            targets.append('CC={0}'.format(self.spec['pgi'].pgcc))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        make('src/rsbench', prefix.bin)
