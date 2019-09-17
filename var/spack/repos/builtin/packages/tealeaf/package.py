# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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

    def edit(self, spec, prefix):
        if spec.target.family == 'aarch64' and spec.satisfies('%gcc@:5.9'):
            filter_file(
                '-march=native', '', join_path('TeaLeaf_ref', 'Makefile')
            )

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
