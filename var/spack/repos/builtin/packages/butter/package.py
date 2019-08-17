# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Butter(Package):
    """butter: Bowtie UTilizing iTerative placEment of Repetitive small rnas.
       A wrapper for bowtie to produce small RNA-seq alignments where
       multimapped small RNAs tend to be placed near regions of confidently
       high density."""

    homepage = "https://github.com/MikeAxtell/butter"
    url      = "https://github.com/MikeAxtell/butter/archive/v0.3.3.tar.gz"

    version('0.3.3', '806ff3cb7afc1d8b75126404056c629d')

    depends_on('perl', type=('build', 'run'))
    depends_on('samtools')
    depends_on('bowtie')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('butter', prefix.bin)
        install('bam2wig', prefix.bin)
