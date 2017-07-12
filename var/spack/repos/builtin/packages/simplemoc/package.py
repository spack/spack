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


class Simplemoc(MakefilePackage):
    """The purpose of this mini-app is to demonstrate the performance
        characterterics and viability of the Method of Characteristics (MOC)
        for 3D neutron transport calculations in the context of full scale
        light water reactor simulation."""

    homepage = "https://github.com/ANL-CESAR/SimpleMOC/"
    url = "https://github.com/ANL-CESAR/SimpleMOC/archive/master.tar.gz"

    tags = ['proxy-app']

    version('1.0', 'd8827221a4ae76e9766a32e16d143e60')

    build_targets = ['--directory=src']

    def edit(self, spec, prefix):

        if self.compiler.name == 'gcc':
            self.build_targets.extend(['COMPILER=gnu'])

        if self.compiler.name == 'intel':
            self.build_targets.extend(['COMPILER=intel'])

        if self.compiler.name == 'mpicc':
            self.build_targets.extend(['COMPILER=bluegene'])

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        make('src/SimpleMOC', prefix.bin)
