##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Sw4lite(MakefilePackage):
    """Sw4lite is a bare bone version of SW4 intended for testing
    performance optimizations in a few important numerical kernels of SW4."""

    tags = ['proxy-app']

    homepage = "https://github.com/geodynamics/sw4lite"
    url      = "https://github.com/geodynamics/sw4lite/archive/v1.0.zip"

    version('develop', git='https://github.com/geodynamics/sw4lite',
            branch='master')
    version('1.0', '3d911165f4f2ff6d5f9c1bd56ab6723f')

    depends_on('mpi')

    @property
    def build_targets(self):
        targets = []
        spec = self.spec
        targets.append('ckernel=yes')
        targets.append('FC=' + spec['mpi'].mpifc)
        targets.append('CXX=' + spec['mpi'].mpicxx)
        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('optimize_c/sw4lite', prefix.bin)
