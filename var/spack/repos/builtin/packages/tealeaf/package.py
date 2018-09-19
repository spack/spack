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

import glob

from spack import *


class Tealeaf(MakefilePackage):
    """Proxy Application. TeaLeaf is a mini-app that solves
       the linear heat conduction equation on a spatially decomposed
       regularly grid using a 5 point stencil with implicit solvers.
    """

    homepage = "http://uk-mac.github.io/TeaLeaf/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/TeaLeaf/TeaLeaf-1.0.tar.gz"

    tags = ['proxy-app']

    version('1.0', '02a907281ad2d09e70ca0a17551c6d79')

    depends_on('mpi')

    @property
    def build_targets(self):
        targets = [
            '--directory=TeaLeaf_ref',
            'MPI_COMPILER={0}'.format(self.spec['mpi'].mpifc),
            'C_MPI_COMPILER={0}'.format(self.spec['mpi'].mpicc),
        ]

        if '%gcc' in self.spec:
            targets.append('COMPILER=GNU')
        elif '%cce' in self.spec:
            targets.append('COMPILER=CRAY')
        elif '%intel' in self.spec:
            targets.append('COMPILER=INTEL')
        elif '%pgi' in self.spec:
            targets.append('COMPILER=PGI')
        elif '%xl' in self.spec:
            targets.append('COMPILER=XL')

        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.tests)

        install('README.md', prefix.doc)
        install('TeaLeaf_ref/tea_leaf', prefix.bin)
        install('TeaLeaf_ref/tea.in', prefix.bin)

        for f in glob.glob('TeaLeaf_ref/*.in'):
            install(f, prefix.doc.tests)
