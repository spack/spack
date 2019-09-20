# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Velvet(MakefilePackage):
    """Velvet is a de novo genomic assembler specially designed for short read
       sequencing technologies."""

    homepage = "http://www.ebi.ac.uk/~zerbino/velvet/"
    url      = "http://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.10.tgz"

    version('1.2.10', '6e28c4b9bedc5f7ab2b947e7266a02f6')

    depends_on('zlib')

    def edit(self, spec, prefix):
        if spec.target.family == 'aarch64':
            makefile = FileFilter('Makefile')
            makefile.filter('-m64', '')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('velvetg', prefix.bin)
        install('velveth', prefix.bin)
