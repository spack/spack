# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sumaclust(MakefilePackage):
    """Sumaclust aims to cluster sequences in a way that is fast and exact at
       the same time."""

    homepage = "https://git.metabarcoding.org/obitools/sumaclust"

    version('1.0.20', '31c7583fbe2e3345d5fe3e9431d9b30c',
            url="https://git.metabarcoding.org/obitools/sumaclust/uploads/69f757c42f2cd45212c587e87c75a00f/sumaclust_v1.0.20.tar.gz")

    def build(self, spec, prefix):
        make('CC={0}'.format(spack_cc))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('sumaclust', prefix.bin)
