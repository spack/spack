# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Last(MakefilePackage):
    """LAST finds similar regions between sequences, and aligns them. It is
       designed for comparing large datasets to each other (e.g. vertebrate
       genomes and/or large numbers of DNA reads)."""

    homepage = "http://last.cbrc.jp/"
    url      = "http://last.cbrc.jp/last-869.zip"
    git      = "https://gitlab.com/mcfrith/last.git"
    maintainers = ['snehring']

    version('1282', commit='4368be912f4759e52b549940276f1adf087f489a')
    version('869', sha256='6371a6282bc1bb02a5e5013cc463625f2ce3e7746ff2ea0bdf9fe6b15605a67c')

    def edit(self, spec, prefix):
        files = ['mat-doc.sh', 'mat-inc.sh', 'seed-doc.sh', 'seed-inc.sh']
        if spec.satisfies('@1282:'):
            files.append('gc-inc.sh')
        with working_dir('build'):
            for f in files:
                set_executable(f)

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix)
