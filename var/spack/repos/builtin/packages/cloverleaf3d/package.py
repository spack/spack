#############################################################################
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


class Cloverleaf3d(MakefilePackage):
    """Proxy Application. CloverLeaf3D is 3D version of the
       CloverLeaf mini-app. CloverLeaf is a mini-app that solves
       the compressible Euler equations on a Cartesian grid,
       using an explicit, second-order accurate method.
    """

    homepage = "http://uk-mac.github.io/CloverLeaf3D/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/CloverLeaf3D/CloverLeaf3D-1.0.tar.gz"

    tags = ['proxy-app']

    version('1.0', '2e86cadd7612487f9da4ddeb1a6de939')

    variant('openacc', default=False, description='Enable OpenACC Support')

    depends_on('mpi')

    @property
    def type_of_build(self):
        build = 'ref'

        if '+openacc' in self.spec:
            build = 'OpenACC'

        return build

    @property
    def build_targets(self):
        targets = [
            'MPI_COMPILER={0}'.format(self.spec['mpi'].mpifc),
            'C_MPI_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '--directory=CloverLeaf3D_{0}'.format(self.type_of_build)
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
            targets.append('COMPILER=XLF')

        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.samples)

        install('README.md', prefix.doc)

        install('CloverLeaf3D_{0}/clover_leaf'.format(self.type_of_build),
                prefix.bin)
        install('CloverLeaf3D_{0}/clover.in'.format(self.type_of_build),
                prefix.bin)

        for f in glob.glob(
                'CloverLeaf3D_{0}/*.in'.format(self.type_of_build)):
            install(f, prefix.doc.samples)
