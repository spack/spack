# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Minimap2(MakefilePackage):
    """Minimap2 is a versatile sequence alignment program that aligns DNA or
       mRNA sequences against a large reference database."""

    homepage = "https://github.com/lh3/minimap2"
    url      = "https://github.com/lh3/minimap2/releases/download/v2.2/minimap2-2.2.tar.bz2"

    version('2.2', '5b68e094f4fa3dfbd9b37d5b654b7715')

    depends_on('py-mappy', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('minimap2', prefix.bin)
