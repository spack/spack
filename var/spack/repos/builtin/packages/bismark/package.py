# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bismark(Package):
    """A tool to map bisulfite converted sequence reads and determine cytosine
    methylation states"""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/bismark"
    url      = "https://github.com/FelixKrueger/Bismark/archive/0.19.0.tar.gz"

    version('0.19.0', 'f403654aded77bf0d1dac1203867ded1')
    version('0.18.2', '42334b7e3ed53ba246f30f1f846b4af8')

    depends_on('bowtie2', type='run')
    depends_on('perl', type='run')
    depends_on('samtools', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('bam2nuc', prefix.bin)
        install('bismark', prefix.bin)
        install('bismark_genome_preparation', prefix.bin)
        install('bismark_methylation_extractor', prefix.bin)
        install('bismark2bedGraph', prefix.bin)
        install('bismark2report', prefix.bin)
        install('bismark2summary', prefix.bin)
        install('coverage2cytosine', prefix.bin)
        install('deduplicate_bismark', prefix.bin)
        install('filter_non_conversion', prefix.bin)
        install('NOMe_filtering', prefix.bin)
