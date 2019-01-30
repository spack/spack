# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FastqScreen(Package):
    """FastQ Screen allows you to screen a library of sequences in FastQ format
       against a set of sequence databases so you can see if the composition of
       the library matches with what you expect."""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/"
    url      = "https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/fastq_screen_v0.11.2.tar.gz"

    version('0.11.2', 'ef79f16ee553aaa0ab2fc14ea11e5473')

    depends_on('perl', type='run')
    depends_on('perl-gd-graph', type='run')
    depends_on('bowtie')
    depends_on('bowtie2')
    depends_on('bwa')
    depends_on('samtools')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
