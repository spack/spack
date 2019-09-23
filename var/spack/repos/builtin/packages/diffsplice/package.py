# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Diffsplice(MakefilePackage):
    """A novel tool for discovering and quantitating alternative splicing
    variants present in an RNA-seq dataset, without relying on annotated
    transcriptome or pre-determined splice pattern."""

    homepage = "http://www.netlab.uky.edu/p/bioinfo/DiffSplice"
    url      = "http://protocols.netlab.uky.edu/~yin/download/diffsplice/diffsplice_0.1.1.tgz"

    version('0.1.2beta', 'a1df6e0b50968f2c229d5d7f97327336')
    version('0.1.1',     'be90e6c072402d5aae0b4e2cbb8c10ac')

    def edit(self, spec, prefix):
        if spec.target.family == 'aarch64':
            makefile = FileFilter(join_path(self.build_directory, 'Makefile'))
            makefile.filter('-m64', '')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('diffsplice', prefix.bin)
