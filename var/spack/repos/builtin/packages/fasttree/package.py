# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fasttree(Package):
    """FastTree infers approximately-maximum-likelihood phylogenetic
       trees from alignments of nucleotide or protein sequences.
       FastTree can handle alignments with up to a million of sequences
       in a reasonable amount of time and memory."""

    homepage = "http://www.microbesonline.org/fasttree"
    url      = "http://www.microbesonline.org/fasttree/FastTree-2.1.10.c"

    version('2.1.10', '1c2c6425a638ec0c61ef064cda687987', expand=False, url='http://www.microbesonline.org/fasttree/FastTree-2.1.10.c')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        cc = Executable(spack_cc)
        cc('-O3', self.compiler.openmp_flag,
           '-DOPENMP', '-finline-functions', '-funroll-loops', '-Wall',
           '-oFastTreeMP', 'FastTree-' + format(spec.version.dotted) + '.c',
           '-lm')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('FastTreeMP', prefix.bin)
